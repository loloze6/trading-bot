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
from risk.portfolio_risk_gate import PortfolioRiskGate  # noqa: E402
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


def _make_bot(sizing, forecasts, *, threshold=0.2, success=True, start_alloc=0.0, legacy=False, gate=None):
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
        performance_tracker=None, symbols=[SYMBOL], risk_gate=gate)
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


def _passed_on(row):
    return row["debug_approve_allocation_change"]["controls"]["min_allocation_change"]["passed_on"]


def test_a_small_signal_move_with_a_large_sized_move_passes_on_sized():
    """D-176 safety review (Finding 2): with a block the band passes when EITHER the signal's change
    OR the sized change reaches the threshold. A vol shock moves the sized exposure a lot while the
    signal moves 0.05: the pre-D-176 (sized) judgement still trades, so it still does."""
    n0 = _first_bar_with_a_full_window()
    calm = _closes(n0 + 1, seed=12, vol=0.01)
    jump = calm + [calm[-1] * 1.25]                               # a vol shock on the last bar
    forecasts = [0.0] * n0 + [10.0, 10.5]                         # signal 1.0 -> 1.05
    bot, execn, tracker, rm = _make_bot(SIZING, forecasts)
    _run(bot, jump)
    # bar n0: signal moves 0 -> 1.0, orders the SIZED target
    t0 = _expected_alloc(10.0, calm)
    assert execn.calls[0]["target_allocation"] == pytest.approx(t0, rel=1e-12)
    assert _passed_on(tracker.rows[n0]) == "both"
    # bar n0 + 1: the sized change alone is above the 0.2 band, the signal change is 0.05
    row = tracker.rows[-1]
    assert abs(row["allocation_change"]) >= 0.2
    assert row["sizing_signal_change"] == pytest.approx(0.05)
    assert row["approved_rebalance"] is True and _passed_on(row) == "sized"
    assert len(execn.calls) == 2
    assert execn.calls[1]["target_allocation"] == pytest.approx(_expected_alloc(10.5, jump), rel=1e-12)
    assert bot._held_signal_allocation[SYMBOL] == pytest.approx(1.05)   # the signal this position was set from


def _alternating_closes(n, step=0.01):
    """Constant-vol closes (+step, -step, ...): the realised vol barely moves bar to bar."""
    out = [100.0]
    for i in range(n - 1):
        out.append(out[-1] * ((1.0 + step) if i % 2 == 0 else 1.0 / (1.0 + step)))
    return out


def test_a_small_signal_move_with_a_small_sized_move_is_rejected():
    n0 = _first_bar_with_a_full_window()
    closes = _alternating_closes(n0 + 2)
    bot, execn, tracker, rm = _make_bot(SIZING, [0.0] * n0 + [10.0, 10.5])
    _run(bot, closes)
    row = tracker.rows[-1]
    assert abs(row["allocation_change"]) < 0.2                    # precondition: sized move below the band
    assert row["sizing_signal_change"] == pytest.approx(0.05)
    assert row["approved_rebalance"] is False and _passed_on(row) is None
    assert len(execn.calls) == 1                                  # rejected: no second order
    assert rm.calls[-1][2] is False and rm.calls[-1][1]["signal_change"] == pytest.approx(0.05)
    assert bot._held_signal_allocation[SYMBOL] == 1.0             # unchanged on a rejection


def test_a_large_signal_move_with_a_small_sized_move_passes_on_signal():
    """Book already within 0.1 of the sized target, signal moved 1.0 from the held 0.0: the signal
    path passes (the order is the small re-centre to the sized target)."""
    n0 = _first_bar_with_a_full_window()
    closes = _closes(n0 + 1, seed=21, vol=0.01)
    t0 = _expected_alloc(10.0, closes)
    bot, execn, tracker, rm = _make_bot(SIZING, [10.0], start_alloc=t0 - 0.1)
    bot.strategy.data_buffer.closes = list(closes[:n0])           # restarted bot with its history loaded
    _drive(bot, n0, closes[n0])
    row = tracker.rows[-1]
    assert row["allocation_change"] == pytest.approx(0.1) and abs(row["allocation_change"]) < 0.2
    assert row["sizing_signal_change"] == pytest.approx(1.0)
    assert row["approved_rebalance"] is True and _passed_on(row) == "signal"
    assert execn.calls[0]["target_allocation"] == pytest.approx(t0, rel=1e-12)
    assert bot._held_signal_allocation[SYMBOL] == 1.0


