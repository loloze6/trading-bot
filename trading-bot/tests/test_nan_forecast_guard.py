"""
Tests for CUL-274: a NaN forecast must never reach risk approval or order
execution, regardless of whether a risk_gate is configured.

Root cause: `generate_signals()` already returns forecast=0.0 explicitly when
not ready or on a caught exception (strategy_base.py) -- NaN is not what
warmup produces. NaN reaching `_process_symbol_candle_completion` means a
"ready" component silently produced a degenerate value (e.g. 0/0 in a
z-score) that numpy/pandas does not raise on. Unchecked, `abs(NaN) != 0.0`
is True and every `>`/`<` risk-threshold comparison against NaN is False, so
both PortfolioRiskGate (when configured) and RiskManager's own controls
silently "pass" a NaN allocation change through to a real order request.

These tests drive TradingBot._process_symbol_candle_completion directly over
lightweight stubs, same harness pattern as test_funding_accrual.py.
"""
import logging
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from execution.portfolio_info import MockPortfolioInfo
from core.trading_bot import TradingBot

SYMBOL = "BTCUSDT"


class _FakeSignal:
    def __init__(self, forecast=0.0):
        self.forecast = forecast


class _FakeStrategy:
    def __init__(self, forecast=0.0):
        self._forecast = forecast

    def update(self, data):
        pass

    def generate_signals(self):
        return _FakeSignal(self._forecast)


class _NaNForecastManager:
    """Mirrors ForecastManager.forecast_to_allocation's real shape: a NaN
    forecast maps straight through to a NaN target_allocation."""
    def forecast_to_allocation(self, forecast):
        return forecast / 10.0

    def calculate_allocation_change(self, target, previous):
        return target - previous


class _RaisingRiskGate:
    """A configured risk_gate whose own NaN guard (the real
    PortfolioRiskGate.apply() behavior) must never even be reached -- the
    fix must catch the NaN before this point. If it IS reached, fail the
    test loudly rather than silently matching the real guard's raise."""
    def observe(self, *a, **k):
        pass

    def apply(self, target_allocation):
        raise AssertionError(
            "risk_gate.apply() was reached with target_allocation="
            f"{target_allocation!r} -- the NaN guard in trading_bot.py "
            "should have raised before this point"
        )


class _FailIfCalledRiskManager:
    def approve_allocation_change(self, symbol, change, data):
        raise AssertionError(
            f"RiskManager.approve_allocation_change was reached with change={change!r} "
            "-- a NaN target_allocation must never reach risk approval"
        )


class _FailIfCalledExecutionHandler:
    def _execute_portfolio_rebalance(self, **kwargs):
        raise AssertionError(
            f"execution_handler._execute_portfolio_rebalance was reached with "
            f"kwargs={kwargs!r} -- a NaN allocation must never reach order execution"
        )


class _FakeDataManager:
    def __init__(self, bar_df):
        self.candle_builder = object()
        self._bar = bar_df

    def get_data_history(self, symbol, count=1):
        return self._bar


class _NoOpTracker:
    def record_state(self, *a, **k):
        pass


class _CaptureLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


def _bar(ts, close):
    return pd.DataFrame({"timestamp": [pd.Timestamp(ts)], "close": [close]})


def _portfolio():
    """Flat (no open position) so previous_allocation is exactly 0.0 and
    allocation_change assertions are unambiguous."""
    return MockPortfolioInfo(initial_balance={
        "USDT": {"free": 20000.0, "locked": 0.0},
        SYMBOL: {"free": 0.0, "locked": 0.0},
    })


def _build_bot(forecast, risk_gate=None, execution_handler=None, risk_manager=None):
    logger = logging.getLogger("test_nan_forecast_guard")
    capture = _CaptureLogHandler()
    logger.addHandler(capture)
    logger.setLevel(logging.DEBUG)

    bot = TradingBot(
        data_manager=_FakeDataManager(_bar("2024-01-01 00:00:00", 20000.0)),
        strategy=_FakeStrategy(forecast=forecast),
        execution_handler=execution_handler or _FailIfCalledExecutionHandler(),
        logger=logger,
        portfolio_info=_portfolio(),
        portfolio_state_tracker=_NoOpTracker(),
        forecast_manager=_NaNForecastManager(),
        risk_manager=risk_manager or _FailIfCalledRiskManager(),
        performance_tracker=None,
        symbols=[SYMBOL],
        risk_gate=risk_gate,
    )
    return bot, capture


def test_nan_forecast_never_reaches_risk_manager_no_gate():
    """Default config (no risk_gate): a NaN forecast must not reach
    RiskManager.approve_allocation_change or order execution."""
    bot, capture = _build_bot(forecast=float("nan"))
    # Must not raise out of the method -- caught internally and logged.
    bot._process_symbol_candle_completion(SYMBOL)

    error_records = [r for r in capture.records if r.levelno >= logging.ERROR]
    assert error_records, "expected an ERROR-level log for the NaN forecast"
    assert "NaN target_allocation" in error_records[0].getMessage()


def test_nan_forecast_never_reaches_configured_risk_gate():
    """With a risk_gate configured, the guard must fire BEFORE risk_gate.apply()
    -- proving the fix isn't just relying on the gate's own NaN check."""
    bot, capture = _build_bot(forecast=float("nan"), risk_gate=_RaisingRiskGate())
    bot._process_symbol_candle_completion(SYMBOL)

    error_records = [r for r in capture.records if r.levelno >= logging.ERROR]
    assert error_records, "expected an ERROR-level log for the NaN forecast"
    assert "NaN target_allocation" in error_records[0].getMessage()


def test_normal_forecast_unaffected_byte_identical_path():
    """A normal, non-NaN forecast must still reach RiskManager exactly as
    before -- the guard must not change behavior on legitimate input."""
    approvals = []

    class _RecordingRiskManager:
        def approve_allocation_change(self, symbol, change, data):
            approvals.append(change)
            return False, {}  # reject, so execution_handler is never called

    bot, capture = _build_bot(forecast=5.0, risk_manager=_RecordingRiskManager())
    bot._process_symbol_candle_completion(SYMBOL)

    assert approvals == [pytest.approx(0.5)]  # 5.0/10 - 0.0 previous allocation
    assert not [r for r in capture.records if r.levelno >= logging.ERROR]


def test_zero_forecast_from_not_ready_or_error_unaffected():
    """The pre-existing, already-correct path: generate_signals() returning
    forecast=0.0 (warmup / caught exception) must not trip the new guard at
    all -- 0.0 is a valid float, not NaN."""
    approvals = []

    class _RecordingRiskManager:
        def approve_allocation_change(self, symbol, change, data):
            approvals.append(change)
            return False, {}

    bot, capture = _build_bot(forecast=0.0, risk_manager=_RecordingRiskManager())
    bot._process_symbol_candle_completion(SYMBOL)

    # allocation_change = 0.0 - 0.0 = 0.0 -> never even reaches risk_manager
    assert approvals == []
    assert not [r for r in capture.records if r.levelno >= logging.ERROR]
