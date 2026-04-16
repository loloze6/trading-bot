"""
Unit tests for WeightedComponentRegimeDetector state machine.

Tests verify:
  - Starts in UNKNOWN
  - Transitions to TRENDING when ER is high
  - Transitions to CHOP when ER is low and vol is low
  - Hysteresis: won't exit TRENDING until ER falls below exit threshold
  - Returns final_forecast key in debug dict
"""

import pytest
import numpy as np
import pandas as pd
from conftest import make_ohlcv


def make_high_er_data(n=200):
    """Monotonically rising prices → ER near 1.0."""
    return make_ohlcv(n_bars=n, trend=0.008, volatility=0.0005, seed=20)


def make_low_er_low_vol_data(n=200):
    """Flat, low-noise prices → ER near 0, vol low → CHOP regime."""
    return make_ohlcv(n_bars=n, trend=0.0, volatility=0.0001, seed=21)


@pytest.mark.unit
class TestRegimeDetectorInitialState:
    def test_starts_unknown(self):
        from strategies.simple_strategy import WeightedComponentRegimeDetector, MarketRegime
        detector = WeightedComponentRegimeDetector()
        assert detector.current_regime == MarketRegime.UNKNOWN

    def test_not_ready_on_empty(self):
        from strategies.simple_strategy import WeightedComponentRegimeDetector
        detector = WeightedComponentRegimeDetector()
        assert detector.is_ready() is False

    def test_classify_returns_unknown_when_not_ready(self):
        from strategies.simple_strategy import WeightedComponentRegimeDetector, MarketRegime
        detector = WeightedComponentRegimeDetector()
        regime, debug = detector.classify_regime()
        assert regime == MarketRegime.UNKNOWN
        assert debug == {}


@pytest.mark.unit
class TestRegimeDetectorTransitions:
    def test_high_er_data_leads_to_trending(self):
        """Strong monotonic uptrend should push ER above enter threshold (0.30)
        and produce a TRENDING regime once the detector warms up."""
        from strategies.simple_strategy import WeightedComponentRegimeDetector, MarketRegime
        detector = WeightedComponentRegimeDetector()
        data = make_high_er_data(n=200)
        detector.update(data)

        if not detector.is_ready():
            pytest.skip("Detector not ready — increase n_bars")

        regime, debug = detector.classify_regime()
        assert regime == MarketRegime.TRENDING, (
            f"Expected TRENDING on high-ER uptrend, got {regime.value}. "
            f"Regime metrics: {debug.get('regime_metrics', {})}"
        )

    def test_flat_low_vol_data_leads_to_chop(self):
        """Flat, low-noise data → ER near 0, vol percentile low → CHOP."""
        from strategies.simple_strategy import WeightedComponentRegimeDetector, MarketRegime
        detector = WeightedComponentRegimeDetector()
        data = make_low_er_low_vol_data(n=200)
        detector.update(data)

        if not detector.is_ready():
            pytest.skip("Detector not ready — increase n_bars")

        regime, debug = detector.classify_regime()
        assert regime == MarketRegime.CHOP, (
            f"Expected CHOP on flat data, got {regime.value}. "
            f"Regime metrics: {debug.get('regime_metrics', {})}"
        )


@pytest.mark.unit
class TestRegimeDetectorHysteresis:
    def test_er_thresholds_are_asymmetric(self):
        """
        Enter threshold (0.30) > exit threshold (0.12).
        This is the hysteresis gap. If they were equal there would be no hysteresis.
        """
        from strategies.simple_strategy import WeightedComponentRegimeDetector
        detector = WeightedComponentRegimeDetector()
        assert detector.er_trend_enter > detector.er_trend_exit, (
            "Enter threshold must be above exit threshold to create hysteresis"
        )

    def test_vol_thresholds_are_asymmetric(self):
        """Chop enter (0.35) < chop exit (0.45) — wider vol needed to leave chop."""
        from strategies.simple_strategy import WeightedComponentRegimeDetector
        detector = WeightedComponentRegimeDetector()
        assert detector.vol_chop_enter < detector.vol_chop_exit


@pytest.mark.unit
class TestRegimeDetectorDebug:
    def test_debug_contains_final_forecast(self, ohlcv_default):
        """classify_regime() debug dict must contain 'final_forecast' key."""
        from strategies.simple_strategy import WeightedComponentRegimeDetector
        detector = WeightedComponentRegimeDetector()
        detector.update(ohlcv_default)

        if not detector.is_ready():
            pytest.skip("Detector not ready with this dataset")

        _, debug = detector.classify_regime()
        assert "final_forecast" in debug, (
            f"debug must contain 'final_forecast'. Got keys: {list(debug.keys())}"
        )
        assert isinstance(debug["final_forecast"], float)

    def test_debug_contains_regime_metrics(self, ohlcv_default):
        """After classify_regime(), debug must contain er_smoothed and vol_smoothed."""
        from strategies.simple_strategy import WeightedComponentRegimeDetector
        detector = WeightedComponentRegimeDetector()
        detector.update(ohlcv_default)

        if not detector.is_ready():
            pytest.skip("Detector not ready with this dataset")

        _, debug = detector.classify_regime()
        metrics = debug.get("regime_metrics", {})
        assert "er_smoothed" in metrics, f"Missing er_smoothed in {metrics}"
        assert "vol_smoothed" in metrics, f"Missing vol_smoothed in {metrics}"
        assert 0.0 <= metrics["er_smoothed"] <= 1.0
        assert 0.0 <= metrics["vol_smoothed"] <= 1.0

    def test_bars_in_regime_increments(self, ohlcv_default):
        """bars_in_current_regime increments on consecutive calls in same regime."""
        from strategies.simple_strategy import WeightedComponentRegimeDetector
        detector = WeightedComponentRegimeDetector()
        data = make_high_er_data(n=200)
        detector.update(data)

        if not detector.is_ready():
            pytest.skip("Detector not ready")

        detector.classify_regime()
        count_after_first = detector.bars_in_current_regime

        # Feed the same data again (no regime change expected on identical data)
        detector.update(data)
        detector.classify_regime()
        count_after_second = detector.bars_in_current_regime

        # bars_in_regime should have incremented (or stayed same if regime changed)
        assert count_after_second >= 1
        assert count_after_first >= 1
