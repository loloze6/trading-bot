"""
F3 (P1a shakedown, 2026-07-04) regression test.

_should_trigger_campaign_review() crashed run_043's second attempt with
`TypeError: unhashable type: 'dict'` at `set(failed)`, where `failed` is
campaign_state.yaml's `failed_families` list. That list is MIXED: the six
historical entries (tagged 2026-07-02, Improvement 07) are dicts with
{name, evidence_window, root_cause}; record_pivot() (still live) appends plain
strings for any NEW pivot. This is the first-ever live reproduction of this crash —
every prior non-kill/non-promote verdict in the campaign was either pre-retag or
backfilled manually, never exercising this exact function.

Fixture below is the real six entries verbatim from campaign_state.yaml as of
2026-07-04 (see strategy-research/campaign_state.yaml `failed_families`).
"""
import sys
from pathlib import Path

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

from run_phase1_research import _should_trigger_campaign_review

_REAL_FAILED_FAMILIES_2026_07_04 = [
    {"name": "rsi_mean_reversion", "evidence_window": "2024_only", "root_cause": "signal_quality"},
    {"name": "keltner_breakout", "evidence_window": "2024_only", "root_cause": "signal_inversion"},
    {"name": "keltner_mean_reversion", "evidence_window": "2024_only", "root_cause": "regime_availability"},
    {"name": "rsi_momentum_trending", "evidence_window": "2024_only", "root_cause": "cost_drag"},
    {"name": "keltner_trend_mean_reversion", "evidence_window": "2024_only", "root_cause": "regime_availability"},
    {"name": "keltner_scoremode", "evidence_window": "2024_only", "root_cause": "signal_quality"},
]


def test_does_not_crash_on_real_dict_shaped_failed_families():
    """The actual failure: this call raised TypeError: unhashable type: 'dict'."""
    campaign = {
        "failed_families": _REAL_FAILED_FAMILIES_2026_07_04,
        "runs": [f"run_{i:03d}" for i in range(11, 40)],
        "review_every_n_runs": 6,
    }
    result = _should_trigger_campaign_review(campaign)  # must not raise
    assert isinstance(result, bool)


def test_six_real_distinct_families_trigger_review():
    campaign = {
        "failed_families": _REAL_FAILED_FAMILIES_2026_07_04,
        "runs": ["run_011"],
        "review_every_n_runs": 6,
    }
    assert _should_trigger_campaign_review(campaign) is True


def test_mixed_dict_and_legacy_string_entries_do_not_crash():
    """record_pivot() (still live) appends a plain string on any NEW pivot — the list
    is genuinely mixed-shape, not uniformly one or the other."""
    mixed = _REAL_FAILED_FAMILIES_2026_07_04 + ["ema_spread_trend_continuation"]
    campaign = {"failed_families": mixed, "runs": ["run_011"], "review_every_n_runs": 6}
    assert _should_trigger_campaign_review(campaign) is True  # 7 distinct names


def test_single_family_below_threshold_does_not_trigger_on_families_alone():
    campaign = {
        "failed_families": [_REAL_FAILED_FAMILIES_2026_07_04[0]],
        "runs": ["run_011", "run_012", "run_013"],
        "review_every_n_runs": 6,
    }
    assert _should_trigger_campaign_review(campaign) is False


def test_budget_trigger_still_works_independent_of_families():
    campaign = {
        "failed_families": [],
        "runs": [f"run_{i:03d}" for i in range(1, 7)],  # len==6, divisible by review_n
        "review_every_n_runs": 6,
    }
    assert _should_trigger_campaign_review(campaign) is True
