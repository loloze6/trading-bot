"""
E-037: the findings register and its triage must not drift apart.

WHY THIS EXISTS
---------------
The first triage pass grouped 25 findings by hand and silently dropped
**E037-07** — one of the highest-severity items in the set. Three more
(E037-28, E037-29, E037-30) were raised later and never added. So the document
written to *manage* the findings had itself drifted from the findings, which is
the exact failure this epic is about, one level up.

It was found by a mechanical check, not by re-reading. This is that check.

WHAT IT CHECKS
--------------
1. Every `## E037-nn` section in FINDINGS.md has a summary-table row.
2. Every finding appears somewhere in S3_TRIAGE.md.
3. The stated severity counts match the actual ones.

Cheap, and it fails the moment a finding is added without being triaged.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pytest

_E = Path(__file__).resolve().parent.parent / "engineering" / "roadmap" / "E-037"
_FINDINGS = _E / "FINDINGS.md"
_TRIAGE = _E / "S3_TRIAGE.md"

pytestmark = pytest.mark.skipif(
    not _FINDINGS.exists(), reason="E-037 records not present in this checkout"
)


def _ids() -> list[str]:
    return re.findall(r"^## (E037-\d+)$", _FINDINGS.read_text(encoding="utf-8"), re.M)


def test_every_finding_has_a_summary_row() -> None:
    text = _FINDINGS.read_text(encoding="utf-8")
    rows = set(re.findall(r"^\| \[(E037-\d+)\]", text, re.M))
    missing = [i for i in _ids() if i not in rows]
    assert not missing, (
        f"finding(s) with no row in the summary table: {missing}. The table is the "
        f"index; a finding absent from it is invisible to anyone scanning."
    )


def test_every_finding_is_triaged() -> None:
    if not _TRIAGE.exists():
        pytest.skip("S3_TRIAGE.md not present")
    triaged = set(re.findall(r"E037-\d+", _TRIAGE.read_text(encoding="utf-8")))
    missing = [i for i in _ids() if i not in triaged]
    assert not missing, (
        f"finding(s) never triaged: {missing}.\n"
        f"S3_TRIAGE.md is what a decision-maker reads; a finding missing from it "
        f"does not get decided. E037-07, a high-severity item, was lost this way."
    )


def test_stated_severity_counts_match() -> None:
    text = _FINDINGS.read_text(encoding="utf-8")
    m = re.search(r"\*\*Counts:\*\* (\d+) high · (\d+) medium · (\d+) low", text)
    assert m, "the summary's '**Counts:** N high · N medium · N low' line is missing"
    stated = {"high": int(m.group(1)), "medium": int(m.group(2)), "low": int(m.group(3))}
    actual = Counter(re.findall(r"\*\*Severity:\*\* (?:✅ )?\*{0,2}(high|medium|low)", text))
    assert stated == dict(actual), (
        f"stated counts {stated} != actual {dict(actual)}. Update the Counts line "
        f"when adding a finding."
    )
