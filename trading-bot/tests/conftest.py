"""
Shared fixtures for the trading-bot test suite.

Design principles:
- Fixtures are pure (no side effects, no I/O, no Binance calls)
- Synthetic OHLCV data is deterministic (fixed seed)
- Logger is a no-op stub — tests should not write to disk
- Components are created with minimal params and can be overridden per-test
"""

import logging
import sys
import os
import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Make the trading-bot package importable from tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Logger fixture — no-op, avoids disk writes during tests
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def silence_logger():
    """
    Attach a no-op strategy_refinement attribute to the trading_bot logger
    so components that call `logger.strategy_refinement` don't crash.
    This runs automatically for every test.
    """
    logger = logging.getLogger("trading_bot")
    logger.strategy_refinement = False
    # Suppress output unless a test explicitly checks logs
    logger.setLevel(logging.CRITICAL)
    yield
    logger.setLevel(logging.CRITICAL)


# ---------------------------------------------------------------------------
# Synthetic OHLCV data factory
# ---------------------------------------------------------------------------

def make_ohlcv(
    n_bars: int = 200,
    start_price: float = 80_000.0,
    trend: float = 0.0,          # drift per bar as fraction of price (e.g. 0.001 = +0.1%/bar)
    volatility: float = 0.005,   # std of per-bar return
    seed: int = 42,
    interval_minutes: int = 60,
    start_time: datetime = None,
) -> pd.DataFrame:
    """
    Generate deterministic synthetic OHLCV data.

    Returns a DataFrame with columns: timestamp, open, high, low, close, volume
    that mimics the format used by HistoricalDataManager / CandleBuilder.
    """
    rng = np.random.default_rng(seed)
    if start_time is None:
        start_time = datetime(2025, 1, 1, 0, 0, 0)

    # Generate close prices via geometric Brownian motion
    returns = rng.normal(loc=trend, scale=volatility, size=n_bars)
    closes = start_price * np.exp(np.cumsum(returns))

    # Build OHLCV
    wicks = rng.uniform(0.001, 0.003, size=n_bars)  # wick as fraction of close
    highs = closes * (1 + wicks)
    lows = closes * (1 - wicks)
    opens = np.roll(closes, 1)
    opens[0] = start_price

    volumes = rng.uniform(100, 1000, size=n_bars)

    timestamps = [start_time + timedelta(minutes=interval_minutes * i) for i in range(n_bars)]

    df = pd.DataFrame({
        "timestamp": timestamps,
        "open": opens,
        "high": highs,
        "low": lows,
        "close": closes,
        "volume": volumes,
    })

    # Add stddev_24 — required by SubStrategyComponent.store_raw_forecast / standardize_forecast
    df["stddev_24"] = df["close"].rolling(24).std().fillna(df["close"].std())

    return df


# ---------------------------------------------------------------------------
# Fixtures built from the factory
# ---------------------------------------------------------------------------

@pytest.fixture
def ohlcv_flat(n_bars=200):
    """Flat market: no trend, moderate volatility."""
    return make_ohlcv(n_bars=n_bars, trend=0.0, volatility=0.003, seed=1)


@pytest.fixture
def ohlcv_trending_up():
    """Strong uptrend: clear directional drift."""
    return make_ohlcv(n_bars=200, trend=0.004, volatility=0.002, seed=2)


@pytest.fixture
def ohlcv_trending_down():
    """Strong downtrend."""
    return make_ohlcv(n_bars=200, trend=-0.004, volatility=0.002, seed=3)


@pytest.fixture
def ohlcv_choppy():
    """High-volatility, mean-reverting chop."""
    return make_ohlcv(n_bars=200, trend=0.0, volatility=0.010, seed=4)


@pytest.fixture
def ohlcv_default():
    """Default 200-bar dataset used when a specific market condition is not required."""
    return make_ohlcv(n_bars=200, seed=42)


# ---------------------------------------------------------------------------
# Component fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def keltner_component():
    """KeltnerBreakoutComponent with default parameters."""
    from strategies.simple_strategy import KeltnerBreakoutComponent
    return KeltnerBreakoutComponent(
        name="KeltnerTest",
        weight=1.0,
        parameters={
            "ema_period": 20,
            "atr_period": 20,
            "atr_multiplier": 1.5,
            "scaling_factor": 20.0,
        },
    )


@pytest.fixture
def er_component():
    """EfficiencyRatioRegimeComponent with default parameters."""
    from strategies.simple_strategy import EfficiencyRatioRegimeComponent
    return EfficiencyRatioRegimeComponent(
        name="ERTest",
        weight=1.0,
        parameters={"period": 24, "smooth_period": 5},
    )


@pytest.fixture
def vol_percentile_component():
    """VolatilityPercentileRegimeComponent with default parameters."""
    from strategies.simple_strategy import VolatilityPercentileRegimeComponent
    return VolatilityPercentileRegimeComponent(
        name="VolRankTest",
        weight=1.0,
        parameters={"vol_period": 20, "lookback_period": 100, "smooth_period": 5},
    )


@pytest.fixture
def regime_detector():
    """WeightedComponentRegimeDetector (live version, 2 components)."""
    from strategies.simple_strategy import WeightedComponentRegimeDetector
    return WeightedComponentRegimeDetector()


# ---------------------------------------------------------------------------
# ForecastManager fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def forecast_manager():
    """ForecastManager with standard parameters."""
    from execution.forecast_manager import ForecastManager
    return ForecastManager(
        max_forecast=20.0,
        min_forecast=-20.0,
        max_allocation=1.0,
        min_allocation=-1.0,
        rebalance_threshold=0.05,
    )


# ---------------------------------------------------------------------------
# Portfolio fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_portfolio():
    """MockPortfolioInfo with 1000 USDT starting balance."""
    from execution.portfolio_info import MockPortfolioInfo
    return MockPortfolioInfo(
        initial_balance={"USDT": {"free": 1000.0, "locked": 0.0}},
        commission_rate=0.001,
    )
