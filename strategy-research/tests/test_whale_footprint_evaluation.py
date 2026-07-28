"""
Tests for tools/whale_footprint_evaluation.py (dispatch W8 step 6).

Every case here is a SYNTHETIC, planted-answer fixture. Nothing in this file
reads trading-bot/local_data/recorded_reserved/ — the harness is built and
tested here but deliberately never run against the real capture.
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_PATH))

from whale_footprint_evaluation import evaluate, load_prereg  # noqa: E402

FEATURES = ["f_signal", "f_noise_a", "f_noise_b"]


def _prereg(required_n=50, coverage_floor=0.05, alpha_corrected=0.0125, fires_once=True,
            economically_untradeable=False, required_ic=None):
    return {
        "features": {"names": list(FEATURES)},
        "test_statistic": {"multiple_comparison_correction": {"alpha_corrected": alpha_corrected}},
        "minimum_n_gate": {"required_attested_bars_per_pair": required_n},
        "required_coverage_floor": {"floor": coverage_floor},
        "single_use": {"fires_exactly_once": fires_once},
        "economic_ic_threshold": {
            "economically_untradeable_at_registered_frequency": economically_untradeable,
            "required_ic_at_registered_frequency": required_ic,
            "finding": "synthetic fixture" if economically_untradeable else None,
        },
    }


def _panel(n_pairs, n_bars, *, attested_fraction=1.0, seed=0,
           signal_strength=0.9, flip_pairs=0):
    """
    Builds `n_pairs` synthetic panels of `n_bars` rows each.

    f_signal correlates with target at `signal_strength` (Spearman, roughly)
    for every pair EXCEPT the first `flip_pairs` pairs, whose f_signal is
    NEGATIVELY correlated with target instead — used to plant an UNSTABLE
    (sign-inconsistent) result while keeping the pooled correlation
    significant. f_noise_a / f_noise_b are independent of target everywhere
    (NULL features in every fixture that doesn't override them).
    """
    rng = np.random.RandomState(seed)
    panels = {}
    for i in range(n_pairs):
        target = rng.normal(size=n_bars)
        sign = -1.0 if i < flip_pairs else 1.0
        f_signal = sign * signal_strength * target + rng.normal(scale=0.4, size=n_bars)
        f_noise_a = rng.normal(size=n_bars)
        f_noise_b = rng.normal(size=n_bars)
        attested = rng.uniform(size=n_bars) < attested_fraction
        panels[f"PAIR{i}"] = pd.DataFrame({
            "f_signal": f_signal, "f_noise_a": f_noise_a, "f_noise_b": f_noise_b,
            "target": target, "attested": attested,
        })
    return panels


# ---------------------------------------------------------------------------


def test_pass_when_a_feature_clears_significance_with_consistent_sign():
    prereg = _prereg(required_n=50, coverage_floor=0.05)
    panels = _panel(n_pairs=10, n_bars=200, attested_fraction=1.0, flip_pairs=0, seed=1)
    result = evaluate(prereg, panels)
    assert result.status == "VERDICT"
    assert result.verdict == "PASS"
    f_signal = next(f for f in result.detail["per_feature"] if f["feature"] == "f_signal")
    assert f_signal["verdict"] == "PASS"
    assert f_signal["sign_consistency"]["holds"] is True


def test_null_when_no_feature_clears_significance():
    prereg = _prereg(required_n=50, coverage_floor=0.05)
    # signal_strength=0 -> f_signal degenerates to noise too
    panels = _panel(n_pairs=10, n_bars=200, attested_fraction=1.0,
                     signal_strength=0.0, seed=2)
    result = evaluate(prereg, panels)
    assert result.status == "VERDICT"
    assert result.verdict == "NULL"
    assert all(f["verdict"] == "NULL" for f in result.detail["per_feature"])


def test_unstable_when_a_feature_clears_but_sign_flips_across_pairs():
    prereg = _prereg(required_n=50, coverage_floor=0.05)
    # 10 pairs, 3 flipped (30% disagreement) -> pooled correlation stays
    # significant (majority direction, large N) but per-pair agreement (70%)
    # falls below the 80% sign_consistency floor.
    panels = _panel(n_pairs=10, n_bars=300, attested_fraction=1.0,
                     flip_pairs=3, signal_strength=0.9, seed=3)
    result = evaluate(prereg, panels)
    assert result.status == "VERDICT"
    f_signal = next(f for f in result.detail["per_feature"] if f["feature"] == "f_signal")
    assert f_signal["verdict"] == "UNSTABLE", (
        f"expected f_signal UNSTABLE (sign flips on 3/10 pairs), got {f_signal!r}"
    )
    assert f_signal["sign_consistency"]["agree_fraction"] == pytest.approx(0.7)
    assert result.verdict == "UNSTABLE"


def test_blocked_by_minimum_n_gate():
    prereg = _prereg(required_n=10_000, coverage_floor=0.05)  # unreachable on purpose
    panels = _panel(n_pairs=5, n_bars=50, attested_fraction=1.0, seed=4)
    result = evaluate(prereg, panels)
    assert result.status == "BLOCKED_MIN_N"
    assert result.verdict is None
    assert result.detail["attested_bars_per_pair_avg"] < result.detail["required"]


def test_blocked_by_economic_infeasibility_before_any_panel_is_touched():
    """A pre-registration whose own cost-model derivation shows the required
    IC exceeds what a Spearman correlation can express (bounded [-1, 1]) must
    block immediately -- no sample size fixes an economically-impossible
    threshold. Checked ahead of the coverage floor and minimum-N: pass a
    panel that would otherwise clear both, to prove this gate is what stops
    it, not a downstream one."""
    prereg = _prereg(required_n=1, coverage_floor=0.0,
                      economically_untradeable=True, required_ic=2.4667)
    panels = _panel(n_pairs=10, n_bars=200, attested_fraction=1.0, seed=8)
    result = evaluate(prereg, panels)
    assert result.status == "BLOCKED_ECONOMIC_INFEASIBILITY"
    assert result.verdict is None
    assert result.detail["required_ic_at_registered_frequency"] == 2.4667
    assert result.detail["max_possible_ic"] == 1.0


def test_economic_gate_absent_or_false_does_not_block():
    """Backward compatible: a prereg with no economic_ic_threshold key at all
    (v1's shape) or economically_untradeable=False must not be affected by
    this gate."""
    prereg = _prereg(required_n=50, coverage_floor=0.05, economically_untradeable=False)
    panels = _panel(n_pairs=10, n_bars=200, attested_fraction=1.0, flip_pairs=0, seed=1)
    result = evaluate(prereg, panels)
    assert result.status == "VERDICT"

    v1_shaped = _prereg(required_n=50, coverage_floor=0.05)
    del v1_shaped["economic_ic_threshold"]
    result2 = evaluate(v1_shaped, panels)
    assert result2.status == "VERDICT"


def test_economic_infeasibility_block_does_not_consume_single_use(tmp_path):
    prereg_path = tmp_path / "prereg.yaml"
    prereg = _prereg(required_n=1, coverage_floor=0.0,
                      economically_untradeable=True, required_ic=2.4667)
    import yaml
    prereg_path.write_text(yaml.safe_dump(prereg), encoding="utf-8")
    loaded = load_prereg(prereg_path)

    panels = _panel(n_pairs=5, n_bars=50, attested_fraction=1.0, seed=9)
    blocked = evaluate(loaded, panels, prereg_path=prereg_path, run_id="run_a")
    assert blocked.status == "BLOCKED_ECONOMIC_INFEASIBILITY"

    loaded["economic_ic_threshold"]["economically_untradeable_at_registered_frequency"] = False
    ok = evaluate(loaded, panels, prereg_path=prereg_path, run_id="run_b")
    assert ok.status == "VERDICT"


def test_blocked_by_coverage_floor():
    prereg = _prereg(required_n=10, coverage_floor=0.50)
    panels = _panel(n_pairs=5, n_bars=200, attested_fraction=0.05, seed=5)
    result = evaluate(prereg, panels)
    assert result.status == "BLOCKED_COVERAGE_FLOOR"
    assert result.detail["attested_fraction"] < result.detail["floor"]


def test_blocked_by_single_use_after_first_execution(tmp_path):
    prereg_path = tmp_path / "prereg.yaml"
    prereg = _prereg(required_n=50, coverage_floor=0.05)
    import yaml
    prereg_path.write_text(yaml.safe_dump(prereg), encoding="utf-8")

    panels = _panel(n_pairs=10, n_bars=200, attested_fraction=1.0, seed=6)
    loaded = load_prereg(prereg_path)

    first = evaluate(loaded, panels, prereg_path=prereg_path, run_id="run_a")
    assert first.status == "VERDICT"

    second = evaluate(loaded, panels, prereg_path=prereg_path, run_id="run_b")
    assert second.status == "BLOCKED_SINGLE_USE"
    assert second.detail["consumed_by"]["run_id"] == "run_a"


def test_blocked_run_does_not_consume_single_use(tmp_path):
    """A gate BLOCK (min-N here) must not stamp consumption -- only a run that
    reaches an actual verdict spends the single use."""
    prereg_path = tmp_path / "prereg.yaml"
    prereg = _prereg(required_n=10_000, coverage_floor=0.05)  # forces BLOCKED_MIN_N
    import yaml
    prereg_path.write_text(yaml.safe_dump(prereg), encoding="utf-8")
    loaded = load_prereg(prereg_path)

    panels = _panel(n_pairs=5, n_bars=50, attested_fraction=1.0, seed=7)
    blocked = evaluate(loaded, panels, prereg_path=prereg_path, run_id="run_a")
    assert blocked.status == "BLOCKED_MIN_N"

    # Now satisfy the gate and confirm the single use is STILL available.
    loaded["minimum_n_gate"]["required_attested_bars_per_pair"] = 10
    ok = evaluate(loaded, panels, prereg_path=prereg_path, run_id="run_b")
    assert ok.status == "VERDICT"


def _tiny_whale_panels(n_pairs=3, n_bars=5):
    return {
        f"PAIR{i}": pd.DataFrame({
            "whale_lt_imbalance": np.zeros(n_bars), "whale_cvd_delta": np.zeros(n_bars),
            "whale_size_shift": np.zeros(n_bars), "target": np.zeros(n_bars),
            "attested": [True] * n_bars,
        })
        for i in range(n_pairs)
    }


def test_the_real_v1_pre_registration_loads_and_wires_into_the_harness():
    """Schema smoke test against the actual committed v1 file -- RETAINED,
    superseded, not deleted (see prereg_whale_footprint_v2.yaml's amendment
    note). Not a real evaluation (the synthetic panel below is far too small
    to clear its minimum_n_gate, which is the point: it proves the wiring
    without ever approaching real capture data)."""
    real_path = (Path(__file__).parent.parent / "protocols" /
                 "prereg_whale_footprint_v1.yaml")
    prereg = load_prereg(real_path)
    assert prereg["features"]["names"] == [
        "whale_lt_imbalance", "whale_cvd_delta", "whale_size_shift",
    ]
    result = evaluate(prereg, _tiny_whale_panels())
    assert result.status == "BLOCKED_MIN_N", (
        "sanity check: a 5-bar synthetic panel must never clear the real "
        "pre-registration's minimum-N gate"
    )


def test_the_real_v2_pre_registration_loads_and_refuses_below_the_gate():
    """Schema smoke test against v2, the file the harness is now pointed at.

    UPDATED BY DISPATCH W10 (2026-07-28). This test previously asserted
    BLOCKED_ECONOMIC_INFEASIBILITY, encoding W9's finding that the family was
    untradeable at its registered bar frequency (required IC 2.4667 > 1.0).
    W10 arbitrated that derivation and found it WRONG on two inputs: it used
    prescreen_signal.py's <5-record fallback constant (15.0) as if it were a
    measured 1h sigma when every archived prescreen measures 61.6-82.9, and
    it asserted avg_holding_bars=1 from the features' recompute frequency
    when the campaign defines that quantity as measured signal persistence
    (realized: 5.74 bars). Corrected required IC is 0.2507, well inside the
    correlation bound, so the economic gate no longer fires and execution
    correctly falls through to the (now live) minimum-N gate.

    The economic gate MECHANISM is unchanged and still covered -- see the two
    tests above that drive it with a synthetic prereg whose flag is true.
    Not a real evaluation; nothing here reads recorded_reserved/."""
    real_path = (Path(__file__).parent.parent / "protocols" /
                 "prereg_whale_footprint_v2.yaml")
    prereg = load_prereg(real_path)
    assert prereg["features"]["names"] == [
        "whale_lt_imbalance", "whale_cvd_delta", "whale_size_shift",
    ]
    assert prereg["metadata"]["supersedes"] == "prereg_whale_footprint_v1.yaml"
    econ = prereg["economic_ic_threshold"]
    assert econ["economically_untradeable_at_registered_frequency"] is False, (
        "W10: the infeasibility finding is withdrawn; the flag must be false"
    )
    assert econ["required_ic_at_registered_frequency"] < 1.0, (
        "a required IC at or above 1.0 is unreachable by a Spearman "
        "correlation -- if this trips again, re-audit the derivation's inputs "
        "before registering the conclusion"
    )
    result = evaluate(prereg, _tiny_whale_panels())
    assert result.status == "BLOCKED_MIN_N", (
        "sanity check: with the economic gate withdrawn, a 5-bar synthetic "
        "panel must still never clear v2's minimum-N gate (321 bars/pair)"
    )


def test_w11_amendment_invariants():
    """
    Dispatch W11 measured sigma for the real 19-pair set and reclassified the
    borrowed H. It was permitted to change ONLY the derived figures; every gate
    parameter had to survive untouched. These assertions are that constraint
    written down, so a later amendment cannot quietly loosen one of them while
    editing the derivation around it.
    """
    real_path = (Path(__file__).parent.parent / "protocols" /
                 "prereg_whale_footprint_v2.yaml")
    prereg = load_prereg(real_path)
    econ = prereg["economic_ic_threshold"]
    assumptions = econ["assumptions_stated"]

    # --- unchanged by W11, by instruction ---------------------------------
    assert assumptions["safety_factor"]["value"] == 2.0
    assert assumptions["round_trip_cost_bps"]["value"] == 18.5
    assert prereg["required_coverage_floor"]["floor"] == 0.80
    assert prereg["minimum_n_gate"]["power_target"] == 0.80
    mcc = prereg["test_statistic"]["multiple_comparison_correction"]
    assert mcc["method"] == "bonferroni"
    assert mcc["family_size"] == 4 and mcc["alpha_corrected"] == 0.0125
    assert prereg["single_use"]["fires_exactly_once"] is True
    assert prereg["single_use"]["consumed_by"] is None, (
        "v2 must still be unconsumed -- W11 did not run the evaluation"
    )
    assert set(prereg["verdict"]["mapping"]) == {"PASS", "UNSTABLE", "NULL"}
    assert prereg["features"]["bar_seconds"] == 3600
    assert prereg["features"]["frozen"] is True

    # --- measured by W11 ---------------------------------------------------
    sigma = assumptions["sigma_bar_bps"]["value"]
    h = assumptions["avg_holding_bars_primary"]["value"]
    assert sigma == 106.8726
    assert len(assumptions["sigma_bar_bps"]["w11_measurement"]["per_pair_bps"]) == 19
    assert assumptions["avg_holding_bars_primary"]["provenance_status"] == (
        "BORROWED_UNMEASURED"
    ), "H is not a measurement of this feature family and must stay labelled as such"

    # --- the derivation is internally consistent ---------------------------
    expected_ic = round(2.0 * 18.5 / (sigma * math.sqrt(h)), 4)
    assert econ["required_ic_at_registered_frequency"] == expected_ic
    assert prereg["minimum_n_gate"]["target_detectable_ic"] == expected_ic, (
        "v2 couples the minimum-N target to the economic required IC; if they "
        "diverge, one of the two was edited without the other"
    )

    # --- and the registered N actually solves it ---------------------------
    n = prereg["minimum_n_gate"]["required_attested_bars_per_pair"]
    n_eff = n * 1.655
    mde = math.tanh((2.4977 + 0.8416) / math.sqrt(n_eff - 3.0))
    assert mde <= expected_ic, (
        f"{n} bars/pair yields MDE {mde:.6f}, which does not reach the "
        f"registered target {expected_ic}"
    )
    assert n > 105, "W11's sample requirement must not be below W10's"


def test_r3_block_adjusted_significance_disagrees_with_raw_scipy_pvalue():
    """
    W14 R2/R3 demonstration, not just assertion. Before this dispatch,
    `_feature_verdict` compared scipy's raw (unadjusted) Spearman p-value
    against `alpha_corrected` -- treating every pooled bar as an independent
    draw. On a WEAK, LARGE-N signal that is anti-conservative: the raw
    p-value clears significance from bar count alone, while the block-24
    Fisher-z estimator (`prescreen_signal._block_adjusted_significance`,
    the same one every 1h prescreen decision in this campaign is gated on)
    correctly does not. Both p-values are computed here from the SAME pooled
    data, so the disagreement is demonstrated rather than asserted from a
    hardcoded number.
    """
    from scipy import stats as _scipy_stats

    alpha_corrected = 0.0125
    # signal_strength=0.02 against noise scale 0.4 (see _panel) gives a real
    # but weak pooled IC; n_pairs x n_bars is large enough that raw-p treats
    # it as overwhelming evidence purely from bar count.
    panels = _panel(n_pairs=20, n_bars=1400, attested_fraction=1.0,
                     signal_strength=0.02, seed=1)
    pooled = pd.concat(
        [df.loc[df["attested"].astype(bool), ["f_signal", "target"]] for df in panels.values()],
        ignore_index=True,
    )
    n_pooled = len(pooled)
    _raw_ic, raw_p = _scipy_stats.spearmanr(pooled["f_signal"], pooled["target"])

    # "BEFORE" behaviour, reconstructed inline (the removed code path's own
    # comparison): the raw p-value clears alpha_corrected on this fixture.
    assert raw_p < alpha_corrected, (
        "fixture must plant a signal the RAW p-value calls significant -- "
        "widen n_bars/n_pairs or the signal strength if this no longer holds"
    )

    prereg = _prereg(required_n=10, coverage_floor=0.0, alpha_corrected=alpha_corrected)
    result = evaluate(prereg, panels)
    assert result.status == "VERDICT"
    f_signal = next(f for f in result.detail["per_feature"] if f["feature"] == "f_signal")

    # "AFTER" behaviour: the harness's own block-adjusted p-value, on the
    # EXACT SAME pooled data, is orders of magnitude larger and does NOT
    # clear alpha_corrected -- flipping the verdict to NULL.
    assert f_signal["p_value"] > raw_p * 1000, (
        f"block-adjusted p ({f_signal['p_value']}) should be orders of "
        f"magnitude larger than the raw scipy p ({raw_p}) on this pooled n "
        f"({n_pooled}) -- the fix may not be wired in"
    )
    assert f_signal["p_value"] >= alpha_corrected, (
        f"expected the block-adjusted estimator to NOT clear alpha_corrected "
        f"on this weak, large-N signal; got p={f_signal['p_value']}"
    )
    assert f_signal["verdict"] == "NULL", (
        "the raw-p-value code path would have called this PASS/UNSTABLE "
        "(spuriously, from bar count alone); the block-adjusted fix must "
        "route it to NULL instead"
    )
    assert f_signal["significance"]["block_size"] == 24
    assert f_signal["significance"]["n_eff"] == n_pooled // 24, (
        "n_eff must derive from the SAME pooled attested count the verdict "
        "itself computed, not a value recomputed independently by the test"
    )


def test_null_scope_is_registered_and_bounded():
    """
    W11 step 5 restated NULL without moving its threshold. Both halves are
    asserted: the scope section exists, and the condition is still the plain
    alpha_corrected test.
    """
    real_path = (Path(__file__).parent.parent / "protocols" /
                 "prereg_whale_footprint_v2.yaml")
    prereg = load_prereg(real_path)
    verdict = prereg["verdict"]
    assert "null_scope" in verdict, "NULL's scope must be registered, not implied"
    scope = verdict["null_scope"]
    for key in ("what_null_means", "it_is_not_a_statement_that",
                "what_null_routes_to", "what_null_does_not_authorize"):
        assert key in scope and scope[key].strip(), f"null_scope.{key} is missing"
    # the threshold itself is untouched
    assert "alpha_corrected" in verdict["mapping"]["NULL"]
    assert prereg["test_statistic"]["multiple_comparison_correction"][
        "alpha_corrected"] == 0.0125
