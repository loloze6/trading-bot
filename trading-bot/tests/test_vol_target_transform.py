"""
vol_target transform op (registry.TRANSFORM_OPS_REGISTRY["vol_target"]).

    out = v * target_annual_vol / (stdev(simple returns of the last `window`
          closes, ddof 1) * sqrt(periods_per_year))

Pins: the formula; only the last window + 1 closes are read (no lookahead:
bars after the current one cannot change it, bars before the window do not
either); fail loud (missing/invalid params, short data, zero volatility, NaN);
the strategy is not ready before the op has its window + 1 closes
(transform_data_periods -> get_required_periods -> required_bars); V14; one
AdvancedStrategy run on synthetic daily data; and that every config WITHOUT
vol_target is byte-identical to master before this op (every other op, the
strategy engine bar for bar, required periods).
"""
import importlib.util
import json
import math
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from strategies.main_strategy import AdvancedStrategy
from strategies.registry import (
    TRANSFORM_OPS_REGISTRY,
    transform_data_periods,
    transform_min_periods,
)
from strategies.strategy_base import MarketRegime
from strategies.strategy_engine import ConfigDrivenStrategyEngine
from tools.validate_config import validate

BASE_COMMIT = "6e0afb35"  # master before vol_target
TB_ROOT = Path(__file__).resolve().parents[1]
PE = "strategies.strategy_components.PriceEvolutionComponent"
SMA = "strategies.strategy_components.SmaTrendLongOnlyComponent"
UNGATED = {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"}
P = {"window": 60, "target_annual_vol": 0.4, "periods_per_year": 365}


def _daily(n, seed=0, vol=0.03, drift=0.002):
    rng = np.random.default_rng(seed)
    close = 100.0 * np.exp(np.cumsum(rng.normal(drift, vol, n)))
    return pd.DataFrame({"timestamp": pd.date_range("2021-01-01", periods=n, freq="D"),
                         "open": close, "high": close * 1.01, "low": close * 0.99,
                         "close": close, "volume": 1.0})


def _expected(v, closes, p=P):
    tail = np.asarray(closes[-(p["window"] + 1):], dtype=float)
    rets = tail[1:] / tail[:-1] - 1.0
    return v * p["target_annual_vol"] / (np.std(rets, ddof=1) * math.sqrt(p["periods_per_year"]))


def _op(v, d, p=P):
    return TRANSFORM_OPS_REGISTRY["vol_target"](v, pd.Series([v]), p, d)


# --- formula and no lookahead -----------------------------------------------

def test_formula_matches_reference():
    d = _daily(200, seed=1)
    for v in (10.0, -7.5, 0.0):
        assert _op(v, d) == pytest.approx(_expected(v, d["close"].to_numpy()), rel=1e-12)


def test_reads_only_the_last_window_plus_one_closes():
    d = _daily(200, seed=2)
    ref = _op(10.0, d)
    older = d.copy()
    older.loc[: len(d) - P["window"] - 2, "close"] *= 3.0  # every close before the window
    assert _op(10.0, older) == ref
    inside = d.copy()
    inside.loc[len(d) - P["window"] - 1, "close"] *= 1.5   # the window's first close
    assert _op(10.0, inside) != ref


def test_future_bars_never_change_a_past_output():
    d = _daily(300, seed=3)
    past = [_op(10.0, d.iloc[:t]) for t in range(61, 200)]
    changed = d.copy()
    changed.loc[200:, "close"] *= 5.0
    assert [_op(10.0, changed.iloc[:t]) for t in range(61, 200)] == past


def test_scales_inversely_with_volatility():
    calm, wild = _daily(200, seed=4, vol=0.01), _daily(200, seed=4, vol=0.04)
    assert _op(10.0, calm) > 3 * _op(10.0, wild)


# --- fail loud --------------------------------------------------------------

@pytest.mark.parametrize("params,needle", [
    ({"target_annual_vol": 0.4, "periods_per_year": 365}, "missing param 'window'"),
    ({"window": 60, "periods_per_year": 365}, "missing param 'target_annual_vol'"),
    ({"window": 60, "target_annual_vol": 0.4}, "missing param 'periods_per_year'"),
    ({**P, "window": 1}, "window must be an int >= 2"),
    ({**P, "window": 60.0}, "window must be an int >= 2"),
    ({**P, "window": True}, "window must be an int >= 2"),
    ({**P, "target_annual_vol": 0}, "target_annual_vol must be a finite number > 0"),
    ({**P, "target_annual_vol": float("nan")}, "target_annual_vol must be a finite number > 0"),
    ({**P, "periods_per_year": -365}, "periods_per_year must be a finite number > 0"),
    ({**P, "periods_per_year": "365"}, "periods_per_year must be a finite number > 0"),
])
def test_invalid_params_raise(params, needle):
    with pytest.raises(ValueError, match=needle):
        _op(10.0, _daily(200), params)


def test_short_data_raises():
    with pytest.raises(ValueError, match="needs 61 closes, got 60"):
        _op(10.0, _daily(60))
    assert math.isfinite(_op(10.0, _daily(61)))


def test_zero_volatility_raises():
    d = _daily(200)
    d["close"] = 100.0
    with pytest.raises(ValueError, match="realised volatility is 0.0"):
        _op(10.0, d)


def test_nan_close_in_window_raises_and_outside_window_does_not():
    d = _daily(200)
    d.loc[len(d) - 5, "close"] = np.nan
    with pytest.raises(ValueError, match="not finite or not positive"):
        _op(10.0, d)
    d2 = _daily(200)
    d2.loc[10, "close"] = np.nan
    assert math.isfinite(_op(10.0, d2))


def test_zero_close_in_window_raises():
    d = _daily(200)
    d.loc[len(d) - 3, "close"] = 0.0
    with pytest.raises(ValueError, match="not finite or not positive"):
        _op(10.0, d)


def test_nan_input_value_and_missing_data_raise():
    with pytest.raises(ValueError, match="input value is not finite"):
        _op(float("nan"), _daily(200))
    with pytest.raises(ValueError, match="needs the bar data"):
        _op(10.0, None)


# --- readiness: required periods include the op's data window ---------------

def _cfg(transforms, period=5):
    return {"warmup": 10, "regimes": {
        "unknown": {"components": [{"id": "s", "class": PE, "params": {"period": period},
                                    "weight": 1.0, "transforms": transforms}]},
        "trending": None, "mean_reversion": None, "chop": None}}


def test_transform_data_periods():
    assert transform_data_periods("vol_target", P) == 61
    assert transform_data_periods("vol_target", {"window": 1}) == 0  # invalid: V14 refuses it
    assert all(transform_data_periods(op, {}) == 0 for op in TRANSFORM_OPS_REGISTRY if op != "vol_target")
    assert transform_min_periods("vol_target", P) == 1


def test_engine_required_periods_include_the_window():
    with_op = ConfigDrivenStrategyEngine(_cfg([{"op": "identity"}, {"op": "vol_target", "params": P}]))
    without = ConfigDrivenStrategyEngine(_cfg([{"op": "identity"}]))
    assert with_op.get_required_periods() == 61
    assert without.get_required_periods() == 6 and without._data_periods == 0


# --- V14 --------------------------------------------------------------------

def _full(transforms):
    return {"regime_detector": UNGATED, "strategies": {"regimes": {
        "unknown": {"components": [{"id": "s", "class": SMA, "params": {"lookback_L": 50},
                                    "weight": 1.0, "transforms": transforms}]},
        "trending": None, "mean_reversion": None, "chop": None}}}


def test_v14_valid_params_pass_and_invalid_fail():
    assert validate(_full([{"op": "identity"}, {"op": "vol_target", "params": P}])) == []
    bad = validate(_full([{"op": "identity"}, {"op": "vol_target", "params": {"window": 0}}]))
    assert [v for v in bad if v.startswith("VIOLATION V14")] == [
        "VIOLATION V14 strategies.regimes.unknown.components[0].transforms[1].params: missing param 'target_annual_vol'",
        "VIOLATION V14 strategies.regimes.unknown.components[0].transforms[1].params: missing param 'periods_per_year'",
        "VIOLATION V14 strategies.regimes.unknown.components[0].transforms[1].params: window must be an int >= 2, got 0",
    ]
    assert not [v for v in validate(_full([{"op": "identity"}])) if "V14" in v]


VT = {"op": "vol_target", "params": P}


def test_v14_refuses_vol_target_outside_a_strategy_components_transforms():
    """Review of this PR: only strategies.<regime>.components[].transforms is
    covered by required periods; elsewhere the op would raise on short data."""
    hist = _full([{"op": "identity"}])
    hist["strategies"]["regimes"]["unknown"]["components"][0]["history_transforms"] = [VT]
    gated = _full([{"op": "identity"}])
    gated["regime_detector"] = {
        "mode": "threshold_rules", "default_regime": "unknown",
        "components": [{"id": "er", "class": "strategies.strategy_components.EfficiencyRatioRegimeComponent",
                        "params": {"period": 20}}],
        "vetoes": [{"component": "er", "transforms": [{"op": "identity"}, VT], "op": ">", "value": 0.5,
                    "regime": "chop"}],
        "rules": []}
    for cfg, loc in ((hist, "strategies.regimes.unknown.components[0].history_transforms[0]"),
                     (gated, "regime_detector.vetoes[0].transforms[1]")):
        v14 = [v for v in validate(cfg) if v.startswith("VIOLATION V14")]
        want = (f"VIOLATION V14 {loc}: vol_target is allowed only in a strategies "
                "component's `transforms`, in a regime without `blocks`")
        assert v14 == [want], v14
    blocks = _full([{"op": "identity"}, VT])
    blocks["strategies"]["regimes"]["unknown"]["blocks"] = []
    msg = ("VIOLATION V14 strategies.regimes.unknown.components[0].transforms[1]: vol_target is "
           "allowed only in a strategies component's `transforms`, in a regime without `blocks`")
    assert msg in validate(blocks)


# --- one strategy run on synthetic daily data -------------------------------

def test_advanced_strategy_run_on_synthetic_daily_data(tmp_path):
    """SMA(50) long/flat (raw 10 when long), identity, vol_target 40%/60/365,
    clip [0, 10]: NOT_READY before 61 bars at least, then on every ready bar exactly clip(10 * 0.4 /
    realised, 0, 10) when long and 0 when flat, never an ERROR bar."""
    tfs = [{"op": "identity"}, {"op": "vol_target", "params": P},
           {"op": "clip", "params": {"min": 0, "max": 10}}]
    path = tmp_path / "cfg.json"
    path.write_text(json.dumps(_full(tfs)), encoding="utf-8")
    strat = AdvancedStrategy(config_path=str(path))
    assert strat.required_bars == 61
    d = _daily(400, seed=7)
    rets = np.random.default_rng(7).normal(0.002, 1.0, 400) * np.r_[np.full(200, 0.012), np.full(200, 0.04)]
    d["close"] = 100.0 * np.exp(np.cumsum(rets))  # calm half (capped at 10), wild half (scaled down)
    n_long = n_flat = n_capped = 0
    first_ready = None
    for i in range(len(d)):
        strat.update(d.iloc[: i + 1])
        out = strat.generate_signals()
        if out.regime == "NOT_READY":
            assert out.forecast == 0.0 and first_ready is None
            continue
        first_ready = first_ready or i + 1
        assert first_ready >= 61
        assert out.regime == "unknown"
        closes = d["close"].to_numpy()[: i + 1]
        long = closes[-2] > closes[-51:-1].mean()  # the component's one-bar lag
        exp = float(np.clip(_expected(10.0, closes), 0, 10)) if long else 0.0
        assert out.forecast == pytest.approx(exp, rel=1e-12, abs=1e-12)
        n_long += long
        n_flat += not long
        n_capped += long and exp == 10.0
    assert strat.component_error_count == 0
    assert n_long > 50 and n_flat > 50 and 0 < n_capped < n_long


# --- byte identity for every config without vol_target ----------------------

def _old_module(rel, name):
    try:
        src = subprocess.run(["git", "show", f"{BASE_COMMIT}:trading-bot/{rel}"], cwd=TB_ROOT,
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        pytest.skip(f"base commit {BASE_COMMIT} not reachable via git: {exc}")
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader=None))
    exec(compile(src, f"{name}.py", "exec"), mod.__dict__)
    return mod


