"""E-074 slice 1: the `trailing_vol` bar-t field (tools/claim_tests.py).

trailing_vol[t] = sample std (ddof=1) of the n one-bar log returns ending at t
(rows t-n .. t), with a required `bars: n` (n >= 2). Defined only where the bar
stamped ts[t] - n*step is in the SAME window and all n bars in between are
present (the `past_return` rule); NaN otherwise -- the first n bars of every
window included; no warm-up rows, nothing chained across windows
(engineering/roadmap/E-074/PHASE_A.md 1.3 item 1 and decision 13).

GATED: the field is not in BAR_T_FIELDS. check_spec refuses it by default with
the exact pre-E-074 message, so no flag-off guide, prompt or retry message
changes; a caller accepts it only with check_spec(..., extra_fields=...).

Covers: a hand computation, no lookahead (every row after t rewritten -- close,
timestamp, forecast, regime), locality (rows before t-n ignored), the first n
bars and missing bars, two windows never chained, no warm-up read, the event
and quantile selectors, check_spec gating, pinned spec hashes. Synthetic data
only (2020 dates); no market data is read.
"""
import math
import sys
from pathlib import Path

import numpy as np
import pytest

SR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR_ROOT / "tools"))

import claim_tests as ct  # noqa: E402
import claim_card as cc  # noqa: E402
import claim_measure as cm  # noqa: E402

T0 = 1577836800          # 2020-01-01 00:00 UTC
HOUR = 3600
DAY = 86400
GUIDE = SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design" / "CLAIM_TESTS.md"
TV = ("trailing_vol",)


def win(close, ts=None, label="w0", step=HOUR, forecast=None, regime=None):
    close = np.asarray(close, dtype=float)
    n = len(close)
    if ts is None:
        ts = T0 + np.arange(n, dtype=np.int64) * step
    fc = np.linspace(-10, 10, n) if forecast is None else np.asarray(forecast, dtype=float)
    rg = np.array(["unknown"] * n, dtype=object) if regime is None else regime
    return ct.Window("SYN", label, np.asarray(ts, dtype=np.int64), close, fc, rg, step)


def _walk(rng, n):
    return 100.0 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))


def _same(a, b):
    return np.array_equal(np.isnan(a), np.isnan(b)) and np.allclose(a, b, equal_nan=True)


# --- the field itself ---------------------------------------------------------

def test_hand_computation():
    close = [100.0, 110.0, 99.0, 99.0, 198.0]
    w = win(close)
    r = ct.trailing_vol(w, 2)
    lr = [math.log(110 / 100), math.log(99 / 110), 0.0, math.log(2.0)]
    expect = [float("nan"), float("nan")]
    for t in range(2, 5):
        a, b = lr[t - 2], lr[t - 1]
        m = (a + b) / 2
        expect.append(math.sqrt(((a - m) ** 2 + (b - m) ** 2) / 1))     # ddof=1
    assert _same(r, np.array(expect))
    r3 = ct.trailing_vol(w, 3)
    assert np.isnan(r3[:3]).all()
    assert np.isclose(r3[3], np.std(lr[0:3], ddof=1))
    assert np.isclose(r3[4], np.std(lr[1:4], ddof=1))


@pytest.mark.parametrize("n", [2, 10, 24])
def test_no_lookahead_every_row_after_t_rewritten(n):
    """Rewriting EVERY row after t -- close, timestamp (still increasing),
    forecast and regime -- never changes trailing_vol[t], for every t."""
    rng = np.random.default_rng(300 + n)
    m = 80
    close = _walk(rng, m)
    ts = T0 + np.arange(m, dtype=np.int64) * HOUR
    base = ct.trailing_vol(win(close, ts=ts), n)
    assert np.isfinite(base[n:]).all()
    for t in range(m):
        for _ in range(3):
            c2, ts2 = close.copy(), ts.copy()
            c2[t + 1:] = rng.uniform(1, 1000, m - t - 1)
            ts2[t + 1:] = ts[t] + np.cumsum(rng.integers(1, 4, m - t - 1)) * HOUR
            fc = rng.normal(0, 9, m)
            rg = np.array(["unknown"] * (t + 1) + ["chop"] * (m - t - 1), dtype=object)
            got = ct.trailing_vol(win(c2, ts=ts2, forecast=fc, regime=rg), n)
            assert _same(got[:t + 1], base[:t + 1]), (n, t)


