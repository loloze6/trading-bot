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

E-036 S2a (2026-09-27, engineering/roadmap/E-036/S1_FINDINGS_SLICE8.md
operator decision): Layer 1 is ADVISORY ONLY -- the calibration cases now
assert its advisory status (admit / warn) through layer1_advisory(), and
evaluate_candidate() never refuses on it. Layer 2 is the binary exact-match
check against campaign_memory.yaml; the family-digest / NEIGHBOUR /
composition-fingerprint tests that stood in this file were RETIRED with that
design (the rejected 2026-09-02 design). The new Layer 2 is tested in
tests/test_e036_s2a_exact_match_gate.py; the two binary checks kept below
are this file's own smoke tests of it.
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
    tested) -- Layer 1's advisory must read ADMIT, not a warning."""
    kb = _load_real_kb()
    adv = gate.layer1_advisory(_FUNDING_4H_CANDIDATE["hypothesis_id"], "4h", kb, _REAL_RUNS_DIR)
    assert adv["status"] == "admit"
    assert "funding_rate_continuous_mean_reversion_expanded_auto" in adv["reasons"][0]


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
    real = gate.layer1_advisory(_FUNDING_4H_CANDIDATE["hypothesis_id"], "4h", kb, _REAL_RUNS_DIR)
    assert real["status"] == "admit"


def test_precedence_rule_warns_on_the_daily_branch_terminated_by_run_059():
    """The additional requirement the dispatching session added (EPIC.md's
    2026-08-23 review entry): a registered lineage_routing=terminate closes
    the lineage it names. run_059's pass_rule_evaluation.yaml registers
    lineage_routing=terminate for the DAILY branch of
    funding_rate_continuous_mean_reversion_expanded_auto -- Layer 1 still
    says so, but since E-036 S2a only as an advisory WARNING: the gate's
    route stays ADMIT (layer1_kb_check itself still returns its REFUSE)."""
    kb = _load_real_kb()
    raw = gate.layer1_kb_check(_FUNDING_DAILY_CANDIDATE["hypothesis_id"], "1d",
                               kb["findings"], _REAL_RUNS_DIR)
    assert raw.route == "refuse"
    assert "closed by a run registered lineage_routing=terminate" in raw["reasons"][0]
    adv = gate.layer1_advisory(_FUNDING_DAILY_CANDIDATE["hypothesis_id"], "1d", kb, _REAL_RUNS_DIR)
    assert adv["status"] == "warn"
    result = gate.evaluate_candidate(("fh", ("BTCUSDT",), "1d", "windows:x"), {"runs": {}}, {},
                                     kb=kb, candidate_hid=_FUNDING_DAILY_CANDIDATE["hypothesis_id"],
                                     candidate_timeframe="1d", runs_dir=_REAL_RUNS_DIR)
    assert result.route == "admit" and result["layer1_advisory"]["status"] == "warn"


def test_precedence_rule_never_touches_the_sibling_4h_branch():
    """Explicit non-interference check: closing the daily branch must not
    accidentally also close 4h (a single shared 'exhausted' flag on the
    parent would do exactly that, wrongly)."""
    kb = _load_real_kb()
    admit_4h = gate.layer1_advisory(_FUNDING_4H_CANDIDATE["hypothesis_id"], "4h", kb, _REAL_RUNS_DIR)
    warn_1d = gate.layer1_advisory(_FUNDING_DAILY_CANDIDATE["hypothesis_id"], "1d", kb, _REAL_RUNS_DIR)
    assert admit_4h["status"] == "admit"
    assert warn_1d["status"] == "warn"


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
    expanded = gate.layer1_advisory(_FUNDING_4H_CANDIDATE["hypothesis_id"], "4h", kb, _REAL_RUNS_DIR)
    assert expanded["status"] == "admit"


def test_layer1_verdict_is_independent_of_kb_finding_list_order():
    """FIX 1 (review, 2026-08-24): two KB findings can both match the same
    candidate via hid containment (a closed base entry and its still-open
    _EXPANDED child). Before the fix, layer1_kb_check returned on the FIRST
    matching finding in raw YAML list order, so [closed, open] and
    [open, closed] disagreed. After the fix, matches are evaluated most-
    specific-first (longest matched hid wins), independent of list order --
    a literal order-swap must produce the SAME verdict both ways."""
    closed_base = {
        "id": "widget_mr_closed_base",
        "hypothesis_id": "WIDGET_MEAN_REVERSION",
        "evidence_runs": [],
        "exhausted": True,
        "reactivation_condition": None,
    }
    open_expanded_child = {
        "id": "widget_mr_expanded_open_child",
        "hypothesis_id": "WIDGET_MEAN_REVERSION_EXPANDED",
        "evidence_runs": [],
        "exhausted": False,
        "reactivation_condition": "retest at 4h",
        "reactivation_consumed_by": None,
    }
    candidate_hid = "WIDGET_MEAN_REVERSION_EXPANDED_4H_RETEST"

    order_a = gate.layer1_kb_check(candidate_hid, "4h",
                                    [closed_base, open_expanded_child], _REAL_RUNS_DIR)
    order_b = gate.layer1_kb_check(candidate_hid, "4h",
                                    [open_expanded_child, closed_base], _REAL_RUNS_DIR)

    assert order_a is not None and order_b is not None
    assert order_a.route == order_b.route == "admit", (
        f"order-dependent verdict: order_a={order_a.route!r} order_b={order_b.route!r} "
        "-- the more specific EXPANDED child's still-open branch must win regardless "
        "of which finding is listed first in the KB"
    )
    assert order_a["layer"] == order_b["layer"] == "kb"


