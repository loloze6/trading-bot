"""E-068 3b: the `past_return` selector field (tools/claim_tests.py).

past_return[t] = close[t] / close[t-n] - 1 with a required `bars: n`, defined
only where the bar stamped ts[t] - n*step is in the SAME window and all n bars
in between are present (row distance exactly n). NaN otherwise -- the first n
bars of every window included; no warm-up rows, nothing chained across windows.

Covers: no lookahead (randomised), two windows, missing bars, the quantile
selector on it, check_spec refusals, spec_hash, claim_measure on it, and the
offline CLI grading it as method_not_calibrated. Synthetic data only (2020
dates); no market data is read.
"""
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import claim_tests as ct  # noqa: E402
import claim_measure as cm  # noqa: E402

T0 = 1577836800          # 2020-01-01 00:00 UTC
HOUR = 3600


def win(close, ts=None, label="w0", step=HOUR):
    close = np.asarray(close, dtype=float)
    n = len(close)
    if ts is None:
        ts = T0 + np.arange(n, dtype=np.int64) * step
    return ct.Window("SYN", label, np.asarray(ts, dtype=np.int64), close,
                     np.linspace(-10, 10, n), np.array(["unknown"] * n, dtype=object), step)


def _walk(rng, n):
    return 100.0 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))


# --- the field itself ---------------------------------------------------------

def test_values_and_the_first_n_bars():
    w = win([100, 110, 99, 99, 198])
    r = ct.past_return(w, 1)
    assert np.isnan(r[0])
    assert np.allclose(r[1:], [0.1, 99 / 110 - 1, 0.0, 1.0])
    r2 = ct.past_return(w, 2)
    assert np.isnan(r2[:2]).all() and np.allclose(r2[2:], [-0.01, 99 / 110 - 1, 1.0])


@pytest.mark.parametrize("n", [1, 3, 7])
def test_no_lookahead_randomised(n):
    """Rewriting any row after t never changes past_return[t], for every t."""
    rng = np.random.default_rng(100 + n)
    close = _walk(rng, 60)
    base = ct.past_return(win(close), n)
    for t in range(60):
        for _ in range(3):
            changed = close.copy()
            changed[t + 1:] = rng.uniform(1, 1000, 60 - t - 1)
            got = ct.past_return(win(changed), n)
            assert np.array_equal(np.isnan(got[:t + 1]), np.isnan(base[:t + 1]))
            assert np.allclose(got[:t + 1], base[:t + 1], equal_nan=True)


def test_two_windows_never_chain():
    """B starts one step after A: B's first n bars are NaN, and A never changes B."""
    rng = np.random.default_rng(1)
    n = 3
    a = win(_walk(rng, 20), label="A")
    b_ts = a.ts[-1] + HOUR + np.arange(20, dtype=np.int64) * HOUR
    b_close = _walk(rng, 20)
    b = win(b_close, ts=b_ts, label="B")
    rb = ct.past_return(b, n)
    assert np.isnan(rb[:n]).all() and np.isfinite(rb[n:]).all()
    # pooled as a test pools windows: any change to A leaves B's selection as it was
    s = _spec({"kind": "event", "field": "past_return", "bars": n, "op": ">", "value": -1.0})
    a2 = win(rng.uniform(1, 1000, 20), label="A")
    per1 = ct._prepare([a, b], s, [1], np.random.default_rng(0))
    per2 = ct._prepare([a2, b], s, [1], np.random.default_rng(0))
    assert np.array_equal(per1[1]["mask"], per2[1]["mask"])
    assert not per1[1]["mask"][:n].any() and per1[1]["mask"][n:].all()


def test_missing_bar_t_minus_n_gives_nan():
    ts = T0 + np.array([0, 1, 2, 4, 5, 6], dtype=np.int64) * HOUR      # 3 h missing
    w = win([100, 101, 102, 104, 105, 106], ts=ts)
    r = ct.past_return(w, 2)
    # t at 4 h: 2 h is present, 3 h is not -> row distance 1, not 2 -> NaN
    # t at 5 h: 3 h is missing -> NaN; t at 6 h: 4 h present, 5 h present -> defined
    assert np.isnan(r[:2]).all() and np.isfinite(r[2])
    assert np.isnan(r[3]) and np.isnan(r[4]) and np.isclose(r[5], 106 / 104 - 1)


def test_a_missing_bar_in_between_gives_nan():
    """The bar stamped exactly n steps back exists, but one in between is gone:
    the timestamp match alone would accept it; the strict row distance does not."""
    ts = T0 + np.array([0, 2, 3], dtype=np.int64) * HOUR               # 1 h missing
    w = win([100, 102, 103], ts=ts)
    r = ct.past_return(w, 2)
    assert np.isnan(r[1])                       # t=2h: needs 0h and 1h present
    assert np.isnan(r[2])                       # t=3h: 1h missing
    assert ct.Window.index_at(w, -2)[1] == 0     # the stamp n steps back IS there


def test_quantile_cannot_select_the_first_L_plus_n_bars():
    rng = np.random.default_rng(5)
    L, n = 10, 4
    close = _walk(rng, 80)
    close[L + n - 1] = close[L + n - 2] * 3        # a huge move right before the boundary
    w = win(close)
    sel = {"kind": "quantile", "field": "past_return", "bars": n, "side": "top", "q": 0.2,
           "lookback": L}
    mask, valid = ct.sel_quantile(w, sel)
    assert not mask[:L + n].any() and not valid[:L + n].any()
    assert valid[L + n:].all() and mask[L + n:].any()


