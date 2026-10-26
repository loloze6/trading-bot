"""
C5.7b-2 -- score provenance, slices S2 + S4 (D-048;
engineering/review_2026-09-27/C5_7B_PROVENANCE_S1.md). Review finding C12.

Behind orchestrator.score_provenance.enabled (added by C5.7b-1):
  S2  `rubric_version` on a reader proposal is a closed per-category set
      (tools/reader_proposals.READER_RUBRIC_VERSIONS), pinned here to the literals.
      `load_proposals(..., strict_provenance=)` defaults False, so every existing `-v1`
      fixture stays valid; under the flag the loader is strict (an old run's v2 files).
  S4  D-198: `resolve_evidence_paths` (the record-only citation resolver) and its tests are
      deleted with the readers.

Proven with stubs only: no LLM, no API call, no backtest, no trial row, no holdout,
nothing under the real campaign_record/ or runs/ (tests/conftest.py's autouse
sandbox redirects rpr.ROOT).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import reader_proposals as rp  # noqa: E402

from _reader_test_helpers import (  # noqa: E402
    ALL_ON, ON, _one_proposal, _set_orchestrator,
)

CAT = "profitability"
CATEGORIES = ["profitability", "forecast_power", "regime_power", "component_attribution",
              "trade_efficiency"]
# Independent pin of each SKILL's rubric literal. regime_power is -v3 since CUL-381
# removed detector_health from its report and its scoring rows.
EXPECTED_RUBRIC = {c: f"{c}-reader-v2" for c in CATEGORIES}
EXPECTED_RUBRIC["regime_power"] = "regime_power-reader-v3"


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _write(tmp_path: Path, cat: str, proposals: list) -> Path:
    d = tmp_path / "proposals"
    d.mkdir(exist_ok=True)
    (d / f"{cat}.yaml").write_text(yaml.safe_dump(proposals, sort_keys=False), encoding="utf-8")
    return d


def _proposal(cat=CAT, rubric=None, evidence=None, pid=None, n=1) -> dict:
    p = _one_proposal(pid=pid or f"{cat}-run_990-{n}")
    p["rubric_version"] = rubric if rubric is not None else rp.READER_RUBRIC_VERSIONS[cat]
    if evidence is not None:
        p["evidence"] = evidence
    return p


# ---------------------------------------------------------------------------
# S2a. the closed set is pinned to the SKILL files
# ---------------------------------------------------------------------------

def test_the_closed_set_covers_exactly_the_reader_categories():
    assert sorted(rp.READER_RUBRIC_VERSIONS) == sorted(CATEGORIES)
    assert sorted(rpr.READER_CATEGORIES) == sorted(CATEGORIES)


@pytest.mark.parametrize("cat", CATEGORIES)
def test_the_rubric_constants_are_the_pinned_literals(cat):
    """D-198: the reader SKILL files this was pinned to are deleted; the literal is pinned
    here (an old run's proposals carry it, so the constant must not drift)."""
    assert rp.READER_RUBRIC_VERSIONS[cat] == EXPECTED_RUBRIC[cat]


# ---------------------------------------------------------------------------
# S2b. strict_provenance in load_proposals
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad", [
    "made-up-v2",                      # unknown
    "forecast_power-reader-v2",        # another category's rubric
    "profitability-reader-v1",         # the old value
    "profitability-reader-v3",         # a future value the constant does not know
    "profitability-reader-v2 ",        # not an exact match
])
def test_strict_rejects_unknown_other_category_and_v1(tmp_path, bad):
    d = _write(tmp_path, CAT, [_proposal(rubric=bad)])
    with pytest.raises(rp.ProposalError, match=r"rubric_version=.* write exactly 'profitability-reader-v2'"):
        rp.load_proposals(d, [CAT], strict_provenance=True)


@pytest.mark.parametrize("value", ["made-up-v2", "forecast_power-reader-v2",
                                   "profitability-reader-v1", "profitability-reader-v3"])
def test_default_accepts_what_strict_rejects(tmp_path, value):
    d = _write(tmp_path, CAT, [_proposal(rubric=value)])
    assert rp.load_proposals(d, [CAT])[CAT][0]["rubric_version"] == value
    assert rp.load_proposals(d, [CAT], strict_provenance=False)[CAT][0]["rubric_version"] == value


@pytest.mark.parametrize("cat", CATEGORIES)
def test_strict_accepts_each_categorys_own_v2(tmp_path, cat):
    d = _write(tmp_path, cat, [_proposal(cat=cat)])
    assert rp.load_proposals(d, [cat], strict_provenance=True)[cat][0]["rubric_version"] == EXPECTED_RUBRIC[cat]


def test_strict_rejects_an_unlisted_category(tmp_path):
    d = _write(tmp_path, "zzz", [{**_proposal(), "proposal_id": "zzz-run_990-1"}])
    with pytest.raises(rp.ProposalError, match="no closed rubric_version is defined for category 'zzz'"):
        rp.load_proposals(d, ["zzz"], strict_provenance=True)


def test_an_empty_or_absent_file_is_still_fine_under_strict(tmp_path):
    d = tmp_path / "proposals"
    d.mkdir()
    (d / f"{CAT}.yaml").write_text("[]\n", encoding="utf-8")
    assert rp.load_proposals(d, [CAT, "regime_power"], strict_provenance=True) == \
        {CAT: [], "regime_power": []}


def test_brief_cards_are_untouched_brief_card_v1_is_still_the_card_rubric():
    import decide_next as dn
    assert dn.BRIEF_CARD_RUBRIC == "brief-card-v1"
    assert "brief-card-v1" not in rp.READER_RUBRIC_VERSIONS.values()


# ---------------------------------------------------------------------------
# S2c. wired into the reader stage under the flag (existing retry path)
# ---------------------------------------------------------------------------

def test_reader_strictness_is_empty_flag_off_and_strict_flag_on():
    _set_orchestrator(ALL_ON)
    assert rpr._reader_strictness() == {}
    _set_orchestrator({**ALL_ON, "score_provenance": {"enabled": False}})
    assert rpr._reader_strictness() == {}
    _set_orchestrator(ON)
    assert rpr._reader_strictness() == {"strict_provenance": True}


# D-198: the citation resolver (resolve_evidence_paths and its tests), the audit-log citation
# block, the reader stage's retry/stamp wiring and their flag-off identity tests went with the
# readers; the closed rubric set (an old run's files, the analyst's reading) stays above.
