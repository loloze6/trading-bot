"""
Integration tests for the execution pipeline.

Tests verify a full trade round-trip through:
  MockPortfolioInfo → MockExecutionHandler → EnhancedPerformanceTracker → CompletedTrade

No BacktestEngine or DataManager required — the execution layer is wired directly.
"""

import pytest
from conftest import make_ohlcv


COMMISSION = 0.001
INITIAL_USDT = 10_000.0


@pytest.fixture
def stack():
    """Wire up the three core components used in backtesting."""
    from execution.portfolio_info import MockPortfolioInfo
    from execution.execution_handler import MockExecutionHandler
    from performance.metrics import EnhancedPerformanceTracker

    portfolio = MockPortfolioInfo(
        initial_balance={"USDT": {"free": INITIAL_USDT, "locked": 0.0}},
        commission_rate=COMMISSION,
    )
    tracker = EnhancedPerformanceTracker(
        commission_rate=COMMISSION,
        initial_capital=INITIAL_USDT,
    )
    handler = MockExecutionHandler(performance_tracker=tracker, portfolio_info=portfolio)
    return handler, portfolio, tracker


def make_data(close_price: float, n: int = 50):
    """Return a minimal OHLCV DataFrame with a specific last close price."""
    data = make_ohlcv(n_bars=n, start_price=close_price, trend=0.0, volatility=0.0, seed=42)
    return data


# ---------------------------------------------------------------------------
# LONG round-trip
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestLongRoundTrip:
    def test_open_long_returns_filled(self, stack):
        handler, portfolio, tracker = stack
        data = make_data(50_000.0)
        result = handler.open_long_position("BTCUSDT", quantity=0.1, data=data)
        assert result["status"] == "FILLED"

    def test_close_long_returns_filled(self, stack):
        handler, portfolio, tracker = stack
        data = make_data(50_000.0)

        handler.open_long_position("BTCUSDT", quantity=0.1, data=data)
        portfolio.update_local_balance("BTCUSDT", data["close"].iloc[-1], 0.1, "LONG")

        result = handler.close_position("BTCUSDT", data=data)
        assert result["status"] == "FILLED"

    def test_profitable_long_produces_positive_pnl(self, stack):
        """Buy at 50k, sell at 55k → expect positive P&L."""
        handler, portfolio, tracker = stack

        entry_data = make_data(50_000.0)
        handler.open_long_position("BTCUSDT", quantity=0.1, data=entry_data)
        portfolio.update_local_balance("BTCUSDT", 50_000.0, 0.1, "LONG")

        exit_data = make_data(55_000.0)
        handler.close_position("BTCUSDT", data=exit_data)

        completed = tracker.completed_trades
        assert len(completed) == 1, f"Expected 1 completed trade, got {len(completed)}"
        trade = completed[0]
        assert trade.profit_loss_absolute > 0, (
            f"Expected positive P&L on buy@50k sell@55k, got {trade.profit_loss_absolute}"
        )

    def test_losing_long_produces_negative_pnl(self, stack):
        """Buy at 55k, sell at 50k → expect negative P&L."""
        handler, portfolio, tracker = stack

        entry_data = make_data(55_000.0)
        handler.open_long_position("BTCUSDT", quantity=0.1, data=entry_data)
        portfolio.update_local_balance("BTCUSDT", 55_000.0, 0.1, "LONG")

        exit_data = make_data(50_000.0)
        handler.close_position("BTCUSDT", data=exit_data)

        completed = tracker.completed_trades
        assert len(completed) == 1
        trade = completed[0]
        assert trade.profit_loss_absolute < 0, (
            f"Expected negative P&L on buy@55k sell@50k, got {trade.profit_loss_absolute}"
        )

    def test_pnl_magnitude_matches_price_move(self, stack):
        """P&L ≈ (exit - entry) × qty for a LONG (before commission)."""
        handler, portfolio, tracker = stack
        qty = 0.1
        entry_price = 50_000.0
        exit_price = 52_000.0

        handler.open_long_position("BTCUSDT", quantity=qty, data=make_data(entry_price))
        portfolio.update_local_balance("BTCUSDT", entry_price, qty, "LONG")
        handler.close_position("BTCUSDT", data=make_data(exit_price))

        trade = tracker.completed_trades[0]
        expected_gross = (exit_price - entry_price) * trade.matched_quantity
        assert trade.profit_loss_absolute == pytest.approx(expected_gross, rel=1e-6)

    def test_completed_trade_side_is_long(self, stack):
        from performance.metrics import PositionSide
        handler, portfolio, tracker = stack
        data = make_data(50_000.0)
        handler.open_long_position("BTCUSDT", quantity=0.1, data=data)
        portfolio.update_local_balance("BTCUSDT", 50_000.0, 0.1, "LONG")
        handler.close_position("BTCUSDT", data=make_data(51_000.0))

        trade = tracker.completed_trades[0]
        assert trade.side == PositionSide.LONG