def test_both_paths_over_the_threshold_report_both():
    n0 = _first_bar_with_a_full_window()
    closes = _closes(n0 + 1, seed=22, vol=0.01)
    bot, execn, tracker, rm = _make_bot(SIZING, [0.0] * n0 + [10.0])
    _run(bot, closes)
    assert _passed_on(tracker.rows[-1]) == "both"


def test_the_40_bar_restart_probe_recentres_on_bar_one():
    """Restart with the book at 1.5, held signal 0.0 (a fresh bot), signal 0.1 and a sized target of
    ~0.2: the signal moved only 0.1 (below the band) but the SIZED change (about -1.3) passes on bar one."""
    n0 = _first_bar_with_a_full_window()
    closes = _closes(n0 + 40, seed=23, vol=0.0052)                # realised ~0.1 annualised -> sized ~2 x signal
    t0 = _expected_alloc(1.0, closes[:n0 + 1])
    assert 0.1 < t0 < 0.3                                         # precondition: sized target ~0.2
    bot, execn, tracker, rm = _make_bot(SIZING, [1.0] * 40, start_alloc=1.5)
    bot.strategy.data_buffer.closes = list(closes[:n0])
    for k in range(40):
        _drive(bot, n0 + k, closes[n0 + k])
        if k == 0:
            assert len(execn.calls) == 1                          # the re-centre happens on bar ONE
            assert execn.calls[0]["target_allocation"] == pytest.approx(t0, rel=1e-12)
            assert execn.calls[0]["actual_allocation"] == 1.5
            assert tracker.rows[0]["sizing_signal_change"] == pytest.approx(0.1)   # < 0.2: the signal path alone would wait
            assert _passed_on(tracker.rows[0]) == "sized"
            assert bot._held_signal_allocation[SYMBOL] == pytest.approx(0.1)
    assert len(tracker.rows) == 40


def test_volatility_alone_resizes_the_book_down_with_the_signal_steady():
    """Entered at the cap in calm vol; vol jumps, the signal never moves: the book is resized down
    as soon as the sized change reaches the threshold."""
    n0 = _first_bar_with_a_full_window()
    calm = _closes(n0 + 4, seed=24, vol=0.002)
    shock = [calm[-1] * 1.06, calm[-1] * 1.06 * 0.94]            # then a violent pair of bars
    closes = calm + shock
    bot, execn, tracker, rm = _make_bot(SIZING, [0.0] * n0 + [10.0] * (len(closes) - n0))
    _run(bot, closes)
    assert execn.calls[0]["target_allocation"] == 2.0             # entered at the cap in calm vol
    for r in tracker.rows[n0 + 1:n0 + 4]:                         # calm bars after entry: capped target unchanged
        assert r["allocation_change"] == 0.0
    assert len(execn.calls) >= 2
    resize = execn.calls[1]
    assert resize["target_allocation"] < 2.0 - 0.2
    row = next(r for r in tracker.rows if r["approved_rebalance"] and r["sizing_target_allocation"] < 1.8)
    assert row["sizing_signal_change"] == 0.0                     # the signal never moved
    assert _passed_on(row) == "sized"
    assert bot._held_signal_allocation[SYMBOL] == 1.0


def test_unmeasurable_volatility_flatten_holds_signal_zero_then_the_book_re_enters():
    """D-176 safety review (Finding 3): a successful order to 0.0 BECAUSE volatility could not be
    measured leaves the remembered signal at 0.0, not at the signal; when volatility recovers with
    the same signal, the book re-enters."""
    n0 = _first_bar_with_a_full_window()
    w = SIZING["window"]
    closes = _closes(n0 + 1 + w + 2, seed=25, vol=0.01)
    closes[n0 + 1] = 0.0                                          # an unmeasurable close
    bot, execn, tracker, rm = _make_bot(SIZING, [0.0] * n0 + [10.0] * (len(closes) - n0))
    for i in range(n0 + 1):
        _drive(bot, i, closes[i])
    assert bot._held_signal_allocation[SYMBOL] == 1.0 and len(execn.calls) == 1
    _drive(bot, n0 + 1, closes[n0 + 1])                           # vol unmeasurable: sized to flat
    assert bot.forecast_manager.last_realised_vol is None
    assert execn.calls[-1]["target_allocation"] == 0.0 and len(execn.calls) == 2
    assert bot._held_signal_allocation[SYMBOL] == 0.0             # not 1.0
    for i in range(n0 + 2, n0 + 2 + w):                           # the bad close is still inside the window
        _drive(bot, i, closes[i])
        assert len(execn.calls) == 2
    _drive(bot, n0 + 2 + w, closes[n0 + 2 + w])                   # the window is clean again
    assert bot.forecast_manager.last_realised_vol is not None
    assert len(execn.calls) == 3
    assert execn.calls[-1]["target_allocation"] == pytest.approx(
        _expected_alloc(10.0, closes[:n0 + 3 + w]), rel=1e-12)
    assert tracker.rows[-1]["sizing_signal_change"] == pytest.approx(1.0)   # judged against the held 0.0
    assert bot._held_signal_allocation[SYMBOL] == 1.0


