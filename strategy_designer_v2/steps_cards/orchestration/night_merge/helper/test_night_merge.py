"""Tests of night_merge on a throwaway repository: two sessions append to the shared files from the same base."""
import json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import night_merge as nm  # noqa: E402

PY = nm.COMPONENTS
IDX = nm.LINES[3]


def g(root, *a):
    subprocess.run(["git", *a], cwd=root, check=True, capture_output=True)


def repo(tmp_path):
    r = tmp_path / "repo"
    for path, text in ((PY, "class A:\n    pass\n"), (IDX, "001_a: x\n"), (nm.BOOKS, json.dumps([{"key": "k0"}])),
                       (f"{nm.REGISTER}/register/INDEX.md", "page\n"), ("other.md", "one\n")):
        (r / path).parent.mkdir(parents=True, exist_ok=True)
        (r / path).write_text(text)
    g(r, "init", "-q", "-b", "work"); g(r, "-c", "user.email=t@t", "-c", "user.name=t", "add", "-A")
    g(r, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "base")
    g(r, "config", "user.email", "t@t"); g(r, "config", "user.name", "t")
    for b, cls, line, key in (("s1", "B", "002_b: y", "k1"), ("s2", "C", "002_c: z", "k2")):
        g(r, "checkout", "-q", "-b", b, "work")
        (r / PY).write_text((r / PY).read_text() + f"\n\nclass {cls}:\n    pass\n")
        (r / IDX).write_text((r / IDX).read_text() + line + "\n")
        books = json.loads((r / nm.BOOKS).read_text()) + [{"key": key}]
        (r / nm.BOOKS).write_text(json.dumps(books))
        (r / f"{nm.REGISTER}/register/INDEX.md").write_text(f"page {b}\n")
        g(r, "commit", "-qam", b)
    g(r, "checkout", "-q", "work")
    return r


def test_two_sessions_merge_by_rule(tmp_path):
    r = repo(tmp_path)
    for b in ("s1", "s2"):
        faults, conflicted = nm.merge_branch(b, str(r))
        assert faults == [], faults
    text = (r / PY).read_text()
    assert [l for l in text.splitlines() if l.startswith("class")] == ["class A:", "class B:", "class C:"]
    assert (r / IDX).read_text().splitlines() == ["001_a: x", "002_b: y", "002_c: z"]
    assert [x["key"] for x in json.loads((r / nm.BOOKS).read_text())] == ["k0", "k1", "k2"]


def test_a_conflict_no_rule_covers_stops_the_merge(tmp_path):
    r = repo(tmp_path)
    for b, text in (("s1", "two\n"), ("s2", "three\n")):
        g(r, "checkout", "-q", b); (r / "other.md").write_text(text); g(r, "commit", "-qam", "other")
    g(r, "checkout", "-q", "work")
    assert nm.merge_branch("s1", str(r))[0] == []
    faults, _ = nm.merge_branch("s2", str(r))
    assert faults == ["other.md: a conflict no rule covers"]
    assert subprocess.run(["git", "status", "--porcelain"], cwd=r, capture_output=True, text=True).stdout == ""   # aborted


def test_python_is_merged_class_by_class():
    base = "import x\n\n\nclass A:\n    pass\n"
    ours = base + "\n\nclass B:\n    pass\n"
    theirs = base.replace("    pass", "    y = 1") + "\n\nclass C:\n    pass\n"       # changes A, adds C
    merged, faults = nm.merge_python(base, ours, theirs)
    assert faults == [] and "    y = 1" in merged
    assert [l for l in merged.splitlines() if l.startswith("class")] == ["class A:", "class B:", "class C:"]
    _, faults = nm.merge_python(base, base.replace("pass", "z = 2"), base.replace("pass", "z = 3"))
    assert faults == ["block changed on both sides: A"]


def test_lines_inserted_on_both_sides_are_kept_and_a_line_changed_on_both_sides_stops():
    merged, faults = nm.merge_lines("a\nz\n", "a\nb\nz\n", "a\nc\nz\n")
    assert merged == "a\nb\nc\nz\n" and faults == []
    _, faults = nm.merge_lines("n = 116\n", "n = 118\n", "n = 117\n")
    assert faults and faults[0].startswith("both sides changed the same lines")
    assert nm.with_count("There are 116 classes.", "class A(X):\nclass B(X):\n") == "There are 2 classes."
    assert any("line lost" in f for f in nm.union_faults("i.md", "a\n", "a\nb\n", "a\nc\n", "a\nb\n"))


def test_brief_numbers_used_twice_are_reported(tmp_path):
    d = tmp_path / nm.SC / "01_brief" / "briefs"
    d.mkdir(parents=True)
    for n in ("031_a.md", "031_b.md", "032_c.md", "INDEX.md"):
        (d / n).write_text("x")
    assert nm.brief_number_clashes(tmp_path) == {"031": ["031_a", "031_b"]}


def test_register_files_derived_from_its_inputs():
    assert nm.derived(f"{nm.REGISTER}/register/matrix.csv") and nm.derived(f"{nm.REGISTER}/register/comparisons/x.json")
    assert not nm.derived(nm.BOOKS) and not nm.derived(f"{nm.REGISTER}/register/held.json")
    assert not nm.derived(f"{nm.REGISTER}/register/returns/a.csv.gz") and not nm.derived("other.md")
