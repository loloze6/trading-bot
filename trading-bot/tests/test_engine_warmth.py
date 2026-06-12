import numpy as np
import pandas as pd
from strategies.strategy_engine import ConfigDrivenStrategyEngine
from strategies.strategy_base import MarketRegime

CFG = {
    "warmup": 5,
    "regimes": {
        "trending": {"components": [{
            "id": "pe", "class": "strategies.strategy_components.PriceEvolutionComponent",
            "params": {"period": 5}, "weight": 1.0,
            "transforms": [{"op": "identity"}],
        }]},
        "mean_reversion": {"components": [{
            "id": "pe2", "class": "strategies.strategy_components.PriceEvolutionComponent",
            "params": {"period": 5}, "weight": 1.0,
            "transforms": [{"op": "identity"}],
        }]},
        "chop": None,
        "unknown": None,
    },
}

def test_all_regime_histories_warm_every_bar():
    eng = ConfigDrivenStrategyEngine(CFG)
    n = 40
    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=n, freq="h"),
        "open": 100.0, "high": 101.0, "low": 99.0,
        "close": np.linspace(100.0, 110.0, n), "volume": 1.0,
    })
    for i in range(6, n + 1):          # component ready from 6 bars (period+1)
        eng.update(df.iloc[:i])
    h_a = eng._history["trending"]["pe"]
    h_b = eng._history["mean_reversion"]["pe2"]
    assert len(h_a) == len(h_b) > 0     # inactive regime is as warm as active
    assert eng.is_ready(MarketRegime.TRENDING)
    assert eng.is_ready(MarketRegime.MEAN_REVERSION)
