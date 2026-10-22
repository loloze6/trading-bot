"""
D-176: strategies.sizing -- vol targeting in the ALLOCATION step.

    allocation = clip(forecast / 10 * target_annual_vol / realised, -max_allocation, +max_allocation)

with `realised` the vol_target op's own number (registry.realised_annual_vol). Optional;
the block's presence is the opt-in (like E-055's strategies.min_allocation_change).

Pins:
  1. byte-identity with the block absent -- on run_084's and run_099's real configs (the
     committed fixtures) and through a real pass of TradingBot._process_symbol_candle_completion
     (the rows, the orders and the risk-manager call equal what forecast / 10 gave before);
  2. the formula, against the vol_target op and against a hand computation;
  3. the clip and the 2.0 default;
  4. warm-up (window closes -> 0.0, window + 1 -> a value; required_bars = window + 1 only
     with a block);
  5. degenerate volatility -> 0.0; a NaN forecast keeps the CUL-274 hold and never reaches
     the band;
  6. the min_allocation_change band judged on the SIGNAL (forecast / 10 against the signal
     the position was last set from);
  7. the validator (V19): malformed blocks and "sized twice";
  8. the launcher hands strategy.sizing to ForecastManager at every call site.

No-lookahead: sizing reads only the strategy buffer's last window + 1 closes, the last being
the bar being decided (strategy.update has already appended it); asserted in
test_a_later_bar_cannot_change_an_earlier_sizing. No network, no market data.
"""
import ast
import copy
import json
import logging
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.launcher import Launcher  # noqa: E402
from core.trading_bot import TradingBot  # noqa: E402
from execution.forecast_manager import ForecastManager  # noqa: E402
from risk.risk_manager import RiskManager  # noqa: E402
from strategies.main_strategy import AdvancedStrategy  # noqa: E402
from strategies.registry import (  # noqa: E402
    TRANSFORM_OPS_REGISTRY, normalise_sizing_block, sizing_block_errors, sizing_realised_vol)
from tests.test_portfolio_risk_gate import (  # noqa: E402
    _CaptureExec, _DM, _FixedPortfolio, _Forecast, _Signal, _Tracker, _bar_df)
from tools.validate_config import validate  # noqa: E402

FIXTURES = REPO_ROOT / "strategy-research" / "tests" / "fixtures"
RUN_084 = FIXTURES / "d142" / "run_084_BTCUSD_2018-05" / "strategy_config.json"
RUN_099 = FIXTURES / "d176" / "run_099_strategy_config.json"

SIZING = {"kind": "vol_target", "window": 5, "target_annual_vol": 0.2, "periods_per_year": 365}
SYMBOL = "BTCUSDT"


# --------------------------------------------------------------------------- helpers

def _closes(n, seed=3, vol=0.02):
    rng = np.random.default_rng(seed)
    return list(100.0 * np.exp(np.cumsum(rng.normal(0.0, vol, n))))


def _ts(i):
    return str(pd.Timestamp("2024-04-01") + pd.Timedelta(hours=int(i)))


class _Buffer:
    def __init__(self):
        self.closes = []

    def get_df(self):
        return pd.DataFrame({"close": list(self.closes)})


class _SizedStrategy:
    """Appends each bar's close in update() (as AdvancedStrategy does) and forecasts from a list."""

    def __init__(self, forecasts):
        self.forecasts = list(forecasts)
        self.i = 0
        self.data_buffer = _Buffer()
        self.required_bars = 1

    def update(self, data):
        self.data_buffer.closes.append(float(data["close"].iloc[-1]))

    def generate_signals(self):
        f = self.forecasts[self.i]
        self.i += 1
        return _Signal(f)

    def reset_history(self):
        pass


class _FillingExec(_CaptureExec):
    """Records every order; on success the portfolio is then AT the order's target."""

    def __init__(self, portfolio, success=True):
        super().__init__(success=success)
        self.portfolio = portfolio

    def _execute_portfolio_rebalance(self, **kwargs):
        ok, dbg = super()._execute_portfolio_rebalance(**kwargs)
        if ok:
            self.portfolio._allocation = kwargs["target_allocation"]
        return ok, dbg