def test_layer1_reactivation_consumed_by_does_not_close_an_unconsumed_sibling_branch():
    """FIX 2 (review, 2026-08-24): reactivation_consumed_by used to REFUSE
    unconditionally for the WHOLE finding, before the branch-aware
    reactivation_condition logic ever ran. A finding naming TWO branches
    ('4h or daily') whose consumed_by records that ONE of them (daily) was
    retested must not also REFUSE the still-open sibling (4h) -- consumed_by
    can only unambiguously mean 'this branch is closed' when exactly one
    branch is named."""
    kb = _kb([{
        "id": "widget_mr_two_branches",
        "hypothesis_id": "WIDGET_MEAN_REVERSION_TWO_BRANCH",
        "evidence_runs": [],
        "exhausted": False,
        "reactivation_condition": "retest at 4h or daily",
        "reactivation_consumed_by": "widget_daily_retest_killed",
    }])
    result = gate.layer1_kb_check("WIDGET_MEAN_REVERSION_TWO_BRANCH", "4h",
                                   kb["findings"], _REAL_RUNS_DIR)
    assert result is not None and result.route == "admit", (
        "the 4h branch was never named by any lineage_routing=terminate run, so "
        "it must still be open even though reactivation_consumed_by is set"
    )


# ---------------------------------------------------------------------------
# Layer 2 -- E-036 S2a: the binary exact-match check (smoke tests; the full
# suite is tests/test_e036_s2a_exact_match_gate.py). RETIRED here with the
# rejected family-digest design: the coarse-triple NEIGHBOUR, the new-
# instrument-for-known-family, the bare-string failed_families, the
# parameter-sweep NEIGHBOUR, the identical-fingerprint REPEAT, the regime-
# collision, the coarse-fidelity and the no-config tests. Each asserted a
# family/fingerprint outcome that no longer exists; their subject (what
# counts as "the same idea") is now the exact key, tested in the new file.
# composition_fingerprint itself stays in build_exclusion_digest.py (the
# legacy digest builder and decide_next's informational digest_advisory),
# so its own bare-config test is kept below.
# ---------------------------------------------------------------------------

def _memory(forecast_hash):
    return {"runs": {"run_001": {
        "run_id": "run_001", "legacy": False, "engineering_fault": None, "timeframe": "1h",
        "protocol_ref": "protocols/unreadable.json",
        "variants": {"run_001": {"status": "tested", "forecast_hash": forecast_hash,
                                 "symbols": ["BTCUSDT"]}}}}}


def test_layer2_exact_repeat_refuses_with_the_matched_memory_variant():
    key = gate.candidate_key("fh-a", ["BTCUSDT"], "protocols/unreadable.json", {},
                             card_timeframe="1h")
    result = gate.layer2_digest_check(key, gate._nov.match_index(_memory("fh-a"), {}))
    assert result.route == "refuse"
    assert result["outcome"] == "repeat"
    assert result["matched"] == [{"run_id": "run_001", "variant_id": "run_001"}]


def test_layer2_anything_else_is_novel_never_a_neighbour():
    key = gate.candidate_key("fh-b", ["BTCUSDT"], "protocols/unreadable.json", {},
                             card_timeframe="1h")
    result = gate.layer2_digest_check(key, gate._nov.match_index(_memory("fh-a"), {}))
    assert result.route == "admit"
    assert result["outcome"] == "novel"
    assert "neighbours" not in result


def test_composition_fingerprint_present_but_empty_config_is_not_none():
    """A present-but-structurally-bare config (e.g. {"regime_detector": {}})
    must still produce a real fingerprint distinguishable from "no config
    at all" -- composition_fingerprint(None-ish input) is the "never had a
    config" case, not "had an empty one"."""
    assert bed.composition_fingerprint({"regime_detector": {}}) == {
        "mode": None, "rule_count": 0, "components": [],
    }
    assert bed.composition_fingerprint({}) is None
    assert bed.composition_fingerprint(None) is None
