"""night_merge: the night sessions' branches merged into the current branch by one tested procedure (next steps 3g).

  python3 orchestration/night_merge/helper/night_merge.py BRANCH [BRANCH ...] --python VENV_PYTHON [--no-tests]

Run from anywhere inside the repository, on the branch that receives the merges, with a clean working tree. For each
branch, in the order given: git's merge; then every conflict is resolved by the rule of its file, or the merge is
stopped and the conflict reported (no guess):
- the components file: three-way, class by class (a class both sides changed differently stops the merge);
- the files the sessions append to (the catalogue, the component index and journal, the brief index): three-way, line
  by line; lines both sides inserted at the same place are all kept; lines both sides changed differently stop the merge;
- the catalogue's class count: derived, recomputed from the components file;
- every merged file checked: nothing lost, nothing invented, every Python class defined once;
- the similarity register's list of books: merged by key;
- the register's derived files (pages, matrix, comparisons): rebuilt once at the end (`ideas_similarities_check.py --all`).
Then both test suites. It reports brief numbers used by more than one brief (next steps 3e). It never pushes.
Card: ../card.md.
"""
import argparse, ast, collections, json, re, subprocess, sys
from pathlib import Path

SC = "strategy_designer_v2/steps_cards"
COMPONENTS = "trading-bot/strategies/strategy_components.py"     # merged class by class
CATALOGUE = f"{SC}/03_test_plan/helper/reference/component_catalogue.md"
LINES = (                                   # appended to by every session: merged line by line
    CATALOGUE,
    f"{SC}/components/INDEX.md",
    f"{SC}/components/journal.jsonl",
    f"{SC}/01_brief/briefs/INDEX.md",
)
REGISTER = f"{SC}/orchestration/ideas_similarities_check"
BOOKS = f"{REGISTER}/register/books.json"
INPUTS = (BOOKS, f"{REGISTER}/register/held.json", f"{REGISTER}/register/returns/")   # what the register is built from


def derived(path):
    """A register file `ideas_similarities_check.py --all` rewrites from its inputs (pages, matrix, comparisons)."""
    return path.startswith(f"{REGISTER}/register/") and not path.startswith(INPUTS)
COUNT = re.compile(r"There are (?:\d+|N) classes")   # derived: recomputed from the components file, never merged


def git(*args, check=True, root=None):
    p = subprocess.run(["git", *args], capture_output=True, text=True, cwd=root)
    if check and p.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.strip() or p.stdout.strip()}")
    return p.stdout


def stage(n, path, root=None):
    """A conflicted file's version: 1 the common ancestor, 2 ours, 3 theirs ('' when that side has none)."""
    p = subprocess.run(["git", "show", f":{n}:{path}"], capture_output=True, text=True, cwd=root)
    return p.stdout if p.returncode == 0 else ""


