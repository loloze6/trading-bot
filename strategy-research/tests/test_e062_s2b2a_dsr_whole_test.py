"""E-062 S2b-2a -- the whole-test daily DSR, pure functions only (D-041 / D-046).

Covers portfolio_whole_test.whole_test_sharpe_stats and, in tools/deflate_sharpe.py,
compute_dsr_whole_test, select_same_basis_sample and the recompute-overlay
validator/loader. Nothing in the pipeline calls them yet (S2b-2b). Expected numbers
are worked by hand in the test (standard-normal quantiles quoted to 10 digits),
never read back from the function under test. Dates are synthetic 2018-2020 dates.
"""
from __future__ import annotations

import copy
import math
import random
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "tools"))

import deflate_sharpe as ds  # noqa: E402
import portfolio_daily as pdv1  # noqa: E402
import portfolio_whole_test as pw  # noqa: E402

NE = pdv1.PortfolioNotEvaluable
BASIS = "whole_test_daily_equal_weight_v1"
D0 = date(2018, 4, 1)


def _series(rets):
    return [(D0 + timedelta(days=i), r) for i, r in enumerate(rets)]


def _real_shaped(n=2695, seed=20260929):
    """Fat-tailed daily returns of a real run's length (run_054: T=2695): a scaled
    Student-t(3)-like draw plus a small drift, clipped above -1."""
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        z = rng.gauss(0.0, 1.0)
        chi = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(3)) / 3.0
        out.append(max(-0.5, 0.0008 + 0.02 * z / math.sqrt(chi)))
    return out


# ---------------------------------------------------------------------------
# whole_test_sharpe_stats
# ---------------------------------------------------------------------------

def test_sr_daily_times_sqrt365_equals_whole_test_sharpe_exactly():
    s = _series(_real_shaped())
    st = pw.whole_test_sharpe_stats(s)
    assert st["T"] == 2695
    assert st["sr_daily"] * math.sqrt(365) == pw.whole_test_sharpe(s)  # bit for bit


def test_whole_test_sharpe_value_unchanged_by_the_refactor():
    """The S2a formula, written out as it stood before this slice: mean / stdev x sqrt(365)."""
    rets = _real_shaped(500, seed=7)
    before = statistics.mean(rets) / statistics.stdev(rets) * math.sqrt(365)
    assert pw.whole_test_sharpe(_series(rets)) == before


def test_moments_on_a_known_series():
    """10 x [-0.01, 0, 0.01, 0.04] (T = 40). mean 0.01; deviations -0.02, -0.01, 0, 0.03.
    m2 = (4e-4 + 1e-4 + 0 + 9e-4) / 4 = 3.5e-4
    m3 = (-8e-6 - 1e-6 + 0 + 2.7e-5) / 4 = 4.5e-6
    m4 = (1.6e-7 + 1e-8 + 0 + 8.1e-7) / 4 = 2.45e-7
    skew = 4.5e-6 / (3.5e-4)^1.5 = 0.687243...; raw kurtosis = 2.45e-7 / 1.225e-7 = 2.0
    sr_daily = 0.01 / sqrt(3.5e-4 x 40 / 39)  (sample stdev, ddof 1)."""
    st = pw.whole_test_sharpe_stats(_series([-0.01, 0.0, 0.01, 0.04] * 10))
    assert st["T"] == 40
    assert st["kurtosis_raw"] == pytest.approx(2.0, abs=1e-12)
    assert st["skew"] == pytest.approx(4.5e-6 / 3.5e-4 ** 1.5, rel=1e-12)
    assert st["skew"] == pytest.approx(0.6872431, abs=1e-7)
    assert st["sr_daily"] == pytest.approx(0.01 / math.sqrt(3.5e-4 * 40 / 39), rel=1e-12)