def test_the_signal_is_judged_against_the_held_signal_not_the_previous_bar():
    """A slowly moving signal (+0.1 a bar) never trades on a last-bar delta; it trades once it has
    moved a full band from where the position was set, and orders the sized target."""
    n0 = _first_bar_with_a_full_window()
    closes = _alternating_closes(n0 + 4)                          # steady vol: the sized path stays out of the way
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


_DATA = pd.DataFrame({"timestamp": [pd.Timestamp("2024-04-01")]})


@pytest.mark.parametrize("sized, signal, passed, on", [
    (0.01, 0.5, True, "signal"),
    (0.9, 0.05, True, "sized"),
    (0.9, 0.5, True, "both"),
    (0.01, 0.05, False, None),
    (0.0, -0.3, True, "signal"),                                  # a sign does not matter
    (-0.9, 0.0, True, "sized"),
    (0.2 - 5e-7, 0.0, True, "sized"),                             # the same 1e-6 tolerance as the legacy band
    (0.0, 0.2 - 5e-7, True, "signal"),
    (0.2 - 2e-6, 0.2 - 2e-6, False, None),
])
def test_with_a_block_the_band_passes_on_either_change(sized, signal, passed, on):
    rm = RiskManager({"min_allocation_change": {"threshold": 0.2}})
    ok, dbg = rm.approve_allocation_change(SYMBOL, sized, _DATA, signal_change=signal)
    assert ok is passed
    assert dbg["controls"]["min_allocation_change"] == {"passed": passed, "passed_on": on}


def test_without_a_block_the_band_judges_the_sized_change_exactly_as_before():
    rm = RiskManager({"min_allocation_change": {"threshold": 0.2}})
    assert rm.approve_allocation_change(SYMBOL, 0.01, _DATA)[0] is False
    ok, dbg = rm.approve_allocation_change(SYMBOL, 0.9, _DATA)
    assert ok is True and dbg["controls"]["min_allocation_change"] == {"passed": True}   # no passed_on key
    assert rm.approve_allocation_change(SYMBOL, 0.9, _DATA, signal_change=None)[0] is True
    assert rm.approve_allocation_change(SYMBOL, 0.01, _DATA, signal_change=None)[0] is False


def test_the_pre_d176_sized_judgement_is_a_subset_of_the_block_rule():
    """Every sized change the legacy band passed, the block rule passes; it adds the signal path."""
    rm = RiskManager({"min_allocation_change": {"threshold": 0.2}})
    for sized in np.linspace(-2.0, 2.0, 81):
        legacy = rm.approve_allocation_change(SYMBOL, float(sized), _DATA)[0]
        for signal in (0.0, 0.05, 0.19, 1.0):
            if legacy:
                assert rm.approve_allocation_change(SYMBOL, float(sized), _DATA, signal_change=signal)[0] is True


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_a_non_finite_signal_change_falls_back_to_the_sized_change(bad):
    rm = RiskManager({"min_allocation_change": {"threshold": 0.2}})
    ok, dbg = rm.approve_allocation_change(SYMBOL, 0.9, _DATA, signal_change=bad)
    assert ok is True and dbg["controls"]["min_allocation_change"] == {"passed": True, "passed_on": "sized"}
    ok, dbg = rm.approve_allocation_change(SYMBOL, 0.05, _DATA, signal_change=bad)
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


# --------------------------------------------------------------------------- V19: every volatility-dividing op

VOL_OPS = {
    "vol_target": VOL_TARGET_OP,
    "vol_normalize": {"op": "vol_normalize", "params": {}},
    "vol_adjusted": {"op": "vol_adjusted", "params": {}},
}