@pytest.mark.parametrize("n", [2, 10])
def test_rows_before_t_minus_n_are_never_read(n):
    """The value at t reads rows t-n .. t only: rewriting rows before t-n leaves it."""
    rng = np.random.default_rng(40 + n)
    m = 60
    close = _walk(rng, m)
    base = ct.trailing_vol(win(close), n)
    for t in range(n + 1, m):
        c2 = close.copy()
        c2[:t - n] = rng.uniform(1, 1000, t - n)
        assert np.isclose(ct.trailing_vol(win(c2), n)[t], base[t]), (n, t)


@pytest.mark.parametrize("n", [2, 24])
def test_first_n_bars_of_a_window_are_nan(n):
    rng = np.random.default_rng(n)
    r = ct.trailing_vol(win(_walk(rng, n + 30)), n)
    assert np.isnan(r[:n]).all() and np.isfinite(r[n:]).all()


def test_window_no_longer_than_n_is_all_nan():
    assert np.isnan(ct.trailing_vol(win([100.0, 101.0, 102.0]), 3)).all()
    assert np.isnan(ct.trailing_vol(win([100.0, 101.0, 102.0]), 2)[:2]).all()


def test_n_below_two_raises():
    with pytest.raises(ValueError):
        ct.trailing_vol(win([100.0, 101.0, 102.0]), 1)


def test_daily_bars():
    rng = np.random.default_rng(9)
    close = _walk(rng, 40)
    r = ct.trailing_vol(win(close, step=DAY), ct.TRAILING_VOL_BARS["daily"])
    n = ct.TRAILING_VOL_BARS["daily"]
    assert np.isnan(r[:n]).all()
    assert np.isclose(r[25], np.std(np.diff(np.log(close))[25 - n:25], ddof=1))


def test_a_missing_bar_gives_nan_around_it():
    """3 h missing: every t whose rows t-n .. t would span it is NaN (the stamp
    n steps back may exist, but the row distance is not n)."""
    hours = [0, 1, 2, 4, 5, 6, 7]
    ts = T0 + np.array(hours, dtype=np.int64) * HOUR
    close = [100.0, 101.0, 103.0, 102.0, 104.0, 107.0, 106.0]
    r = ct.trailing_vol(win(close, ts=ts), 2)
    # t=2h defined (0h,1h,2h); t=4h: 2h present, 3h missing -> NaN; t=5h: 3h
    # missing -> NaN; t=6h: 4h,5h,6h present -> defined; t=7h defined
    assert np.isnan(r[:2]).all() and np.isfinite(r[2])
    assert np.isnan(r[3]) and np.isnan(r[4])
    assert np.isclose(r[5], np.std([math.log(104 / 102), math.log(107 / 104)], ddof=1))
    assert np.isfinite(r[6])
    assert ct.Window.index_at(win(close, ts=ts), -2)[3] == 2   # 2h IS stamped 2 steps back


def test_two_windows_never_chain():
    """B starts one step after A: B's first n bars are NaN, and A never changes B."""
    rng = np.random.default_rng(11)
    n = 5
    a = win(_walk(rng, 30), label="A")
    b_ts = a.ts[-1] + HOUR + np.arange(30, dtype=np.int64) * HOUR
    b = win(_walk(rng, 30), ts=b_ts, label="B")
    rb = ct.trailing_vol(b, n)
    assert np.isnan(rb[:n]).all() and np.isfinite(rb[n:]).all()
    s = ct.TestSpec(selector={"kind": "event", "field": "trailing_vol", "bars": n, "op": ">",
                              "value": -1.0},
                    outcome={"kind": "fwd_return", "horizons": [1]},
                    baseline={"kind": "complement"}, statistic="mean_diff",
                    direction="greater", floor={"min_events": 5})
    a2 = win(rng.uniform(1, 1000, 30), label="A")
    per1 = ct._prepare([a, b], s, [1], np.random.default_rng(0))
    per2 = ct._prepare([a2, b], s, [1], np.random.default_rng(0))
    assert np.array_equal(per1[1]["mask"], per2[1]["mask"])
    assert not per1[1]["mask"][:n].any() and per1[1]["mask"][n:].all()