class _SpyRiskManager(RiskManager):
    def __init__(self, controls_cfg):
        super().__init__(controls_cfg)
        self.calls = []  # (args, kwargs, approved)

    def approve_allocation_change(self, *args, **kwargs):
        res = super().approve_allocation_change(*args, **kwargs)
        self.calls.append((args, kwargs, res[0]))
        return res


def _make_bot(sizing, forecasts, *, threshold=0.2, success=True, start_alloc=0.0, legacy=False):
    portfolio = _FixedPortfolio(equity=100.0, allocation=start_alloc)
    execn = _FillingExec(portfolio, success=success)
    tracker = _Tracker()
    rm = _SpyRiskManager({"min_allocation_change": {"threshold": threshold}})
    if legacy:
        fm = _Forecast()  # the pre-D-176 arithmetic, expressed as the test harness's stub
    else:
        fm = ForecastManager(sizing=sizing) if sizing is not None else ForecastManager()
    bot = TradingBot(
        data_manager=_DM(), strategy=_SizedStrategy(forecasts), execution_handler=execn,
        logger=logging.getLogger("test_d176"), portfolio_info=portfolio,
        portfolio_state_tracker=tracker, forecast_manager=fm, risk_manager=rm,
        performance_tracker=None, symbols=[SYMBOL], risk_gate=None)
    return bot, execn, tracker, rm


def _drive(bot, i, close):
    bot.data_manager.set_bar(_bar_df(_ts(i), close))
    bot._process_symbol_candle_completion(SYMBOL)


def _run(bot, closes):
    for i, c in enumerate(closes):
        _drive(bot, i, c)


def _plain(calls):
    return [{k: v for k, v in c.items() if k != "signal" and not isinstance(v, pd.DataFrame)} for c in calls]


def _row_without_objects(row):
    return {k: v for k, v in row.items() if k not in ("data", "signal")}


def _expected_alloc(forecast, closes, sizing=SIZING):
    """Hand computation: forecast * target / (stdev(simple returns, last window, ddof 1) * sqrt(ppy)) / 10,
    clipped. NaN-free inputs only."""
    sz = normalise_sizing_block(sizing)
    tail = np.asarray(closes[-(sz["window"] + 1):], dtype=float)
    realised = float(np.std(tail[1:] / tail[:-1] - 1.0, ddof=1)) * math.sqrt(sz["periods_per_year"])
    out = forecast * sz["target_annual_vol"] / realised / 10.0
    return min(max(out, -sz["max_allocation"]), sz["max_allocation"])


# --------------------------------------------------------------------------- 1. byte identity, block absent

@pytest.mark.parametrize("config_path", [RUN_084, RUN_099], ids=["run_084", "run_099"])
def test_real_configs_without_a_block_are_untouched(config_path):
    cfg = json.loads(config_path.read_text())
    assert "sizing" not in cfg["strategies"]
    assert [m for m in validate(cfg) if "V19" in m] == []        # V19 silent
    strat = AdvancedStrategy(config_path=str(config_path))
    assert strat.sizing is None
    # required_bars is exactly the pre-D-176 formula
    assert strat.required_bars == max(strat.regime_engine.get_required_periods(),
                                      strat.strategy_engine.get_required_periods(), 24)


@pytest.mark.parametrize("f", [-20.0, -13.37, 0.0, 0.1, 7.0, 20.0])
def test_no_block_forecast_manager_is_forecast_over_ten_exactly(f):
    fm = ForecastManager()
    assert fm.sizing is None
    assert fm.forecast_to_allocation(f) == f / 10.0              # the same float, not approx
    assert fm.forecast_to_allocation(f, closes=[1.0, 2.0]) == f / 10.0   # closes ignored
    assert fm.last_realised_vol is None


