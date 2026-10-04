"""E-068 slice 1 (CUL-386): tools/claim_tests.py (+ the calibration tool).

Every block: a planted effect is detected, and no effect is not. Every
selector: changing any future bar never changes today's selection. Plus the
floor -> inconclusive, future-field refusal, timestamp matching inside a window
only, the null (fake worlds with the signal recomputed), the forecast check,
the warm-up reader, spec_hash stability, the claim-file checks and the CLI.
Synthetic data only (2020-2023 dates); no market data is read.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR_ROOT / "tools"))

import claim_tests as ct  # noqa: E402
import claim_tests_calibration as cal  # noqa: E402
from performance.signal_statistics import spearman_correlation  # noqa: E402

T0 = 1577836800          # 2020-01-01 00:00 UTC
DAY = 86400
HOUR = 3600
FAST = {"method": "block_permutation_v1", "n_resamples": 99, "seed": 7}
DON = {"class": "DonchianBreakoutComponent", "params": {"period": 10, "scaling_factor": 20.0}}
WARM = 30


def make_windows(seed=0, n=300, n_windows=4, plant=None, h=1, sd=0.02):
    """Daily synthetic windows whose forecast is the REAL Donchian(10) of the
    price, computed bar by bar, so the null can recompute it. `plant(t, fc, ts)`
    returns (drift added to returns t+1..t+h, vol multiplier for them)."""
    rng = np.random.default_rng(seed)
    out = []
    for wi in range(n_windows):
        m = n + WARM
        ts_all = (T0 + (wi * (m + 5) + np.arange(m)) * DAY).astype(np.int64)
        close = np.empty(m)
        close[0] = 100.0
        r = rng.normal(0.0, sd, m)
        drift, scale = np.zeros(m), np.ones(m)
        for t in range(m - 1):
            if plant is not None and t >= 9:      # the effect of bar t's signal, first ...
                win = close[t - 9:t + 1]
                hi, lo = win.max(), win.min()
                fc_t = ((0.5 if hi == lo else (close[t] - lo) / (hi - lo)) * 2 - 1) * 20
                d, v = plant(t, fc_t, ts_all[t])
                if isinstance(d, list):               # one drift per lag 1, 2, ...
                    drift[t + 1:t + 1 + len(d)] += np.array(d)[:max(0, m - t - 1)]
                else:
                    drift[t + 1:t + 1 + h] += d
                scale[t + 1:t + 1 + h] *= v
            close[t + 1] = close[t] * np.exp(r[t + 1] * scale[t + 1] + drift[t + 1])  # ... then t+1
        high, low = close * 1.002, close * 0.998
        fc = ct.compute_signal(DON, high, low, close)
        warm = {"ts": ts_all[:WARM], "close": close[:WARM], "high": high[:WARM],
                "low": low[:WARM]}
        reg = np.where(np.arange(n) % 20 < 10, "trend", "range").astype(object)
        out.append(ct.Window("SYN", f"w{wi}", ts_all[WARM:], close[WARM:], fc[WARM:], reg, DAY,
                             high=high[WARM:], low=low[WARM:], warm=warm, signal=DON))
    return out


def spec(selector, outcome=None, baseline=None, statistic="mean_diff", direction="greater",
         floor=None, consistency=None):
    return ct.TestSpec(selector=selector,
                       outcome=outcome or {"kind": "fwd_return", "horizons": [1]},
                       baseline=baseline if baseline is not None or statistic == "rank_ic"
                       else {"kind": "complement"},
                       statistic=statistic, direction=direction,
                       floor=floor or {"min_events": 20}, consistency=consistency,
                       significance=dict(FAST))


def rt(windows, s, eras=None):
    """run_test with a calibrated method (the gate itself is tested separately)."""
    return ct.run_test(windows, s, eras, calibrated=True)


def status(windows, s, eras=None):
    return rt(windows, s, eras)["status"]


# Planted effects are REVERSALS (a rebound after a low signal, a fall after a
# high one): a momentum plant makes the price run away until nearly every bar
# is selected.
EVENT = {"kind": "event", "field": "forecast", "op": "<=", "value": -8}
EVENT_HIGH = {"kind": "event", "field": "forecast", "op": ">=", "value": 8}
LOW_FC = lambda e: (lambda t, fc, ts: (e if fc <= -8 else 0.0, 1.0))  # noqa: E731
HIGH_FC = lambda e: (lambda t, fc, ts: (e if fc >= 8 else 0.0, 1.0))  # noqa: E731


def planted_and_null(s, plant_on, plant_off, seed, h=1):
    """Detects the planted effect; with no effect, at most 1 of 5 seeds is a
    chance 'supported' (the false-positive rate itself is the calibration's job)."""
    assert status(make_windows(seed, plant=plant_on, h=h), s) == "supported"
    hits = sum(status(make_windows(seed + 1000 * k, plant=plant_off, h=h), s) == "supported"
               for k in range(5))
    assert hits <= 1, hits


# --- selectors ------------------------------------------------------------------

def test_selector_event_planted_and_null():
    planted_and_null(spec(EVENT), LOW_FC(0.02), LOW_FC(0.0), 1)


def test_selector_all_rank_ic_planted_and_null():
    s = spec({"kind": "all"}, statistic="rank_ic", floor={"min_blocks": 30})
    ic = lambda b: (lambda t, fc, ts: (b * fc / 20, 1.0))  # noqa: E731
    planted_and_null(s, ic(0.01), ic(0.0), 2)


def test_selector_calendar_planted_and_null():
    monday = lambda e: (lambda t, fc, ts: (e if ((ts // DAY) + 3) % 7 == 0 else 0.0, 1.0))  # noqa: E731
    planted_and_null(spec({"kind": "calendar", "weekdays": [0]}), monday(0.03), monday(0.0), 3)


def test_selector_quantile_planted_and_null():
    sel = {"kind": "quantile", "field": "forecast", "side": "bottom", "q": 0.2, "lookback": 30}
    planted_and_null(spec(sel), LOW_FC(0.02), LOW_FC(0.0), 4)


def test_regime_selectors_select_the_planted_bars_but_cannot_be_graded():
    w = make_windows(5, n_windows=1)[0]
    m, v = ct.sel_regime(w, {"kind": "regime", "value": "trend"})
    assert np.array_equal(m, w.regime == "trend") and v.all()
    m, v = ct.sel_regime_change(w, {"kind": "regime_change", "to": "trend"})
    expected = np.r_[False, (w.regime[1:] == "trend") & (w.regime[:-1] != "trend")]
    assert np.array_equal(m, expected)
    for sel in ({"kind": "regime", "value": "trend"}, {"kind": "regime_change", "to": "trend"}):
        with pytest.raises(ValueError, match="cannot be graded"):
            rt([w], spec(sel))


# --- outcomes ---------------------------------------------------------------------

def test_outcome_fwd_volatility_planted_and_null():
    vol = lambda v: (lambda t, fc, ts: (0.0, v if fc <= -8 else 1.0))  # noqa: E731
    s = spec(EVENT, outcome={"kind": "fwd_volatility", "horizons": [5]})
    planted_and_null(s, vol(3.0), vol(1.0), 6, h=5)


def test_outcome_fwd_max_drawdown_planted_and_null():
    s = spec(EVENT_HIGH, outcome={"kind": "fwd_max_drawdown", "horizons": [5]}, direction="less")
    planted_and_null(s, HIGH_FC(-0.01), HIGH_FC(0.0), 7, h=5)


def test_outcome_trend_ends_planted_and_null():
    # At the top of the range the trailing return is up; a planted fall makes
    # the trend end more often there than elsewhere.
    s = spec(EVENT_HIGH, outcome={"kind": "trend_ends", "horizons": [3]})
    planted_and_null(s, HIGH_FC(-0.015), HIGH_FC(0.0), 8, h=3)


def test_outcome_definitions_exact():
    ts = (T0 + np.arange(6) * HOUR).astype(np.int64)
    close = np.array([100., 110., 99., 121., 100., 130.])
    w = ct.Window("S", "w", ts, close, np.zeros(6), np.array(["x"] * 6, dtype=object), HOUR)
    assert ct.out_fwd_return(w, 2)[0] == pytest.approx(99 / 100 - 1)
    assert ct.out_fwd_mdd(w, 3)[0] == pytest.approx(99 / 100 - 1)
    lr = np.log(close[1:] / close[:-1])
    assert ct.out_fwd_vol(w, 3)[0] == pytest.approx(np.std(lr[0:3], ddof=1))
    te = ct.out_trend_ends(w, 2)          # t=2: past 99/100<0, fwd 100/99>0 -> ends
    assert te[2] == 1.0 and np.isnan(te[0])
    assert te[3] == 0.0                   # past 121/110>0, fwd 130/121>0 -> continues


# --- baselines ----------------------------------------------------------------------

def test_baseline_placebo_planted_and_null():
    planted_and_null(spec(EVENT, baseline={"kind": "placebo", "n_draws": 10}),
                     LOW_FC(0.02), LOW_FC(0.0), 9)


def test_baseline_other_selector_planted_and_null():
    other = {"kind": "other_selector",
             "selector": {"kind": "event", "field": "forecast", "op": ">=", "value": 8}}
    planted_and_null(spec(EVENT, baseline=other), LOW_FC(0.02), LOW_FC(0.0), 10)


def test_baseline_complement_is_valid_and_not_selected():
    w = make_windows(11, n_windows=1)[0]
    mask, valid = ct.sel_event(w, EVENT)
    wref = ct.base_complement(w, mask, valid, {}, 1, None)
    assert np.array_equal(wref > 0, valid & ~mask)


def test_placebo_shifts_skip_whole_calendar_periods():
    assert ct._calendar_period({"kind": "calendar", "hours": [1]}, HOUR) == 24
    assert ct._calendar_period({"kind": "calendar", "weekdays": [5]}, HOUR) == 168
    assert ct._calendar_period({"kind": "calendar", "weekdays": [5]}, DAY) == 7
    assert ct._calendar_period(EVENT, HOUR) is None
    k = ct._shift_offsets(500, 1, np.random.default_rng(0), 5000, period=24)
    assert not np.any(k % 24 == 0) and k.min() >= 2
    k = ct._shift_offsets(120, 5, np.random.default_rng(0), 5000)
    assert k.min() == 6 and k.max() == 114
    with pytest.raises(ValueError, match="too short"):
        ct._shift_offsets(11, 5, np.random.default_rng(0), 1)


# --- statistics -------------------------------------------------------------------------

def test_statistic_hit_rate_planted_and_null():
    planted_and_null(spec(EVENT, statistic="hit_rate"), LOW_FC(0.02), LOW_FC(0.0), 12)


def test_statistic_decay_curve_planted_and_null():
    s = spec(EVENT, statistic="decay_curve",
             outcome={"kind": "fwd_return", "horizons": [1, 2, 3]})
    res = rt(make_windows(13, plant=LOW_FC(0.02)), s)
    assert res["status"] == "supported" and res["peak_horizon"] in (1, 2, 3)
    assert status(make_windows(13, plant=LOW_FC(0.0)), s) != "supported"


def test_direction_less_detects_a_planted_drop():
    res = rt(make_windows(14, plant=HIGH_FC(-0.02)), spec(EVENT_HIGH, direction="less"))
    assert res["status"] == "supported"
    assert res["horizons"][1]["value"] < 0 < res["horizons"][1]["oriented"]
    up = rt(make_windows(14, plant=HIGH_FC(-0.02)), spec(EVENT_HIGH, direction="greater"))
    assert up["status"] == "refuted"
    assert up["horizons"][1]["p_value_opposite"] < 0.05


def test_rank_average_matches_signal_statistics_spearman():
    rng = np.random.default_rng(15)
    for _ in range(20):
        x = rng.integers(0, 8, 60).astype(float)          # many ties
        y = rng.normal(size=60) + 0.3 * x
        assert ct.spearman(x, y) == pytest.approx(spearman_correlation(list(x), list(y)))
    assert np.isnan(ct.spearman(np.ones(10), np.arange(10.)))


def test_null_p_values_are_spread_sanely_over_seeds():
    """No edge: p should be roughly uniform (the full gate is the calibration)."""
    ps = [rt(make_windows(100 + k, n=200, n_windows=3), spec(EVENT))
          ["horizons"][1]["p_value"] for k in range(20)]
    assert 0.3 < float(np.mean(ps)) < 0.7
    assert sum(p < 0.05 for p in ps) <= 4


# --- the null --------------------------------------------------------------------------

def test_fake_window_rebuilds_from_real_units_and_recomputes_the_signal():
    w = make_windows(16, n_windows=1)[0]
    f = ct.fake_window(w, np.random.default_rng(0))
    assert np.array_equal(f.ts, w.ts) and f.step == w.step
    prev = np.r_[w.warm["close"][-1], w.close[:-1]]
    real_units = np.round(np.log(w.close / prev), 12)
    fprev = np.r_[w.warm["close"][-1], f.close[:-1]]
    assert set(np.round(np.log(f.close / fprev), 12)) <= set(real_units)
    expected = ct.compute_signal(DON, *ct._full_path(w, f.close, f.high, f.low))[-len(w.ts):]
    assert np.allclose(f.forecast, expected, equal_nan=True)
    assert not np.allclose(f.close, w.close)


def test_fake_windows_use_blocks_of_the_cadence():
    assert ct.BLOCK_BARS == {"daily": 5, "hourly": 24}
    assert ct.WARMUP_BARS == {"daily": 30, "hourly": 500}
    with pytest.raises(ValueError, match="unsupported bar step"):
        ct._cadence(900)


def test_forecast_check_stops_a_grade_when_the_saved_forecast_differs():
    ws = make_windows(17, n_windows=2)
    assert ct.forecast_check(ws[0]) == 0.0
    ws[1].forecast[50] += 0.5
    with pytest.raises(ValueError, match="recomputed forecast differs"):
        rt(ws, spec(EVENT))


def test_null_needs_signal_and_warmup():
    w = make_windows(18, n_windows=1)[0]
    w.warm = None
    with pytest.raises(ValueError, match="needs the window's signal and warm-up"):
        rt([w], spec(EVENT))


def test_every_horizon_must_pass():
    # +2% on bar t+1, then -2% on bar t+2: h=1 gains 2%, h=2 nets about 0.
    ws = make_windows(19, plant=lambda t, fc, ts: ([0.02, -0.02] if fc <= -8 else 0.0, 1.0))
    one = rt(ws, spec(EVENT, outcome={"kind": "fwd_return", "horizons": [1]}))
    assert one["status"] == "supported"
    both = rt(ws, spec(EVENT, outcome={"kind": "fwd_return", "horizons": [1, 2]}))
    assert both["horizons"][1]["p_value"] < 0.05
    assert both["horizons"][2]["p_value"] >= 0.05
    assert both["status"] != "supported"
    assert both["reasons"] and all(r.startswith("h=2") for r in both["reasons"])


def test_a_weak_later_horizon_makes_it_inconclusive():
    # +2% then -1.7%: h=1 strong; h=2 still the right way (+0.3%) but weak.
    ws = make_windows(40, plant=lambda t, fc, ts: ([0.02, -0.017] if fc <= -8 else 0.0, 1.0))
    res = rt(ws, spec(EVENT, outcome={"kind": "fwd_return", "horizons": [1, 2]}))
    h = res["horizons"]
    assert h[1]["p_value"] < 0.05 and h[2]["oriented"] > 0 and h[2]["p_value"] >= 0.05
    assert res["status"] == "inconclusive"
    assert res["reasons"] == [r for r in res["reasons"] if r.startswith("h=2: right direction")]


def test_opposite_p_equals_the_opposite_spec_p():
    ws = make_windows(41)                  # no effect: the real value sits inside the null
    for stat in ("mean_diff", "rank_ic", "hit_rate"):
        sel = {"kind": "all"} if stat == "rank_ic" else EVENT
        g = rt(ws, spec(sel, statistic=stat, direction="greater"))["horizons"][1]
        lo = rt(ws, spec(sel, statistic=stat, direction="less"))["horizons"][1]
        assert 0.05 < g["p_value"] < 0.95, (stat, g["p_value"])
        assert g["p_value_opposite"] == lo["p_value"] and lo["p_value_opposite"] == g["p_value"]


def test_fake_worlds_permute_whole_blocks_without_replacement():
    w = make_windows(42, n=203, n_windows=1)[0]       # 203 = 40 blocks of 5 + a short one
    f = ct.fake_window(w, np.random.default_rng(1))
    prev = np.r_[w.warm["close"][-1], w.close[:-1]]
    real = np.log(w.close / prev)
    fprev = np.r_[w.warm["close"][-1], f.close[:-1]]
    fake = np.log(f.close / fprev)
    n = 203
    src = np.array([int(np.argmin(np.abs(real - u))) for u in fake])   # units are distinct
    assert sorted(src) == list(range(n))             # each real unit used exactly once
    # Blocks: runs of consecutive real units; exactly one run is the short block.
    runs, cur = [], 1
    for i in range(1, n):
        if (src[i] - src[i - 1]) % n == 1:
            cur += 1
        else:
            runs.append(cur)
            cur = 1
    runs.append(cur)
    assert sum(runs) == n and max(runs) <= 2 * ct.BLOCK_BARS["daily"]
    # The random phase: block starts are not all multiples of 5 across draws.
    starts = set()
    for seed in range(10):
        g = ct.fake_window(w, np.random.default_rng(seed))
        gprev = np.r_[w.warm["close"][-1], g.close[:-1]]
        first = int(np.argmin(np.abs(real - np.log(g.close / gprev)[0])))
        starts.add(first % ct.BLOCK_BARS["daily"])
    assert len(starts) > 1


def test_verdict_rule_amendment_3():
    """refuted only when the wrong-way effect is itself significant; a weak
    wrong-way wobble is inconclusive; supported = right way, p < alpha everywhere."""
    wrong = rt(make_windows(20, plant=HIGH_FC(-0.02)), spec(EVENT_HIGH))
    assert wrong["status"] == "refuted" and "opposite direction" in wrong["reasons"][0]
    wobble = rt(make_windows(20, plant=HIGH_FC(-0.0005)), spec(EVENT_HIGH))
    h = wobble["horizons"][1]
    assert h["oriented"] < 0 and h["p_value_opposite"] >= 0.05
    assert wobble["status"] == "inconclusive"
    assert "wrong direction or zero, not significant" in wobble["reasons"][0]
    good = rt(make_windows(20, plant=LOW_FC(0.02)), spec(EVENT))
    assert good["status"] == "supported" and good["reasons"] == []


def test_right_direction_not_significant_is_inconclusive():
    ws = make_windows(21, plant=LOW_FC(0.02))
    res = rt(ws, ct.TestSpec(**{**spec(EVENT).__dict__, "alpha": 0.0101}))
    assert res["status"] == "supported"     # p = 0.01 with 99 fakes and no fake beats it
    res = rt(ws, ct.TestSpec(**{**spec(EVENT).__dict__, "alpha": 0.01}))
    assert res["status"] == "inconclusive"
    assert res["reasons"][0].startswith("h=1: right direction, p")


# --- no lookahead ------------------------------------------------------------------------

LOOKAHEAD_SELECTORS = [
    EVENT, {"kind": "event", "field": "close", "op": ">", "value": 100},
    {"kind": "all"}, {"kind": "regime", "values": ["trend"]},
    {"kind": "regime_change", "to": "range"},
    {"kind": "calendar", "weekdays": [5, 6], "hours": [0, 12]},
    {"kind": "quantile", "field": "forecast", "side": "top", "q": 0.2, "lookback": 30},
    {"kind": "quantile", "field": "close", "side": "bottom", "q": 0.1, "lookback": 20},
]


@pytest.mark.parametrize("sel", LOOKAHEAD_SELECTORS, ids=lambda s: s["kind"])
def test_selector_never_reads_the_future(sel):
    w = make_windows(22, n_windows=1)[0]
    mask, valid = ct.SELECTORS[sel["kind"]](w, sel)
    rng = np.random.default_rng(23)
    for t in (40, 150, 233, len(w.ts) - 2):
        k = len(w.ts) - t - 1
        fut = ct.Window(w.symbol, w.window, w.ts.copy(), w.close.copy(), w.forecast.copy(),
                        w.regime.copy(), w.step)
        fut.close[t + 1:] = rng.uniform(1, 1000, k)
        fut.forecast[t + 1:] = rng.uniform(-20, 20, k)
        fut.regime[t + 1:] = rng.choice(["trend", "range", "z"], k)
        m2, v2 = ct.SELECTORS[sel["kind"]](fut, sel)
        assert np.array_equal(mask[:t + 1], m2[:t + 1]), t
        assert np.array_equal(valid[:t + 1], v2[:t + 1]), t


def test_quantile_is_trailing_not_whole_sample():
    w = make_windows(24, n_windows=1)[0]
    sel = {"kind": "quantile", "field": "forecast", "side": "top", "q": 0.2, "lookback": 30}
    mask, valid = ct.sel_quantile(w, sel)
    assert not valid[:30].any() and valid[30:].all()
    x = w.forecast
    expected = [x[t] >= np.quantile(x[t - 30:t], 0.8) for t in range(30, len(x))]
    assert np.array_equal(mask[30:], np.array(expected))


def test_check_spec_refuses_a_future_field():
    for field in ("fwd_return", "portfolio_value", "next_close", "high"):
        for sel in ({"kind": "event", "field": field, "op": ">", "value": 0},
                    {"kind": "quantile", "field": field, "side": "top", "q": 0.2, "lookback": 5}):
            errs = ct.check_spec(spec(sel))
            assert any("not a bar-t field" in e for e in errs), (field, errs)
            with pytest.raises(ValueError, match="bar-t field"):
                rt(make_windows(0, n_windows=1), spec(sel))


# --- timestamp matching, inside a window only ---------------------------------------------

def test_outcomes_never_cross_a_window_boundary():
    a, b = make_windows(25, n=100, n_windows=2)
    for fn in ct.OUTCOMES.values():
        assert np.all(np.isnan(fn(a, 5)[-5:]))
    s = spec({"kind": "all"}, statistic="rank_ic",
             outcome={"kind": "fwd_return", "horizons": [5]}, floor={"min_events": 1})
    assert rt([a, b], s)["horizons"][5]["n_events"] == 2 * (100 - 5)


def test_outcomes_match_by_timestamp_across_a_missing_bar():
    ts = (T0 + np.r_[0, 1, 2, 4, 5, 6, 7] * HOUR).astype(np.int64)    # hour 3 missing
    close = np.array([100., 101., 102., 104., 105., 106., 107.])
    w = ct.Window("S", "w", ts, close, np.zeros(7), np.array(["x"] * 7, dtype=object), HOUR)
    y = ct.out_fwd_return(w, 2)
    assert np.isnan(y[1])                          # 01:00 + 2h = 03:00 is missing
    assert y[2] == pytest.approx(104 / 102 - 1)    # 02:00 + 2h = 04:00 (row 3)
    assert y[0] == pytest.approx(102 / 100 - 1)
    assert np.isnan(ct.out_fwd_mdd(w, 2)[2])       # path (02:00, 04:00] has a hole
    assert np.isnan(ct.out_fwd_vol(w, 3)[1])
    assert ct.out_fwd_mdd(w, 2)[3] == pytest.approx(105 / 104 - 1)
    assert np.isnan(ct.out_trend_ends(w, 2)[4])    # 05:00 - 2h = 03:00 missing


# --- floors and consistency ---------------------------------------------------------------

ERAS = [{"era_id": "e1", "range": ["2020-01-01", "2020-12-31"]},
        {"era_id": "e2", "range": ["2021-01-01", "2023-12-31"]}]


@pytest.mark.parametrize("floor", [{"min_events": 10**6}, {"min_windows": 7},
                                   {"min_blocks": 10**5}, {"min_eras": 3}])
def test_floor_gives_inconclusive(floor):
    res = rt(make_windows(26, plant=LOW_FC(0.03)), spec(EVENT, floor=floor), ERAS)
    assert res["status"] == "inconclusive"
    assert any("floor" in r for r in res["reasons"])


def test_eras_needed_but_missing_raises():
    with pytest.raises(ValueError, match="needs eras"):
        rt(make_windows(0, n_windows=1), spec(EVENT, floor={"min_eras": 1}))


def test_window_consistency_rule():
    ws = make_windows(27, plant=LOW_FC(0.02))
    ok = spec(EVENT, consistency={"unit": "window", "min_same_sign": 4})
    assert status(ws, ok) == "supported"
    res = rt(ws, spec(EVENT, consistency={"unit": "window", "min_same_sign": 5}))
    assert res["status"] == "inconclusive" and "same sign in 4 windows" in res["reasons"][0]


def test_per_era_values_reported():
    res = rt(make_windows(28, plant=LOW_FC(0.02)), spec(EVENT), ERAS)
    assert set(res["horizons"][1]["per_era"]) <= {"e1", "e2"}
    assert res["horizons"][1]["n_eras_with_events"] == 2


# --- spec -----------------------------------------------------------------------------------

def test_spec_hash_stable_and_order_independent():
    a = spec(EVENT, outcome={"kind": "fwd_return", "horizons": [1, 2, 3]})
    b = spec({"value": -8.0, "op": "<=", "field": "forecast", "kind": "event"},
             outcome={"horizons": [3, 1, 2], "kind": "fwd_return"})
    assert ct.spec_hash(a) == ct.spec_hash(b) == ct.spec_hash(a)
    assert len(ct.spec_hash(a)) == 64
    assert ct.spec_hash(spec(EVENT, direction="less")) != ct.spec_hash(spec(EVENT))
    assert ct.spec_hash(spec(EVENT, floor={"min_events": 21})) != ct.spec_hash(spec(EVENT))


def test_check_spec_rejects_bad_slots():
    bad = [
        spec({"kind": "nope"}),
        spec(EVENT, outcome={"kind": "fwd_return", "horizons": []}),
        spec(EVENT, outcome={"kind": "fwd_volatility", "horizons": [1]}),
        spec(EVENT, statistic="rank_ic", baseline={"kind": "complement"}),
        spec(EVENT, baseline={"kind": "nope"}),
        spec(EVENT, direction="up"),
        spec(EVENT, floor={"min_trades": 3}),
        spec(EVENT, consistency={"unit": "year", "min_same_sign": 2}),
        ct.TestSpec(EVENT, {"kind": "fwd_return", "horizons": [1]}, {"kind": "complement"},
                    "mean_diff", "greater", {"min_events": 1},
                    significance={"method": "circular_shift_v1", "n_resamples": 999, "seed": 1}),
        ct.TestSpec(EVENT, {"kind": "fwd_return", "horizons": [1]}, {"kind": "complement"},
                    "mean_diff", "greater", {"min_events": 1},
                    significance={"method": "block_analytic_v1"}),
        ct.TestSpec(EVENT, {"kind": "fwd_return", "horizons": [1]}, {"kind": "complement"},
                    "mean_diff", "greater", {"min_events": 1},
                    significance={"method": "bootstrap_null_v1", "n_resamples": 999, "seed": 1}),
        ct.TestSpec(EVENT, {"kind": "fwd_return", "horizons": [1]}, {"kind": "complement"},
                    "mean_diff", "greater", {"min_events": 1},
                    significance={"method": "a851a_episode_v1", "seed": 3}),
    ]
    for s in bad:
        assert ct.check_spec(s), s
    assert ct.check_spec(spec(EVENT)) == []
    with pytest.raises(ValueError, match="unknown spec keys"):
        ct.TestSpec.from_dict({"selector": EVENT, "outcome": {}, "baseline": None,
                               "statistic": "mean_diff", "direction": "greater",
                               "floor": {}, "pass_if": "x"})


def test_registries_and_exercised_markers():
    assert len(ct.SELECTORS) + len(ct.OUTCOMES) + len(ct.BASELINES) + len(ct.STATISTICS) == 17
    every = ({f"selector:{k}" for k in ct.SELECTORS} | {f"outcome:{k}" for k in ct.OUTCOMES}
             | {f"baseline:{k}" for k in ct.BASELINES} | {f"statistic:{k}" for k in ct.STATISTICS})
    assert ct.EXERCISED_ON_REAL_RUNS <= every


def test_pre_registered_regrade_specs_are_valid():
    d = SR_ROOT / "engineering" / "roadmap" / "E-068" / "regrade_specs"
    files = sorted(d.glob("*.yaml"))
    assert len(files) == 2
    n = 0
    for f in files:
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        assert ct.check_claim_file(doc, Path(doc["source_run"])) == []
        for t in doc["tests"]:
            assert ct.check_spec(ct.TestSpec.from_dict(t)) == [], (f.name, t["name"])
            n += 1
    assert n == 3


def test_check_claim_file_refuses_rules_it_would_ignore():
    base = {"claim_id": "c", "source_run": "run_x", "tests": [{"name": "a"}]}
    assert ct.check_claim_file(base, Path("run_x")) == []
    assert ct.check_claim_file({**base, "combine": "any_supported"}, Path("run_x"))
    assert ct.check_claim_file({**base, "across_variants": "average"}, Path("run_x"))
    assert ct.check_claim_file(base, Path("run_y"))
    assert ct.check_claim_file({**base, "pass_if": "x"}, Path("run_x"))
    assert ct.check_claim_file({**base, "tests": [{"name": "a"}, {"name": "a"}]}, Path("run_x"))


# --- signals: the vectorized copies equal the components' update() --------------------------

@pytest.mark.parametrize("cls,params", [
    ("DonchianBreakoutComponent", {"period": 20, "scaling_factor": 20.0}),
    ("DonchianBreakoutComponent", {"period": 14, "scaling_factor": 20.0}),
    ("KeltnerBreakoutComponent", {"ema_period": 20, "atr_period": 20, "atr_multiplier": 2.0,
                                  "scaling_factor": 20.0}),
    ("KeltnerBreakoutComponent", {"ema_period": 26, "atr_period": 20, "atr_multiplier": 2.0,
                                  "scaling_factor": 20.0}),
])
def test_vectorized_signal_equals_component_update(cls, params):
    from strategies import strategy_components as sc
    rng = np.random.default_rng(29)
    n = 90
    c = 100 * np.exp(np.cumsum(rng.normal(0, .02, n)))
    o = np.r_[100, c[:-1]]
    h, lo = np.maximum(o, c) * 1.004, np.minimum(o, c) * 0.996
    df = pd.DataFrame({"open": o, "high": h, "low": lo, "close": c, "volume": 1.0})
    comp = getattr(sc, cls)(parameters=dict(params))
    got = []
    for t in range(n):
        comp.update(df.iloc[:t + 1])
        got.append(comp._raw_value if comp.is_ready() else np.nan)
    vec = ct.SIGNALS[cls](h, lo, c, **params)
    assert np.array_equal(np.isnan(np.array(got, float)), np.isnan(vec))
    assert np.nanmax(np.abs(np.array(got, float) - vec)) < 1e-9


# --- loader, warm-up reader and CLI ---------------------------------------------------------

def _write_cache(path: Path, start_ts: int, n: int, step: int, garbage_after: int | None = None):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        for i in range(n):
            t = start_ts + i * step
            if garbage_after is not None and t >= garbage_after:
                wr.writerow(["NOT-A-DATE", "x", "x", "x", "x", "x"])
                continue
            s = pd.Timestamp(t, unit="s").strftime("%Y-%m-%d %H:%M:%S")
            c = 100 + (i % 7)
            wr.writerow([s, c, c + 1, c - 1, c, 1])


def test_read_warmup_stops_at_the_window_and_checks_gaps(tmp_path):
    p = tmp_path / "c.csv"
    first = T0 + 40 * DAY
    # The row AT `first` must be read to know where to stop; every row after it
    # is unparseable, so reaching any of them would raise.
    _write_cache(p, T0, 60, DAY, garbage_after=first + DAY)
    wu = ct.read_warmup(p, first, DAY, 30)
    assert len(wu["close"]) == 30 and wu["ts"][-1] == first - DAY
    with pytest.raises(ValueError, match="only 40 warm-up rows"):
        ct.read_warmup(p, first, DAY, 41)
    holed = tmp_path / "holed.csv"
    _write_cache(holed, T0, 20, DAY)
    with open(holed, "a", newline="", encoding="utf-8") as f:   # day 20 missing
        csv.writer(f).writerow([pd.Timestamp(T0 + 21 * DAY, unit="s").strftime("%Y-%m-%d"),
                                1, 2, 0, 1, 1])
    with pytest.raises(ValueError, match="gap-free"):
        ct.read_warmup(holed, T0 + 22 * DAY, DAY, 10)


def _write_run(root: Path, windows: list, signal: dict, extra_component=False):
    run = root / "run_x"
    for vid in ("base", "broken"):
        (run / "artifacts" / "variants" / vid).mkdir(parents=True)
    comps = [{"id": "c", "class": "strategies.strategy_components." + signal["class"],
              "params": signal["params"], "weight": 1.0, "transforms": [{"op": "identity"}]}]
    if extra_component:
        comps.append(dict(comps[0], id="d"))
    (run / "artifacts" / "variants" / "base" / "strategy_config.json").write_text(
        json.dumps({"strategies": {"regimes": {"unknown": {"components": comps}}}}))
    results = []
    for i, w in enumerate(windows):
        d = run / "variants" / "base" / "results" / f"r{i}"
        d.mkdir(parents=True)
        with open(d / "bars.csv", "w", newline="", encoding="utf-8") as f:
            wr = csv.writer(f)
            wr.writerow(["timestamp", "high", "low", "close", "forecast", "regime"])
            for t in range(len(w.ts)):
                wr.writerow([pd.Timestamp(int(w.ts[t]), unit="s").strftime("%Y-%m-%d %H:%M:%S"),
                             repr(float(w.high[t])), repr(float(w.low[t])), repr(float(w.close[t])),
                             repr(float(w.forecast[t])), "unknown"])
        results.append({"symbol": "SYNUSD", "window": w.window, "run_id": f"r{i}"})
    with open(run / "artifacts" / "variants" / "base" / "protocol_result.yaml", "w") as f:
        yaml.safe_dump({"results": results}, f)
    return run


def _write_cache_for(root: Path, windows: list) -> Path:
    cdir = root / "cache"
    cdir.mkdir()
    with open(cdir / "kraken_SYNUSD_1d.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        for w in windows:
            for t in range(len(w.warm["ts"])):
                wr.writerow([pd.Timestamp(int(w.warm["ts"][t]), unit="s").strftime("%Y-%m-%d"),
                             0, repr(float(w.warm["high"][t])), repr(float(w.warm["low"][t])),
                             repr(float(w.warm["close"][t])), 1])
            for t in range(len(w.ts)):
                wr.writerow([pd.Timestamp(int(w.ts[t]), unit="s").strftime("%Y-%m-%d"),
                             0, repr(float(w.high[t])), repr(float(w.low[t])), repr(float(w.close[t])), 1])
    return cdir


def test_loader_attaches_signal_and_warmup(tmp_path):
    ws = make_windows(30, n=80, n_windows=2)
    run = _write_run(tmp_path, ws, DON)
    cdir = _write_cache_for(tmp_path, ws)
    graded, not_graded = ct.graded_variants(run)
    assert graded == ["base"] and not_graded == ["broken"]
    got = ct.load_variant_bars(run, "base", ct.cache_resolver(cdir, "kraken_{symbol}_{tf}.csv"))
    assert [w.label for w in got] == ["SYNUSD/w0", "SYNUSD/w1"]
    assert got[0].signal == DON and len(got[0].warm["close"]) == ct.WARMUP_BARS["daily"]
    assert np.allclose(got[0].warm["close"], ws[0].warm["close"])
    assert ct.forecast_check(got[0]) < 1e-9 and len(got[0].sha256) == 64
    (run / "variants" / "base" / "results" / "r1" / "bars.csv").unlink()
    with pytest.raises(FileNotFoundError):
        ct.load_variant_bars(run, "base")


def test_variant_signal_refuses_what_it_cannot_recompute(tmp_path):
    ws = make_windows(31, n=60, n_windows=1)
    run = _write_run(tmp_path, ws, DON, extra_component=True)
    with pytest.raises(ValueError, match="2 components"):
        ct.variant_signal(run, "base")
    p = run / "artifacts" / "variants" / "base" / "strategy_config.json"
    cfg = json.loads(p.read_text())
    comps = cfg["strategies"]["regimes"]["unknown"]["components"]
    cfg["strategies"]["regimes"]["unknown"]["components"] = [dict(comps[0], transforms=[{"op": "tanh"}])]
    p.write_text(json.dumps(cfg))
    with pytest.raises(ValueError, match="identity"):
        ct.variant_signal(run, "base")
    cfg["strategies"]["regimes"]["unknown"]["components"] = [dict(comps[0], **{"class": "a.B"})]
    p.write_text(json.dumps(cfg))
    with pytest.raises(ValueError, match="no vectorized copy"):
        ct.variant_signal(run, "base")


def test_cli_end_to_end_and_refusals(tmp_path):
    ws = make_windows(32, n=80, n_windows=2)
    run = _write_run(tmp_path, ws, DON)
    cdir = _write_cache_for(tmp_path, ws)
    sp = tmp_path / "spec.yaml"
    sp.write_text(yaml.safe_dump({"claim_id": "c", "source_run": "run_x", "tests": [
        {"name": "t", "selector": {"kind": "all"},
         "outcome": {"kind": "fwd_return", "horizons": [1]}, "baseline": None,
         "statistic": "rank_ic", "direction": "greater", "floor": {"min_events": 10**6},
         "significance": dict(FAST)}]}))
    out = tmp_path / "out" / "r.yaml"
    args = ["--run", str(run), "--spec", str(sp), "--cache-dir", str(cdir)]
    assert ct.main(args + ["--out", str(out)]) == 0
    doc = yaml.safe_load(out.read_text())
    assert doc["n_tests_run"] == 0                       # nothing graded without a gate
    assert doc["not_graded_variants"] == ["broken", "base (no passed calibration for its signal)"]
    assert doc["variants"]["base"]["tests"]["t"]["status"] == "method_not_calibrated"
    assert doc["claim_status"] == "method_not_calibrated" and doc["calibrations_passed"] == []
    calib = tmp_path / "calib.yaml"
    calib.write_text(yaml.safe_dump(passed_summary(DON, "rank_ic", selector=[{"kind": "all"}])))
    assert ct.main(args + ["--out", str(out), "--calibration", str(calib)]) == 0
    doc = yaml.safe_load(out.read_text())
    assert doc["variants"]["base"]["tests"]["t"]["status"] == "inconclusive"   # floor not met
    assert doc["n_tests_run"] == 1 and doc["graded_variants"] == ["base"]
    assert len(doc["bars_used"]) == 2 and all(len(b["sha256"]) == 64 for b in doc["bars_used"])
    with pytest.raises(SystemExit, match="inside the run"):
        ct.main(args + ["--out", str(run / "x.yaml")])
    sealed = tmp_path / "holdout_sealed"
    sealed.mkdir()
    with pytest.raises(SystemExit, match="holdout"):
        ct.main(["--run", str(run), "--spec", str(sp), "--cache-dir", str(sealed),
                 "--out", str(out)])


def test_combine_fail_dominates():
    assert ct.combine(["supported", "inconclusive", "refuted"]) == "refuted"
    assert ct.combine(["supported", "inconclusive"]) == "inconclusive"
    assert ct.combine(["supported", "supported"]) == "supported"
    assert ct.combine([]) == "not_graded"


# --- calibration tool -----------------------------------------------------------------------

def test_calibration_tool_runs_cells_and_summarizes(tmp_path):
    cells = [cal.run_cell(ct.SIGNIFICANCE_METHOD, "switching", side, n_sims=2)
             for side in ("upper", "lower")]
    assert [r["row"] for r in cells[0]["rows"]] == ["switching_upper_claimed",
                                                    "switching_upper_opposite"]
    summ = cal.summarize(ct.SIGNIFICANCE_METHOD, cells)
    assert summ["all_pass"] is False                     # 4 of 8 rows only: never a pass
    assert summ["gate"] == {"alpha": 0.05, "ceiling": 0.075, "floor_warning": 0.025,
                            "max_share_undefined": 0.05, "rule": "one_sided"}
    assert summ["scope"]["signal"] == cal.DONCHIAN and summ["scope"]["cadence"] == "daily"
    assert summ["code_sha256"] == cal.code_sha256() and len(summ["code_sha256"]) == 64
    mixed = [dict(cells[0], code_sha256="a" * 64), cells[1]]
    assert cal.summarize(ct.SIGNIFICANCE_METHOD, mixed)["code_sha256"] is None
    w = cal.simulate_windows(np.random.default_rng(0), "switching")
    assert ct.forecast_check(w[0]) == 0.0 and len(w[0].warm["close"]) == 30
    assert all(w[i + 1].ts[0] - w[i].ts[-1] == DAY for i in range(5))   # windows abut


def test_a851a_has_too_few_episodes_on_the_run065_layout_for_the_right_reason():
    """A8.5.1a's no-answer on the gate layout is its own episode rule (gap_bars
    = 48 bars = 48 days on daily data), not a feeding bug: the episode count is
    below 8 with and without eras, and an hourly-scale gap would give many."""
    import episode_significance as es
    ws = cal.simulate_windows(np.random.default_rng(3), "iid")
    s = cal.cell_spec(ct.A851A_METHOD, "upper", 0)
    per = ct._prepare(ws, s, [1], np.random.default_rng(0))
    for p in per:
        p["eras_list"] = None
    a = ct._a851a_horizon(per, 1)
    assert a["method_label"] == "episode_bootstrap_insufficient_n" and a["n_episodes"] < 8
    for p in per:
        p["eras_list"] = [{"era_id": "one", "range": ["2019-01-01", "2025-12-31"]}]
    assert ct._a851a_horizon(per, 1)["n_episodes"] == a["n_episodes"]
    act = np.concatenate([p["mask"] for p in per])
    recs = [{"active": bool(x)} for x in act]
    assert len(es.identify_episodes(recs, gap_bars=2)) >= 8


def test_calibration_counts_undefined_honestly():
    """A8.5.1a on run_065's daily layout: too few episodes, so no p at all --
    counted as undefined (and failing), never as 'no false edge'."""
    c = cal.run_cell(ct.A851A_METHOD, "iid", "upper", n_sims=2)
    for r in c["rows"]:
        assert r["share_undefined"][1] == 1.0
        assert r["share_p_below_0_05_of_defined"][1] is None and r["pass"] is False


# --- operator rule 3: no verdict without a passed gate --------------------------------------

def test_uncalibrated_method_gives_effect_sizes_and_no_verdict():
    res = ct.run_test(make_windows(50, plant=LOW_FC(0.02)), spec(EVENT))
    assert res["status"] == "method_not_calibrated"
    assert "verdict: method not calibrated" in res["reasons"][0]
    h = res["horizons"][1]
    assert h["value"] > 0 and h["p_value"] is None and h["p_value_opposite"] is None
    assert ct.combine(["supported", "method_not_calibrated"]) == "method_not_calibrated"
    assert ct.combine(["refuted", "method_not_calibrated"]) == "method_not_calibrated"


def gate_row(name, shares=None, undefined=0.0, ok=True, n_sims=ct.CALIBRATION_N_SIMS):
    shares = shares or {h: 0.05 for h in range(1, 6)}
    return {"row": name, "pass": ok, "n_sims": n_sims, "share_p_below_0_05_of_defined": shares,
            "share_undefined": {h: undefined for h in shares}}


def passed_summary(signal, statistic, method=None, selector=None, outcome="fwd_return",
                   n_null=None, **over):
    method = method or ct.SIGNIFICANCE_METHOD
    if selector is None:
        selector = [dict(EVENT)]          # the exact selector(s) the gate simulated
    if n_null is None:
        n_null = (ct.A851A_SETTINGS["n_resamples"] if method in ct.A851A_METHODS
                  else FAST["n_resamples"])
    doc = {"method": method, "gate": dict(ct.CALIBRATION_GATE),
           "scope": {"signal": signal, "cadence": "daily", "statistic": statistic,
                     "selector": selector, "outcome": outcome, "n_null": n_null},
           "code_sha256": "f" * 64, "all_pass": True,
           "rows": [gate_row(f"r{i}") for i in range(ct.CALIBRATION_ROWS)]}
    doc.update(over)
    return doc


def test_calibration_lock_needs_a_full_passed_gate_for_this_exact_test(tmp_path):
    ws = make_windows(53, n=60, n_windows=1)
    s = spec(EVENT)
    files = {}
    cases = {
        "good": passed_summary(DON, "mean_diff"),
        "two_keys": {"method": ct.SIGNIFICANCE_METHOD, "all_pass": True},
        "failed": passed_summary(DON, "mean_diff", all_pass=False),
        "row_failed": passed_summary(DON, "mean_diff", rows=[{"pass": False}] * 8),
        "few_rows": passed_summary(DON, "mean_diff", rows=[{"pass": True}] * 4),
        "short_gate": passed_summary(DON, "mean_diff", rows=[
            gate_row(f"r{i}", n_sims=5) for i in range(8)]),
        "copied_rows": passed_summary(DON, "mean_diff", rows=[gate_row("same")] * 8),
        "other_gate": passed_summary(DON, "mean_diff", gate={**ct.CALIBRATION_GATE, "alpha": 0.1}),
        "no_hash": passed_summary(DON, "mean_diff", code_sha256=None),
    }
    for k, doc in cases.items():
        files[k] = tmp_path / f"{k}.yaml"
        files[k].write_text(yaml.safe_dump(doc))
    passed = ct.passed_calibrations(list(files.values()))
    assert [c["file"] for c in passed] == [str(files["good"])]
    assert ct.calibration_for(passed, s, ws)["file"] == str(files["good"])
    other_signal = {**DON, "params": {**DON["params"], "period": 14}}
    for doc in (passed_summary(other_signal, "mean_diff"), passed_summary(DON, "hit_rate"),
                passed_summary(DON, "mean_diff", method=ct.A851A_METHOD),
                {**passed_summary(DON, "mean_diff"),
                 "scope": {**passed_summary(DON, "mean_diff")["scope"], "cadence": "hourly"}}):
        only = tmp_path / "only.yaml"
        only.write_text(yaml.safe_dump(doc))
        assert ct.calibration_for(ct.passed_calibrations([only]), s, ws) is None, doc
    assert ct.passed_calibrations([]) == []


# --- amendment 5: the gate is one-sided ---------------------------------------------------

def test_one_sided_row_rule_fails_flattering_and_warns_on_too_strict():
    j = ct.judge_calibration_row
    assert j(gate_row("x")) == (True, [])
    def h(**v):
        return {k: v.get(f"h{k}", 0.05) for k in range(1, 6)}
    assert j(gate_row("x", h(h1=0.075))) == (True, [])                      # ceiling inclusive
    assert j(gate_row("x", h(h1=0.0751)))[0] is False                       # flattering: fail
    assert j(gate_row("x", h(h1=0.025, h2=0.0225, h3=0.0))) == (True, [2, 3])  # too strict: warn
    assert j(gate_row("x", undefined=0.06))[0] is False                    # no answer: fail
    assert j(gate_row("x", h(h1=None)))[0] is False
    assert j(gate_row("x", {1: 0.05}))[0] is False                         # horizons 1-5 only
    assert j({"row": "x"})[0] is False                                      # no numbers: fail
    bad = gate_row("x")
    bad["share_undefined"] = {1: 0.0}                                       # horizons disagree
    assert j(bad)[0] is False


def test_lock_rejudges_rows_and_refuses_the_old_two_sided_gate(tmp_path):
    ws = make_windows(54, n=60, n_windows=1)
    s = spec(EVENT)
    cases = {
        # the row flag says pass, its numbers flatter: the lock trusts the numbers
        "flag_lies": passed_summary(DON, "mean_diff", rows=[
            gate_row(f"r{i}", {**{k: 0.05 for k in range(1, 6)}, 1: 0.08}) for i in range(8)]),
        "one_horizon": passed_summary(DON, "mean_diff", rows=[
            gate_row(f"r{i}", {1: 0.05}) for i in range(8)]),
        "old_gate": passed_summary(DON, "mean_diff", gate={
            "alpha": 0.05, "pass_range": [0.025, 0.075], "max_share_undefined": 0.05}),
        "strict": passed_summary(DON, "mean_diff", rows=[
            gate_row(f"r{i}", {**{k: 0.04 for k in range(1, 6)}, 1: 0.02 if i < 2 else 0.05})
            for i in range(8)]),
    }
    files = []
    for k, doc in cases.items():
        files.append(tmp_path / f"{k}.yaml")
        files[-1].write_text(yaml.safe_dump(doc))
    passed = ct.passed_calibrations(files)
    assert [Path(c["file"]).stem for c in passed] == ["strict"]
    assert passed[0]["conservative"] == {"r0": [1], "r1": [1]}
    assert ct.calibration_for(passed, s, ws) is passed[0]
    with pytest.raises(ValueError, match="more than one"):          # no choosing the label
        ct.calibration_for(passed + [dict(passed[0], file="twin")], s, ws)
    longer = spec(EVENT, outcome={"kind": "fwd_return", "horizons": [1, 6]})
    assert ct.calibration_for(passed, longer, ws) is None           # beyond the gate's horizons


def test_grade_reports_conservative_next_to_the_verdict(tmp_path):
    ws = make_windows(55, n=80, n_windows=2)
    run = _write_run(tmp_path, ws, DON)
    cdir = _write_cache_for(tmp_path, ws)
    sp = tmp_path / "spec.yaml"
    sp.write_text(yaml.safe_dump({"claim_id": "c", "source_run": "run_x", "tests": [
        {"name": "t", "selector": {"kind": "all"},
         "outcome": {"kind": "fwd_return", "horizons": [1]}, "baseline": None,
         "statistic": "rank_ic", "direction": "greater", "floor": {"min_events": 10**6},
         "significance": dict(FAST)}]}))
    res = ct.cache_resolver(cdir, "kraken_{symbol}_{tf}.csv")
    for rows, status in (([gate_row(f"r{i}") for i in range(8)], "pass"),
                         ([gate_row("r0", {**{k: 0.05 for k in range(1, 6)}, 1: 0.01})]
                          + [gate_row(f"r{i}") for i in range(1, 8)],
                          "conservative")):
        calib = tmp_path / f"calib_{status}.yaml"
        calib.write_text(yaml.safe_dump(passed_summary(DON, "rank_ic", selector=[{"kind": "all"}], rows=rows)))
        t = ct.grade_claim_file(run, sp, res, calibration_files=[calib])["variants"]["base"]["tests"]["t"]
        assert t["status"] == "inconclusive" and t["calibration_status"] == status
        assert t["calibration_conservative_cells"] == ({} if status == "pass" else {"r0": [1]})
    t = ct.grade_claim_file(run, sp, res, calibration_files=[])["variants"]["base"]["tests"]["t"]
    assert t["calibration_status"] is None and t["calibration_conservative_cells"] is None


E068 = Path(__file__).resolve().parents[1] / "engineering" / "roadmap" / "E-068"


def _cells(folder, prefix):
    return [yaml.safe_load(p.read_text(encoding="utf-8"))
            for p in sorted((E068 / folder).glob(f"{prefix}*.yaml"))]


def test_reevaluate_the_committed_shuffle_cells_under_the_one_sided_rule():
    """The existing method-B gate cells (amendment 3, no re-run) pass the
    one-sided rule; the four too-strict cells are the ones reported."""
    cells = _cells("calibration", "cell_block_permutation_v1_")
    assert len(cells) == 4 and not any(c.get("code_sha256") for c in cells)
    res = cal.reevaluate(ct.SIGNIFICANCE_METHOD, cells, {"f": "0" * 64}, "REF", "e" * 64)
    assert res["all_pass"] is True and res["code_sha256"] == "e" * 64
    assert res["scope"]["signal"] == cal.donchian(20) and res["reevaluated"]["rerun"] is False
    assert res["conservative"] == {"iid_lower_opposite": [1], "iid_upper_claimed": [2],
                                   "switching_lower_opposite": [4],
                                   "switching_upper_opposite": [2]}
    assert max(v for r in res["rows"] for v in r["share_p_below_0_05_of_defined"].values()) \
        <= ct.CALIBRATION_GATE["ceiling"]
    with pytest.raises(ValueError, match="own code hash"):
        cal.reevaluate(ct.SIGNIFICANCE_METHOD, [dict(cells[0], code_sha256="a" * 64)],
                       {}, "REF", "e" * 64)
    with pytest.raises(ValueError, match="Donchian"):
        cal.reevaluate(ct.SIGNIFICANCE_METHOD, [dict(cells[0], signal=cal.donchian(14))],
                       {}, "REF", "e" * 64)


def test_reevaluate_cli_reads_the_committed_cells_and_hashes_git_bytes(tmp_path):
    """bc4e67f4 produced the B cells; the CLI re-judges exactly those bytes."""
    import subprocess
    try:
        subprocess.run(["git", "-C", str(cal.REPO_ROOT), "cat-file", "-e", "bc4e67f4"], check=True,
                       capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.skip("history not available (shallow clone)")
    paths = sorted((E068 / "calibration").glob("cell_block_permutation_v1_*.yaml"))
    out = tmp_path / "s.yaml"
    assert cal.main(["reevaluate", "--method", ct.SIGNIFICANCE_METHOD, "--code-ref", "bc4e67f4",
                     "--out", str(out)] + [str(p) for p in paths]) == 0
    doc = yaml.safe_load(out.read_text())
    assert doc["all_pass"] is True and doc["code_sha256"] == cal.code_sha256_at("bc4e67f4")
    assert len(doc["reevaluated"]["cell_files_sha256"]) == 4
    edited = tmp_path / "x"
    with pytest.raises(ValueError):                                 # outside the repo: refused
        cal.committed_cells([edited], "bc4e67f4")


def test_one_sided_rule_does_not_rescue_the_other_methods():
    for folder, prefix in (("calibration", "cell_a851a_episode_v1_"),
                           ("calibration_a4", "cell_timegap_p20_"),
                           ("calibration_a4", "cell_timegap_p14_")):
        cells = _cells(folder, prefix)
        assert len(cells) == 4
        method = cells[0]["method"]
        stamped = [dict(c, code_sha256="e" * 64) for c in cells]
        assert cal.summarize(method, stamped)["all_pass"] is False, prefix


# --- method A: the existing A8.5.1a, fed unchanged ------------------------------------------

def test_a851a_wrapper_equals_a_direct_call_of_the_existing_method():
    import episode_significance as es
    n = 1200
    rng = np.random.default_rng(51)
    fc = np.zeros(n)
    fc[np.arange(30, n - 10, 70)] = 15.0              # isolated events: 17 episodes
    fc[np.arange(31, n - 10, 70)] = 18.0
    close = 100 * np.exp(np.cumsum(rng.normal(0, 0.02, n)))
    ts = (T0 + np.arange(n) * DAY).astype(np.int64)
    w = ct.Window("SYN", "w0", ts, close, fc, np.array(["x"] * n, dtype=object), DAY)
    s = spec({"kind": "event", "field": "forecast", "op": ">=", "value": 12})
    s = ct.TestSpec(**{**s.__dict__, "significance": {"method": ct.A851A_METHOD},
                       "outcome": {"kind": "fwd_return", "horizons": [3]}})
    a = rt([w], s)["horizons"][3]["a851a"]
    y = ct.out_fwd_return(w, 3)
    ok = np.isfinite(y)
    recs = [{"forecast": float(fc[t]), "next_return_bps": float(y[t]) * 1e4,
             "active": bool(fc[t] >= 12), "symbol": "SYN",
             "timestamp": pd.Timestamp(int(ts[t]), unit="s")} for t in np.nonzero(ok)[0]]
    direct = es.compute_a851a_significance(
        recs, era_of=None, gap_bars=48, density_fallback_pct=50.0, min_n_episodes=8,
        block_size=1, n_resamples=2000, seed=ct.A851A_SEED, expected_step=pd.Timedelta(DAY, unit="s"))
    assert a["method_label"] == direct["method"] == "episode_block_bootstrap"
    assert a["n_episodes"] == direct["n_episodes"] == 17
    assert a["pooled_ic"] == direct["pooled_ic"]
    p2 = direct["p_value"]
    assert a["p_value"] == pytest.approx(p2 / 2 if direct["pooled_ic"] > 0 else 1 - p2 / 2)
    assert a["p_value"] + a["p_value_opposite"] == pytest.approx(1.0)


def test_a851a_settings_are_the_existing_ones():
    import episode_significance as es
    assert ct.A851A_SETTINGS == {"gap_bars": es._DEFAULT_GAP_BARS,
                                 "density_fallback_pct": es._DEFAULT_DENSITY_FALLBACK_PCT,
                                 "min_n_episodes": es._MIN_N_EPISODES,
                                 "n_resamples": es._DEFAULT_N_RESAMPLES}


# --- small fixes ------------------------------------------------------------------------------

def test_holdout_guard_checks_the_final_cache_path(tmp_path):
    sealed = tmp_path / "local_data" / "holdout_sealed"
    sealed.mkdir(parents=True)
    _write_cache(sealed / "x.csv", T0, 40, DAY)
    with pytest.raises(ValueError, match="holdout store"):
        ct.read_warmup(sealed / "x.csv", T0 + 35 * DAY, DAY, 10)
    sneaky = ct.cache_resolver(tmp_path / "local_data" / "other", "../holdout_sealed/x.csv")
    with pytest.raises(ValueError, match="holdout store"):
        ct.read_warmup(sneaky("SYN", "daily"), T0 + 35 * DAY, DAY, 10)


def test_variant_signal_refuses_settings_it_does_not_copy(tmp_path):
    ws = make_windows(52, n=60, n_windows=1)
    run = _write_run(tmp_path, ws, DON)
    p = run / "artifacts" / "variants" / "base" / "strategy_config.json"
    good = json.loads(p.read_text())
    assert ct.variant_signal(run, "base") == DON
    for bad in (dict(good, buffer_bars=50),
                dict(good, regime_detector={"rules": [{"x": 1}], "components": []}),
                {**good, "strategies": {**good["strategies"], "history_transforms": []}}):
        p.write_text(json.dumps(bad))
        with pytest.raises(ValueError, match="settings the null does not copy"):
            ct.variant_signal(run, "base")
    regs = good["strategies"]["regimes"]
    p.write_text(json.dumps({"strategies": {"regimes": {**regs, "trending": regs["unknown"]}}}))
    with pytest.raises(ValueError, match="2 non-null regimes"):
        ct.variant_signal(run, "base")


# --- amendment 4: A8.5.1a with its episode gap in time (2 days) -----------------------------

def test_timegap_is_two_days_of_bars():
    assert ct.a851a_gap_bars(ct.A851A_TIMEGAP_METHOD, DAY) == 2
    assert ct.a851a_gap_bars(ct.A851A_TIMEGAP_METHOD, HOUR) == 48      # hourly unchanged
    assert ct.a851a_gap_bars(ct.A851A_METHOD, DAY) == 48               # the old method: bars
    with pytest.raises(ValueError, match="whole number"):
        ct.a851a_gap_bars(ct.A851A_TIMEGAP_METHOD, 7 * 3600)
    assert ct.check_spec(ct.TestSpec(**{**spec(EVENT).__dict__,
                                        "significance": {"method": ct.A851A_TIMEGAP_METHOD}})) == []


def test_timegap_wrapper_equals_a_direct_call_with_a_2_bar_gap():
    import episode_significance as es
    ws = cal.simulate_windows(np.random.default_rng(7), "iid")
    s = ct.TestSpec(**{**cal.cell_spec(ct.A851A_TIMEGAP_METHOD, "upper", 0).__dict__,
                       "outcome": {"kind": "fwd_return", "horizons": [2]}})
    res = rt(ws, s)
    a = res["horizons"][2]["a851a"]
    assert res["a851a_gap_bars"] == 2
    recs = []
    for w in ws:
        y = ct.out_fwd_return(w, 2)
        for t in np.nonzero(np.isfinite(y))[0]:
            recs.append({"forecast": float(w.forecast[t]), "next_return_bps": float(y[t]) * 1e4,
                         "active": bool(w.forecast[t] >= 12), "symbol": "SIM",
                         "timestamp": pd.Timestamp(int(w.ts[t]), unit="s")})
    direct = es.compute_a851a_significance(
        recs, era_of=None, gap_bars=2, density_fallback_pct=50.0, min_n_episodes=8,
        block_size=1, n_resamples=2000, seed=ct.A851A_SEED,
        expected_step=pd.Timedelta(DAY, unit="s"))
    assert a["method_label"] == direct["method"] == "episode_block_bootstrap"
    assert a["n_episodes"] == direct["n_episodes"] >= 8
    assert a["pooled_ic"] == direct["pooled_ic"]
    p2 = direct["p_value"]
    assert a["p_value"] == pytest.approx(p2 / 2 if direct["pooled_ic"] > 0 else 1 - p2 / 2)


def test_method_override_applies_the_amendment_method_without_editing_the_spec(tmp_path):
    ws = make_windows(54, n=80, n_windows=2)
    run = _write_run(tmp_path, ws, DON)
    cdir = _write_cache_for(tmp_path, ws)
    sp = tmp_path / "spec.yaml"
    sp.write_text(yaml.safe_dump({"claim_id": "c", "source_run": "run_x", "tests": [
        {"name": "t", "selector": EVENT, "outcome": {"kind": "fwd_return", "horizons": [1]},
         "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "greater",
         "floor": {"min_events": 1}}]}))
    res = ct.cache_resolver(cdir, "kraken_{symbol}_{tf}.csv")
    doc = ct.grade_claim_file(run, sp, res, method_override=ct.A851A_TIMEGAP_METHOD)
    t = doc["variants"]["base"]["tests"]["t"]
    assert t["significance"] == {"method": ct.A851A_TIMEGAP_METHOD}
    assert doc["method_override"] == ct.A851A_TIMEGAP_METHOD
    assert t["status"] == "method_not_calibrated"          # no calibration file given
    with pytest.raises(ValueError, match="method override"):
        ct.grade_claim_file(run, sp, res, method_override=ct.SIGNIFICANCE_METHOD)


def test_calibration_runs_per_signal_and_never_mixes_them():
    c20 = cal.run_cell(ct.A851A_TIMEGAP_METHOD, "iid", "upper", n_sims=1, period=20)
    c14 = cal.run_cell(ct.A851A_TIMEGAP_METHOD, "iid", "lower", n_sims=1, period=14)
    assert c20["signal"] == cal.DONCHIAN and c14["signal"]["params"]["period"] == 14
    assert cal.summarize(ct.A851A_TIMEGAP_METHOD, [c20, c14])["scope"]["signal"] is None
    assert cal.summarize(ct.A851A_TIMEGAP_METHOD, [c14])["scope"]["signal"] == cal.donchian(14)


def test_variant_without_a_gate_for_its_signal_is_not_graded_and_masks_nothing(tmp_path):
    """Amendment 4 section 4: with a passed gate for Donchian(10) only, a
    Donchian(14) variant is listed as not graded; the claim status and
    N tests run come from the graded variant alone."""
    ws = make_windows(55, n=80, n_windows=2)
    run = _write_run(tmp_path, ws, DON)
    other = run / "artifacts" / "variants" / "p14"
    other.mkdir(parents=True)
    cfg = json.loads((run / "artifacts" / "variants" / "base" / "strategy_config.json").read_text())
    cfg["strategies"]["regimes"]["unknown"]["components"][0]["params"]["period"] = 14
    (other / "strategy_config.json").write_text(json.dumps(cfg))
    (other / "protocol_result.yaml").write_text(
        (run / "artifacts" / "variants" / "base" / "protocol_result.yaml").read_text())
    import shutil
    shutil.copytree(run / "variants" / "base", run / "variants" / "p14")
    cdir = _write_cache_for(tmp_path, ws)
    sp = tmp_path / "spec.yaml"
    sp.write_text(yaml.safe_dump({"claim_id": "c", "source_run": "run_x", "tests": [
        {"name": n, "selector": EVENT, "outcome": {"kind": "fwd_return", "horizons": [1]},
         "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "greater",
         "floor": {"min_events": 10**6}} for n in ("a", "b")]}))
    calib = tmp_path / "calib.yaml"
    calib.write_text(yaml.safe_dump(passed_summary(DON, "mean_diff",
                                                   method=ct.A851A_TIMEGAP_METHOD)))
    res = ct.cache_resolver(cdir, "kraken_{symbol}_{tf}.csv")
    doc = ct.grade_claim_file(run, sp, res, calibration_files=[calib],
                              method_override=ct.A851A_TIMEGAP_METHOD)
    assert doc["graded_variants"] == ["base"]
    assert doc["not_graded_variants"] == ["broken", "p14 (no passed calibration for its signal)"]
    assert doc["variants"]["p14"]["claim_status"] == "method_not_calibrated"
    assert doc["claim_status"] == doc["variants"]["base"]["claim_status"] == "inconclusive"
    assert doc["n_tests_run"] == 2                         # 2 tests x 1 graded variant
    none = ct.grade_claim_file(run, sp, res, calibration_files=[],
                               method_override=ct.A851A_TIMEGAP_METHOD)
    assert none["claim_status"] == "method_not_calibrated" and none["n_tests_run"] == 0


def test_timegap_equals_the_old_method_on_hourly_bars():
    rng = np.random.default_rng(56)
    n = 600
    fc = np.zeros(n)
    fc[np.arange(20, n - 30, 60)] = 15.0
    fc[np.arange(21, n - 30, 60)] = 18.0
    close = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
    w = ct.Window("SYN", "w0", (T0 + np.arange(n) * HOUR).astype(np.int64), close, fc,
                  np.array(["x"] * n, dtype=object), HOUR)
    sel = {"kind": "event", "field": "forecast", "op": ">=", "value": 12}
    outs = []
    for m in (ct.A851A_METHOD, ct.A851A_TIMEGAP_METHOD):
        s = ct.TestSpec(**{**spec(sel).__dict__, "significance": {"method": m},
                           "outcome": {"kind": "fwd_return", "horizons": [3]}})
        outs.append(rt([w], s)["horizons"][3]["a851a"])
    assert outs[0] == outs[1]


def test_a851a_refutes_only_a_significant_negative_ic():
    """Within the events, a stronger forecast is followed by a LOWER return:
    the IC is significantly negative, so the claim (IC > 0) is refuted."""
    rng = np.random.default_rng(57)
    n = 1500
    fc = np.zeros(n)
    idx = np.arange(30, n - 10, 30)
    fc[idx] = rng.uniform(12, 20, len(idx))
    r = rng.normal(0, 0.01, n)
    r[idx + 1] -= (fc[idx] - 12) * 0.01
    close = 100 * np.exp(np.cumsum(r))
    w = ct.Window("SYN", "w0", (T0 + np.arange(n) * DAY).astype(np.int64), close, fc,
                  np.array(["x"] * n, dtype=object), DAY)
    sel = {"kind": "event", "field": "forecast", "op": ">=", "value": 12}
    s = ct.TestSpec(**{**spec(sel).__dict__, "significance": {"method": ct.A851A_TIMEGAP_METHOD},
                       "floor": {"min_events": 10}})
    res = rt([w], s)
    a = res["horizons"][1]["a851a"]
    assert a["pooled_ic"] < 0 and a["p_value_opposite"] < 0.05
    assert res["status"] == "refuted"

