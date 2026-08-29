"""
F5b (P1a shakedown, 2026-07-04) regression test.

main_strategy.update()'s broad exception handler previously did nothing but log —
no count, no classification, no way for anything downstream (prescreen_signal.py) to
tell "the signal is genuinely absent" apart from "a component crashed on every bar."
That ambiguity is exactly what made run_044's real ZeroDivisionError (F5a) look like a
null result instead of a bug.

Uses a deliberately-broken dummy component (not the now-fixed F5a bug, which no longer
reproduces after F5a's fix) to test the counting/classification mechanism in isolation.
"""

import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from strategies.main_strategy import AdvancedStrategy
from strategies.strategy_base import SubStrategyComponent


class _AlwaysThrowsComponent(SubStrategyComponent):
    """Deliberately broken component — stands in for any component bug (F5a's
    ZeroDivisionError is now fixed and can no longer be used to trigger this)."""

    def __init__(self, name="broken", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})

    def update(self, data: pd.DataFrame):
        self.data = data
        raise ZeroDivisionError("simulated component bug")

    def is_ready(self) -> bool:
        return True

    def get_required_periods(self) -> int:
        return 0


def _bars(n=10):
    close = 100.0 + np.arange(n, dtype=float)
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC"),
            "open": close,
            "high": close + 0.5,
            "low": close - 0.5,
            "close": close,
            "volume": 1.0,
        }
    )


def _config_with_broken_component():
    return {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
        "strategies": {
            "warmup": 3,
            "regimes": {
                "unknown": {
                    "components": [
                        {
                            "id": "broken",
                            "class": "tests.test_main_strategy_error_surfacing._AlwaysThrowsComponent",
                            "weight": 1.0,
                            "transforms": [{"op": "identity"}],
                            "params": {},
                        }
                    ]
                },
                "trending": None,
                "mean_reversion": None,
                "chop": None,
            },
        },
    }


def test_component_exceptions_are_counted_and_classified():
    config = _config_with_broken_component()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config, f)
        tmp_path = f.name
    try:
        strat = AdvancedStrategy(config_path=tmp_path)
        assert strat.component_error_count == 0
        assert strat.component_error_samples == []

        bars = _bars(10)
        for i in range(1, len(bars) + 1):
            strat.update(bars.iloc[:i])

        assert strat.component_error_count == 10, "every bar's update() should have failed and been counted"
        assert len(strat.component_error_samples) == AdvancedStrategy._MAX_ERROR_SAMPLES, (
            "sample list must be capped, not grow unbounded"
        )
        sample = strat.component_error_samples[0]
        assert sample["error_type"] == "ZeroDivisionError"
        assert "simulated component bug" in sample["error_message"]
        assert sample["stage"] == "strategy_engine"
        assert sample["bar_index"] == 1
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_no_errors_means_zero_count_and_empty_samples():
    """Non-regression: a healthy strategy must report zero errors, not a false positive."""
    config = {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
        "strategies": {
            "warmup": 3,
            "regimes": {
                "unknown": {
                    "components": [
                        {
                            "id": "pe",
                            "class": "strategies.strategy_components.PriceEvolutionComponent",
                            "weight": 1.0,
                            "transforms": [{"op": "identity"}],
                            "params": {"period": 5},
                        }
                    ]
                },
                "trending": None,
                "mean_reversion": None,
                "chop": None,
            },
        },
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config, f)
        tmp_path = f.name
    try:
        strat = AdvancedStrategy(config_path=tmp_path)
        bars = _bars(10)
        for i in range(1, len(bars) + 1):
            strat.update(bars.iloc[:i])
        assert strat.component_error_count == 0
        assert strat.component_error_samples == []
    finally:
        Path(tmp_path).unlink(missing_ok=True)