def test_no_block_real_bot_pass_equals_the_legacy_forecast_over_ten_pass():
    closes = _closes(40, seed=11)
    forecasts = [0.0, 6.0, 6.5, 12.0, 12.0, -5.0, -5.5, 0.0, 20.0, 3.0] * 4
    new_bot, new_exec, new_tr, new_rm = _make_bot(None, forecasts)
    old_bot, old_exec, old_tr, old_rm = _make_bot(None, forecasts, legacy=True)
    _run(new_bot, closes)
    _run(old_bot, closes)
    assert len(new_tr.rows) == len(old_tr.rows) == 40
    assert [_row_without_objects(r) for r in new_tr.rows] == [_row_without_objects(r) for r in old_tr.rows]
    assert _plain(new_exec.calls) == _plain(old_exec.calls) and len(new_exec.calls) > 0
    # no sizing column at all, and the risk manager is asked exactly as before (no signal_change)
    assert all(not any(k.startswith("sizing_") for k in r) for r in new_tr.rows)
    assert new_rm.calls and all("signal_change" not in kw for _, kw, _ in new_rm.calls)
    assert [(a[:2], kw, ok) for a, kw, ok in new_rm.calls] == [(a[:2], kw, ok) for a, kw, ok in old_rm.calls]
    assert new_bot._held_signal_allocation == {}                 # never touched without a block


# --------------------------------------------------------------------------- 2. formula

def test_formula_equals_the_vol_target_op_over_ten_and_the_hand_computation():
    sizing = {"kind": "vol_target", "window": 60, "target_annual_vol": 0.4, "periods_per_year": 365}
    closes = _closes(200, seed=1, vol=0.03)
    fm = ForecastManager(sizing={**sizing, "max_allocation": 1e9})   # cap out of the way
    d = pd.DataFrame({"close": closes})
    for f in (10.0, -7.5, 3.3, 20.0):
        op = TRANSFORM_OPS_REGISTRY["vol_target"](f, pd.Series([f]), {k: sizing[k] for k in (
            "window", "target_annual_vol", "periods_per_year")}, d)
        assert fm.forecast_to_allocation(f, closes=closes) == op / 10.0       # exactly equal
        assert fm.forecast_to_allocation(f, closes=closes) == pytest.approx(
            _expected_alloc(f, closes, {**sizing, "max_allocation": 1e9}), rel=1e-12)
    assert fm.last_realised_vol == sizing_realised_vol(closes, fm.sizing) > 0


def test_signal_allocation_is_forecast_over_ten():
    assert ForecastManager(sizing=SIZING).signal_allocation(7.0) == 0.7


def test_a_later_bar_cannot_change_an_earlier_sizing():
    """No lookahead: the allocation at bar t is a function of closes[:t+1] only, and only of its
    last window + 1 entries."""
    closes = _closes(60, seed=5)
    fm = ForecastManager(sizing=SIZING)
    t = 30
    a = fm.forecast_to_allocation(8.0, closes=closes[:t + 1])
    assert a == fm.forecast_to_allocation(8.0, closes=closes[t - SIZING["window"]:t + 1])  # older bars do not matter
    shifted = closes[:t + 1]
    shifted[0] *= 7.0                                             # outside the window
    assert fm.forecast_to_allocation(8.0, closes=shifted) == a


# --------------------------------------------------------------------------- 3. clip and default

def test_clip_at_max_allocation_both_signs_and_the_default_is_two():
    closes = _closes(30, seed=2, vol=0.0005)                      # tiny vol -> huge unclipped size
    fm = ForecastManager(sizing=SIZING)
    assert fm.sizing["max_allocation"] == 2.0
    assert _expected_alloc(20.0, closes, {**SIZING, "max_allocation": 1e9}) > 2.0     # would exceed
    assert fm.forecast_to_allocation(20.0, closes=closes) == 2.0
    assert fm.forecast_to_allocation(-20.0, closes=closes) == -2.0
    small = ForecastManager(sizing={**SIZING, "max_allocation": 0.5})
    assert small.forecast_to_allocation(20.0, closes=closes) == 0.5
    assert small.forecast_to_allocation(-20.0, closes=closes) == -0.5


def test_inside_the_cap_is_not_clipped():
    closes = _closes(30, seed=2, vol=0.02)
    fm = ForecastManager(sizing=SIZING)
    got = fm.forecast_to_allocation(1.0, closes=closes)
    assert abs(got) < 2.0 and got == pytest.approx(_expected_alloc(1.0, closes), rel=1e-12)


# --------------------------------------------------------------------------- 4. warm-up

