"""Regression tests for the two warm-up defects parked in
strategy_designer_v2/steps_cards/POTENTIAL_ADJUSTMENTS.md (operator approval 2026-11-16).

Parked A: a regime-detector component that needs 0 bars (BuyAndHoldStrategy) got a
deque(maxlen=0), kept no value, and the strategy was never ready: the launcher's
warm-up check refused every window. Without that check (run_backtest's default), such a
plan would have held flat with no error, which is why A also asserts the plan trades.

Parked B: the strategy engine compared its HISTORY count with required_bars (a ROW
count), so a strategy became ready only after component warm-up + required_bars rows
(SMA-200 + standardise(200, 50): 400 rows while declaring 250). The warm-up now follows
the config: a standardise op's min_periods.

Made-up bars only: no market data, no trial.
"""
import json

import numpy as np
import pandas as pd
import pytest

from strategies.main_strategy import AdvancedStrategy
from strategies.regime_engine import ConfigDrivenRegimeEngine
from strategies.strategy_base import MarketRegime


def _bars(n, seed=0, volume=None):
    rng = np.random.default_rng(seed)
    close = 100 * np.exp(rng.normal(0, 0.02, n).cumsum())
    return pd.DataFrame({
        "timestamp": pd.date_range("2000-01-01", periods=n, freq="D"),
        "open": close, "high": close * 1.01, "low": close * 0.99, "close": close,
        "volume": rng.uniform(1, 2, n) if volume is None else volume,
    })


def _strategy(tmp_path, config):
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))
    return AdvancedStrategy(config_path=str(path))


# -- Parked A -----------------------------------------------------------------------

_VOLUME_VETO = {
    "mode": "threshold_rules",
    "components": [{"id": "const", "class": "strategies.strategy_components.BuyAndHoldStrategy",
                    "params": {}}],
    "vetoes": [{"id": "const",
                "transforms": [{"op": "volume_filter", "params": {"period": 20}}],
                "rules": [{"op": "lte", "value": 0.0}],
                "consecutive_bars": 1, "result": "mean_reversion"}],
    "rules": [],
    "default_regime": "unknown",
}

# 003-01_low-volume-up-move-reverts_1d's pattern: after an up move on low volume,
# a negative (short) forecast.
_PLAN_003_01 = {
    "regime_detector": _VOLUME_VETO,
    "strategies": {"regimes": {
        "mean_reversion": {"components": [{
            "id": "move", "class": "strategies.strategy_components.PriceEvolutionComponent",
            "params": {"period": 1}, "weight": 1.0,
            "transforms": [{"op": "standardise", "params": {"window": 60, "min_periods": 20}},
                           {"op": "negate"}, {"op": "clip", "params": {"max": 0.0}},
                           {"op": "signed_power", "params": {"exponent": 2}}]}]},
        "trending": None, "chop": None, "unknown": None}},
}


def test_zero_bar_detector_component_keeps_one_value():
    eng = ConfigDrivenRegimeEngine(json.loads(json.dumps(_VOLUME_VETO)))
    assert eng.lookback == 1
    eng.update(_bars(1))
    assert eng.is_ready()


def test_zero_bar_detector_plan_is_ready_at_required_bars_and_vetoes_on_low_volume(tmp_path):
    st = _strategy(tmp_path, _PLAN_003_01)
    df = _bars(200, seed=1)
    first_ready = None
    for i in range(len(df)):
        st.update(df.iloc[i:i + 1])
        if not st.is_ready():
            continue
        first_ready = first_ready or i + 1
        regime, _ = st._classify_once()
        vol = df["volume"].iloc[: i + 1]
        low = vol.iloc[-1] < vol.rolling(20).mean().iloc[-1]
        assert (regime == MarketRegime.MEAN_REVERSION) == low, f"row {i + 1}"
    assert first_ready == st.required_bars == 24


def test_zero_bar_detector_plan_is_not_silently_flat(tmp_path):
    # Every other bar: low volume (veto fires) and an up move (the plan shorts it).
    n = 200
    up = np.where(np.arange(n) % 2 == 0, 1.02, 0.985)
    close = 100 * np.cumprod(up)
    df = pd.DataFrame({"timestamp": pd.date_range("2000-01-01", periods=n, freq="D"),
                       "open": close, "high": close * 1.01, "low": close * 0.99, "close": close,
                       "volume": np.where(np.arange(n) % 2 == 0, 1.0, 3.0)})
    st = _strategy(tmp_path, _PLAN_003_01)
    signals = []
    for i in range(n):
        st.update(df.iloc[i:i + 1])
        signals.append(st.generate_signals())
    assert all(s.regime == "NOT_READY" for s in signals[:st.required_bars - 1])
    assert not any(s.regime == "NOT_READY" for s in signals[st.required_bars - 1:])
    assert sum(s.forecast < 0 for s in signals) > 50


# -- Parked B -----------------------------------------------------------------------

def _sma_standardise(min_periods, sizing=False):
    cfg = {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                            "default_regime": "unknown"},
        "strategies": {"regimes": {
            "unknown": {"components": [{
                "id": "sma_cross", "class": "strategies.strategy_components.EMASpreadComponent",
                "params": {"fast_period": 5, "slow_period": 20, "average": "sma"}, "weight": 1.0,
                "transforms": [{"op": "standardise",
                                "params": {"window": 20, "min_periods": min_periods}},
                               {"op": "clip", "params": {"min": 0.0}}]}]},
            "trending": None, "mean_reversion": None, "chop": None}},
    }
    if sizing:
        cfg["strategies"]["sizing"] = {"kind": "vol_target", "window": 10,
                                       "target_annual_vol": 0.38, "periods_per_year": 365,
                                       "max_allocation": 2}
    return cfg


@pytest.mark.parametrize("min_periods, expected", [(5, 25), (12, 32), (20, 40)])
@pytest.mark.parametrize("sizing", [False, True])
def test_ready_at_declared_required_bars_from_standardise_min_periods(tmp_path, min_periods,
                                                                     expected, sizing):
    # SMA-20 has a value from row 20; standardise needs min_periods past values + the
    # current one: ready at row 20 + min_periods, and required_bars says the same.
    # Before the fix: row 20 + 21 - 1 = 40 whatever min_periods was.
    st = _strategy(tmp_path, _sma_standardise(min_periods, sizing))
    assert st.required_bars == expected
    df = _bars(80, seed=2)
    first_ready = None
    for i in range(len(df)):
        st.update(df.iloc[i:i + 1])
        if first_ready is None and st.is_ready():
            first_ready = i + 1
    assert first_ready == expected
