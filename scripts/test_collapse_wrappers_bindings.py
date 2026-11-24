"""Run with LEAN=/path/to/lean python3 scripts/test_collapse_wrappers_bindings.py."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("collapse_wrappers.py")
HEADER = "module\npublic import Core\n@[expose] public section\n"


class WrapperBindings(unittest.TestCase):
    def test_regeneration_preserves_local_targets(self):
        retained = {
            "Explicit": "theorem N.explicitProof (h : True) : True := h\n",
            "Implicit": "theorem N.implicitProof {hi : True} : True := hi\n",
            "Strict": "theorem N.strictProof ⦃hs : True⦄ : True := hs\n",
            "Grouped": "theorem N.groupedProof (_unused hg : True) : True := hg\n",
            "Projection": "theorem N.projectionProof (h : HasProof) : True := h.foo\n",
            "Instance": "theorem N.instanceProof [inst : HasFact] : True := inst.prf\n",
            "Variable": "  variable (hv : HasGoal)\ntheorem N.variableProof : hv.goal := hv.prf\n",
        }
        removed = {
            "Safe": (
                "theorem N.safeProof (p : True) : True := by\n"
                "  first | exact @original | exact original | (intros; apply original <;> assumption)\n"
            ),
            "Root": (
                "theorem N.rootProof (original : True) : True := by\n"
                "  first | exact @_root_.original | exact _root_.original | (intros; apply _root_.original <;> assumption)\n"
            ),
        }
        sources = {
            "Core": (
                "module\n@[expose] public section\n"
                "def h (n : Nat) : Nat := n\n"
                "def hi {n : Nat} : Nat := n\n"
                "def hs ⦃n : Nat⦄ : Nat := n\n"
                "def hg (a b : Nat) : Nat := a + b\n"
                "structure HasGoal where\n  goal : Prop\n  prf : goal\n"
                "def hv.prf : Nat := 0\n"
                "structure HasProof where\n  foo : True\n"
                "class HasFact where\n  prf : True\n"
                "def inst.prf [Inhabited Nat] : Nat := default\n"
                "def h.foo (n : Nat) : Nat := n\n"
                "theorem original (p : True) : True := p\n"
            ),
        }
        for name, body in {**retained, **removed}.items():
            sources[name] = HEADER + body
        sources["Consumer"] = (
            "module\n" + "".join(f"import {name}\n" for name in [*retained, *removed]) +
            "example : True := N.explicitProof True.intro\n"
            "example : True := N.implicitProof (hi := True.intro)\n"
            "example : True := N.strictProof (hs := True.intro)\n"
            "example : True := N.groupedProof True.intro True.intro\n"
            "example : True := N.projectionProof ⟨True.intro⟩\n"
            "example : True := N.instanceProof (inst := ⟨True.intro⟩)\n"
            "example : True := N.variableProof ⟨True, True.intro⟩\n"
            "example : True := N.safeProof True.intro\n"
            "example : True := N.rootProof True.intro\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            src = root / "src"
            src.mkdir()
            for name, text in sources.items():
                (src / f"{name}.lean").write_text(text, encoding="utf-8")
            subprocess.run(["git", "init", "-q", directory], check=True)
            subprocess.run(["git", "-C", directory, "add", "src"], check=True)

            def compile_sources():
                for artifact in src.glob("*.olean*"):
                    artifact.unlink()
                for name in sources:
                    if (src / f"{name}.lean").exists():
                        subprocess.run(
                            [os.environ["LEAN"], "-o", f"{name}.olean", f"{name}.lean"],
                            cwd=src, env={**os.environ, "LEAN_PATH": str(src)}, check=True,
                        )

            if os.environ.get("LEAN"):
                compile_sources()
            subprocess.run([sys.executable, str(SCRIPT), directory], check=True)
            if os.environ.get("LEAN"):
                compile_sources()
            for name in retained:
                self.assertEqual((src / f"{name}.lean").read_text(), sources[name])
            for name in removed:
                self.assertFalse((src / f"{name}.lean").exists())


if __name__ == "__main__":
    unittest.main()