def test_window_closes_give_zero_and_window_plus_one_give_a_value():
    closes = _closes(SIZING["window"] + 1, seed=4)
    fm = ForecastManager(sizing=SIZING)
    assert fm.forecast_to_allocation(10.0, closes=closes[:SIZING["window"]]) == 0.0
    assert fm.last_realised_vol is None
    v = fm.forecast_to_allocation(10.0, closes=closes)
    assert v != 0.0 and v == pytest.approx(_expected_alloc(10.0, closes), rel=1e-12)
    assert fm.last_realised_vol is not None


def _config_with(tmp_path, *, sizing=None, window=20):
    cfg = json.loads(RUN_084.read_text())
    comp = cfg["strategies"]["regimes"]["unknown"]["components"][0]
    comp["transforms"] = [{"op": "standardise", "params": {"window": window, "min_periods": 5}},
                          {"op": "clip", "params": {"min": -20, "max": 20}}]
    if sizing is not None:
        cfg["strategies"]["sizing"] = sizing
    p = tmp_path / "strategy_config.json"
    p.write_text(json.dumps(cfg))
    return str(p)


def test_required_bars_is_window_plus_one_only_with_a_block(tmp_path):
    base = AdvancedStrategy(config_path=_config_with(tmp_path))
    assert base.sizing is None
    big = {**SIZING, "window": 500}
    sized = AdvancedStrategy(config_path=_config_with(tmp_path, sizing=big))
    assert base.required_bars < 501 and sized.required_bars == 501
    assert sized.sizing == {**big, "max_allocation": 2.0}
    small = AdvancedStrategy(config_path=_config_with(tmp_path, sizing={**SIZING, "window": 3}))
    assert small.required_bars == base.required_bars              # a short window changes nothing


# --------------------------------------------------------------------------- 5. degenerate vol and NaN

@pytest.mark.parametrize("bad", ["flat", "nan", "zero", "negative", "inf"])
def test_degenerate_closes_size_to_flat(bad):
    closes = _closes(10, seed=6)
    if bad == "flat":
        closes = [100.0] * 10                                     # zero realised vol
    elif bad == "nan":
        closes[-2] = float("nan")
    elif bad == "zero":
        closes[-3] = 0.0
    elif bad == "negative":
        closes[-3] = -5.0
    else:
        closes[-1] = float("inf")
    fm = ForecastManager(sizing=SIZING)
    assert fm.forecast_to_allocation(15.0, closes=closes) == 0.0
    assert fm.last_realised_vol is None


def test_a_bad_close_outside_the_window_is_ignored():
    closes = _closes(12, seed=6)
    closes[0] = float("nan")
    got = ForecastManager(sizing=SIZING).forecast_to_allocation(10.0, closes=closes)
    assert got == pytest.approx(_expected_alloc(10.0, closes[1:]), rel=1e-12)


def test_a_sizing_block_needs_closes():
    with pytest.raises(ValueError, match="close history"):
        ForecastManager(sizing=SIZING).forecast_to_allocation(10.0)


def test_nan_and_inf_forecast_pass_through_unchanged():
    fm = ForecastManager(sizing=SIZING)
    closes = _closes(20, seed=7)
    assert math.isnan(fm.forecast_to_allocation(float("nan"), closes=closes))
    assert fm.forecast_to_allocation(float("inf"), closes=closes) == float("inf")


def test_nan_forecast_holds_with_a_block_and_the_band_is_never_asked():
    closes = _closes(15, seed=8)
    bot, execn, tracker, rm = _make_bot(SIZING, [float("nan")] * 15, start_alloc=0.5)
    _run(bot, closes)
    assert execn.calls == [] and rm.calls == []                   # CUL-274 hold; no band call
    assert bot.nan_forecast_bars == {SYMBOL: 15}
    row = tracker.rows[-1]
    assert row["allocation_change"] == 0.0 and row["previous_allocation"] == 0.5
    assert "sizing_signal_change" not in row                      # no signal decision on that bar
    assert math.isnan(row["sizing_target_allocation"])
    assert bot._held_signal_allocation == {}


# --------------------------------------------------------------------------- bars.csv columns with a block

