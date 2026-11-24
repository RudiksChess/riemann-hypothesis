"""Run with LEAN=/path/to/lean python3 scripts/test_collapse_wrappers_eligibility.py."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("collapse_wrappers.py")
HEADER = "module\npublic import Core\n@[expose] public section\n"


class WrapperEligibility(unittest.TestCase):
    def test_only_plain_complete_wrappers_are_removed(self):
        retained = {
            "Nested": "theorem N.nestedProof : True ∧ True := by\n  constructor\n  all_goals first | exact original\n",
            "Fallback": "theorem N.fallbackProof : True ∧ True := by\n  first | exact original | exact pairOriginal\n",
            "Simp": "@[simp] theorem N.simpAlias : ∀ n : Nat, f n = n := funOriginal\n",
        }
        removed = {
            "Term": "theorem N.termProof : True := original\n",
            "Exact": "theorem N.exactProof : True := by\n  exact original\n",
            "First": (
                "theorem N.firstProof : True := by\n"
                "  first | exact @original | exact original | (intros; apply original <;> assumption)\n"
            ),
            "Comment": "-- first | exact pairOriginal\ntheorem N.commentProof : True := original\n",
            "Closed": "namespace N\ntheorem closedProof : True := original\nend N\n",
        }
        sources = {
            "Core": (
                "module\n@[expose] public section\n"
                "theorem original : True := by trivial\n"
                "theorem pairOriginal : True ∧ True := ⟨original, original⟩\n"
                "def f (n : Nat) := 0 + n\n"
                "theorem funOriginal : ∀ n : Nat, f n = n := by\n"
                "  intro n\n  exact Nat.zero_add n\n"
            ),
        }
        for name, body in {**retained, **removed}.items():
            sources[name] = HEADER + body
        sources["Consumer"] = (
            "module\n" + "".join(f"import {name}\n" for name in [*retained, *removed]) +
            "example : True ∧ True := N.nestedProof\n"
            "example : True ∧ True := N.fallbackProof\n"
            "example (n : Nat) : f n = n := by simp\n" +
            "".join(f"example : True := N.{name}Proof\n" for name in ["term", "exact", "first", "comment", "closed"])
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
            consumer = (src / "Consumer.lean").read_text()
            self.assertEqual(consumer.count(":= _root_.original"), len(removed))


if __name__ == "__main__":
    unittest.main()