# ---------------------------------------------------------------------------
# SHORT round-trip
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestShortRoundTrip:
    def test_open_short_returns_filled(self, stack):
        handler, portfolio, tracker = stack
        data = make_data(50_000.0)
        result = handler.open_short_position("BTCUSDT", quantity=-0.1, data=data)
        assert result["status"] == "FILLED"

    def test_close_short_returns_filled(self, stack):
        handler, portfolio, tracker = stack
        data = make_data(50_000.0)

        handler.open_short_position("BTCUSDT", quantity=-0.1, data=data)
        portfolio.update_local_balance("BTCUSDT", 50_000.0, 0.1, "SHORT")

        result = handler.close_position("BTCUSDT", data=data)
        assert result["status"] == "FILLED"

    def test_profitable_short_produces_positive_pnl(self, stack):
        """Short at 55k, cover at 50k → expect positive P&L."""
        handler, portfolio, tracker = stack

        entry_data = make_data(55_000.0)
        handler.open_short_position("BTCUSDT", quantity=-0.1, data=entry_data)
        portfolio.update_local_balance("BTCUSDT", 55_000.0, 0.1, "SHORT")

        exit_data = make_data(50_000.0)
        handler.close_position("BTCUSDT", data=exit_data)

        completed = tracker.completed_trades
        assert len(completed) == 1
        trade = completed[0]
        assert trade.profit_loss_absolute > 0, (
            f"Expected positive P&L on short@55k cover@50k, got {trade.profit_loss_absolute}"
        )

    def test_losing_short_produces_negative_pnl(self, stack):
        """Short at 50k, cover at 55k → expect negative P&L."""
        handler, portfolio, tracker = stack

        entry_data = make_data(50_000.0)
        handler.open_short_position("BTCUSDT", quantity=-0.1, data=entry_data)
        portfolio.update_local_balance("BTCUSDT", 50_000.0, 0.1, "SHORT")

        exit_data = make_data(55_000.0)
        handler.close_position("BTCUSDT", data=exit_data)

        completed = tracker.completed_trades
        assert len(completed) == 1
        trade = completed[0]
        assert trade.profit_loss_absolute < 0, (
            f"Expected negative P&L on short@50k cover@55k, got {trade.profit_loss_absolute}"
        )


# ---------------------------------------------------------------------------
# Tracker state consistency
# ---------------------------------------------------------------------------

@pytest.mark.integration
class TestTrackerConsistency:
    def test_no_completed_trades_before_close(self, stack):
        handler, portfolio, tracker = stack
        data = make_data(50_000.0)
        handler.open_long_position("BTCUSDT", quantity=0.1, data=data)
        assert len(tracker.completed_trades) == 0

    def test_single_round_trip_produces_exactly_one_completed_trade(self, stack):
        """One open + one close must produce exactly one CompletedTrade."""
        handler, portfolio, tracker = stack
        entry_price = 50_000.0
        exit_price = 51_000.0

        handler.open_long_position("BTCUSDT", quantity=0.1, data=make_data(entry_price))
        portfolio.update_local_balance("BTCUSDT", entry_price, 0.1, "LONG")
        handler.close_position("BTCUSDT", data=make_data(exit_price))

        assert len(tracker.completed_trades) == 1