def test_with_a_block_the_forecast_stays_the_signal_and_three_columns_are_added():
    closes = _closes(12, seed=9)
    bot, execn, tracker, _ = _make_bot(SIZING, [10.0] * 12)
    _run(bot, closes)
    row = tracker.rows[-1]
    assert row["signal"].forecast == 10.0                         # the unsized signal
    want = _expected_alloc(10.0, closes)
    assert row["sizing_target_allocation"] == pytest.approx(want, rel=1e-12)
    assert row["sizing_realised_vol"] == pytest.approx(
        sizing_realised_vol(closes, normalise_sizing_block(SIZING)), rel=1e-12)
    assert "sizing_signal_change" in row
    # warm-up bars (fewer than window + 1 closes) are sized flat and carry no realised vol
    first = tracker.rows[0]
    assert first["sizing_target_allocation"] == 0.0 and first["sizing_realised_vol"] is None


# --------------------------------------------------------------------------- 6. the band on the signal

def _first_bar_with_a_full_window():
    return SIZING["window"]          # index of the first bar that has window + 1 closes


def test_a_small_signal_move_with_a_large_sized_move_is_rejected():
    n0 = _first_bar_with_a_full_window()
    calm = _closes(n0 + 1, seed=12, vol=0.01)
    jump = calm + [calm[-1] * 1.25]                               # a vol shock on the last bar
    forecasts = [0.0] * n0 + [10.0, 10.5]                         # signal 1.0 -> 1.05
    bot, execn, tracker, rm = _make_bot(SIZING, forecasts)
    _run(bot, jump)
    # bar n0: signal moves 0 -> 1.0, passes the band, orders the SIZED target
    assert len(execn.calls) == 1
    t0 = _expected_alloc(10.0, calm)
    assert execn.calls[0]["target_allocation"] == pytest.approx(t0, rel=1e-12)
    assert bot._held_signal_allocation[SYMBOL] == 1.0
    # bar n0 + 1: the sized change alone is above the 0.2 band, the signal change is 0.05
    row = tracker.rows[-1]
    assert abs(row["allocation_change"]) >= 0.2                   # the old band would have traded
    assert row["sizing_signal_change"] == pytest.approx(0.05)
    assert row["approved_rebalance"] is False
    assert len(execn.calls) == 1                                  # rejected: no second order
    args, kwargs, ok = rm.calls[-1]
    assert ok is False and kwargs["signal_change"] == pytest.approx(0.05)
    assert bot._held_signal_allocation[SYMBOL] == 1.0             # unchanged on a rejection


def test_the_signal_is_judged_against_the_held_signal_not_the_previous_bar():
    """A slowly moving signal (+0.1 a bar) never trades on a last-bar delta; it trades once it has
    moved a full band from where the position was set, and orders the sized target."""
    n0 = _first_bar_with_a_full_window()
    closes = _closes(n0 + 4, seed=13, vol=0.01)
    forecasts = [0.0] * n0 + [10.0, 11.0, 12.0, 13.0]            # signal 1.0 .. 1.3 in steps of 0.1
    bot, execn, tracker, rm = _make_bot(SIZING, forecasts)
    _run(bot, closes)
    # trades: bar n0 (0 -> 1.0) and the bar where the signal reached 1.0 + 0.2 = 1.2 (forecast 12)
    assert len(execn.calls) == 2
    second = execn.calls[1]
    assert second["target_allocation"] == pytest.approx(_expected_alloc(12.0, closes[:n0 + 3]), rel=1e-12)
    assert [kw["signal_change"] for _, kw, _ in rm.calls[:3]] == pytest.approx([1.0, 0.1, 0.2])
    # held signal moved to 1.2 on that success; the next bars are judged against 1.2, not 1.0
    assert bot._held_signal_allocation[SYMBOL] == pytest.approx(1.2)   # forecast 13 is only 0.1 from it


def test_a_signal_move_of_the_threshold_executes_to_the_sized_target():
    n0 = _first_bar_with_a_full_window()
    closes = _closes(n0 + 2, seed=14, vol=0.01)
    forecasts = [0.0] * n0 + [10.0, 13.0]                         # +0.3 >= 0.2
    bot, execn, tracker, rm = _make_bot(SIZING, forecasts)
    _run(bot, closes)
    assert len(execn.calls) == 2
    assert execn.calls[1]["target_allocation"] == pytest.approx(_expected_alloc(13.0, closes), rel=1e-12)
    assert bot._held_signal_allocation[SYMBOL] == pytest.approx(1.3)


