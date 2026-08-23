"""
E-032 S2a, Task 2/3 -- tests for tools/anti_adjacency_gate.py.

The load-bearing test in this file is
test_calibration_case_admits_4h_and_naive_flat_list_gate_would_refuse_it:
it proves the two-layer design earns its complexity rather than merely
existing, by running BOTH the real gate (ADMIT) and a naive flat-list gate
(REFUSE) against the identical candidate and asserting they disagree.
Without that contrast, "the gate is layered" is untested doctrine.

All KB/digest reads here are against synthetic in-memory dicts EXCEPT the
calibration-case tests, which deliberately read the real, committed
campaign_record/campaign_knowledge_base.yaml and runs/run_044,run_059 --
this is the actual historical case S1 traced by hand
(engineering/roadmap/E-032/artifacts/s1_idea_generation.md Task 3), and a
synthetic stand-in would not be testing the same thing. Read-only; nothing
here writes to the real repository.
"""
import sys
from pathlib import Path

import pytest
import yaml

TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_PATH))

import anti_adjacency_gate as gate  # noqa: E402
import build_exclusion_digest as bed  # noqa: E402

_SR = Path(__file__).parent.parent
_REAL_KB_PATH = _SR / "campaign_record" / "campaign_knowledge_base.yaml"
_REAL_RUNS_DIR = _SR / "runs"


