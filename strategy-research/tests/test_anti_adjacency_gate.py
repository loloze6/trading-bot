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
    "edge_source": {
        "evidence_type": "funding_open_interest",
        "specific_mechanism": "Continuous funding-rate sign mean-reversion re-tested at 4h.",
    },
    "target_market": ["BTCUSDT", "ETHUSDT"],
    "timeframe": "4h",
    "thesis": "Re-test the identical continuous funding-rate mean-reversion mechanism at 4h bars.",
}

_FUNDING_DAILY_CANDIDATE = {
    "hypothesis_id": "FUNDING_RATE_CONTINUOUS_MEAN_REVERSION_EXPANDED_DAILY_RETEST",
    "edge_source": {
        "evidence_type": "funding_open_interest",
        "specific_mechanism": "Continuous funding-rate sign mean-reversion re-tested at daily.",
    },
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
    digest = (
        bed.build_digest()
    )  # empty campaign_state ok; Layer 1 resolves this before Layer 2
    result = gate.evaluate_candidate(
        _FUNDING_4H_CANDIDATE,
        digest,
        kb,
        _REAL_RUNS_DIR,
        instrument="BTCUSDT",
        timeframe="4h",
    )
    assert result.route == "admit"
    assert result["layer"] == "kb"
    assert (
        "funding_rate_continuous_mean_reversion_expanded_auto" in result["reasons"][0]
    )


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
        return (
            "refuse"
            if candidate_timeframe in campaign_state["timeframes_tried"]
            else "admit"
        )

    assert "4h" in campaign_state["timeframes_tried"], (
        "precondition: campaign_state.yaml's flat list must still contain '4h' "
        "for this contrast to mean anything"
    )
    naive_route = naive_flat_list_gate("4h")
    assert naive_route == "refuse", "the naive flat-list gate must wrongly refuse 4h"

    kb = _load_real_kb()
    digest = bed.build_digest()
    real_route = gate.evaluate_candidate(
        _FUNDING_4H_CANDIDATE,
        digest,
        kb,
        _REAL_RUNS_DIR,
        instrument="BTCUSDT",
        timeframe="4h",
    ).route
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
    result = gate.evaluate_candidate(
        _FUNDING_DAILY_CANDIDATE,
        digest,
        kb,
        _REAL_RUNS_DIR,
        instrument="BTCUSDT",
        timeframe="1d",
    )
    assert result.route == "refuse"
    assert result["layer"] == "kb"
    assert (
        "closed by a run registered lineage_routing=terminate" in result["reasons"][0]
    )


def test_precedence_rule_never_touches_the_sibling_4h_branch():
    """Explicit non-interference check: closing the daily branch must not
    accidentally also close 4h (a single shared 'exhausted' flag on the
    parent would do exactly that, wrongly)."""
    kb = _load_real_kb()
    digest = bed.build_digest()
    admit_4h = gate.evaluate_candidate(
        _FUNDING_4H_CANDIDATE,
        digest,
        kb,
        _REAL_RUNS_DIR,
        instrument="BTCUSDT",
        timeframe="4h",
    )
    refuse_1d = gate.evaluate_candidate(
        _FUNDING_DAILY_CANDIDATE,
        digest,
        kb,
        _REAL_RUNS_DIR,
        instrument="BTCUSDT",
        timeframe="1d",
    )
    assert admit_4h.route == "admit"
    assert refuse_1d.route == "refuse"


# ---------------------------------------------------------------------------
# Layer 1 unit tests (synthetic KB)
# ---------------------------------------------------------------------------


def _kb(findings):
    return {"findings": findings}


def test_layer1_refuses_exhausted_finding_with_no_reactivation_clause():
    kb = _kb(
        [
            {
                "id": "widget_mean_reversion_no_edge",
                "hypothesis_id": "WIDGET_MEAN_REVERSION",
                "evidence_runs": [],
                "exhausted": True,
                "reactivation_condition": None,
            }
        ]
    )
    result = gate.layer1_kb_check(
        "WIDGET_MEAN_REVERSION", "1h", kb["findings"], _REAL_RUNS_DIR
    )
    assert result is not None and result.route == "refuse"


def test_layer1_refuses_consumed_reactivation():
    kb = _kb(
        [
            {
                "id": "widget_mean_reversion_parked",
                "hypothesis_id": "WIDGET_MEAN_REVERSION",
                "evidence_runs": [],
                "exhausted": False,
                "reactivation_condition": "retest at 4h",
                "reactivation_consumed_by": "widget_4h_retest_killed",
            }
        ]
    )
    result = gate.layer1_kb_check(
        "WIDGET_MEAN_REVERSION", "4h", kb["findings"], _REAL_RUNS_DIR
    )
    assert result is not None and result.route == "refuse"
    assert "already reactivated by" in result["reasons"][0]


def test_layer1_returns_none_when_no_finding_matches_candidate():
    kb = _kb(
        [
            {
                "id": "unrelated_finding",
                "hypothesis_id": "SOMETHING_ELSE_ENTIRELY",
                "evidence_runs": [],
                "exhausted": True,
                "reactivation_condition": None,
            }
        ]
    )
    result = gate.layer1_kb_check(
        "BRAND_NEW_MECHANISM", "1h", kb["findings"], _REAL_RUNS_DIR
    )
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
    expanded_result = gate.evaluate_candidate(
        _FUNDING_4H_CANDIDATE,
        digest,
        kb,
        _REAL_RUNS_DIR,
        instrument="BTCUSDT",
        timeframe="4h",
    )
    assert expanded_result.route == "admit"


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

    order_a = gate.layer1_kb_check(
        candidate_hid, "4h", [closed_base, open_expanded_child], _REAL_RUNS_DIR
    )
    order_b = gate.layer1_kb_check(
        candidate_hid, "4h", [open_expanded_child, closed_base], _REAL_RUNS_DIR
    )

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
    kb = _kb(
        [
            {
                "id": "widget_mr_two_branches",
                "hypothesis_id": "WIDGET_MEAN_REVERSION_TWO_BRANCH",
                "evidence_runs": [],
                "exhausted": False,
                "reactivation_condition": "retest at 4h or daily",
                "reactivation_consumed_by": "widget_daily_retest_killed",
            }
        ]
    )
    result = gate.layer1_kb_check(
        "WIDGET_MEAN_REVERSION_TWO_BRANCH", "4h", kb["findings"], _REAL_RUNS_DIR
    )
    assert result is not None and result.route == "admit", (
        "the 4h branch was never named by any lineage_routing=terminate run, so "
        "it must still be open even though reactivation_consumed_by is set"
    )


# ---------------------------------------------------------------------------
# Layer 2 unit tests (synthetic digest)
# ---------------------------------------------------------------------------


def _digest(families, failed_families_passthrough=None):
    return {
        "families": families,
        "failed_families_passthrough": failed_families_passthrough or [],
        "components_built_passthrough": [],
    }


def test_layer2_coarse_triple_match_admits_as_neighbour_not_refuse():
    """E-036 S2: this test used to assert REFUSE for a bare (family,
    instrument, timeframe) collision -- exactly the over-coarse behavior
    E-036 exists to fix (see engineering/roadmap/E-036/EPIC.md: a keltner
    candidate at a different atr_mult than a prior run was wrongly REFUSEd
    on this same triple-only key). A digest entry with no fingerprint
    (fidelity="coarse", the shape every entry had before this story) can
    now only ever produce NEIGHBOUR, never REPEAT -- design point 3. The
    genuine-repeat case (identical fingerprint -> REFUSE) is covered
    separately below."""
    digest = _digest(
        {
            "keltner_channel": {
                "confidence": "keyword_bounded",
                "triples": [
                    {
                        "instrument": "AVAXUSDT",
                        "timeframe": "4h",
                        "fidelity": "coarse",
                        "fingerprint": None,
                        "run_ids": ["run_030"],
                    },
                ],
            },
        }
    )
    candidate = {
        "hypothesis_id": "KELTNER_NEW",
        "target_market": ["AVAXUSDT"],
        "timeframe": "4h",
        "thesis": "Keltner mean reversion on AVAX.",
    }
    result = gate.evaluate_candidate(candidate, digest, _kb([]), _REAL_RUNS_DIR)
    assert result.route == "admit"
    assert result["layer"] == "digest"
    assert result["outcome"] == "neighbour"
    assert result["neighbours"][0]["run_ids"] == ["run_030"]
    assert result["neighbours"][0]["fidelity"] == "coarse"


def test_layer2_admits_new_instrument_for_known_family():
    digest = _digest(
        {
            "keltner_channel": {
                "confidence": "keyword_bounded",
                "triples": [
                    {
                        "instrument": "AVAXUSDT",
                        "timeframe": "4h",
                        "run_ids": ["run_030"],
                    },
                ],
            },
        }
    )
    candidate = {
        "hypothesis_id": "KELTNER_NEW_SYMBOL",
        "target_market": ["DOTUSDT"],
        "timeframe": "4h",
        "thesis": "Keltner mean reversion on DOT.",
    }
    result = gate.evaluate_candidate(candidate, digest, _kb([]), _REAL_RUNS_DIR)
    assert result.route == "admit"


def test_layer2_never_auto_refuses_on_bare_string_failed_family():
    digest = _digest(
        {},
        failed_families_passthrough=[
            {"family": "sma_trend", "detail": "bare_string_low_detail"}
        ],
    )
    candidate = {
        "hypothesis_id": "SMA_NEW",
        "target_market": ["BTCUSDT"],
        "timeframe": "1h",
        "thesis": "SMA crossover on BTC.",
    }
    result = gate.evaluate_candidate(candidate, digest, _kb([]), _REAL_RUNS_DIR)
    assert result.route == "admit", (
        "a bare-string low-detail entry must never be a silent veto"
    )
    assert result["low_detail_prior_failure"] is True


# ---------------------------------------------------------------------------
# E-036 S2 -- composition fingerprint (mandatory regression tests, per
# EPIC.md's "Done when" and the dispatching session's test list). These
# prove the defect measured in EPIC.md is closed: the digest key was
# (family, instrument, timeframe) alone, which collapsed 21 of 39 runs
# carrying both a hypothesis_card.yaml and a candidate_strategy_config.json
# into "already tried" -- a parameter sweep read as a repeat.
# ---------------------------------------------------------------------------


def _kc_config(atr_mult, regime="mean_reversion", component_id="keltner"):
    """Same candidate_strategy_config.json shape as the real corpus (e.g.
    runs/run_016/artifacts/candidate_strategy_config.json)."""
    return {
        "regime_detector": {"mode": "threshold_rules", "rules": [{"regime": regime}]},
        "strategies": {
            "regimes": {
                regime: {
                    "components": [
                        {
                            "id": component_id,
                            "class": "strategies.strategy_components.KeltnerBreakoutComponent",
                            "params": {"atr_multiplier": atr_mult, "ema_period": 20},
                            "weight": 1.0,
                            "transforms": [{"op": "identity"}],
                        },
                    ]
                }
            }
        },
    }


def _kc_digest_structured(instrument, timeframe, run_id, config):
    fingerprint = bed.composition_fingerprint(config)
    return _digest(
        {
            "keltner_channel": {
                "confidence": "structural_indicator_id",
                "triples": [
                    {
                        "instrument": instrument,
                        "timeframe": timeframe,
                        "fidelity": "structured",
                        "fingerprint": fingerprint,
                        "run_ids": [run_id],
                    },
                ],
            },
        }
    )


_KELTNER_CANDIDATE_BASE = {
    "hypothesis_id": "KELTNER_ATR_SWEEP",
    "target_market": ["BTCUSDT"],
    "timeframe": "1h",
    "library_lookup": {"indicator_id": "keltner_channel"},
    "thesis": "Keltner channel mean reversion on BTC, 1h.",
}


def test_reproduced_case_parameter_sweep_admits_as_neighbour_not_refuse():
    """THE headline case from EPIC.md, reproduced and closed: a keltner
    candidate at atr_mult=3.0, with a prior run on record at atr_mult=2.0
    for the SAME (family, instrument, timeframe) -- must ADMIT as a
    NEIGHBOUR, with the prior run_id attached, not REFUSE. Before E-036,
    the digest's (family, instrument, timeframe)-only key REFUSEd this
    exact shape of candidate (EPIC.md: "candidate: keltner_channel,
    BTCUSDT, 1h, atr_mult 3.0 (prior run used 2.0) ... verdict: refuse")."""
    prior_config = _kc_config(atr_mult=2.0)
    digest = _kc_digest_structured("BTCUSDT", "1h", "run_016", prior_config)
    candidate_config = _kc_config(atr_mult=3.0)

    result = gate.evaluate_candidate(
        _KELTNER_CANDIDATE_BASE,
        digest,
        _kb([]),
        _REAL_RUNS_DIR,
        instrument="BTCUSDT",
        timeframe="1h",
        candidate_config=candidate_config,
    )

    assert result.route == "admit", (
        "a parameter sweep (different atr_mult, same family/instrument/timeframe) "
        "must ADMIT -- this is the exact case the current triple-only key wrongly REFUSEd"
    )
    assert result["layer"] == "digest"
    assert result["outcome"] == "neighbour"
    assert result["neighbours"][0]["run_ids"] == ["run_016"]
    assert result["neighbours"][0]["fidelity"] == "structured"
    assert "differ" in result["neighbours"][0]["differs"]


def test_genuine_repeat_identical_fingerprint_refuses():
    """The only case that blocks (EPIC.md design point 2): SAME family,
    instrument, timeframe AND an IDENTICAL composition fingerprint on both
    sides (both fidelity="structured"). This is a genuine re-run and must
    REFUSE."""
    config = _kc_config(atr_mult=2.0)
    digest = _kc_digest_structured("BTCUSDT", "1h", "run_016", config)
    # A fresh candidate proposing the byte-for-byte identical composition.
    identical_config = _kc_config(atr_mult=2.0)

    result = gate.evaluate_candidate(
        _KELTNER_CANDIDATE_BASE,
        digest,
        _kb([]),
        _REAL_RUNS_DIR,
        instrument="BTCUSDT",
        timeframe="1h",
        candidate_config=identical_config,
    )

    assert result.route == "refuse"
    assert result["layer"] == "digest"
    assert result["outcome"] == "repeat"
    assert result["run_ids"] == ["run_016"]


def test_same_component_identical_params_different_regime_does_not_collide():
    """EPIC.md design point 4: (mean_reversion, rsi, period=14) and
    (trending, rsi, period=14) are different strategies and must not
    collide. Regime is folded into the fingerprint for free -- an
    IDENTICAL component/params/weight under a DIFFERENT regime must not
    read as a REPEAT (nor even collide as a NEIGHBOUR entry sharing the
    same fingerprint -- the fingerprints themselves must differ)."""
    mr_config = _kc_config(atr_mult=2.0, regime="mean_reversion")
    trending_config = _kc_config(atr_mult=2.0, regime="trending")
    assert bed.composition_fingerprint(mr_config) != bed.composition_fingerprint(
        trending_config
    ), (
        "same component, same params, different regime must produce DIFFERENT "
        "fingerprints -- the regime is part of identity"
    )

    digest = _kc_digest_structured("BTCUSDT", "1h", "run_016", mr_config)
    result = gate.evaluate_candidate(
        _KELTNER_CANDIDATE_BASE,
        digest,
        _kb([]),
        _REAL_RUNS_DIR,
        instrument="BTCUSDT",
        timeframe="1h",
        candidate_config=trending_config,
    )

    assert result.route == "admit"
    assert result["outcome"] == "neighbour", (
        "same family/instrument/timeframe still collides at that grain, but the "
        "differing regime means it is a NEIGHBOUR, never mistaken for the SAME "
        "strategy"
    )


def test_coarse_fidelity_entry_never_produces_repeat():
    """Design point 3: a coarse-fidelity match can never produce REPEAT, at
    most NEIGHBOUR -- even when the candidate itself DOES supply a
    structured config. We cannot prove an exact repeat from a record that
    never captured composition."""
    digest = _digest(
        {
            "keltner_channel": {
                "confidence": "structural_indicator_id",
                "triples": [
                    {
                        "instrument": "BTCUSDT",
                        "timeframe": "1h",
                        "fidelity": "coarse",
                        "fingerprint": None,
                        "run_ids": ["run_777"],
                    },
                ],
            },
        }
    )
    candidate_config = _kc_config(atr_mult=2.0)

    result = gate.evaluate_candidate(
        _KELTNER_CANDIDATE_BASE,
        digest,
        _kb([]),
        _REAL_RUNS_DIR,
        instrument="BTCUSDT",
        timeframe="1h",
        candidate_config=candidate_config,
    )

    assert result.route == "admit"
    assert result["outcome"] == "neighbour"
    assert result["neighbours"][0]["fidelity"] == "coarse"


def test_candidate_with_no_structured_config_never_produces_repeat():
    """Complement of the coarse-entry case: when the CANDIDATE side has no
    structured config (candidate_config=None, e.g. the pre-backtest-
    specification call site), REPEAT must also be unreachable -- there is
    nothing to compare the prior run's fingerprint against."""
    config = _kc_config(atr_mult=2.0)
    digest = _kc_digest_structured("BTCUSDT", "1h", "run_016", config)

    result = gate.evaluate_candidate(
        _KELTNER_CANDIDATE_BASE,
        digest,
        _kb([]),
        _REAL_RUNS_DIR,
        instrument="BTCUSDT",
        timeframe="1h",
        candidate_config=None,
    )

    assert result.route == "admit"
    assert result["outcome"] == "neighbour"


def test_composition_fingerprint_present_but_empty_config_is_not_none():
    """A present-but-structurally-bare config (e.g. {"regime_detector": {}},
    the pre-E-036 fixture default in test_variant_anti_adjacency_gate.py)
    must still produce a real fingerprint distinguishable from "no config
    at all" -- composition_fingerprint(None-ish input) is the "never had a
    config" case, not "had an empty one"."""
    assert bed.composition_fingerprint({"regime_detector": {}}) == {
        "mode": None,
        "rule_count": 0,
        "components": [],
    }
    assert bed.composition_fingerprint({}) is None
    assert bed.composition_fingerprint(None) is None