def test_every_other_op_is_unchanged():
    old = _old_module("strategies/registry.py", "_old_registry")
    assert set(TRANSFORM_OPS_REGISTRY) - set(old.TRANSFORM_OPS_REGISTRY) == {"vol_target"}
    assert {k: v for k, v in old.TRANSFORM_MIN_PERIODS.items()} == \
        {k: v for k, v in __import__("strategies.registry", fromlist=["x"]).TRANSFORM_MIN_PERIODS.items()
         if k != "vol_target"}
    d = _daily(200, seed=5)
    d["stddev_24"] = d["close"].rolling(24).std()
    h = pd.Series(np.random.default_rng(6).normal(0, 3, 120))
    params = {"factor": 3, "min_abs": 1, "min": -2, "max": 2, "span": 7, "period": 20}
    for op in old.TRANSFORM_OPS_REGISTRY:
        new_v = TRANSFORM_OPS_REGISTRY[op](1.7, h, params, d)
        old_v = old.TRANSFORM_OPS_REGISTRY[op](1.7, h, params, d)
        assert new_v == old_v or (math.isnan(new_v) and math.isnan(old_v)), op


LEGACY_CFG = {
    "warmup": 30,
    "regimes": {
        "unknown": {"components": [
            {"id": "a", "class": PE, "params": {"period": 5}, "weight": 2.0, "lookback": 200,
             "transforms": [{"op": "ratio_to_mean"}, {"op": "scale", "params": {"factor": 10}},
                            {"op": "vol_adjusted"}, {"op": "threshold_filter", "params": {"min_abs": 3}}]},
            {"id": "b", "class": PE, "params": {"period": 20}, "weight": 1.0,
             "history_transforms": [{"op": "scale", "params": {"factor": 2}}],
             "transforms": [{"op": "zscore"}, {"op": "clip", "params": {"min": -2, "max": 2}}]},
        ]},
        "trending": {"components": [
            {"id": "c", "class": SMA, "params": {"lookback_L": 30}, "weight": 1.0,
             "transforms": [{"op": "percentile"}]}]},
        "mean_reversion": None, "chop": None,
    },
}


