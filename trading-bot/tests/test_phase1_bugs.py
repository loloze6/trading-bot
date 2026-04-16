"""
Phase 1 bug-fix regression tests.

Each test corresponds to a named bug from the lead-dev assessment.
They are designed to fail on the unfixed code and pass after the fix.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from conftest import make_ohlcv


# ---------------------------------------------------------------------------
# B2 — CompositeStrategy must not shadow the ComponentOutput class name
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_composite_forecast_returns_correct_types(ohlcv_default):
    """
    CompositeStrategy.generate_forecast() previously shadowed ComponentOutput
    with a local variable of the same name.  Verify the return types are correct
    and no NameError is raised.
    """
    from strategies.simple_strategy import WeightedComponentStrategy
    strategy = WeightedComponentStrategy(name="TestStrategy", compo1_weight=1.0)
    strategy.update(ohlcv_default)

    result = strategy.generate_forecast()
    # Returns (forecast: float, confidence: float, debug: dict)
    forecast, confidence, debug = result
    assert isinstance(forecast, float)
    assert isinstance(confidence, float)
    assert isinstance(debug, dict)


# ---------------------------------------------------------------------------
# Q9 — Regime components (standardized_forecast=False) must be ready
#       without the 50-bar standardization warmup
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_regime_component_ready_without_standardization_warmup():
    """
    EfficiencyRatioRegimeComponent has standardized_forecast=False.
    is_ready_with_standardization() must return True once the underlying
    data requirement is met — it must NOT require 50+ bars of rolling-buffer
    warmup.
    """
    from strategies.simple_strategy import EfficiencyRatioRegimeComponent
    comp = EfficiencyRatioRegimeComponent(
        name="ER_test",
        weight=1.0,
        parameters={"period": 10, "smooth_period": 3},
    )
    # Feed exactly enough data for is_ready() (period + 1 = 11 bars)
    data = make_ohlcv(n_bars=15, seed=10)
    comp.update(data)

    assert comp.is_ready(), "Component should be ready with enough data"
    assert comp.is_ready_with_standardization(), (
        "Regime component should NOT need standardization warmup — "
        "is_ready_with_standardization() must equal is_ready() when "
        "standardized_forecast=False"
    )


@pytest.mark.unit
def test_vol_percentile_component_ready_without_standardization_warmup():
    """Same check for VolatilityPercentileRegimeComponent."""
    from strategies.simple_strategy import VolatilityPercentileRegimeComponent
    comp = VolatilityPercentileRegimeComponent(
        name="VolRank_test",
        weight=1.0,
        parameters={"vol_period": 5, "lookback_period": 10, "smooth_period": 3},
    )
    data = make_ohlcv(n_bars=25, seed=11)
    comp.update(data)

    assert comp.is_ready()
    assert comp.is_ready_with_standardization()


# ---------------------------------------------------------------------------
# B3 — score_regime must not always be None
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_score_regime_is_not_none_when_active(ohlcv_default):
    """
    AdvancedStrategy.generate_signals() embeds score_regime in debug_info.
    Previously this was always None because the wrong dict key was read.
    After the fix it should be a float once the strategy is ready.
    """
    from strategies.main_strategy import AdvancedStrategy
    strategy = AdvancedStrategy()

    # Feed enough bars to warm up the strategy
    for i in range(50, len(ohlcv_default) + 1):
        strategy.update(ohlcv_default.iloc[:i])

    output = strategy.generate_signals()

    if output.regime == "NOT_READY":
        pytest.skip("Strategy not ready with this dataset — increase n_bars in fixture")

    score = output.debug_info.get("score_regime")
    assert score is not None, (
        "score_regime should be a float (the regime detector's composite score), "
        "not None. Check that debug_regime.get('final_forecast') is used."
    )
    assert isinstance(score, float), f"Expected float, got {type(score)}: {score}"


# ---------------------------------------------------------------------------
# Q5 — calculate_rebalance_needed must be removed (dead method)
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_forecast_manager_dead_method_removed(forecast_manager):
    """calculate_rebalance_needed() was a dead duplicate of needs_rebalance(). It should no longer exist."""
    assert not hasattr(forecast_manager, "calculate_rebalance_needed"), (
        "calculate_rebalance_needed() is a dead method that compared against "
        "the stored target instead of the actual market allocation. "
        "It should have been removed."
    )


# ---------------------------------------------------------------------------
# B4 — MockExecutionHandler.close_position must not crash when the
#       balance dict uses the full symbol key ('BTCUSDT')
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_mock_close_long_position_no_crash(ohlcv_default):
    """
    After opening a LONG, close_position() must succeed and return a FILLED
    status.  Previously it crashed with AttributeError when the balance key
    lookup returned None.
    """
    from execution.portfolio_info import MockPortfolioInfo
    from execution.execution_handler import MockExecutionHandler
    from performance.metrics import EnhancedPerformanceTracker

    portfolio = MockPortfolioInfo(
        initial_balance={"USDT": {"free": 10_000.0, "locked": 0.0}},
        commission_rate=0.001,
    )
    tracker = EnhancedPerformanceTracker(commission_rate=0.001, initial_capital=10_000)
    handler = MockExecutionHandler(performance_tracker=tracker, portfolio_info=portfolio)

    data = ohlcv_default

    # Open a LONG
    open_result = handler.open_long_position(
        symbol="BTCUSDT",
        quantity=0.01,
        data=data,
    )
    assert open_result["status"] == "FILLED"

    # Simulate the balance update that TradingBot does after open
    portfolio.update_local_balance("BTCUSDT", data["close"].iloc[-1], 0.01, "LONG")

    # Close the position — this must not raise
    close_result = handler.close_position(symbol="BTCUSDT", data=data)
    assert close_result["status"] == "FILLED", (
        f"close_position returned {close_result}"
    )


@pytest.mark.unit
def test_mock_close_short_position_no_crash(ohlcv_default):
    """Same crash test for a SHORT position."""
    from execution.portfolio_info import MockPortfolioInfo
    from execution.execution_handler import MockExecutionHandler
    from performance.metrics import EnhancedPerformanceTracker

    portfolio = MockPortfolioInfo(
        initial_balance={"USDT": {"free": 10_000.0, "locked": 0.0}},
        commission_rate=0.001,
    )
    tracker = EnhancedPerformanceTracker(commission_rate=0.001, initial_capital=10_000)
    handler = MockExecutionHandler(performance_tracker=tracker, portfolio_info=portfolio)

    data = ohlcv_default

    # Open a SHORT
    open_result = handler.open_short_position(
        symbol="BTCUSDT",
        quantity=-0.01,
        data=data,
    )
    assert open_result["status"] == "FILLED"

    # Simulate balance update
    portfolio.update_local_balance("BTCUSDT", data["close"].iloc[-1], 0.01, "SHORT")

    # Close — must not raise
    close_result = handler.close_position(symbol="BTCUSDT", data=data)
    assert close_result["status"] == "FILLED", (
        f"close_position returned {close_result}"
    )


# ---------------------------------------------------------------------------
# B3 supplement — verify that the 'final_forecast' key exists in debug_regime
# (pure unit test on the regime detector, no full strategy needed)
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_regime_detector_debug_has_final_forecast():
    """
    WeightedComponentRegimeDetector.classify_regime() must include
    'final_forecast' in its returned debug dict so that AdvancedStrategy
    can populate score_regime correctly.
    """
    from strategies.simple_strategy import WeightedComponentRegimeDetector
    detector = WeightedComponentRegimeDetector()
    data = make_ohlcv(n_bars=200, seed=99)

    detector.update(data)

    if not detector.is_ready():
        pytest.skip("Detector not ready with 200 bars")

    _, debug = detector.classify_regime()
    assert "final_forecast" in debug, (
        f"debug_regime must contain 'final_forecast'. Got keys: {list(debug.keys())}"
    )
    assert isinstance(debug["final_forecast"], float)