@pytest.mark.parametrize("op", sorted(VOL_OPS))
def test_every_volatility_dividing_op_in_transforms_beside_a_block_is_refused_as_sized_twice(op):
    cfg = _base_cfg()
    comp = cfg["strategies"]["regimes"]["unknown"]["components"][0]
    comp["transforms"].append(copy.deepcopy(VOL_OPS[op]))
    assert _v19(cfg) == []                                        # no block: accepted as before
    cfg["strategies"]["sizing"] = dict(SIZING)
    msgs = _v19(cfg)
    assert len(msgs) == 1 and "sized twice" in msgs[0]
    assert "components[0].transforms[2]" in msgs[0]
    if op == "vol_target":
        assert f"this {op} op sizes the forecast" in msgs[0] and f"remove the {op} op" in msgs[0]
    else:
        assert f"this {op} op in transforms sizes the forecast" in msgs[0]
        for words in ("before standardise", "in the component", "as a regime"):
            assert words in msgs[0]


def test_vol_normalize_in_history_transforms_is_accepted_beside_a_block():
    """standardise divides it out (STRATEGY_DESIGN_GUIDE.md:301): it does not size the forecast."""
    cfg = _base_cfg()
    cfg["strategies"]["regimes"]["unknown"]["components"][0]["history_transforms"] = [copy.deepcopy(VOL_OPS["vol_normalize"])]
    assert _v19(cfg) == []
    cfg["strategies"]["sizing"] = dict(SIZING)
    assert _v19(cfg) == []


def test_vol_adjusted_in_history_transforms_beside_a_block_is_refused_as_sized_twice():
    """operator 2026-10-22: vol_adjusted is refused in both lists (the earlier ruling allowing it is withdrawn)."""
    cfg = _base_cfg()
    cfg["strategies"]["regimes"]["unknown"]["components"][0]["history_transforms"] = [copy.deepcopy(VOL_OPS["vol_adjusted"])]
    assert _v19(cfg) == []                                        # no block: accepted as before
    cfg["strategies"]["sizing"] = dict(SIZING)
    msgs = _v19(cfg)
    assert len(msgs) == 1 and "sized twice" in msgs[0] and "history_transforms[0]" in msgs[0]
    assert "this vol_adjusted op in history_transforms sizes the forecast" in msgs[0]
    for words in ("before standardise", "in the component", "as a regime"):
        assert words in msgs[0]


@pytest.mark.parametrize("op", ["vol_normalize", "vol_adjusted"])
def test_the_new_ops_in_transforms_are_found_at_top_level_and_nested_positions(op):
    cfg = _base_cfg()
    cfg["strategies"]["sizing"] = dict(SIZING)
    cfg["strategies"]["regimes"]["unknown"]["components"][0]["transforms"].append(copy.deepcopy(VOL_OPS[op]))
    cfg["regime_detector"]["components"] = [{"id": "d", "transforms": [copy.deepcopy(VOL_OPS[op])]}]
    cfg["strategies"]["regimes"]["unknown"]["blocks"] = [
        {"id": "b", "source": {"parts": [{"id": "p", "transforms": [copy.deepcopy(VOL_OPS[op])]}]}}]
    twice = [m for m in _v19(cfg) if "sized twice" in m]
    assert len(twice) == 3 and all(op in m and "before standardise" in m for m in twice)


def test_vol_target_in_history_transforms_beside_a_block_is_still_refused():
    cfg = _base_cfg()
    cfg["strategies"]["sizing"] = dict(SIZING)
    cfg["strategies"]["regimes"]["unknown"]["components"][0]["history_transforms"] = [copy.deepcopy(VOL_TARGET_OP)]
    msgs = _v19(cfg)
    assert len(msgs) == 1 and "sized twice" in msgs[0] and "history_transforms[0]" in msgs[0]


# --------------------------------------------------------------------------- real AdvancedStrategy + RollingBuffer warm-up

def _synthetic_df():
    return pd.read_csv(FIXTURES / "d176" / "synthetic_daily_ohlcv.csv", parse_dates=["timestamp"])


def _run099_sized_config(tmp_path, *, with_block):
    cfg = json.loads(RUN_099.read_text())
    comp = cfg["strategies"]["regimes"]["unknown"]["components"][0]
    comp["transforms"] = [t for t in comp["transforms"] if t["op"] != "vol_target"]
    if with_block:
        cfg["strategies"]["sizing"] = {"kind": "vol_target", "window": 60, "target_annual_vol": 0.2,
                                       "periods_per_year": 365}
    assert [m for m in validate(cfg) if "V19" in m] == []
    p = tmp_path / ("sized.json" if with_block else "plain.json")
    p.write_text(json.dumps(cfg))
    return str(p)