def test_engine_without_vol_target_matches_master_bar_for_bar():
    Old = _old_module("strategies/strategy_engine.py", "_old_strategy_engine").ConfigDrivenStrategyEngine
    new, old = ConfigDrivenStrategyEngine(LEGACY_CFG), Old(LEGACY_CFG)
    assert new.get_required_periods() == old.get_required_periods()
    assert new.lookback == old.lookback and new._warmup == old._warmup
    df = _daily(300, seed=8)
    df["stddev_24"] = df["close"].rolling(24).std()
    n = 0
    for i in range(1, len(df) + 1):
        new.update(df.iloc[:i])
        old.update(df.iloc[:i])
        for regime in (MarketRegime.UNKNOWN, MarketRegime.TRENDING, MarketRegime.CHOP):
            assert new.is_ready(regime) == old.is_ready(regime)
            assert new.forecast(regime) == old.forecast(regime)
            n += 1
    assert n == 900


def test_shipped_strategy_config_required_bars_unchanged():
    old_engine = _old_module("strategies/strategy_engine.py", "_old_strategy_engine2")
    cfg = json.loads((TB_ROOT / "strategy_config.json").read_text(encoding="utf-8"))
    assert ConfigDrivenStrategyEngine(cfg["strategies"]).get_required_periods() == \
        old_engine.ConfigDrivenStrategyEngine(cfg["strategies"]).get_required_periods()