def test_moments_agree_with_scipy_population_moments():
    stats = pytest.importorskip("scipy.stats")
    rets = _real_shaped(1394, seed=11)
    st = pw.whole_test_sharpe_stats(_series(rets))
    assert st["skew"] == pytest.approx(float(stats.skew(rets, bias=True)), rel=1e-9)
    assert st["kurtosis_raw"] == pytest.approx(
        float(stats.kurtosis(rets, fisher=False, bias=True)), rel=1e-9)


def test_stats_keep_the_s2a_not_evaluable_rules():
    with pytest.raises(NE):
        pw.whole_test_sharpe_stats(_series([0.01, -0.01] * 14 + [0.0]))  # 29 returns
    with pytest.raises(NE):
        pw.whole_test_sharpe_stats(_series([0.001] * 40))  # zero stdev
    with pytest.raises(ValueError):
        pw.whole_test_sharpe_stats(_series([0.01] * 39 + [float("nan")]))


# ---------------------------------------------------------------------------
# compute_dsr_whole_test
# ---------------------------------------------------------------------------

# Standard-normal quantiles (10 digits): Phi^-1(0.9) = 1.2815515655,
# Phi^-1(1 - 1/(10e)) = Phi^-1(0.9632120559) = 1.7892417646.
# Z(10) = (1 - 0.5772156649) x 1.2815515655 + 0.5772156649 x 1.7892417646 = 1.5745983013
Z10 = 1.5745983013
# Phi^-1(1 - 1/12) = 1.3829941271, Phi^-1(1 - 1/(12e)) = 1.8712297694
# Z(12) = 0.4227843351 x 1.3829941271 + 0.5772156649 x 1.8712297694 = 1.6648113880
Z12 = 1.6648113880

CAND = {"sr_daily": 0.2, "T": 401, "skew": -0.5, "kurtosis_raw": 6.0}


def _dsr_by_hand(sr, sr0, t, skew, kurt):
    return statistics.NormalDist().cdf(
        (sr - sr0) * math.sqrt(t - 1) / math.sqrt(1 - skew * sr + (kurt - 1) / 4 * sr * sr))


def test_z_expected_max_quantiles():
    assert ds._expected_max_z(10) == pytest.approx(Z10, abs=1e-10)
    assert ds._expected_max_z(12) == pytest.approx(Z12, abs=1e-10)


def test_hand_computed_blp_example_cross_sigma():
    """Candidate SR = 0.2 per day, T = 401, skew -0.5, raw kurtosis 6.
    Same-basis sample {0.0, 0.1, 0.2} (K = 3, floor 3), N = 10.
      mean_K = 0.1; V = (0.01 + 0 + 0.01) / 2 = 0.01 (ddof 1); sigma_K = 0.1
      sigma_null = 1 / sqrt(400) = 0.05  ->  max(0.1, 0.05) = 0.1 (cross)
      SR0 = max(0.1, 0) + 0.1 x 1.5745983013 = 0.2574598301
      denominator = 1 - (-0.5)(0.2) + ((6 - 1)/4)(0.04) = 1 + 0.1 + 0.05 = 1.15
      z = (0.2 - 0.2574598301) x sqrt(400) / sqrt(1.15) = -1.1491966027 / 1.0723805292
        = -1.0716313576
      DSR = Phi(-1.0716313576) = 0.1419428215"""
    r = ds.compute_dsr_whole_test(CAND, [0.0, 0.1, 0.2], 10, 3)
    assert r["status"] == "ok" and r["reason"] is None
    assert (r["K"], r["N"], r["T"], r["min_same_basis"]) == (3, 10, 401, 3)
    assert r["mean_same_basis"] == pytest.approx(0.1, abs=1e-15)
    assert r["sigma_cross"] == pytest.approx(0.1, abs=1e-15)
    assert r["sigma_null"] == pytest.approx(0.05, abs=1e-15)
    assert r["sigma_source"] == "cross" and r["sigma_used"] == pytest.approx(0.1, abs=1e-15)
    assert r["z_expected_max"] == pytest.approx(Z10, abs=1e-10)
    assert r["sr0"] == pytest.approx(0.2574598301, abs=1e-10)
    assert r["dsr"] == pytest.approx(0.1419428215, abs=1e-9)


