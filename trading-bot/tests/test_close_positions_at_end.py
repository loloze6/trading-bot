"""
Regression guard for TradingBot._close_all_positions_at_end (core/trading_bot.py:324).

Two NameErrors lived in that method, both dormant because the method only runs when a
backtest ends holding an OPEN position -- the reference window (2024-04-01 -> 2024-05-30)
ends flat, so every baseline in this fork was measured without executing the body.

  1. `postRebalance_current_allocation = ... if success else previous_allocation` (:374).
     `previous_allocation` is defined nowhere in the method; the in-scope name holding the
     pre-rebalance allocation is `actual_allocation`. Python evaluates only the taken
     branch of a ternary, so the undefined name is invisible until the close rebalance
     FAILS -- exactly the path that matters, since it is the one that has to record what
     the portfolio still holds.

  2. The `else:` of `if abs(allocation_change) != 0.0:` (:367, position open but the
     computed change is zero) never binds `success_execute_portfolio_rebalance` or
     `debug_execute_portfolio_rebalance`, yet :371-374 and the record_state call below
     read both unconditionally.

Neither NameError propagates: the per-symbol body is wrapped in `except Exception` (:399),
which logs and moves on. So the observable damage is silent -- the close bar is simply
never recorded into portfolio_states.csv -- and the assertions below check exactly that
pair of consequences (nothing logged from the exception handler; the close bar recorded).

Both tests drive the real engine through run_backtest. Faults are injected at public
collaborator methods (MockExecutionHandler._execute_portfolio_rebalance,
ForecastManager.calculate_allocation_change) and scoped to the close by a flag raised
around TradingBot.stop() -- the private method under test is never called directly, and
every value it reads is one the engine actually produced.
"""
import logging
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Measured window: the last bar the engine processes for this window is 2024-10-05 21:00,
# at which the default strategy_config.json holds a LONG BTCUSDT position -- so
# _close_all_positions_at_end runs for real. Found by probing bar-by-bar open-position
# state; no config tweak needed. Well clear of the sealed 2026 holdout, and the start is
# late enough to keep the run near 500 bars (~2.5s) rather than marking these tests slow.
# test_window_still_ends_with_an_open_position below fails loudly if this ever stops
# holding, since a flat ending would make both regression tests vacuously pass.
START_DATE = "2024-09-15"
END_DATE = "2024-10-05"
SYMBOL = "BTCUSDT"


class _RecordingHandler(logging.Handler):
    """Collects records emitted while the end-of-backtest close runs."""

    def __init__(self, sink):
        super().__init__(level=logging.NOTSET)
        self.sink = sink

    def emit(self, record):
        self.sink.append(record)


class _CloseResult:
    """What one instrumented backtest observed about its end-of-backtest close."""

    def __init__(self):
        self.records = []
        self.open_symbols_at_close = []
        self.states_recorded_during_close = 0


def _run_backtest_with_close_fault(monkeypatch, results_dir, install_fault):
    """Run the window end to end with `install_fault` active only during the close."""
    from core.launcher import run_backtest
    from core.trading_bot import TradingBot

    result = _CloseResult()
    closing = {"active": False}
    handler = _RecordingHandler(result.records)
    original_stop = TradingBot.stop

    def stop(self):
        tracker = self.portfolio_state_tracker
        states_before = len(tracker.states)
        result.open_symbols_at_close = sorted(self.performance_tracker.get_open_positions())
        self.logger.addHandler(handler)
        closing["active"] = True
        try:
            return original_stop(self)
        finally:
            closing["active"] = False
            self.logger.removeHandler(handler)
            result.states_recorded_during_close = len(tracker.states) - states_before

    monkeypatch.setattr(TradingBot, "stop", stop)
    install_fault(monkeypatch, closing)

    run_backtest(
        config_path=str(PROJECT_ROOT / "strategy_config.json"),
        symbol=SYMBOL,
        start=START_DATE,
        end=END_DATE,
        results_root=str(results_dir),
        # Keep the tracker's interim trades.json out of the shared results dir (D4).
        trades_log_file=str(Path(results_dir) / "interim_trades.json"),
    )
    return result