def test_no_warm_up_read(monkeypatch):
    """PHASE_A decision 13: no warm-up cache read. Real-looking warm-up rows
    attached to the window change nothing (the first n bars stay NaN), and the
    cache reader is never called by the field or its selectors."""
    def boom(*a, **k):
        raise AssertionError("read_warmup must not be called")
    monkeypatch.setattr(ct, "read_warmup", boom)
    rng = np.random.default_rng(13)
    n = 24
    close = _walk(rng, 120)
    plain = win(close)
    warmed = win(close)
    wc = _walk(rng, 500)
    warmed.warm = {"close": wc, "high": wc, "low": wc}
    assert _same(ct.trailing_vol(warmed, n), ct.trailing_vol(plain, n))
    assert np.isnan(ct.trailing_vol(warmed, n)[:n]).all()
    sel = {"kind": "quantile", "field": "trailing_vol", "bars": n, "side": "top", "q": 0.2,
           "lookback": 30}
    m1, v1 = ct.sel_quantile(warmed, sel)
    m2, v2 = ct.sel_quantile(plain, sel)
    assert np.array_equal(m1, m2) and np.array_equal(v1, v2)


# --- the selectors read it ----------------------------------------------------

def test_event_selector_reads_it():
    w = win([100.0, 110.0, 99.0, 99.0, 198.0])
    r = ct.trailing_vol(w, 2)
    mask, valid = ct.sel_event(w, {"kind": "event", "field": "trailing_vol", "bars": 2,
                                   "op": ">", "value": 0.3})
    assert valid.tolist() == [False, False, True, True, True]
    assert mask.tolist() == [bool(np.isfinite(x) and x > 0.3) for x in r]


def test_quantile_selector_is_trailing_and_skips_the_first_L_plus_n_bars():
    rng = np.random.default_rng(5)
    L, n = 10, 4
    close = _walk(rng, 80)
    w = win(close)
    sel = {"kind": "quantile", "field": "trailing_vol", "bars": n, "side": "top", "q": 0.2,
           "lookback": L}
    mask, valid = ct.sel_quantile(w, sel)
    assert not valid[:L + n].any() and valid[L + n:].all() and mask.any()
    x = ct.trailing_vol(w, n)
    for t in np.nonzero(valid)[0]:
        assert mask[t] == (x[t] >= np.quantile(x[t - L:t], 0.8))


# --- gating: check_spec -------------------------------------------------------

def _spec(selector, baseline=None):
    return ct.TestSpec(selector=selector, outcome={"kind": "fwd_return", "horizons": [1, 24]},
                       baseline=baseline or {"kind": "complement"}, statistic="mean_diff",
                       direction="greater", floor={"min_events": 30})


EV = {"kind": "event", "field": "trailing_vol", "bars": 24, "op": ">", "value": 0.0}
QV = {"kind": "quantile", "field": "trailing_vol", "bars": 24, "side": "top", "q": 0.1,
      "lookback": 50}


def test_default_check_spec_refuses_it_with_the_pre_e074_messages():
    """Pinned literally from origin/master before the change: flag-off retry
    messages (which reach the 1a prompt) are byte-identical."""
    assert ct.check_spec(_spec(dict(EV))) == [
        "selector: field 'trailing_vol' is not a bar-t field (allowed: ['forecast', 'close', "
        "'past_return']); a selector may not read the future",
        "selector: `bars` is only allowed with field ['past_return']"]
    ev = {k: v for k, v in EV.items() if k != "bars"}
    assert ct.check_spec(_spec(ev)) == [
        "selector: field 'trailing_vol' is not a bar-t field (allowed: ['forecast', 'close', "
        "'past_return']); a selector may not read the future"]
    assert ct.check_spec(_spec({"kind": "event", "field": "close", "bars": 2, "op": ">",
                                "value": 0.0})) == [
        "selector: `bars` is only allowed with field ['past_return']"]


