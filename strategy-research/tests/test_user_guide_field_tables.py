"""
E-037 E037-24 gate: USER_GUIDE.md §3's field tables must not drift further from
the artifacts they describe.

WHY THIS EXISTS
---------------
S2 audited every §3 field table against every matching artifact on disk and
found five entries documenting fields that appear in ZERO real files —
`escalation_request.yaml` at 3 of 3, `protocol_result.yaml` at 6 of 7. The
root was that the tables were written from intended design and never
reconciled with output. Nothing detected that, because nothing was looking.

WHAT IT CHECKS, AND WHAT IT DELIBERATELY DOES NOT
-------------------------------------------------
It is a RATCHET, not a clean-room assertion. The known backlog is recorded in
KNOWN_PHANTOM below and tolerated; the test fails only when a NEW phantom
field appears, or when an entry's phantom set grows. Same principle as the
repo's other drift guards: pre-existing debt is not a test failure, new debt
is.

That choice is deliberate. A strict test would fail on commit one and be
disabled by the second person who hit it. A ratchet stays green today, blocks
regression, and shrinks as S3/S4 fix entries — and shrinking it is enforced
too: if an entry gets fixed but stays listed here, the test fails and tells
you to remove it. The baseline cannot silently rot.

LIMITATION (stated, not hidden)
-------------------------------
This detects documented-but-absent keys. It CANNOT distinguish a renamed
field from a deleted one, and it says nothing about real fields that are
undocumented — the other half of E037-24, which needs a human read. Passing this
test does not mean §3 is correct; it means §3 got no worse.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

_SR = Path(__file__).resolve().parent.parent
_GUIDE = _SR / "docs" / "USER_GUIDE.md"

# Entry heading -> fields documented but present in ZERO real artifacts.
# Measured 2026-08-30 (E-037 S2). Shrink this as entries are fixed; the test
# fails if an entry listed here turns out to be clean.
#
# 2026-09-03 (CUL-187): the last four entries all fixed the same way as
# verdict_interpretation.yaml below -- table replaced with the artifact's
# real fields, phantom names preserved as a historical note in prose (not in
# the table), so none of them carry a documented-but-absent field any more.
# Baseline now empty; kept as a dict (not deleted) so the next drift has a
# place to land and the docstring's shrink-to-empty claim stays checkable.
KNOWN_PHANTOM: dict[str, set[str]] = {
    # 2026-09-03 (E037-02/03/04/05/08): both real, verified directly against
    # prescreen_signal.py source, just absent from the specific 10 sample
    # files this test's _instances() glob picks up under runs/*/artifacts/ --
    # situational, not invented. `a86_power_check` only appears on the two
    # orchestrator-written stub shapes (A8.6 blocked before the tool ever
    # runs, run_phase1_research.py:2368/6400), which none of the 10 sampled
    # runs hit. `gap_stats_by_symbol` is written by prescreen_signal.py:1630
    # but only carries entries when a real data gap was actually found and
    # dropped (#50 A) -- none of the 10 sampled runs had one.
    "`prescreen_result.yaml`": {"a86_power_check", "gap_stats_by_symbol"},
    # NOTE: `verdict_interpretation.yaml` is deliberately absent. S2 rewrote that
    # table from real artifacts, so its five phantom names (altitude, verdict,
    # diagnostic_rule_applied, parameter_bracket, next_altitude) no longer appear
    # as documented fields -- they survive as intended-design prose above the
    # table, which this parser correctly does not treat as a field claim. It is
    # the worked example of an entry leaving this baseline. (2026-08-31)
    #
    # `escalation_request.yaml`, `protocol_result.yaml` / `protocol_summary.json`,
    # `regime_detector_report.yaml`, `regime_audit_decision.yaml`: fixed the same
    # way 2026-09-03 (CUL-187) -- see USER_GUIDE.md for each entry's real table.
}


def _documented_fields() -> dict[str, list[str]]:
    """Parse §3's field tables -> {entry heading: [field names]}."""
    text = _GUIDE.read_text(encoding="utf-8")
    section = text[text.index("## 3. Artifacts"): text.index("## 4. Skills")]
    out: dict[str, list[str]] = {}
    for entry in re.split(r"\n### ", section)[1:]:
        head = entry.split("\n")[0].strip()
        table = re.search(r"\| Field \|.*\n\|[-| ]+\n((?:\|.*\n)+)", entry)
        if not table:
            continue
        fields = []
        for row in table.group(1).strip().split("\n"):
            cell = row.split("|")[1].strip()
            fields.extend(re.findall(r"`([A-Za-z0-9_]+)`", cell))
        if fields:
            out[head] = fields
    return out


