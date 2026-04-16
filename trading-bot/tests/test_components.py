"""
Unit tests for individual strategy components.

Each component test verifies:
  - is_ready() gating (not ready with insufficient data, ready with enough)
  - Forecast is within [-20, +20]
  - Directional correctness (positive signal on bullish data, negative on bearish)
  - Math sanity (specific known inputs produce expected outputs)
"""

import pytest
import numpy as np
import pandas as pd
from conftest import make_ohlcv


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_trending_up(n=200):
    """Monotonically rising prices — ER should be ≈1, Keltner should be bullish."""
    return make_ohlcv(n_bars=n, trend=0.005, volatility=0.001, seed=10)


def make_trending_down(n=200):
    return make_ohlcv(n_bars=n, trend=-0.005, volatility=0.001, seed=11)


def make_flat(n=200):
    return make_ohlcv(n_bars=n, trend=0.0, volatility=0.0005, seed=12)


# ---------------------------------------------------------------------------
# KeltnerBreakoutComponent
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestKeltnerBreakoutComponent:
    def _make(self, **params):
        from strategies.simple_strategy import KeltnerBreakoutComponent
        defaults = {"ema_period": 20, "atr_period": 20, "atr_multiplier": 1.5, "scaling_factor": 20.0}
        defaults.update(params)
        return KeltnerBreakoutComponent(name="KeltnerTest", weight=1.0, parameters=defaults)

    def test_not_ready_with_insufficient_data(self):
        comp = self._make(ema_period=20, atr_period=20)
        data = make_ohlcv(n_bars=10)  # needs max(20,20)+1 = 21
        comp.update(data)
        assert comp.is_ready() is False

    def test_ready_with_sufficient_data(self):
        comp = self._make(ema_period=20, atr_period=20)
        data = make_ohlcv(n_bars=50)
        comp.update(data)
        assert comp.is_ready() is True

    def test_forecast_in_valid_range(self, ohlcv_default):
        comp = self._make()
        comp.update(ohlcv_default)
        output = comp.generate_forecast()
        assert -20.0 <= output.forecast <= 20.0

    def test_bullish_breakout_gives_positive_forecast(self):
        """Strong uptrend pushing price above Keltner upper band → forecast > 0.
        Uses standardized_forecast=False to bypass the 50-bar standardization warmup
        and test the raw directional signal directly."""
        comp = self._make(scaling_factor=20.0, standardized_forecast=False)
        data = make_trending_up(n=100)
        comp.update(data)
        output = comp.generate_forecast()
        # On a clean uptrend, price should be near/above the upper band
        assert output.forecast > 0, (
            f"Expected positive forecast on uptrend, got {output.forecast}"
        )

    def test_bearish_breakout_gives_negative_forecast(self):
        """Strong downtrend pushing price below Keltner lower band → forecast < 0.
        Uses standardized_forecast=False to bypass the 50-bar standardization warmup."""
        comp = self._make(scaling_factor=20.0, standardized_forecast=False)
        data = make_trending_down(n=100)
        comp.update(data)
        output = comp.generate_forecast()
        assert output.forecast < 0, (
            f"Expected negative forecast on downtrend, got {output.forecast}"
        )

    def test_price_at_ema_gives_near_zero_forecast(self):
        """Flat market: price oscillates around EMA → oscillator ≈ 0 → forecast ≈ 0.
        Uses standardized_forecast=False to bypass the 50-bar standardization warmup."""
        comp = self._make(scaling_factor=20.0, standardized_forecast=False)
        data = make_flat(n=100)
        comp.update(data)
        output = comp.generate_forecast()
        assert abs(output.forecast) < 10.0, (
            f"Expected near-zero forecast on flat market, got {output.forecast}"
        )

    def test_forecast_is_zero_before_ready(self):
        comp = self._make()
        data = make_ohlcv(n_bars=5)
        comp.update(data)
        output = comp.generate_forecast()
        assert output.forecast == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# EfficiencyRatioRegimeComponent
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestEfficiencyRatioRegimeComponent:
    def _make(self, period=10, smooth=3):
        from strategies.simple_strategy import EfficiencyRatioRegimeComponent
        return EfficiencyRatioRegimeComponent(
            name="ERTest", weight=1.0,
            parameters={"period": period, "smooth_period": smooth}
        )

    def test_not_ready_with_insufficient_data(self):
        comp = self._make(period=10)
        data = make_ohlcv(n_bars=5)  # needs period+1 = 11
        comp.update(data)
        assert comp.is_ready() is False

    def test_ready_with_enough_data(self):
        comp = self._make(period=10)
        data = make_ohlcv(n_bars=20)
        comp.update(data)
        assert comp.is_ready() is True

    def test_perfectly_trending_data_has_high_er(self):
        """
        Perfectly linear data (no noise): net change == path length → ER = 1.0.
        Smoothed value should be close to 1.0.
        """
        comp = self._make(period=10, smooth=1)
        # Build strictly monotonic prices to isolate the math
        n = 30
        timestamps = [pd.Timestamp("2025-01-01") + pd.Timedelta(hours=i) for i in range(n)]
        closes = np.linspace(100.0, 200.0, n)
        data = pd.DataFrame({
            "timestamp": timestamps,
            "open": closes,
            "high": closes * 1.001,
            "low": closes * 0.999,
            "close": closes,
            "volume": np.ones(n) * 100,
            "stddev_24": np.full(n, 1.0),
        })
        comp.update(data)
        assert comp.basic_forecast > 0.8, (
            f"ER should be close to 1.0 for linear trend, got {comp.basic_forecast}"
        )

    def test_zigzag_data_has_low_er(self):
        """
        Alternating up/down moves cancel out → net change ≈ 0, path length > 0 → ER ≈ 0.
        """
        comp = self._make(period=10, smooth=1)
        n = 30
        timestamps = [pd.Timestamp("2025-01-01") + pd.Timedelta(hours=i) for i in range(n)]
        closes = np.array([100.0 + (5.0 if i % 2 == 0 else -5.0) for i in range(n)],
                          dtype=float)
        data = pd.DataFrame({
            "timestamp": timestamps,
            "open": closes,
            "high": closes + 0.1,
            "low": closes - 0.1,
            "close": closes,
            "volume": np.ones(n) * 100,
            "stddev_24": np.full(n, 1.0),
        })
        comp.update(data)
        assert comp.basic_forecast < 0.3, (
            f"ER should be near 0 for zigzag data, got {comp.basic_forecast}"
        )

    def test_er_is_between_zero_and_one(self, ohlcv_default):
        comp = self._make()
        comp.update(ohlcv_default)
        if comp.is_ready():
            assert 0.0 <= comp.basic_forecast <= 1.0


