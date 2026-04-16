"""Unit tests for ForecastManager."""

import pytest
from execution.forecast_manager import ForecastManager


@pytest.fixture
def fm():
    return ForecastManager(
        max_forecast=20.0,
        min_forecast=-20.0,
        max_allocation=1.0,
        min_allocation=-1.0,
        rebalance_threshold=0.05,
    )


@pytest.mark.unit
class TestForecastToAllocation:
    """forecast_to_allocation must be a linear map from [-20, +20] → [-1, +1]."""

    def test_zero_forecast_is_neutral(self, fm):
        assert fm.forecast_to_allocation(0.0) == pytest.approx(0.0)

    def test_max_forecast_is_full_long(self, fm):
        assert fm.forecast_to_allocation(20.0) == pytest.approx(1.0)

    def test_min_forecast_is_full_short(self, fm):
        assert fm.forecast_to_allocation(-20.0) == pytest.approx(-1.0)

    def test_half_forecast_is_half_allocation(self, fm):
        assert fm.forecast_to_allocation(10.0) == pytest.approx(0.5)
        assert fm.forecast_to_allocation(-10.0) == pytest.approx(-0.5)

    def test_linear_midpoints(self, fm):
        # f(5) = 0.25, f(-5) = -0.25
        assert fm.forecast_to_allocation(5.0) == pytest.approx(0.25)
        assert fm.forecast_to_allocation(-5.0) == pytest.approx(-0.25)

    def test_above_max_clamped_to_one(self, fm):
        # Forecast above 20 should be clamped, result is still 1.0
        result = fm.forecast_to_allocation(25.0)
        assert result == pytest.approx(1.0)

    def test_below_min_clamped_to_minus_one(self, fm):
        result = fm.forecast_to_allocation(-25.0)
        assert result == pytest.approx(-1.0)


@pytest.mark.unit
class TestNeedsRebalance:
    """needs_rebalance uses the ACTUAL market allocation, not stored target."""

    def test_no_rebalance_below_threshold(self, fm):
        # Change of 0.03 < threshold of 0.05
        needs, delta = fm.needs_rebalance("BTCUSDT", new_target=0.03, current_actual=0.0)
        assert needs is False
        assert delta == pytest.approx(0.03)

    def test_rebalance_above_threshold(self, fm):
        # Change of 0.10 > threshold of 0.05
        needs, delta = fm.needs_rebalance("BTCUSDT", new_target=0.10, current_actual=0.0)
        assert needs is True
        assert delta == pytest.approx(0.10)

    def test_rebalance_at_exactly_threshold(self, fm):
        # Change of 0.05 == threshold → must trigger (>= check)
        needs, delta = fm.needs_rebalance("BTCUSDT", new_target=0.05, current_actual=0.0)
        assert needs is True

    def test_sign_flip_long_to_short_triggers_rebalance(self, fm):
        # From +50% long to -50% short: change = -1.0, well above threshold
        needs, delta = fm.needs_rebalance("BTCUSDT", new_target=-0.5, current_actual=0.5)
        assert needs is True
        assert delta == pytest.approx(-1.0)

    def test_no_rebalance_when_already_at_target(self, fm):
        needs, delta = fm.needs_rebalance("BTCUSDT", new_target=0.5, current_actual=0.5)
        assert needs is False
        assert delta == pytest.approx(0.0)

    def test_negative_direction_detected(self, fm):
        # Small reduction below threshold should NOT rebalance
        needs, delta = fm.needs_rebalance("BTCUSDT", new_target=0.47, current_actual=0.50)
        assert needs is False

    def test_large_negative_reduction_triggers_rebalance(self, fm):
        needs, delta = fm.needs_rebalance("BTCUSDT", new_target=0.0, current_actual=0.50)
        assert needs is True
        assert delta == pytest.approx(-0.50)


@pytest.mark.unit
class TestGetPositionType:
    def test_positive_allocation_is_long(self, fm):
        fm.current_allocations["BTCUSDT"] = 0.5
        assert fm.get_position_type("BTCUSDT") == "LONG"

    def test_negative_allocation_is_short(self, fm):
        fm.current_allocations["BTCUSDT"] = -0.3
        assert fm.get_position_type("BTCUSDT") == "SHORT"

    def test_zero_allocation_is_neutral(self, fm):
        fm.current_allocations["BTCUSDT"] = 0.0
        assert fm.get_position_type("BTCUSDT") == "NEUTRAL"

    def test_unknown_symbol_is_neutral(self, fm):
        assert fm.get_position_type("UNKNOWN") == "NEUTRAL"