def merge_lines(base, ours, theirs):
    """git's three-way line merge. Where both sides only inserted lines at the same place, ours then theirs; where both
    changed the same lines of the base, a fault (no guess). Returns (text, faults)."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        f = {k: Path(d) / k for k in ("ours", "base", "theirs")}
        for k, v in (("ours", ours), ("base", base), ("theirs", theirs)):
            f[k].write_text(v)
        out = subprocess.run(["git", "merge-file", "-p", "--diff3", str(f["ours"]), str(f["base"]), str(f["theirs"])],
                             capture_output=True, text=True).stdout
    text, faults, i, lines = [], [], 0, out.splitlines(keepends=True)
    while i < len(lines):
        if not lines[i].startswith("<<<<<<< "):
            text.append(lines[i]); i += 1
            continue
        part, sides = "ours", {"ours": [], "base": [], "theirs": []}
        i += 1
        while not lines[i].startswith(">>>>>>> "):
            if lines[i].startswith("||||||| "):
                part = "base"
            elif lines[i].startswith("======="):
                part = "theirs"
            else:
                sides[part].append(lines[i])
            i += 1
        i += 1
        if any(l.strip() for l in sides["base"]):
            lines_, why = merge_hunk(sides["base"], sides["ours"], sides["theirs"])
            if why:
                faults.append("both sides changed the same lines: " + why)
            text += lines_
        else:
            text += sides["ours"] + sides["theirs"]
    return "".join(text), faults


def merge_hunk(base, ours, theirs):
    """One conflict hunk, line by line: git joins changes on neighbouring lines into one hunk; here each side's changes
    are placed against the base's lines, and only lines both sides changed differently are a fault (the same change on
    both sides is kept once). Inserts both sides made at the same place are kept, ours first. Returns (lines, why) with why empty when merged."""
    import difflib
    def changes(side):
        out = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, base, side, autojunk=False).get_opcodes():
            if tag == "replace" and i2 - i1 == j2 - j1:  # rows edited in place: one change per row
                out += [(i1 + k, i1 + k + 1, side[j1 + k:j1 + k + 1]) for k in range(i2 - i1)]
            elif tag != "equal":
                out.append((i1, i2, side[j1:j2]))
        return out
    co = changes(ours)
    ct = [c for c in changes(theirs) if c not in co]        # the same change made by both sides is one change
    for a1, a2, _ in co:
        for b1, b2, _ in ct:
            if max(a1, b1) < min(a2, b2):
                return ours + theirs, " ".join("".join(base[max(a1, b1):min(a2, b2)]).split())[:120]
    out, i = [], 0
    for i1, i2, new in sorted(co + ct, key=lambda c: (c[0], c[1] - c[0])):
        out += base[i:i1] if i1 > i else []
        out += new
        i = max(i, i2)
    return out + base[i:], ""


def units(text):
    """A Python file cut into its top-level blocks: ('__head__', the lines before the first), then one per class or
    function, keyed by its name (decorators and the comments right above it included)."""
    out, key, buf, pending = [], "__head__", [], []
    for line in text.splitlines(keepends=True):
        m = re.match(r"(?:async\s+)?(?:class|def)\s+(\w+)", line)
        if m:
            out.append((key, "".join(buf)))
            key, buf, pending = m.group(1), pending + [line], []
        elif line.startswith(("@", "#")) or (not line.strip() and pending):
            pending.append(line)
        elif not line.strip():
            pending.append(line)
        else:
            buf += pending + [line]
            pending = []
    out.append((key, "".join(buf + pending)))
    return out


def merge_python(base, ours, theirs):
    """Three-way, block by block (`units`): a block one side changed takes that side's version; one both changed
    differently is a fault; a block one side removed (the other unchanged) goes; theirs' new blocks come after ours.
    Returns (text, faults)."""
    b, o, t = dict(units(base)), units(ours), dict(units(theirs))
    keys, faults, merged = {k for k, _ in o}, [], []
    for k, v in o:
        if k in t:
            if t[k] != b.get(k) and v == b.get(k):
                v = t[k]
            elif t[k] != v and v != b.get(k) and t[k] != b.get(k):
                faults.append(f"block changed on both sides: {k}")
        elif k in b and v == b[k]:
            continue                                      # theirs removed it, ours did not change it
        merged.append(v)
    merged += [v for k, v in units(theirs) if k not in keys and k not in b]
    return "".join(merged), faults


def with_count(text, components):
    """The catalogue's class count, recomputed from the components file."""
    n = len(re.findall(r"^class \w+\(", components, re.M))
    return COUNT.sub(f"There are {n} classes", text, count=1)


def union_faults(path, base, ours, theirs, merged):
    """What a merge must keep: every line of each side, as often as that side has it, unless the other side removed
    it; no line more often than the two sides' additions allow; in Python, the file parses, each class once."""
    out = []
    c = {k: collections.Counter(l for l in v.splitlines() if l.strip() and not COUNT.search(l)) for k, v in
         (("base", base), ("ours", ours), ("theirs", theirs), ("merged", merged))}
    for line in set(c["ours"]) | set(c["theirs"]) | set(c["merged"]):
        m, o, t, b = c["merged"][line], c["ours"][line], c["theirs"][line], c["base"][line]
        if m < max(o, t) and not (o < b or t < b):
            out.append(f"line lost: {line[:80]!r}")
        elif m > max(o + t - b, o, t):
            out.append(f"line repeated: {line[:80]!r}")
    if path.endswith(".py"):
        try:
            tree = ast.parse(merged)
        except SyntaxError as e:
            return out + [f"does not parse: {e}"]
        names = collections.Counter(n.name for n in tree.body if isinstance(n, ast.ClassDef))
        out += [f"class defined {k} times: {n}" for n, k in names.items() if k > 1]
    return out


def merge_books(base, ours, theirs):
    """The register's books by key: ours, then theirs' new keys; a key both sides changed differently is a fault."""
    b = {x["key"]: x for x in json.loads(base or "[]")}
    o, t = json.loads(ours or "[]"), json.loads(theirs or "[]")
    keys = {x["key"]: x for x in o}
    faults = []
    for x in t:
        k = x["key"]
        if k not in keys:
            keys[k] = x
            o.append(x)
        elif keys[k] != x and b.get(k) != x and b.get(k) != keys[k]:
            faults.append(f"book changed on both sides: {k}")
    return json.dumps(o, indent=2) + "\n", faults


def brief_number_clashes(root):
    """Brief numbers used by more than one brief file in step 1's list (next steps 3e)."""
    by = collections.defaultdict(list)
    for p in sorted((Path(root) / SC / "01_brief" / "briefs").glob("[0-9][0-9][0-9]_*.md")):
        by[p.name[:3]].append(p.stem)
    return {n: v for n, v in by.items() if len(v) > 1}


