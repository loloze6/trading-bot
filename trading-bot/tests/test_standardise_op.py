"""
standardise transform op (registry.TRANSFORM_OPS_REGISTRY["standardise"]).

    out = clip(target * h[-1] / mean(|h| over the last `window` values BEFORE
          the current one), -cap, cap)

Pins: the formula on hand-computed cases; the current value is not in its own
denominator; only the last `window` past values count; NaN in the past is
skipped; the 1e-10 guard and the min_periods wait return 0.0; the param check
(standardise_param_errors) and that the op and V15 refuse the same params; V5
lists it as a history op; transform_min_periods = min_periods + 1; the deque
holds window + 1; one ConfigDrivenStrategyEngine run; and that no other op's
registry entry or min-periods entry changed.

All data is synthetic.
"""
import importlib.util
import json
import math
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from strategies.registry import (
    TRANSFORM_MIN_PERIODS,
    TRANSFORM_OPS_REGISTRY,
    apply_transform_pipeline,
    component_effective_lookback,
    standardise_block_forecast,
    standardise_param_errors,
    transform_min_periods,
)
from strategies.strategy_base import MarketRegime
from strategies.strategy_engine import ConfigDrivenStrategyEngine
from tools.validate_config import validate

PE = "strategies.strategy_components.PriceEvolutionComponent"
SMA = "strategies.strategy_components.SmaTrendLongOnlyComponent"
UNGATED = {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"}
P4 = {"window": 4, "min_periods": 2}


def _op(values, p):
    """The op on a history list (the last value is the current one)."""
    return TRANSFORM_OPS_REGISTRY["standardise"](values[-1], pd.Series(values, dtype=float), p, None)


# --- formula, hand computed ---------------------------------------------------

def test_hand_computed_value():
    # past = [1, -2, 3, -4] -> mean |past| = 2.5; current 2 -> 10 * 2 / 2.5 = 8.0
    assert _op([1.0, -2.0, 3.0, -4.0, 2.0], P4) == pytest.approx(8.0, abs=1e-12)


def test_negative_input_keeps_its_sign():
    assert _op([1.0, -2.0, 3.0, -4.0, -2.0], P4) == pytest.approx(-8.0, abs=1e-12)


def test_zero_current_value_stays_zero():
    assert _op([1.0, -2.0, 3.0, -4.0, 0.0], P4) == 0.0


def test_clip_at_plus_and_minus_cap():
    # 10 * 5 / 2.5 = 20 exactly; 10 * 50 / 2.5 = 200 -> clipped to the default cap 20
    assert _op([1.0, -2.0, 3.0, -4.0, 5.0], P4) == 20.0
    assert _op([1.0, -2.0, 3.0, -4.0, 50.0], P4) == 20.0
    assert _op([1.0, -2.0, 3.0, -4.0, -50.0], P4) == -20.0


def test_custom_target_and_cap():
    p = {**P4, "target": 5, "cap": 12.0}
    assert _op([1.0, -2.0, 3.0, -4.0, 2.0], p) == pytest.approx(4.0, abs=1e-12)      # 5 * 2 / 2.5
    assert _op([1.0, -2.0, 3.0, -4.0, 20.0], p) == 12.0                              # 40 -> cap 12
    assert _op([1.0, -2.0, 3.0, -4.0, -20.0], p) == -12.0


def test_defaults_are_target_10_and_cap_20():
    explicit = {**P4, "target": 10, "cap": 20}
    for cur in (2.0, -3.3, 9.0, -77.0):
        assert _op([1.0, -2.0, 3.0, -4.0, cur], P4) == _op([1.0, -2.0, 3.0, -4.0, cur], explicit)


def test_matches_the_shared_block_formula():
    h = [0.5, -1.5, 2.5, -0.5, 3.0, 1.0]
    past = np.abs(h[-5:-1]).mean()
    assert _op(h, P4) == standardise_block_forecast(1.0, float(past), 10.0, 20.0)


# --- no lookahead / window ----------------------------------------------------

def test_current_value_is_not_in_its_own_denominator():
    # past mean 2.5; current 3 -> 10 * 3 / 2.5 = 12.0. With the current value in the
    # mean it would be 10 * 3 / mean([1, 2, 3, 4, 3]) = 10.71...
    assert _op([1.0, -2.0, 3.0, -4.0, 3.0], P4) == pytest.approx(12.0, abs=1e-12)
    assert _op([1.0, -2.0, 3.0, -4.0, 3.0], P4) != pytest.approx(10 * 3 / np.mean([1, 2, 3, 4, 3]))
    # a huge current value is not damped by itself: it saturates at the cap
    assert _op([1.0, -2.0, 3.0, -4.0, 1e9], P4) == 20.0


def test_only_the_last_window_past_values_count():
    base = _op([1.0, -2.0, 3.0, -4.0, 2.0], P4)
    # an old outlier BEFORE the window of 4 past values has no effect
    assert _op([1e6, 1.0, -2.0, 3.0, -4.0, 2.0], P4) == base
    assert _op([-1e6, 7.0, 1.0, -2.0, 3.0, -4.0, 2.0], P4) == base
    # the oldest value INSIDE the window does
    assert _op([1e6, -2.0, 3.0, -4.0, 2.0], P4) != base


def test_future_values_never_change_a_past_output():
    p = {"window": 8, "min_periods": 3}
    h = list(np.random.default_rng(3).normal(0, 3, 40))
    out_at_20 = _op(h[:21], p)
    # the output at bar 20 is a function of h[:21] alone: later bars are not read
    assert _op(h[:21], p) == out_at_20
    assert out_at_20 == pytest.approx(
        float(np.clip(10.0 * h[20] / np.abs(h[12:20]).mean(), -20.0, 20.0)), abs=1e-12)


def test_nan_in_the_past_is_skipped_by_the_mean():
    # past = [1, nan, 3, -4] -> mean |.| skipping nan = 8/3
    got = _op([1.0, float("nan"), 3.0, -4.0, 2.0], P4)
    assert got == pytest.approx(10 * 2 / (8.0 / 3.0), abs=1e-12)


def test_all_nan_past_returns_zero_not_nan():
    assert _op([float("nan")] * 4 + [2.0], P4) == 0.0


# --- guards -------------------------------------------------------------------

def test_past_mean_at_or_below_1e_10_returns_zero():
    assert _op([0.0, 0.0, 0.0, 0.0, 5.0], P4) == 0.0
    assert _op([1e-10, -1e-10, 1e-10, -1e-10, 5.0], P4) == 0.0       # mean exactly 1e-10: not > 1e-10
    assert _op([1e-9, -1e-9, 1e-9, -1e-9, 5.0], P4) == 20.0          # 5e9 -> cap


def test_fewer_than_min_periods_past_values_returns_zero():
    p = {"window": 10, "min_periods": 5}
    cur = 2.0
    for n_past in range(0, 5):
        assert _op([1.0, -2.0, 3.0, -1.0][:n_past] + [cur], p) == 0.0, n_past
    # exactly min_periods past values: a real, non-zero value
    got = _op([1.0, -2.0, 3.0, -1.0, 2.0] + [cur], p)
    assert got == pytest.approx(10 * 2.0 / np.mean([1, 2, 3, 1, 2]), abs=1e-12)
    assert got != 0.0


def test_single_value_history_returns_zero():
    assert _op([5.0], P4) == 0.0


# --- param check --------------------------------------------------------------

@pytest.mark.parametrize("params, needle", [
    ({"min_periods": 2}, "missing param 'window'"),
    ({"window": 4}, "missing param 'min_periods'"),
    ({}, "missing param 'window'"),
    ({"window": True, "min_periods": 2}, "window must be an int >= 2"),
    ({"window": 4.0, "min_periods": 2}, "window must be an int >= 2"),
    ({"window": 1, "min_periods": 2}, "window must be an int >= 2"),
    ({"window": "4", "min_periods": 2}, "window must be an int >= 2"),
    ({"window": 4, "min_periods": 1}, "min_periods must be an int with 2 <= min_periods <= window"),
    ({"window": 4, "min_periods": 5}, "min_periods must be an int with 2 <= min_periods <= window"),
    ({"window": 4, "min_periods": True}, "min_periods must be an int with 2 <= min_periods <= window"),
    ({"window": 4, "min_periods": 2.0}, "min_periods must be an int with 2 <= min_periods <= window"),
    ({**P4, "target": 0}, "target must be a finite number > 0"),
    ({**P4, "target": -1}, "target must be a finite number > 0"),
    ({**P4, "target": float("inf")}, "target must be a finite number > 0"),
    ({**P4, "target": float("nan")}, "target must be a finite number > 0"),
    ({**P4, "target": True}, "target must be a finite number > 0"),
    ({**P4, "target": "10"}, "target must be a finite number > 0"),
    ({**P4, "cap": 0}, "cap must be a finite number > 0"),
    ({**P4, "cap": -20.0}, "cap must be a finite number > 0"),
    ({**P4, "cap": float("inf")}, "cap must be a finite number > 0"),
    ({**P4, "cap": True}, "cap must be a finite number > 0"),
    ([4, 2], "params must be a mapping"),
    (None, "params must be a mapping"),
    ("window=4", "params must be a mapping"),
])
def test_param_errors_refuse_and_the_op_raises_the_same(params, needle):
    errors = standardise_param_errors(params)
    assert errors and any(needle in e for e in errors), errors
    with pytest.raises(ValueError, match="standardise: "):
        TRANSFORM_OPS_REGISTRY["standardise"](1.0, pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]), params, None)


