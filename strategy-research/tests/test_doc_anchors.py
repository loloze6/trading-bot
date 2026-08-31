"""
E-037: keep documentation `file:line` / `file::symbol` anchors honest.

WHY THIS EXISTS
---------------
E-037 wrote ~80 explicit code anchors into USER_GUIDE.md and the E-037 records.
Nine of roughly forty were wrong on first write and were corrected by hand. Line
numbers rot on every edit above them, so without a check the whole set silently
decays into confident-looking noise — the same failure mode as the phantom
fields in §3 (see FINDINGS.md E037-24), one layer down.

WHAT IT CHECKS
--------------
1. `file.py:N`      -> the file exists and N is a real line in it.
2. `file.py::name`  -> the file exists and defines that top-level name.

(2) is the maintainable form and the one to prefer when writing new anchors: a
function or constant name survives edits above it, is greppable, and tells the
reader what to look for. A line number does none of those. This test accepts
both so the existing corpus stays green, and reports the split so the migration
is visible rather than aspirational.

WHAT IT DELIBERATELY DOES NOT CHECK
-----------------------------------
Bare `:N` anchors — the shorthand used inside a stage block that has already
named its file — are counted but not validated. Resolving them needs the
enclosing prose context, and two attempts at doing that automatically produced
wrong attributions (E-037 S3, 2026-08-31). Guessing here would be worse than
not checking: a confidently wrong anchor is more harmful than an unchecked one.

Passing this test means no anchor points at nothing. It does not mean an anchor
points at the *right* thing — only a human read establishes that.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

_SR = Path(__file__).resolve().parent.parent

DOCS = [
    _SR / "docs" / "USER_GUIDE.md",
    _SR / "CLAUDE.md",
    _SR / "engineering" / "roadmap" / "E-037" / "S1_TARGET_SHAPE.md",
    _SR / "engineering" / "roadmap" / "E-037" / "FINDINGS.md",
    _SR / "engineering" / "roadmap" / "E-037" / "S3_TRIAGE.md",
    _SR / "engineering" / "roadmap" / "E-037" / "S2_RELOCATION_INVENTORY.md",
]

# basename -> path. Only files E-037 actually anchors into.
SOURCES = {
    "prescreen_signal.py": _SR / "tools" / "prescreen_signal.py",
    "episode_significance.py": _SR / "tools" / "episode_significance.py",
    "run_phase1_research.py": _SR / "workflow" / "run_phase1_research.py",
    "run_campaign.py": _SR / "workflow" / "run_campaign.py",
}

ANCHOR = re.compile(
    r"`(?P<file>[A-Za-z0-9_./-]+\.py)(?P<sep>::|:)(?P<target>[A-Za-z0-9_]+|\d+(?:-\d+)?)`"
)


def _top_level_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    return names


def _anchors() -> list[tuple[str, str, str, str]]:
    """(doc name, basename, sep, target) for every explicit anchor."""
    found = []
    for doc in DOCS:
        if not doc.exists():
            continue
        for m in ANCHOR.finditer(doc.read_text(encoding="utf-8")):
            found.append(
                (doc.name, m.group("file").split("/")[-1], m.group("sep"), m.group("target"))
            )
    return found


_ALL = _anchors()
_KNOWN = [a for a in _ALL if a[1] in SOURCES]


def test_some_anchors_are_present() -> None:
    """Guard against the regex silently matching nothing after a docs reshuffle."""
    assert len(_KNOWN) >= 50, (
        f"only {len(_KNOWN)} anchors found across {len(DOCS)} docs -- the parser has "
        f"probably stopped matching. Check ANCHOR against the docs' current style."
    )


@pytest.mark.parametrize("doc,basename,sep,target", _KNOWN,
                         ids=[f"{d}:{b}{s}{t}" for d, b, s, t in _KNOWN])
def test_anchor_resolves(doc: str, basename: str, sep: str, target: str) -> None:
    src = SOURCES[basename]
    assert src.exists(), f"{doc} anchors into {basename}, which no longer exists at {src}"

    if sep == "::":
        names = _top_level_names(src)
        assert target in names, (
            f"{doc} references `{basename}::{target}`, but {basename} defines no "
            f"top-level `{target}`. It was renamed or removed -- update the doc."
        )
    else:
        n = int(target.split("-")[0])
        total = len(src.read_text(encoding="utf-8").splitlines())
        assert 1 <= n <= total, (
            f"{doc} references `{basename}:{n}`, but {basename} has {total} lines. "
            f"The anchor is stale. Prefer the `{basename}::symbol` form when fixing "
            f"it -- symbols survive edits, line numbers do not."
        )


def test_report_anchor_style_split(capsys: pytest.CaptureFixture) -> None:
    """Not a gate -- prints the line-number vs symbol split so migration is visible."""
    by_line = sum(1 for a in _KNOWN if a[2] == ":")
    by_symbol = sum(1 for a in _KNOWN if a[2] == "::")
    bare = 0
    for doc in DOCS:
        if doc.exists():
            bare += len(re.findall(r"`:\d+(?:-\d+)?`", doc.read_text(encoding="utf-8")))
    with capsys.disabled():
        print(
            f"\n  doc anchors -- by line number: {by_line} | by symbol: {by_symbol} "
            f"| bare `:N` (unvalidated): {bare}"
        )
    assert by_line + by_symbol == len(_KNOWN)
