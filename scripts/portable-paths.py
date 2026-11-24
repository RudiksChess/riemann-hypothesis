#!/usr/bin/env python3
"""Keep the paths of Lean modules portable, and rename the ones that are not.

A module path is portable if every component consists of ASCII letters, digits and `_`.
Other characters make the tree hard to use: `₂` in a path breaks checkouts and tools on some
systems (#179), and `'` needs quoting in every shell command.

    portable-paths.py check  [ROOT]   # exit 1 and list the offenders, if any
    portable-paths.py rename [ROOT]   # rename the offenders and every reference to them

`rename` changes module names and nothing else.  A module name occurs in three places:

  * the path of its file;
  * `import` lines in the header of a file;
  * the records scripts/clump.py leaves in a clump file: the `-- Members:` line, the seam
    markers around each member and the member's original header in its `-- clump-header:`
    line.  Members that were folded into a clump have no file of their own, so these records
    are the only place their names live, and `clump.py unclump` recreates their files from
    them.

Declaration names and namespaces are left alone, also where they resemble a module name:
a namespace such as `GroundTheory.Heights₂` is not a path.

The new name of a component replaces `₂` by `2` and `'` by `Prime`.  Any other character
outside the portable set stops the run, as does a new name that is already taken.
"""

import argparse
import json
import os
import re
import subprocess
import sys

# These five mirror scripts/clump.py.
SEAM_BEGIN = "-- ===== clump member: "
SEAM_END = "-- ===== end clump member: "
SEAM_TAIL = " ====="
HEADER_TAG = "-- clump-header: "
MEMBERS_TAG = "-- Members: "
# As in clump.py, a `--` comment may follow the module name, also without a space.
IMPORT_RE = re.compile(
    r"^(\s*(?:(?:public|private|meta)\s+)*import\s+(?:all\s+)?)(\S+?)(\s*(?:--.*)?)$")

PORTABLE_RE = re.compile(r"[A-Za-z0-9_]+")
REPLACEMENTS = {"₂": "2", "'": "Prime"}


def portable(name):
    return all(PORTABLE_RE.fullmatch(c) for c in name.split("."))


def new_name(name):
    out = name
    for old, new in REPLACEMENTS.items():
        out = out.replace(old, new)
    if not portable(out):
        sys.exit(f"error: no rule to make this module name portable: {name}")
    return out


def lean_files(root):
    out = subprocess.run(["git", "-C", root, "ls-files", "-z", "src/*.lean"],
                         capture_output=True, check=True).stdout.decode()
    return [p for p in out.split("\0") if p]


def module_of(path):
    return path[len("src/"):-len(".lean")].replace("/", ".")


def path_of(name):
    return "src/" + name.replace(".", "/") + ".lean"


def read(root, path):
    with open(os.path.join(root, path), encoding="utf-8", newline="") as f:
        return f.read()


def members(text):
    """Names of the clump members recorded in a file (none if it is not a clump file)."""
    return [l[len(SEAM_BEGIN):-len(SEAM_TAIL)] for l in text.split("\n")
            if l.startswith(SEAM_BEGIN) and l.endswith(SEAM_TAIL)]


def inventory(root):
    """All module names: files on disk, and members recorded in clump files."""
    files = lean_files(root)
    names = {}  # module name -> where it is recorded
    for p in files:
        names.setdefault(module_of(p), p)
    for p in files:
        text = read(root, p)
        if SEAM_BEGIN in text:
            for m in members(text):
                names.setdefault(m, p + " (clump member)")
    return files, names


def comment_depth(line, depth):
    """Nesting depth of `/- … -/` comments after `line`, given the depth before it."""
    i = 0
    while i < len(line) - 1:
        two = line[i:i + 2]
        if two == "/-":
            depth += 1
            i += 2
        elif two == "-/" and depth:
            depth -= 1
            i += 2
        elif two == "--" and not depth:
            break
        else:
            i += 1
    return depth


def rewrite_header(lines, mapping, where):
    """Rename the modules on the import lines that open `lines`. Returns the number changed.

    The header is `module`, the imports, blank lines and comments; it ends at the first other line.
    """
    n = depth = 0
    for i, l in enumerate(lines):
        s = l.strip()
        if depth or s.startswith("/-"):
            depth = comment_depth(l, depth)
            continue
        if s == "" or s == "module" or s.startswith("--"):
            continue
        m = IMPORT_RE.match(l)
        if not m:
            break
        mod = m.group(2)
        if mod in mapping:
            lines[i] = m.group(1) + mapping[mod] + m.group(3)
            n += 1
        elif not portable(mod):
            sys.exit(f"error: {where}: import of a module that is not in the tree: {mod}")
    return n


