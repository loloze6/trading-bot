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


def test_standalone_construction_still_uses_configs_own_warmup():
    """CUL-273: a standalone ConfigDrivenStrategyEngine (no set_warmup() call,
    e.g. this file's own direct construction, or test_feed_dependencies.py)
    must be byte-identical to before this ticket -- the class's own
    config-driven default only changes for callers who explicitly opt into
    the single-source-of-truth via set_warmup()."""
    eng = ConfigDrivenStrategyEngine(CFG)
    assert eng._warmup == 5          # CFG's own "warmup": 5, unaffected by CUL-273


def test_set_warmup_overrides_and_is_capped_at_min_buf():
    """CUL-273: set_warmup(required_bars) is what AdvancedStrategy calls once
    required_bars is known -- proves it actually takes effect, and proves the
    min_buf cap still applies (a required_bars larger than the smallest
    component deque must not set warmup above that deque's maxlen, or that
    component could never satisfy len(h) >= warmup)."""
    eng = ConfigDrivenStrategyEngine(CFG)
    original_warmup = eng._warmup   # CFG's own "warmup": 5
    eng.set_warmup(3)
    assert eng._warmup == 3 != original_warmup, "set_warmup must actually take effect"

    # Force a real min_buf ceiling via a per-component "lookback" override
    # smaller than the requested required_bars.
    cfg_small_deque = {
        "warmup": 5,
        "regimes": {
            "trending": {"components": [{
                "id": "pe", "class": "strategies.strategy_components.PriceEvolutionComponent",
                "params": {"period": 5}, "weight": 1.0,
                "transforms": [{"op": "identity"}], "lookback": 8,
            }]},
            "mean_reversion": None, "chop": None, "unknown": None,
        },
    }
    eng2 = ConfigDrivenStrategyEngine(cfg_small_deque)
    eng2.set_warmup(120)
    assert eng2._min_buf < 120, "test fixture must actually exercise the cap -- otherwise this proves nothing"
    assert eng2._warmup == eng2._min_buf, "must be capped at the smallest deque's maxlen, not the raw required_bars"


def test_advanced_strategy_reconciles_warmup_with_required_bars():
    """CUL-273 Task B: the real live/backtest path (AdvancedStrategy) must set
    strategy_engine._warmup == required_bars -- the single-source-of-truth
    this ticket exists to establish, not an independently-derived, possibly
    drifted number. Uses this fork's real strategy_config.json, the same
    config every other test in this session's investigation measured
    (required_bars=120, the pre-fix _warmup was 51 -- a real, measured drift,
    not a hypothetical one)."""
    from strategies.main_strategy import AdvancedStrategy
    s = AdvancedStrategy(config_path="strategy_config.json")
    assert s.strategy_engine._warmup == s.required_bars