def test_event_selector_reads_it():
    w = win([100, 110, 99, 99, 198])
    mask, valid = ct.sel_event(w, {"kind": "event", "field": "past_return", "bars": 1,
                                   "op": ">=", "value": 0.05})
    assert valid.tolist() == [False, True, True, True, True]
    assert mask.tolist() == [False, True, False, False, True]


# --- check_spec ---------------------------------------------------------------

def _spec(selector):
    return ct.TestSpec(selector=selector, outcome={"kind": "fwd_return", "horizons": [1]},
                       baseline={"kind": "complement"}, statistic="mean_diff",
                       direction="greater", floor={"min_events": 5})


Q = {"kind": "quantile", "field": "past_return", "side": "top", "q": 0.1, "lookback": 100}


@pytest.mark.parametrize("bars,ok", [(None, False), (0, False), (1.0, False), (True, False),
                                     ("2", False), (-1, False), (1, True), (24, True)])
def test_check_spec_bars(bars, ok):
    sel = dict(Q) if bars is None else dict(Q, bars=bars)
    errs = ct.check_spec(_spec(sel))
    assert (errs == []) is ok, errs
    if not ok:
        assert any("needs `bars`" in e for e in errs)


def test_check_spec_refuses_bars_on_other_fields():
    for sel in ({"kind": "event", "field": "close", "op": ">", "value": 1, "bars": 2},
                {"kind": "quantile", "field": "forecast", "side": "top", "q": 0.1,
                 "lookback": 10, "bars": 1},
                {"kind": "all", "bars": 1}):
        errs = ct.check_spec(_spec(sel))
        assert any("`bars` is only allowed" in e for e in errs), (sel, errs)
    assert ct.check_spec(_spec({"kind": "event", "field": "past_return", "bars": 3,
                                "op": "<", "value": -0.02})) == []


def test_spec_hash_bars_and_key_order():
    a = _spec(dict(Q, bars=1))
    b = _spec(dict(Q, bars=2))
    assert ct.spec_hash(a) != ct.spec_hash(b)
    reordered = _spec({"bars": 1, "lookback": 100, "q": 0.1, "side": "top",
                       "field": "past_return", "kind": "quantile"})
    assert ct.spec_hash(reordered) == ct.spec_hash(a)


def test_existing_spec_hash_unchanged():
    """A spec written before 3b keeps its identity (run_070's first test)."""
    s = ct.TestSpec(selector={"kind": "quantile", "field": "close", "side": "top", "q": 0.1,
                              "lookback": 100},
                    outcome={"kind": "fwd_return", "horizons": [1, 2, 4, 6, 12]},
                    baseline={"kind": "complement"}, statistic="decay_curve", direction="less",
                    floor={"min_events": 50, "min_windows": 4},
                    consistency={"unit": "window", "min_same_sign": 3})
    assert ct.spec_hash(s) == "c688b1863f8cb3ff4d3a3bb05e0c15d5b885d27a65d3b805ad1990263fa83a99"


# --- slice 3 measurement and the offline CLI ----------------------------------

def test_claim_measure_runs_on_a_synthetic_window():
    rng = np.random.default_rng(9)
    ws = [win(_walk(rng, 400), label=f"w{i}",
              ts=T0 + (i * 1000 + np.arange(400, dtype=np.int64)) * HOUR) for i in range(2)]
    test = {"name": "big_up_moves", "selector": dict(Q, bars=1, lookback=50),
            "outcome": {"kind": "fwd_return", "horizons": [1, 3]},
            "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "less",
            "floor": {"min_events": 5}}
    out = cm.measure_test(ws, test, None)
    assert out["status"] == cm.MEASURED
    assert out["horizons"][1]["n_events"] > 0 and out["horizons"][1]["value"] is not None


def test_offline_cli_grades_past_return_as_method_not_calibrated(tmp_path):
    from test_e068_claim_tests import DON, _write_cache_for, _write_run, make_windows
    ws = make_windows(41, n=80, n_windows=2)
    run = _write_run(tmp_path, ws, DON)
    cdir = _write_cache_for(tmp_path, ws)
    sp = tmp_path / "spec.yaml"
    sp.write_text(yaml.safe_dump({"claim_id": "c", "source_run": "run_x", "tests": [
        {"name": "t", "selector": {"kind": "event", "field": "past_return", "bars": 2,
                                   "op": ">", "value": 0.0},
         "outcome": {"kind": "fwd_return", "horizons": [1]},
         "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "greater",
         "floor": {"min_events": 5},
         "significance": {"method": ct.SIGNIFICANCE_METHOD, "n_resamples": 99, "seed": 7}}]}))
    out = tmp_path / "out" / "r.yaml"
    assert ct.main(["--run", str(run), "--spec", str(sp), "--cache-dir", str(cdir),
                    "--out", str(out)]) == 0
    doc = yaml.safe_load(out.read_text())
    t = doc["variants"]["base"]["tests"]["t"]
    assert t["status"] == "method_not_calibrated"
    assert t["horizons"][1]["n_events"] > 0