def rewrite(text, mapping, where):
    """Rename modules in one file's text. Returns (new text, number of references changed)."""
    lines = text.split("\n")
    n = rewrite_header(lines, mapping, where)
    if SEAM_BEGIN not in text:
        return "\n".join(lines), n
    for i, l in enumerate(lines):
        if l.startswith(MEMBERS_TAG):
            old = l[len(MEMBERS_TAG):].split(", ")
            new = [mapping.get(m, m) for m in old]
            n += sum(a != b for a, b in zip(old, new))
            lines[i] = MEMBERS_TAG + ", ".join(new)
        elif l.startswith(HEADER_TAG):
            raw = l[len(HEADER_TAG):]
            try:
                info = json.loads(raw)
            except json.JSONDecodeError:
                # A record someone cut short cannot be rewritten; it is safe to keep only if it
                # holds none of the characters `rename` replaces.
                if any(c in raw for c in REPLACEMENTS):
                    sys.exit(f"error: {where}:{i + 1}: clump-header is not valid JSON")
                print(f"warning: {where}:{i + 1}: clump-header is not valid JSON, left as it is",
                      file=sys.stderr)
                continue
            # clump.py writes `", "` and `": "` and keeps non-ASCII characters; some records in
            # the tree have no spaces, and some have `\uXXXX` escapes.
            for fmt in ({"ensure_ascii": a, "separators": b}
                        for a in (False, True) for b in (None, (",", ":"))):
                if json.dumps(info, **fmt) == raw:
                    break
            else:
                sys.exit(f"error: {where}:{i + 1}: clump-header is not in a known format")
            if info["m"] in mapping:
                info["m"] = mapping[info["m"]]
                n += 1
            h = info["h"].split("\n")
            n += rewrite_header(h, mapping, f"{where}:{i + 1}")
            info["h"] = "\n".join(h)
            lines[i] = HEADER_TAG + json.dumps(info, **fmt)
        else:
            for tag in (SEAM_BEGIN, SEAM_END):
                if l.startswith(tag) and l.endswith(SEAM_TAIL):
                    m = l[len(tag):-len(SEAM_TAIL)]
                    if m in mapping:
                        lines[i] = tag + mapping[m] + SEAM_TAIL
                        n += 1
    return "\n".join(lines), n


def check(root):
    _, names = inventory(root)
    bad = sorted(m for m in names if not portable(m))
    if not bad:
        print(f"all {len(names)} module names are portable")
        return 0
    for m in bad:
        print(f"{names[m]}: {m}")
    print(f"\n{len(bad)} module names are not portable (allowed in a component: ASCII letters, "
          "digits and `_`).\nRename new files by hand; `scripts/portable-paths.py rename` "
          "renames modules that already have importers.", file=sys.stderr)
    return 1


def rename(root):
    files, names = inventory(root)
    mapping = {m: new_name(m) for m in names if not portable(m)}
    if not mapping:
        print("nothing to rename")
        return 0
    taken = set(names) - set(mapping)
    seen = {}
    for old, new in sorted(mapping.items()):
        if new in taken or new in seen:
            sys.exit(f"error: {old} and {seen.get(new, new)} would both be called {new}")
        seen[new] = old
    # On a case-insensitive file system two names that differ only in case are one file.
    lower = {}
    for m in taken | set(seen):
        if m.lower() in lower:
            sys.exit(f"error: {m} and {lower[m.lower()]} differ only in case")
        lower[m.lower()] = m

    # `names` has tracked files only; an untracked file at a new path would stop `git mv` halfway.
    for m in mapping:
        q = path_of(mapping[m])
        if module_of(names[m]) == m and os.path.lexists(os.path.join(root, q)):
            sys.exit(f"error: {q} exists and is not tracked; move it away first")

    # Every file is checked before the first one is written, so an error leaves the tree as it was.
    moved = refs = 0
    changed = {}
    for p in files:
        new_text, n = rewrite(read(root, p), mapping, p)
        if n:
            changed[p] = new_text
            refs += n
    touched = len(changed)
    for p, new_text in changed.items():
        with open(os.path.join(root, p), "w", encoding="utf-8", newline="") as f:
            f.write(new_text)
    for p in files:
        m = module_of(p)
        if m in mapping:
            q = path_of(mapping[m])
            os.makedirs(os.path.dirname(os.path.join(root, q)), exist_ok=True)
            subprocess.run(["git", "-C", root, "mv", p, q], check=True)
            moved += 1
    print(f"renamed {len(mapping)} modules ({moved} files, {len(mapping) - moved} clump "
          f"members without a file) and {refs} references to them in {touched} files")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("command", choices=["check", "rename"])
    p.add_argument("root", nargs="?", default=os.path.join(os.path.dirname(__file__), ".."))
    a = p.parse_args()
    sys.exit(check(a.root) if a.command == "check" else rename(a.root))


if __name__ == "__main__":
    main()
