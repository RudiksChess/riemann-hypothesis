#!/usr/bin/env python3
"""portable-paths.py on small trees in a temporary Git repository, with clump.py's own output."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"),
                                                  Path(__file__).resolve().parents[1] / (name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pp = load("portable-paths")
clump = load("clump")

TREE = {
    "A/Leaf₂/Base": "module\n\npublic import Mathlib.Data.Nat.Basic\n\ntheorem a : True := trivial\n",
    "A/Leaf₂/Mid": "module\n\npublic import A.Leaf₂.Base\n\ntheorem b : True := a\n",
    "A/Z'": "module\n\nimport A.Leaf₂.Mid\n\ntheorem c : True := b\n",
    "A/Z''": "module\n\npublic meta import A.Z'\nimport all A.Leaf₂.Base\n\ntheorem d : True := c",
    # `Heights₂` is a namespace here and the import-like line is not in the header: both stay.
    "A/Top": "module\n\nimport A.Z''\n\nnamespace A.Heights₂\n/-\nimport A.Z'\n-/\n"
             "theorem e : True := d\nend A.Heights₂\n",
}


class Tree:
    def __init__(self, test, files):
        self.dir = tempfile.TemporaryDirectory()
        test.addCleanup(self.dir.cleanup)
        self.root = self.dir.name
        self.git("init", "-q")
        for name, text in files.items():
            p = Path(self.root, "src", name + ".lean")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        self.git("add", "-A")

    def git(self, *args):
        return subprocess.run(["git", "-C", self.root, *args], check=True,
                              capture_output=True).stdout.decode()

    def files(self):
        out = {}
        for p in self.git("ls-files", "-z", "src").split("\0"):
            if p:
                out[p[len("src/"):-len(".lean")]] = Path(self.root, p).read_text(encoding="utf-8")
        return out

    def run(self, command):
        with contextlib.redirect_stdout(io.StringIO()) as out, \
                contextlib.redirect_stderr(io.StringIO()):
            code = command(self.root)
        return code, out.getvalue()

    def fold(self, root, members):
        """Fold `members` (dependencies first, `root` last) into one clump file."""
        clump.apply(self.root, {root: members})
        self.git("add", "-A")


def renamed(text):
    for old, new in (("A.Leaf₂.", "A.Leaf2."), ("import A.Z''", "import A.ZPrimePrime"),
                     ("import A.Z'", "import A.ZPrime")):
        text = text.replace(old, new)
    return text


EXPECTED = {
    "A/Leaf2/Base": TREE["A/Leaf₂/Base"],
    "A/Leaf2/Mid": renamed(TREE["A/Leaf₂/Mid"]),
    "A/ZPrime": renamed(TREE["A/Z'"]),
    "A/ZPrimePrime": renamed(TREE["A/Z''"]),
    "A/Top": TREE["A/Top"].replace("import A.Z''\n\nnamespace", "import A.ZPrimePrime\n\nnamespace"),
}


class PortablePaths(unittest.TestCase):
    def test_names(self):
        self.assertTrue(pp.portable("A.B_c.D2"))
        for bad in ("A.B₂", "A.B'", "A.B-c", "A.Bé", "A..B", "A.B C"):
            self.assertFalse(pp.portable(bad), bad)
        self.assertEqual(pp.new_name("A.B₂.C''"), "A.B2.CPrimePrime")
        with self.assertRaises(SystemExit):
            pp.new_name("A.Bé")

    def test_check(self):
        t = Tree(self, TREE)
        code, out = t.run(pp.check)
        self.assertEqual(code, 1)
        self.assertEqual(len(out.splitlines()), 4)
        self.assertEqual(t.run(pp.rename)[0], 0)
        self.assertEqual(t.run(pp.check)[0], 0)

    def test_rename_standalone(self):
        t = Tree(self, TREE)
        t.run(pp.rename)
        self.assertEqual(t.files(), EXPECTED)
        # A second run finds nothing to do.
        self.assertIn("nothing to rename", t.run(pp.rename)[1])
        self.assertEqual(t.files(), EXPECTED)

    def test_rename_inside_clumps(self):
        """Renaming a clumped tree and unclumping gives the renamed standalone tree."""
        t = Tree(self, TREE)
        t.fold("A.Leaf₂.Mid", ["A.Leaf₂.Base", "A.Leaf₂.Mid"])   # the root keeps a bad name
        t.fold("A.Top", ["A.Z'", "A.Z''", "A.Top"])               # bad names survive as members only
        self.assertEqual(sorted(t.files()), ["A/Leaf₂/Mid", "A/Top"])
        code, out = t.run(pp.check)
        self.assertEqual((code, len(out.splitlines())), (1, 4))

        t.run(pp.rename)
        files = t.files()
        self.assertEqual(sorted(files), ["A/Leaf2/Mid", "A/Top"])
        self.assertNotIn("Leaf₂", "".join(files.values()))
        self.assertIn("-- Members: A.ZPrime, A.ZPrimePrime, A.Top\n", files["A/Top"])
        self.assertIn("/-\nimport A.Z'\n-/", files["A/Top"])
        self.assertIn("namespace A.Heights₂", files["A/Top"])
        self.assertIn("import A.Leaf2.Mid\n", files["A/Top"].split(clump.CLUMP_MARK)[0])
        self.assertEqual(t.run(pp.check)[0], 0)

        with contextlib.redirect_stdout(io.StringIO()):
            clump.unclump(t.root)
        t.git("add", "-A")
        self.assertEqual(t.files(), EXPECTED)

    def test_keeps_compact_clump_headers(self):
        """Some records in the tree have no spaces after `,` and `:`; they stay that way."""
        t = Tree(self, TREE)
        t.fold("A.Top", ["A.Z'", "A.Z''", "A.Top"])
        p = Path(t.root, "src/A/Top.lean")
        lines = p.read_text(encoding="utf-8").split("\n")
        for i, l in enumerate(lines):
            if l.startswith(pp.HEADER_TAG):
                info = json.loads(l[len(pp.HEADER_TAG):])
                lines[i] = pp.HEADER_TAG + json.dumps(info, ensure_ascii=False, separators=(",", ":"))
        p.write_text("\n".join(lines), encoding="utf-8")

        t.run(pp.rename)
        headers = [l for l in t.files()["A/Top"].split("\n") if l.startswith(pp.HEADER_TAG)]
        self.assertEqual(len(headers), 3)
        for l in headers:
            self.assertTrue(l.startswith(pp.HEADER_TAG + '{"m":"A.'), l)
        self.assertIn('{"m":"A.ZPrimePrime","h":"module\\n\\npublic meta import A.ZPrime\\n',
                      "".join(headers))
        with contextlib.redirect_stdout(io.StringIO()):
            clump.unclump(t.root)
        t.git("add", "-A")
        self.assertEqual(t.files(), EXPECTED)

    def test_keeps_escaped_clump_headers(self):
        """A record written with `\\uXXXX` escapes is read, and is plain ASCII afterwards anyway."""
        t = Tree(self, TREE)
        t.fold("A.Leaf₂.Mid", ["A.Leaf₂.Base", "A.Leaf₂.Mid"])
        p = Path(t.root, "src/A/Leaf₂/Mid.lean")
        lines = p.read_text(encoding="utf-8").split("\n")
        for i, l in enumerate(lines):
            if l.startswith(pp.HEADER_TAG):
                lines[i] = pp.HEADER_TAG + json.dumps(json.loads(l[len(pp.HEADER_TAG):]))
        self.assertIn("\\u2082", "\n".join(lines))
        p.write_text("\n".join(lines), encoding="utf-8")
        t.run(pp.rename)
        text = t.files()["A/Leaf2/Mid"]
        self.assertNotIn("\\u2082", text)
        self.assertIn('"h": "module\\n\\npublic import A.Leaf2.Base\\n', text)

    def test_cut_clump_headers(self):
        """A record that is not valid JSON stays if it has nothing to rename, and stops the run if it has."""
        for member, ok in (("A.Top", True), ("A.Z''", False)):
            t = Tree(self, TREE)
            t.fold("A.Top", ["A.Z'", "A.Z''", "A.Top"])
            p = Path(t.root, "src/A/Top.lean")
            lines = p.read_text(encoding="utf-8").split("\n")
            i = lines.index(pp.SEAM_BEGIN + member + pp.SEAM_TAIL) + 1
            self.assertTrue(lines[i].startswith(pp.HEADER_TAG))
            lines[i] = lines[i][:len(pp.HEADER_TAG) + 30]
            p.write_text("\n".join(lines), encoding="utf-8")
            before = t.files()
            if ok:
                self.assertEqual(t.run(pp.rename)[0], 0)
                self.assertIn(lines[i] + "\n", t.files()["A/Top"])
            else:
                with self.assertRaises(SystemExit):
                    t.run(pp.rename)
                self.assertEqual(t.files(), before)

    def test_refuses_collisions(self):
        t = Tree(self, {"A/B₂": "module\n", "A/B2": "module\n"})
        with self.assertRaises(SystemExit):
            t.run(pp.rename)
        self.assertEqual(sorted(t.files()), ["A/B2", "A/B₂"])
        t = Tree(self, {"A/B₂": "module\n", "A/b2": "module\n"})
        with self.assertRaises(SystemExit):
            t.run(pp.rename)

    def test_comments_in_the_header(self):
        """Comments between the imports do not end the header; imports inside them stay."""
        t = Tree(self, {
            "A/B₂": "module\n",
            "A/C'": "module\n",
            "A/D": "module\n\n-- import A.C'\npublic import A.B₂ -- why\n/- nested /- import A.C' -/\n"
                   "import A.C'\n-/\nimport A.C'--note\n\ntheorem t : True := trivial\nimport A.B₂\n",
        })
        self.assertEqual(t.run(pp.rename)[0], 0)
        self.assertEqual(
            t.files()["A/D"],
            "module\n\n-- import A.C'\npublic import A.B2 -- why\n/- nested /- import A.C' -/\n"
            "import A.C'\n-/\nimport A.CPrime--note\n\ntheorem t : True := trivial\nimport A.B₂\n")

    def test_refuses_untracked_destination(self):
        files = {"A/B₂": "module\n", "A/C": "module\n\nimport A.B₂\n"}
        t = Tree(self, files)
        other = Path(t.root, "src/A/B2.lean")
        other.write_text("-- not ours\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            t.run(pp.rename)
        self.assertEqual(t.files(), files)
        self.assertEqual(other.read_text(encoding="utf-8"), "-- not ours\n")
        self.assertEqual(t.git("-c", "core.quotePath=false", "status", "--porcelain").split(),
                         ["A", "src/A/B₂.lean", "A", "src/A/C.lean", "??", "src/A/B2.lean"])

    def test_refuses_unknown_import(self):
        t = Tree(self, {"A/B₂": "module\n\nimport A.Gone₂\n"})
        with self.assertRaises(SystemExit):
            t.run(pp.rename)


if __name__ == "__main__":
    unittest.main()