def test_real_strategy_warmup_with_a_block_and_the_first_sized_allocation(tmp_path):
    """The real AdvancedStrategy (and its RollingBuffer) over the synthetic series: no allocation
    before required_bars = max(existing, window + 1); the first sized allocation equals
    forecast / 10 * target / realised (hand-computed from the series), clipped."""
    plain = AdvancedStrategy(config_path=_run099_sized_config(tmp_path, with_block=False))
    strat = AdvancedStrategy(config_path=_run099_sized_config(tmp_path, with_block=True))
    assert strat.sizing is not None and plain.sizing is None
    assert strat.required_bars == max(plain.required_bars, 60 + 1)
    fm = ForecastManager(sizing=strat.sizing)
    df = _synthetic_df()
    closes = df["close"].to_numpy(dtype=float)

    first_alloc_bar = None
    for i in range(len(df)):
        strat.update(df.iloc[i:i + 1])
        signal = strat.generate_signals()
        buf = strat.data_buffer.get_df()["close"].to_numpy(dtype=float)
        # the buffer is a bounded deque; it always holds >= window + 1 closes once they exist, the
        # bar being decided is the last one, and the tail equals the series
        assert min(i + 1, 61) <= len(buf) <= i + 1 and buf[-1] == closes[i]
        assert (buf == closes[i + 1 - len(buf):i + 1]).all()
        alloc = fm.forecast_to_allocation(signal.forecast, closes=buf)
        if i + 1 < strat.required_bars:
            assert not strat.is_ready() and signal.forecast == 0.0 and alloc == 0.0   # no allocation yet
        if alloc != 0.0:
            first_alloc_bar = i
            break
    assert first_alloc_bar is not None and first_alloc_bar + 1 >= strat.required_bars
    f = signal.forecast
    tail = closes[first_alloc_bar - 60:first_alloc_bar + 1]
    realised = float(np.std(tail[1:] / tail[:-1] - 1.0, ddof=1)) * math.sqrt(365)
    want = min(max(f / 10.0 * 0.2 / realised, -2.0), 2.0)
    assert alloc == pytest.approx(want, rel=1e-12) and f > 0
    assert fm.last_realised_vol == pytest.approx(realised, rel=1e-12)


# --------------------------------------------------------------------------- PortfolioRiskGate acts on the SIZED target

def test_the_risk_gate_cap_clamps_the_sized_target_not_the_signal():
    n0 = _first_bar_with_a_full_window()
    closes = _closes(n0 + 1, seed=31, vol=0.01)
    sized = _expected_alloc(10.0, closes)                         # ~1: above the 0.5 cap, signal is 1.0
    assert sized > 0.5
    gate = PortfolioRiskGate({"absolute_allocation_cap": {"cap": 0.5}})
    bot, execn, tracker, rm = _make_bot(SIZING, [0.0] * n0 + [10.0], gate=gate)
    _run(bot, closes)
    row = tracker.rows[-1]
    assert row["risk_target_raw"] == pytest.approx(sized, rel=1e-12)   # the gate saw the sized target
    assert row["risk_cap_clamped"] is True
    assert execn.calls[0]["target_allocation"] == 0.5
    assert row["sizing_target_allocation"] == pytest.approx(sized, rel=1e-12)  # telemetry keeps the pre-gate size
    assert bot._held_signal_allocation[SYMBOL] == 1.0


def test_the_risk_gate_kill_flattens_a_sized_book_through_the_bypass():
    n0 = _first_bar_with_a_full_window()
    closes = _closes(n0 + 3, seed=32, vol=0.01)
    gate = PortfolioRiskGate({"max_drawdown_kill": {"threshold": 0.25}})
    bot, execn, tracker, rm = _make_bot(SIZING, [0.0] * n0 + [10.0] * 3, gate=gate)
    bot.portfolio_info.set_equity(100.0)
    for i in range(n0 + 1):
        _drive(bot, i, closes[i])
    assert len(execn.calls) == 1 and bot._held_signal_allocation[SYMBOL] == 1.0
    held_alloc = execn.calls[0]["target_allocation"]
    bot.portfolio_info.set_equity(70.0)                           # 30% drawdown: the kill trips
    _drive(bot, n0 + 1, closes[n0 + 1])
    assert gate.killed is True
    assert len(execn.calls) == 2 and execn.calls[1]["target_allocation"] == 0.0
    assert execn.calls[1]["actual_allocation"] == pytest.approx(held_alloc)
    assert len(rm.calls) == 1                                     # the flatten bypassed the band
    assert tracker.rows[-1]["succcess_execute_portfolio_rebalance"] is True
    assert bot._held_signal_allocation[SYMBOL] == 0.0             # a forced flat forgets the signal