def test_k_below_floor_uses_sigma_null_and_ignores_the_sample():
    """Same candidate, floor 4 > K = 3: SR0 = sigma_null x Z(10) = 0.05 x 1.5745983013
    = 0.0787299151; the sample's mean and spread are not used (a wild sample gives the
    same SR0)."""
    for sample in ([0.0, 0.1, 0.2], [-5.0, 0.0, 9.0], []):
        r = ds.compute_dsr_whole_test(CAND, sample, 10, 4)
        assert r["status"] == "ok"
        assert r["sigma_source"] == "null"
        assert r["sigma_used"] == pytest.approx(0.05, abs=1e-15)
        assert r["mean_same_basis"] is None and r["sigma_cross"] is None
        assert r["sr0"] == pytest.approx(0.0787299151, abs=1e-10)
        assert r["dsr"] == pytest.approx(_dsr_by_hand(0.2, 0.05 * Z10, 401, -0.5, 6.0), abs=1e-9)


def test_k_at_or_above_floor_takes_the_larger_sigma_both_ways():
    # sigma_K = 0.01 < sigma_null = 0.05 -> null; mean 0.02 still added
    r = ds.compute_dsr_whole_test(CAND, [0.01, 0.02, 0.03], 10, 3)
    assert r["sigma_source"] == "null" and r["sigma_cross"] == pytest.approx(0.01, abs=1e-15)
    assert r["sr0"] == pytest.approx(0.02 + 0.05 * Z10, abs=1e-10)
    # sigma_K = 0.1 > 0.05 -> cross (the hand example)
    r = ds.compute_dsr_whole_test(CAND, [0.0, 0.1, 0.2], 10, 3)
    assert r["sigma_source"] == "cross"
    assert r["sr0"] == pytest.approx(0.1 + 0.1 * Z10, abs=1e-10)


def test_zero_variance_at_or_above_floor_falls_to_sigma_null():
    r = ds.compute_dsr_whole_test(CAND, [0.03, 0.03, 0.03], 10, 3)
    assert r["status"] == "ok"
    assert r["sigma_cross"] == 0.0 and r["sigma_source"] == "null"
    assert r["sr0"] == pytest.approx(0.03 + 0.05 * Z10, abs=1e-10)
    assert r["dsr"] is not None


def test_negative_mean_does_not_lower_sr0():
    """mean_K = -0.1, sigma_K = 0.1: SR0 = max(-0.1, 0) + 0.1 x Z(10) = 0.1574598301,
    not -0.1 + 0.1574598301."""
    r = ds.compute_dsr_whole_test(CAND, [-0.2, -0.1, 0.0], 10, 3)
    assert r["mean_same_basis"] == pytest.approx(-0.1, abs=1e-15)
    assert r["sr0"] == pytest.approx(0.1574598301, abs=1e-10)


def test_n_below_two_is_not_evaluable():
    for n, sample in ((1, [0.2]), (0, [])):
        r = ds.compute_dsr_whole_test(CAND, sample, n, 3)
        assert r["status"] == "not_evaluable" and r["dsr"] is None
        assert f"N={n}" in r["reason"]


def test_n_below_k_raises():
    with pytest.raises(ValueError, match="smaller than the same-basis sample"):
        ds.compute_dsr_whole_test(CAND, [0.0, 0.1, 0.2], 2, 3)


def test_candidate_block_not_ok_is_not_evaluable():
    r = ds.compute_dsr_whole_test({"status": "not_evaluable", "reason": "29 daily returns"},
                                  [0.1, 0.2], 12, 10)
    assert r["status"] == "not_evaluable" and r["dsr"] is None
    assert "not_evaluable" in r["reason"] and "29 daily returns" in r["reason"]