def _reject_the_close_order(monkeypatch, closing):
    """Make the close rebalance report failure, as a rejected order would."""
    from execution.execution_handler import MockExecutionHandler

    original = MockExecutionHandler._execute_portfolio_rebalance

    def _execute_portfolio_rebalance(self, *args, **kwargs):
        if closing["active"]:
            return False, {"error": "injected: close order rejected"}
        return original(self, *args, **kwargs)

    monkeypatch.setattr(
        MockExecutionHandler, "_execute_portfolio_rebalance", _execute_portfolio_rebalance
    )


def _zero_the_close_allocation_change(monkeypatch, closing):
    """Make the close compute a zero allocation change against an open position.

    Reached for real when the pre-close allocation is already 0.0 while the tracker still
    holds the position -- a wiped-out total portfolio value (the `total_value > 0` guard in
    MockPortfolioInfo._calculate_actual_allocation returns 0.0 flat) or tracker/balance
    divergence. Both are hard to stage end to end, so the arithmetic that selects the
    branch is forced here instead; everything else in the run is real.
    """
    from execution.forecast_manager import ForecastManager

    original = ForecastManager.calculate_allocation_change

    def calculate_allocation_change(self, target_allocation, current_allocation):
        if closing["active"]:
            return 0.0
        return original(self, target_allocation, current_allocation)

    monkeypatch.setattr(
        ForecastManager, "calculate_allocation_change", calculate_allocation_change
    )


def _close_path_errors(records):
    """Records the `except Exception` handler at core/trading_bot.py:399 emitted."""
    return [r for r in records if "Error closing" in r.getMessage()]


def _describe(records):
    return "; ".join(
        f"{r.getMessage()} [{r.exc_info[1]!r}]" if r.exc_info else r.getMessage()
        for r in records
    )


@pytest.fixture(scope="module")
def rejected_close(tmp_path_factory):
    with pytest.MonkeyPatch.context() as monkeypatch:
        yield _run_backtest_with_close_fault(
            monkeypatch, tmp_path_factory.mktemp("rejected_close"), _reject_the_close_order
        )


@pytest.fixture(scope="module")
def zero_change_close(tmp_path_factory):
    with pytest.MonkeyPatch.context() as monkeypatch:
        yield _run_backtest_with_close_fault(
            monkeypatch,
            tmp_path_factory.mktemp("zero_change_close"),
            _zero_the_close_allocation_change,
        )


def test_window_still_ends_with_an_open_position(rejected_close):
    """Anti-vacuity guard: a flat ending would skip the method these tests cover."""
    assert rejected_close.open_symbols_at_close == [SYMBOL], (
        f"{START_DATE}..{END_DATE} no longer ends holding {SYMBOL}, so "
        "_close_all_positions_at_end returns early and the two regression tests below "
        "prove nothing. Re-probe for a window whose final bar holds a position."
    )


def test_close_survives_a_rejected_close_order(rejected_close):
    errors = _close_path_errors(rejected_close.records)
    assert not errors, (
        "_close_all_positions_at_end raised when the close rebalance reported failure: "
        f"{_describe(errors)}"
    )


def test_rejected_close_order_still_records_the_close_bar(rejected_close):
    assert rejected_close.states_recorded_during_close == 1, (
        "the close bar must reach the portfolio state tracker even when the close "
        f"rebalance fails; recorded {rejected_close.states_recorded_during_close} rows"
    )


def test_close_survives_a_zero_allocation_change(zero_change_close):
    errors = _close_path_errors(zero_change_close.records)
    assert not errors, (
        "_close_all_positions_at_end raised on the zero-allocation-change branch: "
        f"{_describe(errors)}"
    )


def test_zero_allocation_change_still_records_the_close_bar(zero_change_close):
    assert zero_change_close.states_recorded_during_close == 1, (
        "the close bar must reach the portfolio state tracker on the zero-change branch; "
        f"recorded {zero_change_close.states_recorded_during_close} rows"
    )