def _load_real_kb() -> dict:
    with open(_REAL_KB_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Calibration case (real repo data)
# ---------------------------------------------------------------------------

_FUNDING_4H_CANDIDATE = {
    "hypothesis_id": "FUNDING_RATE_CONTINUOUS_MEAN_REVERSION_EXPANDED_4H_RETEST",
    "edge_source": {"evidence_type": "funding_open_interest",
                     "specific_mechanism": "Continuous funding-rate sign mean-reversion re-tested at 4h."},
    "target_market": ["BTCUSDT", "ETHUSDT"],
    "timeframe": "4h",
    "thesis": "Re-test the identical continuous funding-rate mean-reversion mechanism at 4h bars.",
}

_FUNDING_DAILY_CANDIDATE = {
    "hypothesis_id": "FUNDING_RATE_CONTINUOUS_MEAN_REVERSION_EXPANDED_DAILY_RETEST",
    "edge_source": {"evidence_type": "funding_open_interest",
                     "specific_mechanism": "Continuous funding-rate sign mean-reversion re-tested at daily."},
    "target_market": ["BTCUSDT", "ETHUSDT"],
    "timeframe": "1d",
    "thesis": "Re-test the identical continuous funding-rate mean-reversion mechanism at daily bars.",
}


def test_calibration_case_admits_the_4h_funding_retest():
    """S1's verified verdict: the 4h branch of
    funding_rate_continuous_mean_reversion_expanded_auto's reactivation_condition
    is open and unconsumed (the daily branch was consumed by
    funding_mr_daily_retest_killed; 4h was explicitly deferred, never
    tested) -- Layer 1 must ADMIT."""
    kb = _load_real_kb()
    digest = bed.build_digest()  # empty campaign_state ok; Layer 1 resolves this before Layer 2
    result = gate.evaluate_candidate(_FUNDING_4H_CANDIDATE, digest, kb, _REAL_RUNS_DIR,
                                      instrument="BTCUSDT", timeframe="4h")
    assert result.route == "admit"
    assert result["layer"] == "kb"
    assert "funding_rate_continuous_mean_reversion_expanded_auto" in result["reasons"][0]


def test_calibration_case_naive_flat_list_gate_would_refuse_the_same_candidate():
    """The contrast that proves the layering earns its complexity. A naive
    gate keyed on campaign_state.yaml's flat, family-blind timeframes_tried
    list sees '4h' in that list (entirely from unrelated keltner-family
    runs) and refuses -- wrongly. This is the exact false-refusal S1's
    story exists to prevent, reproduced here as a regression fixture rather
    than merely asserted in prose."""
    with open(_SR / "campaign_record" / "campaign_state.yaml", encoding="utf-8") as f:
        campaign_state = yaml.safe_load(f)

    def naive_flat_list_gate(candidate_timeframe: str) -> str:
        return "refuse" if candidate_timeframe in campaign_state["timeframes_tried"] else "admit"

    assert "4h" in campaign_state["timeframes_tried"], (
        "precondition: campaign_state.yaml's flat list must still contain '4h' "
        "for this contrast to mean anything"
    )
    naive_route = naive_flat_list_gate("4h")
    assert naive_route == "refuse", "the naive flat-list gate must wrongly refuse 4h"

    kb = _load_real_kb()
    digest = bed.build_digest()
    real_route = gate.evaluate_candidate(_FUNDING_4H_CANDIDATE, digest, kb, _REAL_RUNS_DIR,
                                          instrument="BTCUSDT", timeframe="4h").route
    assert real_route == "admit"
    assert real_route != naive_route, (
        "the layered gate and the naive flat-list gate must DISAGREE on this "
        "candidate -- proving the layering changes the outcome, not just the "
        "code path"
    )


def test_precedence_rule_refuses_the_daily_branch_terminated_by_run_059():
    """The additional requirement the dispatching session added (EPIC.md's
    2026-08-23 review entry): a registered lineage_routing=terminate closes
    the lineage it names. run_059's pass_rule_evaluation.yaml registers
    lineage_routing=terminate for the DAILY branch of
    funding_rate_continuous_mean_reversion_expanded_auto (via
    funding_mr_daily_retest_killed's explicit textual reference to the
    parent) -- a fresh candidate proposing that same daily branch must be
    REFUSED, even though the KB parent's own reactivation_condition text
    still nominally lists 'daily' as a branch."""
    kb = _load_real_kb()
    digest = bed.build_digest()
    result = gate.evaluate_candidate(_FUNDING_DAILY_CANDIDATE, digest, kb, _REAL_RUNS_DIR,
                                      instrument="BTCUSDT", timeframe="1d")
    assert result.route == "refuse"
    assert result["layer"] == "kb"
    assert "closed by a run registered lineage_routing=terminate" in result["reasons"][0]


def test_precedence_rule_never_touches_the_sibling_4h_branch():
    """Explicit non-interference check: closing the daily branch must not
    accidentally also close 4h (a single shared 'exhausted' flag on the
    parent would do exactly that, wrongly)."""
    kb = _load_real_kb()
    digest = bed.build_digest()
    admit_4h = gate.evaluate_candidate(_FUNDING_4H_CANDIDATE, digest, kb, _REAL_RUNS_DIR,
                                        instrument="BTCUSDT", timeframe="4h")
    refuse_1d = gate.evaluate_candidate(_FUNDING_DAILY_CANDIDATE, digest, kb, _REAL_RUNS_DIR,
                                         instrument="BTCUSDT", timeframe="1d")
    assert admit_4h.route == "admit"
    assert refuse_1d.route == "refuse"


# ---------------------------------------------------------------------------
# Layer 1 unit tests (synthetic KB)
# ---------------------------------------------------------------------------

def _kb(findings):
    return {"findings": findings}


def test_layer1_refuses_exhausted_finding_with_no_reactivation_clause():
    kb = _kb([{
        "id": "widget_mean_reversion_no_edge",
        "hypothesis_id": "WIDGET_MEAN_REVERSION",
        "evidence_runs": [],
        "exhausted": True,
        "reactivation_condition": None,
    }])
    result = gate.layer1_kb_check("WIDGET_MEAN_REVERSION", "1h", kb["findings"], _REAL_RUNS_DIR)
    assert result is not None and result.route == "refuse"


def test_layer1_refuses_consumed_reactivation():
    kb = _kb([{
        "id": "widget_mean_reversion_parked",
        "hypothesis_id": "WIDGET_MEAN_REVERSION",
        "evidence_runs": [],
        "exhausted": False,
        "reactivation_condition": "retest at 4h",
        "reactivation_consumed_by": "widget_4h_retest_killed",
    }])
    result = gate.layer1_kb_check("WIDGET_MEAN_REVERSION", "4h", kb["findings"], _REAL_RUNS_DIR)
    assert result is not None and result.route == "refuse"
    assert "already reactivated by" in result["reasons"][0]


def test_layer1_returns_none_when_no_finding_matches_candidate():
    kb = _kb([{
        "id": "unrelated_finding",
        "hypothesis_id": "SOMETHING_ELSE_ENTIRELY",
        "evidence_runs": [],
        "exhausted": True,
        "reactivation_condition": None,
    }])
    result = gate.layer1_kb_check("BRAND_NEW_MECHANISM", "1h", kb["findings"], _REAL_RUNS_DIR)
    assert result is None


def test_layer1_does_not_conflate_family_siblings_with_different_verdicts():
    """The bug found and fixed while building this gate: two KB findings in
    the SAME FAMILY (both 'funding_rate_extreme' under classify_family) but
    with UNRELATED hypothesis_ids and opposite verdicts must not let one
    settle the other. H-041-A (exhausted, no reactivation) must never
    REFUSE a candidate that only matches FUNDING_RATE_CONTINUOUS_MEAN_
    REVERSION_EXPANDED's still-open branch."""
    kb = _load_real_kb()
    # H-041-A's own finding must independently refuse a same-hid candidate...
    h041a_result = gate.layer1_kb_check("H-041-A", "1h", kb["findings"], _REAL_RUNS_DIR)
    assert h041a_result is not None and h041a_result.route == "refuse"
    # ...but must have NO bearing on the unrelated EXPANDED lineage's candidate.
    digest = bed.build_digest()
    expanded_result = gate.evaluate_candidate(_FUNDING_4H_CANDIDATE, digest, kb, _REAL_RUNS_DIR,
                                               instrument="BTCUSDT", timeframe="4h")
    assert expanded_result.route == "admit"


# ---------------------------------------------------------------------------
# Layer 2 unit tests (synthetic digest)
# ---------------------------------------------------------------------------

def _digest(families, failed_families_passthrough=None):
    return {
        "families": families,
        "failed_families_passthrough": failed_families_passthrough or [],
        "components_built_passthrough": [],
    }


def test_layer2_refuses_exact_family_instrument_timeframe_triple():
    digest = _digest({
        "keltner_channel": {"confidence": "keyword_bounded", "triples": [
            {"instrument": "AVAXUSDT", "timeframe": "4h", "run_ids": ["run_030"]},
        ]},
    })
    candidate = {"hypothesis_id": "KELTNER_NEW", "target_market": ["AVAXUSDT"], "timeframe": "4h",
                 "thesis": "Keltner mean reversion on AVAX."}
    result = gate.evaluate_candidate(candidate, digest, _kb([]), _REAL_RUNS_DIR)
    assert result.route == "refuse"
    assert result["layer"] == "digest"


def test_layer2_admits_new_instrument_for_known_family():
    digest = _digest({
        "keltner_channel": {"confidence": "keyword_bounded", "triples": [
            {"instrument": "AVAXUSDT", "timeframe": "4h", "run_ids": ["run_030"]},
        ]},
    })
    candidate = {"hypothesis_id": "KELTNER_NEW_SYMBOL", "target_market": ["DOTUSDT"], "timeframe": "4h",
                 "thesis": "Keltner mean reversion on DOT."}
    result = gate.evaluate_candidate(candidate, digest, _kb([]), _REAL_RUNS_DIR)
    assert result.route == "admit"


def test_layer2_never_auto_refuses_on_bare_string_failed_family():
    digest = _digest(
        {},
        failed_families_passthrough=[{"family": "sma_trend", "detail": "bare_string_low_detail"}],
    )
    candidate = {"hypothesis_id": "SMA_NEW", "target_market": ["BTCUSDT"], "timeframe": "1h",
                 "thesis": "SMA crossover on BTC."}
    result = gate.evaluate_candidate(candidate, digest, _kb([]), _REAL_RUNS_DIR)
    assert result.route == "admit", "a bare-string low-detail entry must never be a silent veto"
    assert result["low_detail_prior_failure"] is True