@pytest.mark.parametrize("params", [
    P4,
    {"window": 2, "min_periods": 2},
    {"window": 100, "min_periods": 30, "target": 5, "cap": 12.5},
    {"window": 20, "min_periods": 20, "target": 0.5, "cap": 1},
])
def test_valid_params_give_no_errors(params):
    assert standardise_param_errors(params) == []


# --- V5 / V15 -----------------------------------------------------------------

def _full(transforms):
    return {"regime_detector": UNGATED, "strategies": {"regimes": {
        "unknown": {"components": [{"id": "s", "class": SMA, "params": {"lookback_L": 50},
                                    "weight": 1.0, "transforms": transforms}]},
        "trending": None, "mean_reversion": None, "chop": None}}}


def _v(violations, code):
    return [v for v in violations if v.startswith(f"VIOLATION {code}")]


def test_v15_valid_params_give_no_violation():
    cfg = _full([{"op": "standardise", "params": {"window": 20, "min_periods": 5}}])
    assert validate(cfg) == []
    cfg = _full([{"op": "standardise", "params": {"window": 20, "min_periods": 5, "target": 8, "cap": 15}},
                 {"op": "clip", "params": {"min": -10, "max": 10}}])
    assert validate(cfg) == []


def test_v15_bad_params_give_violation_lines():
    cfg = _full([{"op": "standardise", "params": {"window": 1, "min_periods": 5, "cap": 0}}])
    loc = "strategies.regimes.unknown.components[0].transforms[0].params"
    assert _v(validate(cfg), "V15") == [
        f"VIOLATION V15 {loc}: window must be an int >= 2, got 1",
        f"VIOLATION V15 {loc}: min_periods must be an int with 2 <= min_periods <= window, got 5",
        f"VIOLATION V15 {loc}: cap must be a finite number > 0, got 0",
    ]


