"""E-068 slice 1 (CUL-386): tools/claim_tests.py.

Every block: a planted effect is detected, and no effect is not. Every
selector: changing any future bar never changes today's selection. Plus the
floor -> inconclusive, future-field refusal, timestamp matching inside a window
only, the shift range, spec_hash stability, and the bars.csv loader/CLI.
Synthetic data only (2020 dates); no market data is read.
"""
import csv
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR_ROOT / "tools"))

import claim_tests as ct  # noqa: E402
from performance.signal_statistics import spearman_correlation  # noqa: E402

T0 = 1577836800          # 2020-01-01 00:00 UTC
HOUR = 3600
FAST = {"method": "circular_shift_v1", "n_resamples": 199, "seed": 7}


def make_windows(seed=0, n=500, n_windows=6, effect=0.0, sel_fn=None, vol_effect=0.0,
                 drift_effect=0.0, ic_beta=0.0, h=1, step=HOUR):
    """Synthetic windows. forecast ~ AR(1); regime in blocks. The planted effect
    acts on the bars AFTER a bar selected by sel_fn(window_fields) -> bool mask."""
    rng = np.random.default_rng(seed)
    out = []
    for wi in range(n_windows):
        ts = T0 + (wi * (n + 50) + np.arange(n)) * step
        fc = np.zeros(n)
        for t in range(1, n):
            fc[t] = 0.7 * fc[t - 1] + rng.normal(0, 7)
        fc = np.clip(fc, -20, 20)
        reg = np.empty(n, dtype=object)
        t = 0
        while t < n:
            L = int(rng.integers(5, 30))
            reg[t:t + L] = rng.choice(["trend", "range"])
            t += L
        fields = {"ts": ts, "forecast": fc, "regime": reg}
        sel = sel_fn(fields) if sel_fn is not None else np.zeros(n, dtype=bool)
        r = rng.normal(0, 0.01, n)
        scale = np.ones(n)
        for t in np.nonzero(sel)[0]:
            if t + 1 < n:
                r[t + 1] += effect
            r[t + 1:t + 1 + h] += drift_effect
            scale[t + 1:t + 1 + h] = 1 + vol_effect
        r = r * scale
        r[1:] += ic_beta * fc[:-1] * 0.001
        close = 100 * np.exp(np.cumsum(r))
        out.append(ct.Window("SYN", f"w{wi}", ts.astype(np.int64), close, fc, reg, step))
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


def status(windows, s, eras=None):
    return ct.run_test(windows, s, eras)["status"]


# --- selectors: planted effect detected, none not detected -----------------

