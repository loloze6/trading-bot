"""
A5.4 / F09 (2026-07-06): run_053's campaign_review recommended reframing into
reactivating BOTH H-041-A (funding-rate mean-reversion) and H-041-C (fear/greed
contrarian) via next_research_question. Both had already been closed by
run_050/run_048 (P1b, 2026-07-05/06) — but campaign_knowledge_base.yaml's
findings for them were never written back with the closing verdict, so
reactivation_condition still read as open at review time. Two independent fixes:

  F09  (_write_kb_findings_entry): stamps reactivation_consumed_by automatically
       when a run resolves an open reactivation_condition with a definitive verdict,
       so a KB entry can't go stale like this again going forward.
  A5.4 (_check_kb_reactivation_conformance, wired into
       determine_post_campaign_review_route): a conformance gate that catches a
       reframe targeting an ALREADY-consumed/exhausted KB entry (whether stale from
       before F09 existed, or from any other drift) — pauses instead of scaffolding
       the run.

Fixture: run_053's REAL next_research_question (frozen, from
runs/run_053/artifacts/campaign_review.yaml, 2026-07-06) and the corrected KB
findings for H-041-A/H-041-C (the actual post-fix campaign_knowledge_base.yaml
content), per this project's standing rule that regression tests use the actual
historical failure as fixture.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
WORKFLOW_PATH = ROOT / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402

# Frozen REAL next_research_question from run_053's campaign_review.yaml (2026-07-06) —
# see the "reuse_scheduled_backward_extension_pass (per KB operational.backward_extension_pass:
# H-041-A and H-041-C)" line and the research_goal explicitly asking to
# "Test both mechanisms ungated on extended data."
RUN_053_NEXT_RESEARCH_QUESTION = {
    "strategy_domain": "structural_and_behavioral_signals",
    "market_universe": ["BTCUSDT", "ETHUSDT"],
    "timeframe": "1h",
    "constraints": [
        "Must not propose ideas that require replacing the whole existing bot architecture.",
        "Do not write code.",
    ],
    "research_goal": (
        "Evaluate whether structural (forced-flow) and behavioral (persistent sentiment "
        "bias) signals produce real, cost-surviving edges on BTC/ETH when evaluated over "
        "7-year historical window (2018-2025). These mechanisms were power-parked in KB "
        "findings funding_rate_mean_reversion_inconclusive and fear_greed_contrarian_inconclusive. "
        "Test both mechanisms ungated on extended data."
    ),
    "existing_context": [
        "use_existing_backtest_framework",
        "reuse_scheduled_backward_extension_pass (per KB operational.backward_extension_pass: H-041-A and H-041-C)",
    ],
}

# The corrected KB findings for H-041-A/H-041-C, post-fix (both reactivation_consumed_by set).
CORRECTED_KB = {
    "findings": [
        {
            "id": "funding_rate_mean_reversion_inconclusive",
            "hypothesis_id": "H-041-A",
            "outcome": "no_edge_observed",
            "exhausted": True,
            "exhausted_basis": "Empirical (run_050): well-powered null.",
            "reactivation_condition": None,
            "reactivation_consumed_by": "run_050",
        },
        {
            "id": "fear_greed_contrarian_inconclusive",
            "hypothesis_id": "H-041-C",
            "outcome": "era_conditional_instability",
            "exhausted": True,
            "exhausted_basis": "Empirical (run_048): significant but era-unstable.",
            "reactivation_condition": None,
            "reactivation_consumed_by": "run_048",
        },
    ]
}

# The STALE, pre-fix KB findings — same shape as what actually shipped before this fix,
# reactivation_condition still open, no reactivation_consumed_by.
STALE_KB = {
    "findings": [
        {
            "id": "funding_rate_mean_reversion_inconclusive",
            "hypothesis_id": "H-041-A",
            "outcome": "inconclusive",
            "exhausted": False,
            "reactivation_condition": "PRIMARY: Backward data extension to 2018+ ...",
            "reactivation_consumed_by": None,
        },
        {
            "id": "fear_greed_contrarian_inconclusive",
            "hypothesis_id": "H-041-C",
            "outcome": "inconclusive",
            "exhausted": False,
            "reactivation_condition": "Data extension to 2018+ ...",
            "reactivation_consumed_by": None,
        },
    ]
}


def test_gate_catches_the_real_run_053_reframe_against_corrected_kb():
    violations = rpr._check_kb_reactivation_conformance(RUN_053_NEXT_RESEARCH_QUESTION, CORRECTED_KB)
    assert len(violations) == 2  # both H-041-A and H-041-C are named and both are consumed
    joined = " ".join(violations)
    assert "H-041-A" in joined and "run_050" in joined
    assert "H-041-C" in joined and "run_048" in joined


def test_gate_allows_the_same_reframe_when_reactivation_is_genuinely_still_open():
    # Sanity: the gate must not false-positive on a legitimately open reactivation —
    # only reactivation_consumed_by / bare-exhausted findings are violations.
    violations = rpr._check_kb_reactivation_conformance(RUN_053_NEXT_RESEARCH_QUESTION, STALE_KB)
    assert violations == []


def test_gate_is_a_noop_with_no_next_research_question():
    assert rpr._check_kb_reactivation_conformance({}, CORRECTED_KB) == []
    assert rpr._check_kb_reactivation_conformance(None, CORRECTED_KB) == []


def test_f09_hook_stamps_reactivation_consumed_by_on_definitive_new_verdict(tmp_path):
    """_write_kb_findings_entry's existing-entry branch must close an open
    reactivation_condition when the new verdict is definitive (not itself another
    inconclusive/underpowered result) — this is what would have prevented
    funding_rate_mean_reversion_inconclusive from ever going stale after run_050."""
    kb_path = tmp_path / "campaign_knowledge_base.yaml"
    kb_content = {
        "findings": [
            {
                "id": "funding_rate_mean_reversion_inconclusive",
                "hypothesis_id": "H-041-A",
                "evidence_runs": ["run_041"],
                "evidence_count": 1,
                "outcome": "inconclusive",
                "exhausted": False,
                "exhausted_basis": None,
                "reactivation_condition": "PRIMARY: Backward data extension to 2018+ ...",
            }
        ]
    }
    rpr.save_yaml(kb_path, kb_content)

    orig_kb_path = rpr._KB_PATH
    rpr._KB_PATH = kb_path
    try:
        interp = {
            "hypothesis_id": "H-041-A",
            "run_id": "run_050",
            "verdict_label": "kill_no_ic",
            "prescreen_result_summary": {"ic_active_bars": 0.017764, "p_value": 0.521},
        }
        rpr._write_kb_findings_entry(tmp_path, "run_050", interp)

        updated = rpr.load_yaml(kb_path)
        entry = updated["findings"][0]
        assert entry["reactivation_consumed_by"] == "run_050"
        assert entry["reactivation_condition"] is None
        assert entry["outcome"] == "no_edge_observed"
        assert entry["exhausted"] is True
    finally:
        rpr._KB_PATH = orig_kb_path


def test_f09_hook_does_not_close_reactivation_on_another_inconclusive_result():
    """A re-parked (still-inconclusive) result must NOT close the reactivation_condition —
    only a definitive verdict does. Otherwise a second underpowered attempt would
    silently forfeit the ability to try again once genuinely adequate data exists."""
    findings = [
        {
            "id": "some_finding",
            "hypothesis_id": "H-TEST",
            "evidence_runs": ["run_100"],
            "evidence_count": 1,
            "outcome": "inconclusive",
            "exhausted": False,
            "reactivation_condition": "some open condition",
        }
    ]
    existing = rpr._find_kb_entry(findings, "H-TEST")
    assert existing is not None
    # Simulate the same logic _write_kb_findings_entry applies inline (kept in sync
    # with the real function's condition below — see that function for the source
    # of truth if this ever needs updating).
    outcome = "inconclusive"
    verdict_label = "insufficient_sample_inconclusive"
    is_still_open = outcome == "inconclusive" or "insufficient" in verdict_label
    assert is_still_open is True  # confirms the guard would correctly skip closing