def test_the_held_signal_updates_only_on_success():
    n0 = _first_bar_with_a_full_window()
    closes = _closes(n0 + 2, seed=15, vol=0.01)
    forecasts = [0.0] * n0 + [10.0, 10.1]
    bot, execn, tracker, rm = _make_bot(SIZING, forecasts, success=False)
    _run(bot, closes)
    # the order failed: the held signal stays at 0.0, so the next bar is judged against 0.0 again
    assert bot._held_signal_allocation.get(SYMBOL, 0.0) == 0.0
    assert len(execn.calls) == 2                                  # it retried rather than waiting for a band
    assert [kw["signal_change"] for _, kw, _ in rm.calls] == pytest.approx([1.0, 1.01])


def test_a_rejection_does_not_update_the_held_signal():
    n0 = _first_bar_with_a_full_window()
    closes = _closes(n0 + 2, seed=16, vol=0.01)
    bot, execn, tracker, rm = _make_bot(SIZING, [0.0] * n0 + [10.0, 10.1])
    _run(bot, closes)
    assert len(execn.calls) == 1 and rm.calls[-1][2] is False
    assert bot._held_signal_allocation[SYMBOL] == 1.0


def test_a_forced_flat_resets_the_held_signal_to_zero():
    n0 = _first_bar_with_a_full_window()
    closes = _closes(n0 + 3, seed=17, vol=0.01)
    bot, execn, tracker, rm = _make_bot(SIZING, [0.0] * n0 + [10.0, 10.0, 10.0])
    for i in range(n0 + 1):
        _drive(bot, i, closes[i])
    assert bot._held_signal_allocation[SYMBOL] == 1.0
    bot._active_gap_tier[SYMBOL] = "large"                        # a large gap forces flat (bypasses the band)
    _drive(bot, n0 + 1, closes[n0 + 1])
    assert execn.calls[-1]["target_allocation"] == 0.0
    assert bot._held_signal_allocation[SYMBOL] == 0.0
    del bot._active_gap_tier[SYMBOL]
    _drive(bot, n0 + 2, closes[n0 + 2])                           # the signal is still 1.0: a full re-entry
    assert execn.calls[-1]["target_allocation"] == pytest.approx(_expected_alloc(10.0, closes[:n0 + 3]), rel=1e-12)
    assert bot._held_signal_allocation[SYMBOL] == 1.0


def test_a_failed_forced_flat_keeps_the_held_signal():
    n0 = _first_bar_with_a_full_window()
    closes = _closes(n0 + 2, seed=18, vol=0.01)
    bot, execn, tracker, rm = _make_bot(SIZING, [0.0] * n0 + [10.0, 10.0])
    for i in range(n0 + 1):
        _drive(bot, i, closes[i])
    execn.success = False
    bot._active_gap_tier[SYMBOL] = "large"
    _drive(bot, n0 + 1, closes[n0 + 1])
    assert bot._held_signal_allocation[SYMBOL] == 1.0


def test_signal_change_drives_the_band_and_only_the_band():
    rm = RiskManager({"min_allocation_change": {"threshold": 0.2}})
    data = pd.DataFrame({"timestamp": [pd.Timestamp("2024-04-01")]})
    # sized change tiny, signal change big -> passes; the reverse -> rejected
    assert rm.approve_allocation_change(SYMBOL, 0.01, data, signal_change=0.5)[0] is True
    assert rm.approve_allocation_change(SYMBOL, 0.9, data, signal_change=0.05)[0] is False
    # None: the sized change is judged, exactly as before
    assert rm.approve_allocation_change(SYMBOL, 0.01, data)[0] is False
    assert rm.approve_allocation_change(SYMBOL, 0.9, data)[0] is True
    assert rm.approve_allocation_change(SYMBOL, 0.9, data, signal_change=None)[0] is True
    # a sign does not matter
    assert rm.approve_allocation_change(SYMBOL, 0.0, data, signal_change=-0.3)[0] is True


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_a_non_finite_signal_change_is_refused(bad):
    rm = RiskManager({"min_allocation_change": {"threshold": 0.2}})
    data = pd.DataFrame({"timestamp": [pd.Timestamp("2024-04-01")]})
    ok, dbg = rm.approve_allocation_change(SYMBOL, 0.9, data, signal_change=bad)
    assert ok is False and dbg["controls"]["min_allocation_change"]["passed"] is False