def test_the_public_registry_is_unchanged():
    assert ct.BAR_T_FIELDS == ("forecast", "close", "past_return")
    assert ct.FIELDS_WITH_BARS == ("past_return",)
    assert ct.GATED_BAR_T_FIELDS == ("trailing_vol",)
    assert not set(ct.GATED_BAR_T_FIELDS) & set(ct.BAR_T_FIELDS)
    assert ct.TRAILING_VOL_BARS == {"hourly": 24, "daily": 10}     # PHASE_A table 2.1


def test_flag_off_guide_and_pipeline_checks_do_not_expose_it():
    """The guide every claim_tests prompt reads never names it, and the
    pipeline's checks (claim_card, claim_measure) still refuse it."""
    assert "trailing_vol" not in GUIDE.read_text(encoding="utf-8")
    t = {"name": "t", "selector": dict(EV), "outcome": {"kind": "fwd_return", "horizons": [1]},
         "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "greater",
         "floor": {"min_events": 30}}
    errs, h, _ = cc._check_test(t, "claim.tests[0]")
    assert errs and h is None
    with pytest.raises(ValueError):
        cm.test_spec(t)


def test_extra_fields_accept_it_in_event_quantile_and_other_selector():
    assert ct.check_spec(_spec(dict(EV)), extra_fields=TV) == []
    assert ct.check_spec(_spec(dict(QV)), extra_fields=TV) == []
    other = {"kind": "other_selector", "selector": dict(QV)}
    assert ct.check_spec(_spec({"kind": "all"}, baseline=other), extra_fields=TV) == []
    assert ct.check_spec(_spec({"kind": "all"}, baseline=other)) != []


@pytest.mark.parametrize("bars", [None, 0, 1, True, "24", 2.0])
def test_extra_fields_bars_must_be_an_int_of_at_least_two(bars):
    sel = {k: v for k, v in EV.items() if k != "bars"}
    if bars is not None:
        sel["bars"] = bars
    assert ct.check_spec(_spec(sel), extra_fields=TV) == [
        "selector: field trailing_vol needs `bars`: an int >= 2 (the number of one-bar "
        "returns, in bars of the card's timeframe)"]


def test_extra_fields_keep_past_return_rules_and_widen_the_messages():
    pr = {"kind": "event", "field": "past_return", "bars": 0, "op": ">", "value": 0.0}
    assert ct.check_spec(_spec(pr), extra_fields=TV) == [
        "selector: field past_return needs `bars`: an int >= 1 (the length of the past move, "
        "in bars of the card's timeframe)"]
    bad = {"kind": "event", "field": "volume", "op": ">", "value": 0.0}
    assert ct.check_spec(_spec(bad), extra_fields=TV) == [
        "selector: field 'volume' is not a bar-t field (allowed: ['forecast', 'close', "
        "'past_return', 'trailing_vol']); a selector may not read the future"]


def test_unknown_extra_field_raises():
    with pytest.raises(ValueError):
        ct.check_spec(_spec(dict(EV)), extra_fields=("volume",))
    with pytest.raises(ValueError):
        ct.check_spec(_spec(dict(EV)), extra_fields=("forecast",))


def test_existing_spec_hashes_are_unchanged():
    """Pinned from origin/master before the change."""
    fc = {"kind": "event", "field": "forecast", "op": ">", "value": 0.0}
    pr = {"kind": "quantile", "field": "past_return", "bars": 24, "side": "top", "q": 0.1,
          "lookback": 50}
    assert ct.spec_hash(_spec(fc)) == \
        "549e7e18521c8066bfb5c100931aebe10e70f01fa8c48557bc15a94ef824bb6d"
    assert ct.spec_hash(_spec(pr)) == \
        "f7aa1681a2c8458dac098c0d10f05c95c2fa8f693c816a73f1f150f8e63530e0"
    assert ct.spec_hash(_spec(dict(EV))) == \
        "b5612ce3fd96e93dab12bf760ad520017d642cedb7a12b313aab1febed812f2d"