def merge_branch(branch, root):
    """One branch merged and committed; the faults that stopped it (the merge aborted), or []."""
    fetched = subprocess.run(["git", "fetch", "-q", "origin", branch], capture_output=True, cwd=root).returncode == 0
    p = subprocess.run(["git", "merge", "--no-ff", "--no-commit", "FETCH_HEAD" if fetched else branch],
                       capture_output=True, text=True, cwd=root)
    conflicted = [l for l in git("diff", "--name-only", "--diff-filter=U", root=root).splitlines() if l]
    faults = []
    for path in conflicted:
        base, ours, theirs = stage(1, path, root), stage(2, path, root), stage(3, path, root)
        if path == COMPONENTS or path in LINES:
            if path == CATALOGUE:                             # the count is derived: set after the merge
                base, ours, theirs = (COUNT.sub("There are N classes", x) for x in (base, ours, theirs))
            merged, f = (merge_python if path == COMPONENTS else merge_lines)(base, ours, theirs)
            faults += [f"{path}: {x}" for x in f + union_faults(path, base, ours, theirs, merged)]
        elif path == BOOKS:
            merged, f = merge_books(base, ours, theirs)
            faults += [f"{path}: {x}" for x in f]
        elif derived(path):
            merged = ours                                     # rebuilt at the end
        else:
            faults.append(f"{path}: a conflict no rule covers")
            continue
        (Path(root) / path).write_text(merged)
        git("add", path, root=root)
    if p.returncode and not conflicted:
        faults.append(f"git merge failed: {p.stderr.strip()[:300]}")
    cat = Path(root) / CATALOGUE
    if not faults and cat.exists() and (Path(root) / COMPONENTS).exists():
        fixed = with_count(cat.read_text(), (Path(root) / COMPONENTS).read_text())
        if fixed != cat.read_text():
            cat.write_text(fixed)
            git("add", CATALOGUE, root=root)
    if faults:
        git("merge", "--abort", check=False, root=root)
        return faults, conflicted
    git("commit", "-q", "-m", f"Merge night branch {branch} (night_merge: {len(conflicted)} conflicts resolved by rule)", root=root)
    return [], conflicted


def main():
    a = argparse.ArgumentParser()
    a.add_argument("branches", nargs="+")
    a.add_argument("--python", required=True, help="a venv with trading-bot/requirements.txt (the register, the tests)")
    a.add_argument("--no-tests", action="store_true")
    args = a.parse_args()
    root = git("rev-parse", "--show-toplevel").strip()
    if git("status", "--porcelain", "--untracked-files=no", root=root).strip():
        sys.exit("the working tree has changes: commit or stash them first")
    touched = False
    for b in args.branches:
        faults, conflicted = merge_branch(b, root)
        if faults:
            print(f"{b}: NOT merged (the merge was aborted):")
            print("".join(f"  - {f}\n" for f in faults), end="")
            sys.exit(1)
        touched |= any(c == BOOKS or derived(c) for c in conflicted) or bool(
            git("diff", "--name-only", "HEAD^1", "HEAD", "--", f"{REGISTER}/register", root=root).strip())
        print(f"{b}: merged ({len(conflicted)} conflicts resolved by rule{': ' + ', '.join(Path(c).name for c in conflicted) if conflicted else ''})")
    if touched:
        r = subprocess.run([args.python, f"{REGISTER}/helper/ideas_similarities_check.py", "--all"], capture_output=True,
                           text=True, cwd=root)
        print(f"register rebuilt (--all): exit {r.returncode}; {(r.stdout.strip().splitlines() or [''])[-1][:200]}")
        if r.returncode:
            sys.exit(1)
        git("add", "-A", f"{REGISTER}/register", root=root)
        if git("diff", "--cached", "--name-only", root=root).strip():
            git("commit", "-q", "-m", "Similarity register rebuilt over every book after the night merges (night_merge)", root=root)
    # Step 10 (common/data_use.md): after the register's rebuild, a new portfolio version when the list of candidates
    # changed (orchestration/combine/card.md); with no new common record it writes nothing.
    r = subprocess.run([args.python, f"{SC}/orchestration/combine/helper/update.py"], capture_output=True, text=True, cwd=root)
    print(f"portfolio update: exit {r.returncode}; {((r.stdout + r.stderr).strip().splitlines() or [''])[-1][:200]}")
    git("add", "-A", f"{SC}/orchestration/combine/portfolios", root=root)
    if git("diff", "--cached", "--name-only", root=root).strip():
        git("commit", "-q", "-m", "Portfolio version built after the night merges (combine/update.py)", root=root)
    for n, v in brief_number_clashes(root).items():
        print(f"brief number {n} used by {len(v)} briefs: {', '.join(v)}")
    if not args.no_tests:
        for name, cmd, cwd in (("cards", [args.python, "-m", "pytest", "-q", SC], root),
                               ("bot", [args.python, "-m", "pytest", "-q"], str(Path(root) / "trading-bot"))):
            r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
            print(f"{name} tests: {(r.stdout.strip().splitlines() or ['no output'])[-1]}")
    print("done: nothing pushed")


if __name__ == "__main__":
    main()