# ---------------------------------------------------------------------------
# VolatilityPercentileRegimeComponent
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestVolatilityPercentileRegimeComponent:
    def _make(self, vol_period=5, lookback=20, smooth=2):
        from strategies.simple_strategy import VolatilityPercentileRegimeComponent
        return VolatilityPercentileRegimeComponent(
            name="VolTest", weight=1.0,
            parameters={"vol_period": vol_period, "lookback_period": lookback, "smooth_period": smooth}
        )

    def test_not_ready_with_insufficient_data(self):
        comp = self._make(vol_period=5, lookback=20)
        data = make_ohlcv(n_bars=10)  # needs 25
        comp.update(data)
        assert comp.is_ready() is False

    def test_ready_with_enough_data(self):
        comp = self._make(vol_period=5, lookback=20)
        data = make_ohlcv(n_bars=30)
        comp.update(data)
        assert comp.is_ready() is True

    def test_percentile_between_zero_and_one(self, ohlcv_default):
        comp = self._make(vol_period=10, lookback=50, smooth=3)
        comp.update(ohlcv_default)
        if comp.is_ready():
            assert 0.0 <= comp.basic_forecast <= 1.0

    def test_high_volatility_gives_high_percentile(self):
        """Data that ends with a volatility spike should produce a high percentile rank."""
        # Start with low-vol base, then spike at the end
        rng = np.random.default_rng(99)
        n = 60
        timestamps = [pd.Timestamp("2025-01-01") + pd.Timedelta(hours=i) for i in range(n)]
        # Calm for first 50, then volatile for last 10
        low_vol = rng.normal(0, 0.001, 50)
        high_vol = rng.normal(0, 0.05, 10)
        returns = np.concatenate([low_vol, high_vol])
        prices = 100.0 * np.exp(np.cumsum(returns))
        data = pd.DataFrame({
            "timestamp": timestamps,
            "open": prices,
            "high": prices * 1.002,
            "low": prices * 0.998,
            "close": prices,
            "volume": np.ones(n) * 100,
            "stddev_24": np.full(n, 1.0),
        })
        comp = self._make(vol_period=5, lookback=30, smooth=1)
        comp.update(data)
        if comp.is_ready():
            assert comp.basic_forecast > 0.6, (
                f"Expected high percentile after vol spike, got {comp.basic_forecast}"
            )