def test_non_positive_denominator_is_not_evaluable():
    # valid moments (kurt = 1 + skew^2): the argument is (1 - skew*SR/2)^2 = 0 at SR = 0.5
    r = ds.compute_dsr_whole_test({"sr_daily": 0.5, "T": 100, "skew": 4.0, "kurtosis_raw": 17.0},
                                  [], 12, 10)
    assert r["status"] == "not_evaluable" and r["dsr"] is None and "denominator" in r["reason"]


def test_candidate_t_below_the_s2a_floor_is_not_evaluable():
    for t in (0, 1, 3, pw.SHARPE_MIN_DAILY_RETURNS - 1):
        r = ds.compute_dsr_whole_test({"sr_daily": 3.0, "T": t, "skew": 0.0, "kurtosis_raw": 3.0},
                                      [], 12, 10)
        assert r["status"] == "not_evaluable" and r["dsr"] is None, t
        assert "SHARPE_MIN_DAILY_RETURNS" in r["reason"]
    r = ds.compute_dsr_whole_test({"sr_daily": 3.0, "T": pw.SHARPE_MIN_DAILY_RETURNS,
                                   "skew": 0.0, "kurtosis_raw": 3.0}, [], 12, 10)
    assert r["status"] == "ok" and r["dsr"] is not None


def test_kurtosis_equal_to_one_plus_skew_squared_is_accepted():
    r = ds.compute_dsr_whole_test({"sr_daily": 0.1, "T": 100, "skew": 2.0, "kurtosis_raw": 5.0},
                                  [], 12, 10)
    assert r["status"] == "ok"


@pytest.mark.parametrize("kwargs", [
    {"min_same_basis": 1},
    {"min_same_basis": True},
    {"n_total": 12.0},
    {"same_basis_srs": [0.1, float("nan")]},
    {"same_basis_srs": [0.1, True]},
    {"candidate_stats": {**CAND, "sr_daily": float("inf")}},
    {"candidate_stats": {**CAND, "T": 1.5}},
    {"candidate_stats": {**CAND, "T": -1}},
    {"candidate_stats": {**CAND, "status": "OK"}},
    {"candidate_stats": {**CAND, "status": None}},
    {"candidate_stats": {**CAND, "skew": 4.0, "kurtosis_raw": 1.0}},   # kurt < 1 + skew^2
    {"candidate_stats": {k: v for k, v in CAND.items() if k != "skew"}},
    {"candidate_stats": None},
])
def test_malformed_inputs_raise(kwargs):
    base = {"candidate_stats": CAND, "same_basis_srs": [0.1, 0.2], "n_total": 12,
            "min_same_basis": 10}
    with pytest.raises(ValueError):
        ds.compute_dsr_whole_test(**{**base, **kwargs})


def test_sanity_pin_n12_t2695_normal_hurdle_is_1_22_annualised():
    """D-046's measured hurdle: N = 12, T = 2695, normal returns (skew 0, raw kurtosis 3),
    K below the floor -> the per-day SR at which DSR reaches 0.95, annualised x sqrt(365),
    is about 1.22."""
    def dsr(sr):
        return ds.compute_dsr_whole_test(
            {"sr_daily": sr, "T": 2695, "skew": 0.0, "kurtosis_raw": 3.0}, [], 12, 10)["dsr"]
    lo, hi = 0.0, 0.2
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if dsr(mid) < 0.95 else (lo, mid)
    assert hi * math.sqrt(365) == pytest.approx(1.22, abs=0.01)


# ---------------------------------------------------------------------------
# select_same_basis_sample + overlay
# ---------------------------------------------------------------------------

SHA = "a" * 64


def _block(sr, basis=BASIS, status="ok"):
    if status != "ok":
        return {"basis": basis, "status": status, "reason": "missing curve", "sr_daily": None,
                "n_daily_returns": None, "skew": None, "kurtosis": None}
    return {"basis": basis, "status": "ok", "reason": None, "sr_daily": sr,
            "n_daily_returns": 2695, "skew": -0.4, "kurtosis": 11.6}