EVENT = {"kind": "event", "field": "forecast", "op": ">=", "value": 8}
SELECTOR_CASES = [
    (EVENT, lambda f: f["forecast"] >= 8),
    ({"kind": "all"}, None),
    ({"kind": "regime", "value": "trend"}, lambda f: f["regime"] == "trend"),
    ({"kind": "regime_change", "to": "trend"},
     lambda f: np.r_[False, (f["regime"][1:] == "trend") & (f["regime"][:-1] != "trend")]),
    ({"kind": "calendar", "hours": [0, 1, 2, 3, 4, 5]},
     lambda f: ((f["ts"] % 86400) // 3600) < 6),
]


@pytest.mark.parametrize("sel,fn", [c for c in SELECTOR_CASES if c[1] is not None],
                         ids=lambda x: x["kind"] if isinstance(x, dict) else "")
def test_selector_planted_and_null(sel, fn):
    s = spec(sel, floor={"min_events": 10})
    assert status(make_windows(1, effect=0.01, sel_fn=fn), s) == "supported"
    assert status(make_windows(1, effect=0.0, sel_fn=fn), s) != "supported"


def test_selector_quantile_planted_and_null():
    sel = {"kind": "quantile", "field": "forecast", "side": "top", "q": 0.2, "lookback": 50}

    def fn(f):
        x, out = f["forecast"], np.zeros(len(f["forecast"]), dtype=bool)
        for t in range(50, len(x)):
            out[t] = x[t] >= np.quantile(x[t - 50:t], 0.8)
        return out
    s = spec(sel)
    assert status(make_windows(2, effect=0.01, sel_fn=fn), s) == "supported"
    assert status(make_windows(2, effect=0.0, sel_fn=fn), s) != "supported"


def test_selector_all_with_rank_ic_planted_and_null():
    s = spec({"kind": "all"}, statistic="rank_ic", floor={"min_blocks": 30})
    assert status(make_windows(3, ic_beta=1.0), s) == "supported"
    assert status(make_windows(3, ic_beta=0.0), s) != "supported"


# --- outcomes ----------------------------------------------------------------

def test_outcome_fwd_volatility_planted_and_null():
    fn = lambda f: f["forecast"] >= 8  # noqa: E731
    s = spec(EVENT, outcome={"kind": "fwd_volatility", "horizons": [5]})
    assert status(make_windows(4, vol_effect=2.0, sel_fn=fn, h=5), s) == "supported"
    assert status(make_windows(4, vol_effect=0.0, sel_fn=fn, h=5), s) != "supported"


def test_outcome_fwd_max_drawdown_planted_and_null():
    fn = lambda f: f["forecast"] >= 8  # noqa: E731
    s = spec(EVENT, outcome={"kind": "fwd_max_drawdown", "horizons": [5]}, direction="less")
    assert status(make_windows(5, drift_effect=-0.006, sel_fn=fn, h=5), s) == "supported"
    assert status(make_windows(5, drift_effect=0.0, sel_fn=fn, h=5), s) != "supported"


def _trend_windows(ends: bool, seed=6, n_blocks=60, h=3):
    """Blocks: an up leg of random length >= h, then h bars that go down (trend
    ends; the turn is marked forecast=1) or keep rising (continues;
    forecast=-1). Kinds and lengths are random: a strictly periodic layout
    would let whole-period shifts copy the effect."""
    rng = np.random.default_rng(seed)
    out = []
    for wi in range(4):
        r, fc = [], []
        for b in range(n_blocks):
            kind_a = rng.random() < 0.5
            down = kind_a and ends
            up_len = int(rng.integers(h, h + 4))
            r += list(0.01 + rng.normal(0, 0.002, up_len))
            r += list((-0.01 if down else 0.01) + rng.normal(0, 0.002, h))
            f = np.zeros(up_len + h)
            f[up_len - 1] = 1 if kind_a else -1
            fc += list(f)
        n = len(r)
        ts = T0 + (wi * (n + 10) + np.arange(n)) * HOUR
        out.append(ct.Window("SYN", f"t{wi}", ts.astype(np.int64), 100 * np.exp(np.cumsum(r)),
                             np.array(fc, float), np.array(["x"] * n, dtype=object), HOUR))
    return out


def test_outcome_trend_ends_planted_and_null():
    s = spec({"kind": "event", "field": "forecast", "op": ">=", "value": 1},
             outcome={"kind": "trend_ends", "horizons": [3]}, floor={"min_events": 50})
    assert status(_trend_windows(True), s) == "supported"
    assert status(_trend_windows(False), s) != "supported"


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


# --- baselines ---------------------------------------------------------------

def test_baseline_placebo_planted_and_null():
    fn = lambda f: f["forecast"] >= 8  # noqa: E731
    s = spec(EVENT, baseline={"kind": "placebo", "n_draws": 10})
    assert status(make_windows(8, effect=0.01, sel_fn=fn), s) == "supported"
    assert status(make_windows(8, effect=0.0, sel_fn=fn), s) != "supported"


def test_baseline_other_selector_planted_and_null():
    fn = lambda f: f["forecast"] >= 8  # noqa: E731
    other = {"kind": "other_selector",
             "selector": {"kind": "event", "field": "forecast", "op": "<=", "value": -8}}
    s = spec(EVENT, baseline=other)
    assert status(make_windows(9, effect=0.01, sel_fn=fn), s) == "supported"
    assert status(make_windows(9, effect=0.0, sel_fn=fn), s) != "supported"


def test_baseline_complement_is_valid_and_not_selected():
    w = make_windows(10, n_windows=1)[0]
    mask, valid = ct.sel_event(w, EVENT)
    wref = ct.base_complement(w, mask, valid, {}, 1, None)
    assert np.array_equal(wref > 0, valid & ~mask)


# --- statistics --------------------------------------------------------------

def test_statistic_hit_rate_planted_and_null():
    fn = lambda f: f["forecast"] >= 8  # noqa: E731
    s = spec(EVENT, statistic="hit_rate")
    assert status(make_windows(11, effect=0.01, sel_fn=fn), s) == "supported"
    assert status(make_windows(11, effect=0.0, sel_fn=fn), s) != "supported"


def test_statistic_decay_curve_planted_and_null():
    fn = lambda f: f["forecast"] >= 8  # noqa: E731
    s = spec(EVENT, statistic="decay_curve",
             outcome={"kind": "fwd_return", "horizons": [1, 2, 3]})
    res = ct.run_test(make_windows(12, effect=0.01, sel_fn=fn), s)
    assert res["status"] == "supported" and res["peak_horizon"] in (1, 2, 3)
    assert status(make_windows(12, effect=0.0, sel_fn=fn), s) != "supported"


def test_direction_less_detects_a_planted_drop():
    fn = lambda f: f["forecast"] >= 8  # noqa: E731
    s = spec(EVENT, direction="less")
    res = ct.run_test(make_windows(13, effect=-0.01, sel_fn=fn), s)
    assert res["status"] == "supported"
    assert res["horizons"][1]["value"] < 0 < res["horizons"][1]["oriented"]
    s_up = spec(EVENT, direction="greater")
    assert status(make_windows(13, effect=-0.01, sel_fn=fn), s_up) == "refuted"


def test_rank_average_matches_signal_statistics_spearman():
    rng = np.random.default_rng(14)
    for _ in range(20):
        x = rng.integers(0, 8, 60).astype(float)          # many ties
        y = rng.normal(size=60) + 0.3 * x
        assert ct.spearman(x, y) == pytest.approx(spearman_correlation(list(x), list(y)))
    assert np.isnan(ct.spearman(np.ones(10), np.arange(10.)))


def test_null_p_values_are_spread_sanely_over_seeds():
    fn = lambda f: f["forecast"] >= 8  # noqa: E731
    s = spec(EVENT)
    ps = [ct.run_test(make_windows(100 + k, n=300, n_windows=4, sel_fn=fn), s)
          ["horizons"][1]["p_value"] for k in range(30)]
    assert 0.3 < float(np.mean(ps)) < 0.7
    assert sum(p < 0.05 for p in ps) <= 5


# --- no lookahead --------------------------------------------------------------

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
    w = make_windows(20, n_windows=1)[0]
    mask, valid = ct.SELECTORS[sel["kind"]](w, sel)
    rng = np.random.default_rng(21)
    for t in (40, 150, 333, len(w.ts) - 2):
        fut = ct.Window(w.symbol, w.window, w.ts.copy(), w.close.copy(), w.forecast.copy(),
                        w.regime.copy(), w.step)
        fut.close[t + 1:] = rng.uniform(1, 1000, len(fut.close) - t - 1)
        fut.forecast[t + 1:] = rng.uniform(-20, 20, len(fut.close) - t - 1)
        fut.regime[t + 1:] = rng.choice(["trend", "range", "z"], len(fut.close) - t - 1)
        m2, v2 = ct.SELECTORS[sel["kind"]](fut, sel)
        assert np.array_equal(mask[:t + 1], m2[:t + 1]), t
        assert np.array_equal(valid[:t + 1], v2[:t + 1]), t


def test_quantile_is_trailing_not_whole_sample():
    w = make_windows(22, n_windows=1)[0]
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
                ct.run_test(make_windows(0, n_windows=1), spec(sel))


# --- timestamp matching, inside a window only ----------------------------------

def test_outcomes_never_cross_a_window_boundary():
    a, b = make_windows(23, n=100, n_windows=2)
    b = ct.Window("SYN", "b", a.ts + 100 * HOUR, b.close, b.forecast, b.regime, HOUR)
    for fn in ct.OUTCOMES.values():
        y = fn(a, 5)
        assert np.all(np.isnan(y[-5:]))
    s = spec({"kind": "all"}, statistic="rank_ic",
             outcome={"kind": "fwd_return", "horizons": [5]}, floor={"min_events": 1})
    res = ct.run_test([a, b], s)
    assert res["horizons"][5]["n_events"] == 2 * (100 - 5)


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


# --- the shift ------------------------------------------------------------------

def test_shift_offsets_are_longer_than_the_longest_horizon():
    k = ct._shift_offsets(120, 5, np.random.default_rng(0), 5000)
    assert k.min() == 6 and k.max() == 114
    with pytest.raises(ValueError, match="too short"):
        ct._shift_offsets(11, 5, np.random.default_rng(0), 1)


def test_calendar_shifts_skip_whole_periods():
    assert ct._calendar_period({"kind": "calendar", "hours": [1]}, HOUR) == 24
    assert ct._calendar_period({"kind": "calendar", "weekdays": [5]}, HOUR) == 168
    assert ct._calendar_period({"kind": "calendar", "weekdays": [5]}, 86400) == 7
    assert ct._calendar_period(EVENT, HOUR) is None
    k = ct._shift_offsets(500, 1, np.random.default_rng(0), 5000, period=24)
    assert not np.any(k % 24 == 0) and k.min() >= 2


def test_rank_ic_shift_moves_the_forecast_not_the_mask():
    """With selector=all the mask is all True; the p-value must still be
    meaningful, so the forecast itself is shifted. A strong IC -> small p."""
    s = spec({"kind": "all"}, statistic="rank_ic", floor={"min_events": 10})
    res = ct.run_test(make_windows(24, ic_beta=1.0), s)
    assert res["horizons"][1]["p_value"] < 0.01
    assert res["horizons"][1]["n_placebo"] == FAST["n_resamples"]


def test_every_horizon_must_pass():
    fn = lambda f: f["forecast"] >= 8  # noqa: E731
    # +2% on bar t+1 and -1% on each of t+1, t+2: h=1 gains 1%, h=2 nets 0.
    ws = make_windows(25, effect=0.02, drift_effect=-0.01, h=2, sel_fn=fn)
    res = ct.run_test(ws, spec(EVENT, outcome={"kind": "fwd_return", "horizons": [1, 2]}))
    assert res["horizons"][1]["p_value"] < 0.05
    assert res["horizons"][2]["p_value"] >= 0.05
    assert res["status"] == "refuted" and res["reasons"][0].startswith("h=2")
    one = ct.run_test(ws, spec(EVENT, outcome={"kind": "fwd_return", "horizons": [1]}))
    assert one["status"] == "supported"


# --- floors and consistency -------------------------------------------------------

ERAS = [{"era_id": "e1", "range": ["2020-01-01", "2020-01-31"]},
        {"era_id": "e2", "range": ["2020-02-01", "2020-12-31"]}]


@pytest.mark.parametrize("floor", [{"min_events": 10**6}, {"min_windows": 7},
                                   {"min_blocks": 10**5}, {"min_eras": 3}])
def test_floor_gives_inconclusive(floor):
    fn = lambda f: f["forecast"] >= 8  # noqa: E731
    res = ct.run_test(make_windows(26, effect=0.02, sel_fn=fn), spec(EVENT, floor=floor), ERAS)
    assert res["status"] == "inconclusive"
    assert any("floor" in r for r in res["reasons"])


def test_eras_needed_but_missing_raises():
    with pytest.raises(ValueError, match="needs eras"):
        ct.run_test(make_windows(0, n_windows=1), spec(EVENT, floor={"min_eras": 1}))


def test_window_consistency_rule():
    fn = lambda f: f["forecast"] >= 8  # noqa: E731
    ws = make_windows(27, effect=0.01, sel_fn=fn)
    ok = spec(EVENT, consistency={"unit": "window", "min_same_sign": 6})
    assert status(ws, ok) == "supported"
    too_many = spec(EVENT, consistency={"unit": "window", "min_same_sign": 7})
    res = ct.run_test(ws, too_many)
    assert res["status"] == "refuted" and "same sign in 6 windows" in res["reasons"][0]


def test_per_era_values_reported():
    fn = lambda f: f["forecast"] >= 8  # noqa: E731
    res = ct.run_test(make_windows(28, effect=0.01, sel_fn=fn), spec(EVENT), ERAS)
    assert set(res["horizons"][1]["per_era"]) <= {"e1", "e2"}
    assert res["horizons"][1]["n_eras_with_events"] >= 1


# --- spec ---------------------------------------------------------------------------

def test_spec_hash_stable_and_order_independent():
    a = spec(EVENT, outcome={"kind": "fwd_return", "horizons": [1, 2, 3]})
    b = spec({"value": 8.0, "op": ">=", "field": "forecast", "kind": "event"},
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
                    significance={"method": "bootstrap", "n_resamples": 10, "seed": 1}),
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
        for t in yaml.safe_load(f.read_text(encoding="utf-8"))["tests"]:
            assert ct.check_spec(ct.TestSpec.from_dict(t)) == [], (f.name, t["name"])
            n += 1
    assert n == 3


# --- loader and CLI -------------------------------------------------------------------

def _write_run(root: Path, n=60):
    run = root / "run_x"
    for vid, ok in (("base", True), ("broken", False)):
        (run / "artifacts" / "variants" / vid).mkdir(parents=True)
    results = []
    for i, win in enumerate(("2020-01", "2020-05")):
        rid = f"r{i}"
        d = run / "variants" / "base" / "results" / rid
        d.mkdir(parents=True)
        with open(d / "bars.csv", "w", newline="", encoding="utf-8") as f:
            wr = csv.writer(f)
            wr.writerow(["timestamp", "close", "forecast", "regime", "extra"])
            for t in range(n):
                ts = np.datetime64(T0 + (i * 200 + t) * 86400, "s").astype(str).replace("T", " ")
                wr.writerow([ts, 100 + t, (t % 41) - 20, "unknown", 1])
        results.append({"symbol": "BTCUSD", "window": win, "run_id": rid})
    with open(run / "artifacts" / "variants" / "base" / "protocol_result.yaml", "w") as f:
        yaml.safe_dump({"results": results}, f)
    return run


def test_loader_mapping_and_not_graded(tmp_path):
    run = _write_run(tmp_path)
    graded, not_graded = ct.graded_variants(run)
    assert graded == ["base"] and not_graded == ["broken"]
    ws = ct.load_variant_bars(run, "base")
    assert [w.label for w in ws] == ["BTCUSD/2020-01", "BTCUSD/2020-05"]
    assert ws[0].step == 86400 and len(ws[0].ts) == 60 and len(ws[0].sha256) == 64
    (run / "variants" / "base" / "results" / "r1" / "bars.csv").unlink()
    with pytest.raises(FileNotFoundError):
        ct.load_variant_bars(run, "base")


def test_cli_end_to_end_and_refuses_to_write_into_the_run(tmp_path):
    run = _write_run(tmp_path)
    sp = tmp_path / "spec.yaml"
    sp.write_text(yaml.safe_dump({"claim_id": "c", "tests": [
        {"name": "t", "selector": {"kind": "all"},
         "outcome": {"kind": "fwd_return", "horizons": [1]}, "baseline": None,
         "statistic": "rank_ic", "direction": "greater", "floor": {"min_events": 10**6},
         "significance": dict(FAST)}]}))
    out = tmp_path / "out" / "r.yaml"
    assert ct.main(["--run", str(run), "--spec", str(sp), "--out", str(out)]) == 0
    doc = yaml.safe_load(out.read_text())
    assert doc["n_tests_run"] == 1 and doc["not_graded_variants"] == ["broken"]
    assert doc["variants"]["base"]["tests"]["t"]["status"] == "inconclusive"
    assert len(doc["bars_used"]) == 2 and all(len(b["sha256"]) == 64 for b in doc["bars_used"])
    with pytest.raises(SystemExit, match="inside the run"):
        ct.main(["--run", str(run), "--spec", str(sp), "--out", str(run / "x.yaml")])


def test_combine_fail_dominates():
    assert ct.combine(["supported", "inconclusive", "refuted"]) == "refuted"
    assert ct.combine(["supported", "inconclusive"]) == "inconclusive"
    assert ct.combine(["supported", "supported"]) == "supported"
    assert ct.combine([]) == "inconclusive"