# ---------------------------------------------------------------------------
# CompositeStrategy weight normalization
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestCompositeStrategyWeighting:
    def test_weights_are_normalized_to_one(self):
        """CompositeStrategy must normalize component weights so they sum to 1."""
        from strategies.simple_strategy import KeltnerBreakoutComponent
        from strategies.strategy_base import CompositeStrategy

        c1 = KeltnerBreakoutComponent("K1", weight=3.0,
                                       parameters={"ema_period": 20, "atr_period": 20,
                                                   "atr_multiplier": 1.5, "scaling_factor": 20.0})
        c2 = KeltnerBreakoutComponent("K2", weight=1.0,
                                       parameters={"ema_period": 20, "atr_period": 20,
                                                   "atr_multiplier": 1.5, "scaling_factor": 20.0})
        strategy = CompositeStrategy([c1, c2], name="WeightTest")
        total = sum(c.weight for c in strategy.components)
        assert total == pytest.approx(1.0), f"Weights should sum to 1, got {total}"
        assert strategy.components[0].weight == pytest.approx(0.75)
        assert strategy.components[1].weight == pytest.approx(0.25)

    def test_single_component_has_weight_one(self):
        from strategies.simple_strategy import KeltnerBreakoutComponent
        from strategies.strategy_base import CompositeStrategy

        c1 = KeltnerBreakoutComponent("K1", weight=7.0,
                                       parameters={"ema_period": 20, "atr_period": 20,
                                                   "atr_multiplier": 1.5, "scaling_factor": 20.0})
        strategy = CompositeStrategy([c1], name="SingleTest")
        assert strategy.components[0].weight == pytest.approx(1.0)

    def test_forecast_is_weighted_sum(self, ohlcv_default):
        """
        With two components of equal weight, the composite forecast must equal
        the average of the individual forecasts.
        """
        from strategies.simple_strategy import KeltnerBreakoutComponent
        from strategies.strategy_base import CompositeStrategy
        import numpy as np

        params = {"ema_period": 20, "atr_period": 20, "atr_multiplier": 1.5, "scaling_factor": 20.0}
        c1 = KeltnerBreakoutComponent("K1", weight=1.0, parameters=params)
        c2 = KeltnerBreakoutComponent("K2", weight=1.0, parameters=params)
        strategy = CompositeStrategy([c1, c2], name="EqualWeightTest")
        strategy.update(ohlcv_default)

        if not strategy.is_ready():
            pytest.skip("Strategy not ready")

        forecast, _, debug = strategy.generate_forecast()
        components = debug.get("ensemble", [])
        if not components:
            pytest.skip("No ensemble data")

        expected = sum(c["weighted_contribution"] for c in components)
        expected = float(np.clip(expected, -20, 20))
        assert forecast == pytest.approx(expected)