def _entry(tid, source, sr, basis=BASIS, status="ok"):
    return {"trial_id": tid, "source": source, **_block(sr, basis, status),
            "inputs_sha256": {"protocol_result": SHA, "portfolio_states": {"w1.csv": SHA}},
            "code_sha256": {"portfolio_whole_test.py": SHA}}


def _row(tid, source="backtest", fh=None, **extra):
    r = {"trial_id": tid, "source": source, "sharpe": None, "statistic_valid": "neither",
         "forecast_hash": fh or f"h_{tid}_{source}"}
    r.update(extra)
    return r


def _mixed_ledger():
    return [
        # legacy backtest row with a per-window-median Sharpe: N only, never K
        _row("run_054", sharpe=5.0, statistic_valid="sharpe"),
        _row("run_054", source="prescreen"),
        _row("run_055", source="backtest_failed", statistic_valid="failed"),
        _row("run_070", whole_test=_block(0.05)),                        # K
        _row("run_071", whole_test=_block(-0.02)),                       # K
        _row("run_072", whole_test=_block(0.9, basis="whole_test_daily_equal_weight_v2")),
        _row("run_073", whole_test=_block(None, status="not_evaluable")),
        _row("run_074", whole_test=_block(0.7), invalidated_artifact=True),  # out of N and K
        _row("run_075", fh="h_run_070_backtest", whole_test=_block(0.05)),   # dedup onto 070
    ]


def test_mixed_legacy_and_whole_test_rows_never_mix():
    got = ds.select_same_basis_sample(_mixed_ledger())
    assert got["srs"] == [0.05, -0.02]
    assert [r["trial_id"] for r in got["rows"]] == ["run_070", "run_071"]
    assert {r["origin"] for r in got["rows"]} == {"native"}
    assert got["K"] == 2 and got["basis"] == BASIS
    # N: 9 rows - 1 invalidated - 1 dedup = 7
    assert got["N"] == 7


def test_n_is_todays_rule_and_does_not_depend_on_the_overlay():
    ledger = _mixed_ledger()
    legacy_n = ds.compute_promotion_audit("h", 0.1, {"trial_sharpes": ledger})[
        "total_hypotheses_tested"]
    overlay = ds.validate_basis_overlay({"entries": [_entry("run_054", "backtest", 0.0512)]})
    with_ov = ds.select_same_basis_sample(ledger, overlay)
    assert ds.select_same_basis_sample(ledger)["N"] == with_ov["N"] == legacy_n == 7
    assert with_ov["K"] == 3 and 0.0512 in with_ov["srs"]
    assert [r["origin"] for r in with_ov["rows"] if r["trial_id"] == "run_054"] == ["overlay"]


def test_overlay_used_on_target_basis_when_native_block_is_another_basis():
    ov = ds.validate_basis_overlay({"entries": [_entry("run_072", "backtest", 0.3)]})
    got = ds.select_same_basis_sample(_mixed_ledger(), ov)
    assert [(r["trial_id"], r["origin"]) for r in got["rows"]
            if r["trial_id"] == "run_072"] == [("run_072", "overlay")]


def test_native_beats_an_equal_overlay_entry():
    ov = ds.validate_basis_overlay({"entries": [_entry("run_070", "backtest", 0.05)]})
    got = ds.select_same_basis_sample(_mixed_ledger(), ov)
    assert [r["origin"] for r in got["rows"] if r["trial_id"] == "run_070"] == ["native"]
    assert got["srs"] == [0.05, -0.02]


def test_native_and_overlay_that_differ_raise():
    ov = ds.validate_basis_overlay({"entries": [_entry("run_070", "backtest", 0.06)]})
    with pytest.raises(ValueError, match="differ"):
        ds.select_same_basis_sample(_mixed_ledger(), ov)