def _instances(head: str) -> list[Path]:
    m = re.match(r"`([^`]+)`", head)
    if not m:
        return []
    fn = m.group(1)
    if fn.startswith("config/"):
        p = _SR / fn
        return [p] if p.is_file() else []
    pats = [f"runs/*/artifacts/{fn}", f"runs/*/{fn}", f"campaign_record/{fn}", fn]
    return [p for pat in pats for p in _SR.glob(pat) if p.is_file()]


def _all_keys(node):
    """Every key at EVERY depth.

    Top-level-only was the original bug, found 2026-08-31: it reported
    `median_sharpe` as absent from protocol_result.yaml, where it is present --
    nested -- in 31 of 38 files. "Not a top-level key" is a different claim from
    "does not exist", and conflating the two turned a misfiling into an
    accusation of invention. Same correction applied to
    `class_conditional_sensitivity` in regime_detector_report.yaml.
    """
    if isinstance(node, dict):
        for k, v in node.items():
            yield k
            yield from _all_keys(v)
    elif isinstance(node, list):
        for x in node:
            yield from _all_keys(x)


def _real_keys(paths: list[Path]) -> tuple[set[str], int]:
    keys: set[str] = set()
    n = 0
    for p in paths:
        try:
            raw = p.read_text(encoding="utf-8")
            doc = json.loads(raw) if p.suffix == ".json" else yaml.safe_load(raw)
        except Exception:
            continue
        if isinstance(doc, dict):
            keys |= set(_all_keys(doc))
            n += 1
    return keys, n


@pytest.mark.parametrize("head", sorted(_documented_fields()))
def test_no_new_phantom_fields(head: str) -> None:
    """A documented field absent from every real artifact is a phantom field."""
    fields = _documented_fields()[head]
    paths = _instances(head)
    real, n = _real_keys(paths)
    if n == 0:
        pytest.skip(f"no real instances of {head} on disk to check against")

    phantom = {f for f in fields if f not in real}
    allowed = KNOWN_PHANTOM.get(head, set())

    new = phantom - allowed
    assert not new, (
        f"NEW phantom field(s) in USER_GUIDE.md §3 for {head}: {sorted(new)}.\n"
        f"These are documented but appear in none of the {n} real artifact(s) on disk.\n"
        f"Either the field name is wrong, or the entry describes intended design "
        f"rather than the artifact -- see E-037 FINDINGS.md E037-24.\n"
        f"If it is genuinely intended-design, mark it as such in the entry AND add "
        f"it to KNOWN_PHANTOM in this file with a dated note."
    )

    fixed = allowed - phantom
    assert not fixed, (
        f"{head}: {sorted(fixed)} is listed in KNOWN_PHANTOM but now appears in real "
        f"artifacts. Remove it from the baseline -- a stale allowlist stops the ratchet "
        f"from tightening."
    )


def test_baseline_entries_still_exist() -> None:
    """KNOWN_PHANTOM must not name entries the guide no longer has."""
    documented = set(_documented_fields())
    stale = set(KNOWN_PHANTOM) - documented
    assert not stale, (
        f"KNOWN_PHANTOM names §3 entries that no longer exist (or were renamed): "
        f"{sorted(stale)}. Update the baseline."
    )
