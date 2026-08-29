"""
Known-answer tests for run_campaign.py's mechanical wishlist trigger evaluation
(2026-07-10). Closes the run_045/046 gap: campaign_review previously recommended
consuming a wishlist family without anyone (human or code) checking its
trigger_condition -- see meta_findings.daily_regime_overlay_recommended_before_a23_trigger
in campaign_knowledge_base.yaml. Now every trigger_condition is a structured
predicate, mechanically evaluated against the KB.
"""

import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
if str(WORKFLOW_PATH) not in sys.path:
    sys.path.insert(0, str(WORKFLOW_PATH))

import run_campaign as rc


@pytest.mark.real_repo_readonly
def test_er_overlay_predicate_does_not_fire_against_real_kb():
    """2026-07-10, post-incident (see strategy-research/docs/analysis-reports/INCIDENT_20260710.md):
    this test previously asserted 'true' because p4_sma_trend_longonly_daily_auto's
    outcome was kill_ungated_regime_mismatch. A metric-basis audit found the
    median_sharpe behind that kill verdict was a LIFO-fragment trade-exit-day
    statistic with a basis problem under sparse trading (1-8 trades/window);
    recomputed bar-level from bars.csv total_portfolio_value it is positive for
    both symbols (BTCUSDT +0.579, ETHUSDT +0.032), flipping protocol_verdict to
    refine. The KB entry's outcome is now refine_pending_regime_gating, which
    fails this predicate's outcome-in-[kill_ungated_regime_mismatch] condition
    cleanly -- the predicate correctly reports 'false' (not_triggered), not
    'true'. This assertion encodes CURRENT ground truth, not a fixed
    expectation to preserve across future KB corrections -- if it fails again
    because the KB changed, recompute the underlying numbers before assuming
    either this test or the KB is wrong (see the incident's arbitration
    doctrine in docs/TIMEFRAME_CHANGE_PLAYBOOK.md section 5)."""
    result = rc.evaluate_wishlist_predicate("daily_timeframe_er_overlay")
    assert result["result"] == "false"
    assert result["matched_finding_id"] is None


def test_unknown_family_is_missing_field():
    result = rc.evaluate_wishlist_predicate("nonexistent_family_xyz")
    assert result["result"] == "missing_field"


def test_get_dotted_field_traverses_nested_dicts():
    d = {"signal_property": {"per_trade_expectancy_bps": 1050.5}}
    assert rc._get_dotted_field(d, "signal_property.per_trade_expectancy_bps") == 1050.5


def test_get_dotted_field_missing_returns_sentinel():
    d = {"signal_property": {}}
    assert (
        rc._get_dotted_field(d, "signal_property.per_trade_expectancy_bps")
        is rc._MISSING
    )
    assert rc._get_dotted_field(d, "nonexistent.path") is rc._MISSING


def test_apply_predicate_op_all_operators():
    assert rc._apply_predicate_op(">", 5, 3) is True
    assert rc._apply_predicate_op(">=", 3, 3) is True
    assert rc._apply_predicate_op("<", 2, 3) is True
    assert rc._apply_predicate_op("<=", 3, 3) is True
    assert rc._apply_predicate_op("==", "x", "x") is True
    assert rc._apply_predicate_op("!=", "x", "y") is True
    assert rc._apply_predicate_op("in", "a", ["a", "b"]) is True
    assert rc._apply_predicate_op(">", 1, 3) is False


def test_predicate_false_when_no_finding_satisfies_all_conditions(
    tmp_path, monkeypatch
):
    """A finding that satisfies SOME but not all conditions must not fire --
    all_of means every condition on the SAME finding."""
    kb = {
        "findings": [
            {
                "id": "partial_match",
                "outcome": "kill_ungated_regime_mismatch",
                "signal_property": {
                    "per_trade_expectancy_bps": -50.0,  # fails: not > 0
                    "per_trade_expectancy_t_stat": 2.0,
                },
            },
        ]
    }
    wishlist = {
        "candidates": [
            {
                "family": "test_family",
                "trigger_condition": {
                    "predicate": {
                        "source": "kb_finding",
                        "all_of": [
                            {
                                "field": "signal_property.per_trade_expectancy_bps",
                                "op": ">",
                                "value": 0,
                            },
                            {
                                "field": "outcome",
                                "op": "in",
                                "value": ["kill_ungated_regime_mismatch"],
                            },
                        ],
                    }
                },
            },
        ]
    }
    (tmp_path / "campaign_record").mkdir(exist_ok=True)
    kb_path = tmp_path / "campaign_record" / "campaign_knowledge_base.yaml"
    dw_dir = tmp_path / "config"
    dw_dir.mkdir(parents=True, exist_ok=True)
    dw_path = dw_dir / "detector_wishlist.yaml"
    kb_path.write_text(yaml.safe_dump(kb), encoding="utf-8")
    dw_path.write_text(yaml.safe_dump(wishlist), encoding="utf-8")

    monkeypatch.setattr(rc, "ROOT", tmp_path)
    result = rc.evaluate_wishlist_predicate("test_family")
    assert result["result"] == "false"