def test_overlay_entry_for_a_row_absent_from_the_ledger_raises():
    ov = ds.validate_basis_overlay({"entries": [_entry("run_999", "backtest", 0.1)]})
    with pytest.raises(ValueError, match="not merged"):
        ds.select_same_basis_sample(_mixed_ledger(), ov)


def test_overlay_not_evaluable_entry_counts_in_n_only():
    ov = ds.validate_basis_overlay({"entries": [
        _entry("run_054", "backtest", None, status="not_evaluable")]})
    got = ds.select_same_basis_sample(_mixed_ledger(), ov)
    assert got["K"] == 2 and got["N"] == 7


def test_overlay_identical_duplicate_kept_once_and_differing_duplicate_raises():
    e = _entry("run_054", "backtest", 0.0512)
    assert len(ds.validate_basis_overlay({"entries": [e, copy.deepcopy(e)]})) == 1
    e2 = copy.deepcopy(e)
    e2["sr_daily"] = 0.0513
    with pytest.raises(ValueError, match="two different entries"):
        ds.validate_basis_overlay({"entries": [e, e2]})


@pytest.mark.parametrize("mutate", [
    lambda e: e.update(generated_at="<utc timestamp>"),        # a timestamp: not deterministic
    lambda e: e.pop("code_sha256"),
    lambda e: e.update(status="maybe"),
    lambda e: e.update(sr_daily=float("nan")),
    lambda e: e.update(reason="x"),                            # ok with a reason
    lambda e: e.update(inputs_sha256={"protocol_result": "not-a-sha"}),
    lambda e: e.update(trial_id=""),
    lambda e: e.update(n_daily_returns=True),
    lambda e: e.update(n_daily_returns=pw.SHARPE_MIN_DAILY_RETURNS - 1),
])
def test_overlay_entry_validation_refuses(mutate):
    e = _entry("run_054", "backtest", 0.0512)
    mutate(e)
    with pytest.raises(ValueError):
        ds.validate_basis_overlay({"entries": [e]})


def test_overlay_top_level_shape():
    assert ds.validate_basis_overlay(None) == {}
    assert ds.validate_basis_overlay({}) == {}
    assert ds.validate_basis_overlay({"entries": None}) == {}
    with pytest.raises(ValueError):
        ds.validate_basis_overlay([_entry("run_054", "backtest", 0.05)])
    with pytest.raises(ValueError):
        ds.validate_basis_overlay({"entries": [], "version": 1})


def test_native_block_with_unknown_key_raises():
    ledger = [_row("run_070", whole_test={**_block(0.05), "annualised": 0.95})]
    with pytest.raises(ValueError, match="unknown"):
        ds.select_same_basis_sample(ledger)


def test_load_basis_overlay_reads_a_file_and_a_missing_file_is_empty(tmp_path):
    assert ds.load_basis_overlay(tmp_path / "absent.yaml") == {}
    p = tmp_path / "trial_sharpe_basis_recompute.yaml"
    e = _entry("run_054", "backtest", 0.0512)
    p.write_text(yaml.safe_dump({"entries": [e]}, sort_keys=True), encoding="utf-8")
    before = p.read_bytes()
    got = ds.load_basis_overlay(p)
    assert got == {("run_054", "backtest", BASIS): e}
    assert p.read_bytes() == before  # read-only


def test_ok_native_block_below_the_s2a_floor_raises():
    blk = {**_block(0.05), "n_daily_returns": pw.SHARPE_MIN_DAILY_RETURNS - 1}
    with pytest.raises(ValueError, match="n_daily_returns"):
        ds.select_same_basis_sample([_row("run_1", whole_test=blk)])
    blk["n_daily_returns"] = pw.SHARPE_MIN_DAILY_RETURNS
    assert ds.select_same_basis_sample([_row("run_1", whole_test=blk)])["K"] == 1