def test_v15_missing_params_and_missing_params_key():
    cfg = _full([{"op": "standardise"}])
    loc = "strategies.regimes.unknown.components[0].transforms[0].params"
    assert _v(validate(cfg), "V15") == [
        f"VIOLATION V15 {loc}: missing param 'window'",
        f"VIOLATION V15 {loc}: missing param 'min_periods'",
    ]


def test_v15_and_the_op_refuse_exactly_the_same_params():
    for params in (P4, {"window": 4}, {**P4, "target": 0}, {"window": 4, "min_periods": 9},
                   {**P4, "cap": float("inf")}):
        v15 = [v.split(": ", 1)[1] for v in _v(validate(_full([{"op": "standardise", "params": params}])), "V15")]
        assert v15 == standardise_param_errors(params)


def test_v15_is_silent_for_configs_without_standardise():
    assert not _v(validate(_full([{"op": "identity"}])), "V15")
    assert not _v(validate(_full([{"op": "zscore"}, {"op": "scale", "params": {"factor": 5}}])), "V15")


def test_v5_refuses_standardise_after_a_scalar_op():
    sp = {"op": "standardise", "params": {"window": 20, "min_periods": 5}}
    bad = validate(_full([{"op": "scale", "params": {"factor": 2}}, sp]))
    assert _v(bad, "V5"), bad
    assert not _v(validate(_full([sp, {"op": "scale", "params": {"factor": 2}}])), "V5")