def test_other_controls_still_see_the_sized_change():
    seen = []

    class _Rm(RiskManager):
        def _ctrl_probe(self, change, symbol, p):
            seen.append(change)
            return True

    rm = _Rm({"min_allocation_change": {"threshold": 0.2}, "probe": {}})
    data = pd.DataFrame({"timestamp": [pd.Timestamp("2024-04-01")]})
    assert rm.approve_allocation_change(SYMBOL, 0.9, data, signal_change=0.5)[0] is True
    assert seen == [0.9]


# --------------------------------------------------------------------------- 7. validator V19

def _base_cfg():
    cfg = json.loads(RUN_084.read_text())
    cfg["strategies"]["regimes"]["unknown"]["components"][0]["transforms"] = [
        {"op": "standardise", "params": {"window": 20, "min_periods": 5}},
        {"op": "clip", "params": {"min": -20, "max": 20}}]
    return cfg


def _v19(cfg):
    return [m for m in validate(cfg) if "V19" in m]


def test_a_valid_block_passes_with_and_without_max_allocation():
    cfg = _base_cfg()
    assert _v19(cfg) == []
    cfg["strategies"]["sizing"] = dict(SIZING)
    assert _v19(cfg) == []
    cfg["strategies"]["sizing"]["max_allocation"] = 1.5
    assert _v19(cfg) == []
    assert validate(cfg) == validate(_base_cfg())                 # nothing else changes


@pytest.mark.parametrize("patch", [
    {"kind": "kelly"}, {"kind": None},
    {"window": 1}, {"window": 5.0}, {"window": True}, {"window": "5"},
    {"target_annual_vol": 0}, {"target_annual_vol": -0.2}, {"target_annual_vol": float("nan")},
    {"target_annual_vol": "0.2"},
    {"periods_per_year": 0}, {"periods_per_year": float("inf")}, {"periods_per_year": True},
    {"max_allocation": 0}, {"max_allocation": -1}, {"max_allocation": "2"},
    {"max_allocation": True}, {"max_allocation": float("nan")},
    {"typo_key": 1},
], ids=lambda p: next(iter(p)) + "=" + repr(next(iter(p.values()))))
def test_a_malformed_block_is_refused(patch):
    cfg = _base_cfg()
    cfg["strategies"]["sizing"] = {**SIZING, **patch}
    msgs = _v19(cfg)
    assert msgs and all(m.startswith("VIOLATION V19 strategies.sizing") for m in msgs)
    with pytest.raises(ValueError):
        normalise_sizing_block(cfg["strategies"]["sizing"])
    assert sizing_block_errors(cfg["strategies"]["sizing"])


@pytest.mark.parametrize("missing", ["kind", "window", "target_annual_vol", "periods_per_year"])
def test_a_missing_required_key_is_refused(missing):
    cfg = _base_cfg()
    cfg["strategies"]["sizing"] = {k: v for k, v in SIZING.items() if k != missing}
    assert _v19(cfg)


@pytest.mark.parametrize("block", [[], "vol_target", 3, {}])
def test_a_non_mapping_or_empty_block_is_refused(block):
    cfg = _base_cfg()
    cfg["strategies"]["sizing"] = block
    assert _v19(cfg)


VOL_TARGET_OP = {"op": "vol_target", "params": {"window": 60, "target_annual_vol": 0.2, "periods_per_year": 365}}


def test_a_vol_target_op_beside_a_block_is_refused_as_sized_twice():
    cfg = json.loads(RUN_099.read_text())                         # run_099's real config holds the op
    assert _v19(cfg) == []                                        # no block: D-149's clause unchanged
    cfg["strategies"]["sizing"] = dict(SIZING)
    msgs = _v19(cfg)
    assert len(msgs) == 1 and "sized twice" in msgs[0]
    assert "strategies.regimes.unknown.components[0].transforms[2]" in msgs[0]