def test_sentinel_absence_on_dead_record_does_not_mask_clean_false(
    tmp_path, monkeypatch
):
    """2026-07-10: a record whose relevant field predates its schema (explicitly
    marked NOT_COMPUTED_SENTINEL) must NOT force 'missing_field' when that same
    record already fails some OTHER, resolvable condition -- it was never going
    to match regardless of the unresolved field's true value. Only a record
    that COULD otherwise match (all other conditions hold) with a genuinely
    unresolved field is a real data gap. Regression for the
    keltner_mean_reversion_no_edge masking case: that record's outcome
    (no_edge_observed) already excludes it from a predicate requiring
    outcome in [kill_ungated_regime_mismatch] -- its pre-schema absence of
    per_trade_expectancy_bps must not turn a clean false into missing_field."""
    kb = {
        "findings": [
            {
                "id": "dead_record_pre_schema",
                "outcome": "no_edge_observed",
                "signal_property": {
                    "per_trade_expectancy_bps": rc.NOT_COMPUTED_SENTINEL
                },
            },
        ]
    }
    wishlist = {
        "candidates": [
            {
                "family": "test_family3",
                "trigger_condition": {
                    "predicate": {
                        "source": "kb_finding",
                        "all_of": [
                            {
                                "field": "signal_property.per_trade_expectancy_bps",
                                "op": ">",
                                "value": 0,
                            },
                            {
                                "field": "outcome",
                                "op": "in",
                                "value": ["kill_ungated_regime_mismatch"],
                            },
                        ],
                    }
                },
            },
        ]
    }
    (tmp_path / "campaign_record").mkdir(exist_ok=True)
    kb_path = tmp_path / "campaign_record" / "campaign_knowledge_base.yaml"
    dw_dir = tmp_path / "config"
    dw_dir.mkdir(parents=True, exist_ok=True)
    dw_path = dw_dir / "detector_wishlist.yaml"
    kb_path.write_text(yaml.safe_dump(kb), encoding="utf-8")
    dw_path.write_text(yaml.safe_dump(wishlist), encoding="utf-8")

    monkeypatch.setattr(rc, "ROOT", tmp_path)
    result = rc.evaluate_wishlist_predicate("test_family3")
    assert result["result"] == "false"


def test_sentinel_absence_on_record_that_could_otherwise_match_is_missing_field(
    tmp_path, monkeypatch
):
    """Contrast case: when the ONLY blocker is the unresolved/sentinel field --
    every other condition already holds -- that IS a genuine data gap and must
    still report missing_field."""
    kb = {
        "findings": [
            {
                "id": "could_match_but_unscored",
                "outcome": "kill_ungated_regime_mismatch",
                "signal_property": {
                    "per_trade_expectancy_bps": rc.NOT_COMPUTED_SENTINEL
                },
            },
        ]
    }
    wishlist = {
        "candidates": [
            {
                "family": "test_family4",
                "trigger_condition": {
                    "predicate": {
                        "source": "kb_finding",
                        "all_of": [
                            {
                                "field": "signal_property.per_trade_expectancy_bps",
                                "op": ">",
                                "value": 0,
                            },
                            {
                                "field": "outcome",
                                "op": "in",
                                "value": ["kill_ungated_regime_mismatch"],
                            },
                        ],
                    }
                },
            },
        ]
    }
    (tmp_path / "campaign_record").mkdir(exist_ok=True)
    kb_path = tmp_path / "campaign_record" / "campaign_knowledge_base.yaml"
    dw_dir = tmp_path / "config"
    dw_dir.mkdir(parents=True, exist_ok=True)
    dw_path = dw_dir / "detector_wishlist.yaml"
    kb_path.write_text(yaml.safe_dump(kb), encoding="utf-8")
    dw_path.write_text(yaml.safe_dump(wishlist), encoding="utf-8")

    monkeypatch.setattr(rc, "ROOT", tmp_path)
    result = rc.evaluate_wishlist_predicate("test_family4")
    assert result["result"] == "missing_field"
    assert result["matched_finding_id"] == "could_match_but_unscored"


def test_predicate_missing_field_when_finding_lacks_required_field(
    tmp_path, monkeypatch
):
    kb = {
        "findings": [
            {"id": "incomplete_finding", "outcome": "kill_ungated_regime_mismatch"},
            # no signal_property at all -- the predicate's field can't be found
        ]
    }
    wishlist = {
        "candidates": [
            {
                "family": "test_family2",
                "trigger_condition": {
                    "predicate": {
                        "source": "kb_finding",
                        "all_of": [
                            {
                                "field": "signal_property.per_trade_expectancy_bps",
                                "op": ">",
                                "value": 0,
                            },
                        ],
                    }
                },
            },
        ]
    }
    (tmp_path / "campaign_record").mkdir(exist_ok=True)
    kb_path = tmp_path / "campaign_record" / "campaign_knowledge_base.yaml"
    dw_dir = tmp_path / "config"
    dw_dir.mkdir(parents=True, exist_ok=True)
    dw_path = dw_dir / "detector_wishlist.yaml"
    kb_path.write_text(yaml.safe_dump(kb), encoding="utf-8")
    dw_path.write_text(yaml.safe_dump(wishlist), encoding="utf-8")

    monkeypatch.setattr(rc, "ROOT", tmp_path)
    result = rc.evaluate_wishlist_predicate("test_family2")
    assert result["result"] == "missing_field"
    assert result["matched_finding_id"] == "incomplete_finding"
