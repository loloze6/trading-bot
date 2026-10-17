"""
D-147: a component waits for its history ops' stated minimum before it forecasts.

A component's history fills only once the component itself is ready. Engine readiness
used to be len(history) >= _warmup, and the forecast guard len(history) < 2, so a
ratio_to_mean / zscore / percentile / ema component could forecast on a handful of
values. Now (registry.history_op_min_periods, strategy_engine.py):

  * _op_min[regime][cid] = the largest transform_min_periods among the component's
    history ops (transforms + history_transforms), 1 when it has none;
  * _need[regime][cid]   = max(2, _op_min): is_ready needs len(h) >= max(_warmup, _need)
    and forecast() returns (0.0, {"not_ready_component": cid}) below it;
  * get_required_periods adds _op_min - 1 per component (block regimes: untouched);
  * validate_config's V5 reuses registry.HISTORY_OPS (one definition).

Synthetic data only; no network, no local_data.
"""
import json

import numpy as np
import pandas as pd
import pytest

from strategies import registry
from strategies.main_strategy import AdvancedStrategy
from strategies.registry import HISTORY_OPS, history_op_min_periods
from strategies.strategy_base import MarketRegime
from strategies.strategy_engine import ConfigDrivenStrategyEngine
from tools import validate_config

PE = "strategies.strategy_components.PriceEvolutionComponent"
UNGATED = {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"}
PERIOD = 5                       # PriceEvolutionComponent: ready from PERIOD + 1 bars
COMP_PERIODS = PERIOD + 1


def _ohlcv(n, seed=0):
    rng = np.random.default_rng(seed)
    close = 100.0 * np.exp(np.cumsum(rng.normal(0.0, 0.01, n)))
    return pd.DataFrame({"timestamp": pd.date_range("2024-01-01", periods=n, freq="h"),
                         "open": close, "high": close * 1.001, "low": close * 0.999,
                         "close": close, "volume": 1.0})


def _comp(cid, transforms, weight=1.0, **extra):
    spec = {"id": cid, "class": PE, "params": {"period": PERIOD}, "weight": weight,
            "transforms": transforms}
    spec.update(extra)
    return spec


def _engine_cfg(components, warmup=2):
    return {"warmup": warmup,
            "regimes": {"unknown": {"components": components},
                        "trending": None, "mean_reversion": None, "chop": None}}


RATIO_PIPE = [{"op": "ratio_to_mean"}, {"op": "scale", "params": {"factor": 10.0}}]


# --- 1. history_op_min_periods -------------------------------------------------

@pytest.mark.parametrize("spec, expected", [
    ({}, 1),
    ({"transforms": []}, 1),
    ({"transforms": [{"op": "scale", "params": {"factor": 3.0}},
                     {"op": "clip", "params": {"min": -1, "max": 1}}]}, 1),
    ({"transforms": [{"op": "sigmoid"}, {"op": "negate"}, {"op": "threshold_filter"}]}, 1),
    ({"transforms": [{"op": "identity"}]}, 1),
    ({"transforms": [{"op": "ratio_to_mean"}, {"op": "scale", "params": {"factor": 10.0}}]}, 30),
    ({"transforms": [{"op": "zscore"}]}, 30),
    ({"transforms": [{"op": "percentile"}]}, 50),
    ({"transforms": [{"op": "negate_percentile"}]}, 50),
    ({"transforms": [{"op": "ema", "params": {"span": 10}}]}, 30),
    ({"transforms": [{"op": "ema", "params": {"span": 20}}]}, 60),
    ({"transforms": [{"op": "ema"}]}, 30),                                  # default span 10
    # a history op in history_transforms counts, even with scalar-only transforms
    ({"transforms": [{"op": "scale", "params": {"factor": 2.0}}],
      "history_transforms": [{"op": "zscore"}]}, 30),
    # the max over transforms + history_transforms
    ({"transforms": [{"op": "ratio_to_mean"}],
      "history_transforms": [{"op": "percentile"}]}, 50),
    ({"transforms": [{"op": "zscore"}, {"op": "ema", "params": {"span": 20}},
                     {"op": "ratio_to_mean"}]}, 60),
])
def test_history_op_min_periods(spec, expected):
    assert history_op_min_periods(spec) == expected


def test_data_ops_do_not_count():
    """vol_target reads bar data, not history (TRANSFORM_MIN_PERIODS 1)."""
    spec = {"transforms": [{"op": "vol_target", "params": {"window": 60, "target_annual_vol": 0.4,
                                                           "periods_per_year": 365}}]}
    assert history_op_min_periods(spec) == 1


def test_history_ops_membership_matches_the_registry_group():
    assert HISTORY_OPS == {"identity", "percentile", "negate_percentile", "zscore",
                           "ratio_to_mean", "ema"}
    assert HISTORY_OPS <= set(registry.TRANSFORM_OPS_REGISTRY)


# --- 2. one definition ----------------------------------------------------------

def test_validate_config_reuses_the_registry_history_ops():
    assert validate_config.HISTORY_OPS is registry.HISTORY_OPS
    assert not hasattr(validate_config, "_HISTORY_OPS")


# --- 3. a ratio_to_mean component waits for 30 history values ---------------------

def test_ratio_to_mean_component_waits_for_30_history_values():
    cfg = _engine_cfg([_comp("r", RATIO_PIPE)], warmup=2)
    eng = ConfigDrivenStrategyEngine(cfg)
    eng.set_warmup(2)                      # the warmup must not be what holds it back
    assert eng._warmup == 2 and eng._need["unknown"]["r"] == 30
    df = _ohlcv(80, seed=3)
    seen_ready = False
    for i in range(1, len(df) + 1):
        eng.update(df.iloc[:i])
        h = eng._history["unknown"]["r"]
        f, dbg = eng.forecast(MarketRegime.UNKNOWN)
        if len(h) < 30:
            assert not eng.is_ready(MarketRegime.UNKNOWN), f"ready at {len(h)} history values"
            assert f == 0.0
            assert dbg == {"not_ready_component": "r"}
        else:
            assert eng.is_ready(MarketRegime.UNKNOWN), f"not ready at {len(h)} history values"
            vals = np.asarray(list(h), dtype=float)
            expected = float(np.clip(10.0 * vals[-1] / np.abs(vals).mean(), -20.0, 20.0))
            assert f == pytest.approx(expected, rel=1e-12)
            assert "not_ready_component" not in dbg
            if len(h) == 30:
                seen_ready = True
                assert f != 0.0            # non-degenerate series: a real forecast, not a 0
    assert seen_ready
    # the bar that makes the 30th value: component ready at COMP_PERIODS bars -> 30th at +29
    first = None
    eng2 = ConfigDrivenStrategyEngine(cfg)
    eng2.set_warmup(2)
    for i in range(1, len(df) + 1):
        eng2.update(df.iloc[:i])
        if eng2.is_ready(MarketRegime.UNKNOWN):
            first = i
            break
    assert first == COMP_PERIODS + 29


def test_slowest_component_gates_a_mixed_regime():
    """identity (need 2) + ratio_to_mean (need 30): nothing forecasts until the slow one is ready."""
    cfg = _engine_cfg([_comp("fast", [{"op": "identity"}]), _comp("slow", RATIO_PIPE)], warmup=2)
    eng = ConfigDrivenStrategyEngine(cfg)
    eng.set_warmup(2)
    assert eng._need["unknown"] == {"fast": 2, "slow": 30}
    df = _ohlcv(60, seed=4)
    for i in range(1, len(df) + 1):
        eng.update(df.iloc[:i])
        n = len(eng._history["unknown"]["slow"])
        n_fast = len(eng._history["unknown"]["fast"])
        f, dbg = eng.forecast(MarketRegime.UNKNOWN)
        if n < 30:
            assert not eng.is_ready(MarketRegime.UNKNOWN)
            # components are checked in config order: the first one still short is named
            assert (f, dbg) == (0.0, {"not_ready_component": "fast" if n_fast < 2 else "slow"})
        else:
            assert eng.is_ready(MarketRegime.UNKNOWN)
            assert f != 0.0


def test_history_transforms_op_also_gates_readiness():
    """A history op in history_transforms (applied at append time) counts as well."""
    comp = _comp("h", [{"op": "scale", "params": {"factor": 5.0}}],
                 history_transforms=[{"op": "zscore"}])
    # history_transforms run on a one-value series (history op over 1 value), but the
    # stated minimum is still 30 -- that is the contract this change enforces.
    eng = ConfigDrivenStrategyEngine(_engine_cfg([comp]))
    assert eng._op_min["unknown"]["h"] == 30 and eng._need["unknown"]["h"] == 30


# --- 4. get_required_periods ----------------------------------------------------

def test_get_required_periods_adds_op_min_minus_one():
    eng = ConfigDrivenStrategyEngine(_engine_cfg([_comp("r", RATIO_PIPE)]))
    assert eng.get_required_periods() == COMP_PERIODS + 29
    pct = ConfigDrivenStrategyEngine(_engine_cfg([_comp("p", [{"op": "percentile"}])]))
    assert pct.get_required_periods() == COMP_PERIODS + 49
    mixed = ConfigDrivenStrategyEngine(_engine_cfg([_comp("a", [{"op": "identity"}]),
                                                    _comp("b", RATIO_PIPE)]))
    assert mixed.get_required_periods() == COMP_PERIODS + 29


def test_advanced_strategy_required_bars_follows(tmp_path):
    def full(components):
        return {"regime_detector": UNGATED, "strategies": {"regimes": {
            "unknown": {"components": components},
            "trending": None, "mean_reversion": None, "chop": None}}}

    p_ratio = tmp_path / "ratio.json"
    p_ratio.write_text(json.dumps(full([_comp("r", RATIO_PIPE)])), encoding="utf-8")
    s = AdvancedStrategy(config_path=str(p_ratio))
    # required_bars = max(regime, strategy engine, 24); engine side = 6 + 29 = 35
    assert s.strategy_engine.get_required_periods() == COMP_PERIODS + 29
    assert s.required_bars == COMP_PERIODS + 29
    # set_warmup(required_bars) is capped at the smallest deque (lookback = max(6, 30) = 30)
    assert s.strategy_engine._warmup == min(s.required_bars, s.strategy_engine._min_buf) == 30

    p_id = tmp_path / "identity.json"
    p_id.write_text(json.dumps(full([_comp("i", [{"op": "identity"}])])), encoding="utf-8")
    s2 = AdvancedStrategy(config_path=str(p_id))
    assert s2.strategy_engine.get_required_periods() == COMP_PERIODS     # unchanged
    assert s2.required_bars == 24                                        # the floor


# --- 5. identity-only config is unchanged ----------------------------------------

def test_identity_only_required_periods_unchanged():
    eng = ConfigDrivenStrategyEngine(_engine_cfg([_comp("i", [{"op": "identity"}])]))
    assert eng._op_min["unknown"]["i"] == 1
    assert eng._need["unknown"]["i"] == 2          # the old forecast guard's floor
    assert eng.get_required_periods() == COMP_PERIODS


def test_scalar_only_component_has_no_extra_wait():
    pipe = [{"op": "scale", "params": {"factor": 4.0}}, {"op": "clip", "params": {"min": -5, "max": 5}}]
    eng = ConfigDrivenStrategyEngine(_engine_cfg([_comp("s", pipe)]))
    assert eng._need["unknown"]["s"] == 2
    assert eng.get_required_periods() == COMP_PERIODS


@pytest.mark.parametrize("k", [2, 3, 4, 7])
def test_identity_readiness_flips_exactly_at_warmup(k):
    # lookback override so the deque (hence the warmup cap) is larger than every k
    eng = ConfigDrivenStrategyEngine(
        _engine_cfg([_comp("i", [{"op": "identity"}], lookback=20)], warmup=k))
    eng.set_warmup(k)
    assert eng._warmup == k
    df = _ohlcv(40, seed=5)
    for i in range(1, len(df) + 1):
        eng.update(df.iloc[:i])
        n = len(eng._history["unknown"]["i"])
        assert eng.is_ready(MarketRegime.UNKNOWN) == (n >= k), f"n={n}, k={k}"
        f, dbg = eng.forecast(MarketRegime.UNKNOWN)
        if n < 2:
            assert (f, dbg) == (0.0, {"not_ready_component": "i"})   # the forecast guard's floor
        else:
            assert f != 0.0 and "not_ready_component" not in dbg


def test_identity_forecast_non_zero_from_two_values_with_warmup_2():
    eng = ConfigDrivenStrategyEngine(_engine_cfg([_comp("i", [{"op": "identity"}])]))
    eng.set_warmup(2)
    df = _ohlcv(30, seed=6)
    for i in range(1, COMP_PERIODS + 1):               # first history value at COMP_PERIODS bars
        eng.update(df.iloc[:i])
    assert len(eng._history["unknown"]["i"]) == 1
    assert not eng.is_ready(MarketRegime.UNKNOWN)
    assert eng.forecast(MarketRegime.UNKNOWN) == (0.0, {"not_ready_component": "i"})
    eng.update(df.iloc[:COMP_PERIODS + 1])
    assert len(eng._history["unknown"]["i"]) == 2
    assert eng.is_ready(MarketRegime.UNKNOWN)
    f, _ = eng.forecast(MarketRegime.UNKNOWN)
    assert f != 0.0


# --- 6. block regimes are untouched -----------------------------------------------

def test_block_regime_is_in_neither_dict_and_keeps_the_block_chain_formula():
    """Same fixture shape as test_e060_block_standardisation._block_cfg (which already pins
    get_required_periods == 70 + 40 + 30 for the chain); here a block component also carries a
    history op, which must add nothing: block regimes are outside _op_min/_need."""
    src = {"required_bars": 70, "warmup": 40, "buffer_bars": 170,
           "regime_detector": UNGATED, "parts": {"unknown": ["b0__x"]}}
    cfg = {"warmup": 10, "regimes": {
        "unknown": {
            "components": [_comp("b0__x", RATIO_PIPE, lookback=60)],
            "blocks": [{"id": "b0", "weight": 1.0, "components": ["b0__x"], "source": src}],
            "block_standardisation": {"target": 10.0, "window": 100, "min_periods": 30},
        },
        "trending": None, "mean_reversion": None, "chop": None}}
    eng = ConfigDrivenStrategyEngine(cfg)
    assert "unknown" not in eng._op_min and "unknown" not in eng._need
    assert eng.get_required_periods() == 70 + 40 + 30