def test_sized_twice_is_found_in_history_transforms_and_nested_positions():
    cfg = _base_cfg()
    cfg["strategies"]["sizing"] = dict(SIZING)
    comp = cfg["strategies"]["regimes"]["unknown"]["components"][0]
    comp["history_transforms"] = [copy.deepcopy(VOL_TARGET_OP)]
    assert len([m for m in _v19(cfg) if "sized twice" in m]) == 1
    nested = _base_cfg()
    nested["strategies"]["sizing"] = dict(SIZING)
    nested["strategies"]["regimes"]["unknown"]["blocks"] = [
        {"id": "b", "source": {"parts": [{"id": "p", "transforms": [copy.deepcopy(VOL_TARGET_OP)]}]}}]
    nested["regime_detector"]["components"] = [{"id": "d", "transforms": [copy.deepcopy(VOL_TARGET_OP)]}]
    twice = [m for m in _v19(nested) if "sized twice" in m]
    assert len(twice) == 2
    assert any("blocks[0].source.parts[0].transforms[0]" in m for m in twice)
    assert any("regime_detector.components[0].transforms[0]" in m for m in twice)


def test_run_084_without_a_block_still_validates_as_before():
    cfg = json.loads(RUN_084.read_text())
    assert any(s.get("op") == "vol_target" for s in
               cfg["strategies"]["regimes"]["unknown"]["components"][0]["transforms"])
    assert _v19(cfg) == []
    AdvancedStrategy(config_path=str(RUN_084))                    # still constructs


def test_advanced_strategy_refuses_a_sized_twice_config(tmp_path):
    cfg = json.loads(RUN_084.read_text())                         # holds a vol_target op
    cfg["strategies"]["sizing"] = dict(SIZING)
    p = tmp_path / "strategy_config.json"
    p.write_text(json.dumps(cfg))
    with pytest.raises(ValueError, match="invalid strategy_config"):
        AdvancedStrategy(config_path=str(p))


# --------------------------------------------------------------------------- 8. launcher wiring

def test_launcher_builds_the_forecast_manager_with_the_block():
    launcher = Launcher()
    _, fm, _ = launcher._build_risk_and_forecast_managers(sizing=dict(SIZING))
    assert fm.sizing == {**SIZING, "max_allocation": 2.0}
    _, fm0, _ = launcher._build_risk_and_forecast_managers()
    assert fm0.sizing is None
    assert fm0.forecast_to_allocation(10.0) == 1.0


def test_build_mock_stack_hands_the_block_to_the_manager_builder(monkeypatch):
    seen = {}

    class _Stop(Exception):
        pass

    def spy(self, min_allocation_change_override=None, sizing=None):
        seen["sizing"] = sizing
        raise _Stop

    monkeypatch.setattr(Launcher, "_build_risk_and_forecast_managers", spy)
    with pytest.raises(_Stop):
        Launcher()._build_mock_stack(None, 1000.0, sizing=dict(SIZING))
    assert seen["sizing"] == SIZING
    with pytest.raises(_Stop):
        Launcher()._build_mock_stack(None, 1000.0)
    assert seen["sizing"] is None


def test_every_launcher_call_site_passes_strategy_sizing():
    """The four sites that hold an AdvancedStrategy (live, two backtest paths, run_backtest) each pass
    strategy.sizing; a new site that forgot it would silently run unsized."""
    tree = ast.parse((PROJECT_ROOT / "core" / "launcher.py").read_text(encoding="utf-8"))
    sites = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            name = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", "")
            if name in ("_build_mock_stack", "_build_risk_and_forecast_managers"):
                kw = {k.arg: k.value for k in n.keywords}
                sites.append((name, kw))
    assert len(sites) == 5                                        # four strategy sites + the stack's own call
    from_strategy = [kw for _, kw in sites if "sizing" in kw and isinstance(kw["sizing"], ast.Attribute)
                     and ast.unparse(kw["sizing"]) == "strategy.sizing"]
    assert len(from_strategy) == 4
    assert [kw for name, kw in sites if "sizing" not in kw] == []