# --- required periods / deque size --------------------------------------------

def test_transform_min_periods_is_min_periods_plus_one():
    assert transform_min_periods("standardise", {"window": 20, "min_periods": 5}) == 6
    assert transform_min_periods("standardise", {"window": 2, "min_periods": 2}) == 3
    assert transform_min_periods("standardise", {"window": 100, "min_periods": 100}) == 101


def test_transform_min_periods_for_invalid_params_is_the_table_entry():
    assert TRANSFORM_MIN_PERIODS["standardise"] == 2
    for bad in ({}, {"window": 1, "min_periods": 5}, {"window": 4}):
        assert transform_min_periods("standardise", bad) == 2


def test_component_effective_lookback_holds_window_plus_one():
    spec = {"id": "s", "transforms": [{"op": "standardise", "params": {"window": 20, "min_periods": 5}}]}
    assert component_effective_lookback(spec, 6) == 21
    assert component_effective_lookback(spec, 50) == 50          # the component's own need is larger
    spec_hist = {"id": "s", "history_transforms": [{"op": "identity"}],
                 "transforms": [{"op": "standardise", "params": {"window": 30, "min_periods": 5}}]}
    assert component_effective_lookback(spec_hist, 6) == 31
    bad = {"id": "s", "transforms": [{"op": "standardise", "params": {"window": 1, "min_periods": 5}}]}
    assert component_effective_lookback(bad, 6) == 6             # invalid params do not size anything


# --- engine -------------------------------------------------------------------

def _bars(n, seed=0):
    rng = np.random.default_rng(seed)
    close = 100.0 * np.exp(np.cumsum(rng.normal(0.0005, 0.02, n)))
    return pd.DataFrame({"timestamp": pd.date_range("2022-01-01", periods=n, freq="D"),
                         "open": close, "high": close * 1.01, "low": close * 0.99,
                         "close": close, "volume": 1.0})


def _engine_cfg(transforms, period=5):
    return {"warmup": 10, "regimes": {
        "unknown": {"components": [{"id": "s", "class": PE, "params": {"period": period},
                                    "weight": 1.0, "transforms": transforms}]},
        "trending": None, "mean_reversion": None, "chop": None}}


SP = {"window": 20, "min_periods": 5}


def test_engine_deque_holds_window_plus_one_and_forecast_is_the_op_on_the_history():
    eng = ConfigDrivenStrategyEngine(_engine_cfg([{"op": "standardise", "params": SP}]))
    h = eng._history["unknown"]["s"]
    assert h.maxlen >= 21 and eng.lookback == 21
    df = _bars(120, seed=4)
    checked = 0
    for i in range(1, len(df) + 1):
        eng.update(df.iloc[:i])
        if not eng.is_ready(MarketRegime.UNKNOWN) or len(h) < 2:
            continue
        values = list(h)
        cur, past = values[-1], np.abs(values[-21:-1])
        expected = 0.0 if len(past) < 5 or not past.mean() > 1e-10 \
            else float(np.clip(10.0 * cur / past.mean(), -20.0, 20.0))
        forecast, debug = eng.forecast(MarketRegime.UNKNOWN)
        assert forecast == pytest.approx(expected, abs=1e-12)
        assert debug["s"]["post_pipeline_value"] == pytest.approx(expected, abs=1e-12)
        assert forecast == apply_transform_pipeline(pd.Series(values), [{"op": "standardise", "params": SP}])
        checked += 1
    assert checked > 50


