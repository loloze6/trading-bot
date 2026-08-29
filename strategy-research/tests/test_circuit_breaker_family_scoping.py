"""
F6 (P1a shakedown, 2026-07-04) regression test.

Fixture: the run_044 sequence. verdict_interpreter set status=refine for a brand-new
family (funding_rate_mean_reversion, its first-ever refine attempt), but the GLOBAL
recent_parameter_dimensions list already held two entries
(['regime_filter_er_threshold', 'er_threshold']) left over from long-closed,
unrelated Keltner/RSI-era families. The old code read that global list regardless of
family, so len(recent_dims) >= 2 forced an immediate pivot — on a family that had
never been refined even once. Also covers _family_names() (shares the F3 dict/string
mismatch bug, here in the escalate-to-pivot counter) and the
component_execution_error breaker-immunity rule.
"""

import sys
from pathlib import Path

import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr
from run_phase1_research import _apply_circuit_breaker, _family_names, determine_post_verdict_route


# The real, pre-purge global list from campaign_state.yaml, and the real six dict-shaped
# failed_families entries — both frozen here as the actual historical fixture.
_STALE_GLOBAL_DIMS = ["regime_filter_er_threshold", "er_threshold"]

_REAL_FAILED_FAMILIES = [
    {"name": "rsi_mean_reversion", "evidence_window": "2024_only", "root_cause": "signal_quality"},
    {"name": "keltner_breakout", "evidence_window": "2024_only", "root_cause": "signal_inversion"},
    {"name": "keltner_mean_reversion", "evidence_window": "2024_only", "root_cause": "regime_availability"},
    {"name": "rsi_momentum_trending", "evidence_window": "2024_only", "root_cause": "cost_drag"},
    {"name": "keltner_trend_mean_reversion", "evidence_window": "2024_only", "root_cause": "regime_availability"},
    {"name": "keltner_scoremode", "evidence_window": "2024_only", "root_cause": "signal_quality"},
]

_RUN_044_INTERP = {
    "hypothesis_id": "FUNDING_RATE_CONTINUOUS_MEAN_REVERSION",
    "status": "refine",
    "hypothesis_family": "funding_rate_mean_reversion",
    "proposed_change_dimension": "component_initialization_validation",
    "root_cause": {
        "mechanism_failure": "insufficient_sample_inconclusive",
        "supporting_evidence": "active_n_bars=0 across 16032 bars",
        "confidence": "high",
    },
}


def test_new_family_first_refine_is_not_forced_to_pivot_under_per_family_scoping():
    """THE regression: under the new per-family scheme, funding_rate_mean_reversion's
    dimension history is empty (it's never been refined before) — status must stay
    'refine', NOT be forced to 'pivot' by unrelated Keltner-era history."""
    campaign = {
        "recent_parameter_dimensions_by_family": {},  # brand new family: no entry yet
        "failed_families": _REAL_FAILED_FAMILIES,
    }
    result = _apply_circuit_breaker("refine", _RUN_044_INTERP, campaign)
    assert result == "refine", (
        f"expected 'refine' to survive for a family with no prior dimension history, got '{result}'"
    )


def test_old_global_list_would_have_wrongly_forced_pivot_if_it_leaked_in():
    """Documents the bug precisely: if funding_rate_mean_reversion's dimension history
    were (incorrectly) the stale global list, the breaker WOULD force pivot — showing
    the fix is doing real work, not a no-op."""
    campaign_with_leaked_history = {
        "recent_parameter_dimensions_by_family": {
            "funding_rate_mean_reversion": list(_STALE_GLOBAL_DIMS),  # simulates the bug
        },
        "failed_families": _REAL_FAILED_FAMILIES,
    }
    result = _apply_circuit_breaker("refine", _RUN_044_INTERP, campaign_with_leaked_history)
    assert result == "pivot", "sanity check: 2+ real dimensions for THIS family should still force pivot"