def test_engine_forecast_is_zero_until_min_periods_past_values_exist_then_nonzero():
    eng = ConfigDrivenStrategyEngine(_engine_cfg([{"op": "standardise", "params": SP}]))
    eng._warmup = 2          # let the engine forecast as soon as the op can
    df = _bars(60, seed=5)
    first_nonzero = None
    for i in range(1, len(df) + 1):
        eng.update(df.iloc[:i])
        h = eng._history["unknown"]["s"]
        if len(h) < 2:
            continue
        forecast, _ = eng.forecast(MarketRegime.UNKNOWN)
        if len(h) <= 5:                  # min_periods past values need len(h) >= 6
            assert forecast == 0.0, len(h)
        elif first_nonzero is None and forecast != 0.0:
            first_nonzero = len(h)
    assert first_nonzero == 6


def test_engine_required_periods_follow_the_larger_of_component_and_window():
    eng = ConfigDrivenStrategyEngine(_engine_cfg([{"op": "standardise", "params": SP}]))
    plain = ConfigDrivenStrategyEngine(_engine_cfg([{"op": "identity"}]))
    assert plain.lookback == 6 and plain.get_required_periods() == 6
    assert eng.lookback == 21
    assert eng._data_periods == 0                     # a history op reads no OHLCV window


# --- every other op / config unchanged ------------------------------------------

BASE_COMMIT = "022226b2"  # master before the standardise op
TB_ROOT = Path(__file__).resolve().parents[1]


def _old_module(rel, name):
    try:
        src = subprocess.run(["git", "show", f"{BASE_COMMIT}:trading-bot/{rel}"], cwd=TB_ROOT,
                             capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        pytest.skip(f"base commit {BASE_COMMIT} not reachable via git: {exc}")
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader=None))
    exec(compile(src, f"{name}.py", "exec"), mod.__dict__)
    return mod


def test_every_other_op_and_min_periods_entry_is_unchanged():
    old = _old_module("strategies/registry.py", "_old_registry_s")
    assert set(TRANSFORM_OPS_REGISTRY) - set(old.TRANSFORM_OPS_REGISTRY) == {"standardise"}
    assert old.TRANSFORM_MIN_PERIODS == {k: v for k, v in TRANSFORM_MIN_PERIODS.items() if k != "standardise"}
    d = _bars(200, seed=5)
    d["stddev_24"] = d["close"].rolling(24).std()
    h = pd.Series(np.random.default_rng(6).normal(0, 3, 120))
    params = {"factor": 3, "min_abs": 1, "min": -2, "max": 2, "span": 7, "period": 20,
              "window": 60, "target_annual_vol": 0.4, "periods_per_year": 365}  # last three: vol_target
    for op in old.TRANSFORM_OPS_REGISTRY:
        new_v = TRANSFORM_OPS_REGISTRY[op](1.7, h, params, d)
        old_v = old.TRANSFORM_OPS_REGISTRY[op](1.7, h, params, d)
        assert new_v == old_v or (math.isnan(new_v) and math.isnan(old_v)), op
        assert transform_min_periods(op, params) == old.transform_min_periods(op, params), op


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


def test_engine_without_standardise_matches_master_bar_for_bar():
    Old = _old_module("strategies/strategy_engine.py", "_old_strategy_engine_s").ConfigDrivenStrategyEngine
    new, old = ConfigDrivenStrategyEngine(LEGACY_CFG), Old(LEGACY_CFG)
    assert new.get_required_periods() == old.get_required_periods()
    assert new.lookback == old.lookback and new._warmup == old._warmup
    df = _bars(300, seed=8)
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


def test_shipped_strategy_config_required_periods_and_lookback_unchanged():
    old_engine = _old_module("strategies/strategy_engine.py", "_old_strategy_engine_s2")
    cfg = json.loads((TB_ROOT / "strategy_config.json").read_text(encoding="utf-8"))
    new, old = (ConfigDrivenStrategyEngine(cfg["strategies"]),
                old_engine.ConfigDrivenStrategyEngine(cfg["strategies"]))
    assert new.get_required_periods() == old.get_required_periods()
    assert new.lookback == old.lookback