def test_unrelated_family_dimension_history_stays_isolated():
    """A family that legitimately has 2 tried dimensions must still force pivot for
    ITSELF, while leaving other families (including a brand-new one) untouched."""
    campaign = {
        "recent_parameter_dimensions_by_family": {
            "keltner_breakout": ["atr_multiplier", "scaling_factor"],
        },
        "failed_families": _REAL_FAILED_FAMILIES,
    }
    keltner_interp = {**_RUN_044_INTERP, "hypothesis_family": "keltner_breakout"}
    assert _apply_circuit_breaker("refine", keltner_interp, campaign) == "pivot"
    assert _apply_circuit_breaker("refine", _RUN_044_INTERP, campaign) == "refine"


def test_family_names_extracts_from_mixed_dict_and_string_entries():
    """_family_names() must handle the same mixed dict/string shape F3 fixed in
    _should_trigger_campaign_review — failed_families.count(family) on raw dict
    entries never matches a plain string, silently defeating the escalate breaker."""
    mixed = _REAL_FAILED_FAMILIES + ["ema_spread_trend_continuation", "ema_spread_trend_continuation"]
    names = _family_names(mixed)
    assert names.count("keltner_breakout") == 1
    assert names.count("ema_spread_trend_continuation") == 2
    assert names.count("rsi_mean_reversion") == 1


def test_escalate_breaker_now_fires_on_dict_shaped_repeat_failures():
    """Before this fix, failed_families.count(family) against dict entries always
    returned 0 — a family could never trigger the 2-pivots-in-a-family escalate rule
    as long as its failed_families entries were dict-shaped (true for every entry
    tagged since Improvement 07, 2026-07-02)."""
    campaign = {
        "recent_parameter_dimensions_by_family": {},
        "failed_families": _REAL_FAILED_FAMILIES,  # keltner_breakout appears once here
    }
    # Simulate a SECOND keltner_breakout failure just recorded (now 2 total).
    campaign["failed_families"] = campaign["failed_families"] + [
        {"name": "keltner_breakout", "evidence_window": "baseline_v2", "root_cause": "signal_inversion"}
    ]
    interp = {"hypothesis_family": "keltner_breakout", "status": "pivot"}
    assert _apply_circuit_breaker("pivot", interp, campaign) == "escalate"


def test_component_execution_error_is_immune_to_the_breaker(tmp_path, monkeypatch):
    """F6's other half: an engineering-failure diagnosis must short-circuit to
    human_pause BEFORE the circuit breaker (or anything else) can touch status."""
    monkeypatch.setattr(rpr, "ROOT", tmp_path)

    run_dir = tmp_path / "runs" / "run_test"
    (run_dir / "artifacts").mkdir(parents=True)
    interp_with_engineering_failure = {
        "hypothesis_id": "X",
        "status": "refine",
        "hypothesis_family": "some_family",
        "proposed_change_dimension": "whatever",
        "root_cause": {
            "mechanism_failure": "component_execution_error",
            "supporting_evidence": "active_n_bars=0, component_error_count=8040",
        },
    }
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump(interp_with_engineering_failure), encoding="utf-8"
    )
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump(
            {
                "run_id": "run_test",
                "status": "running",
                "current_stage": "verdict_interpreter",
                "pending_stage": "verdict_interpreter",
                "completed_stages": [],
            }
        ),
        encoding="utf-8",
    )
    # campaign_state.yaml with 2 stale dims for "some_family" — if the breaker ran at
    # all, it would force pivot; must never get the chance.
    (tmp_path / "campaign_state.yaml").write_text(
        yaml.safe_dump(
            {
                "recent_parameter_dimensions_by_family": {"some_family": ["dim_a", "dim_b"]},
                "failed_families": [],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", tmp_path / "campaign_state.yaml")

    next_stage = determine_post_verdict_route(run_dir, "run_test")

    assert next_stage == "human_pause"
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state["status"] == "paused_for_human"
    assert state["flags"]["component_execution_error_flagged"] is True
    # campaign_state must be untouched — no trial/family consumed for an engineering bug
    campaign_after = yaml.safe_load((tmp_path / "campaign_state.yaml").read_text(encoding="utf-8"))
    assert campaign_after["failed_families"] == []
