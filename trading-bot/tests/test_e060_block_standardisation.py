"""
E-060 S3a -- block standardisation at combination time (engine side).

The opt-in `blocks` + `block_standardisation` keys on a strategies regime make
ConfigDrivenStrategyEngine keep each block's FINAL forecast history and
combine blocks as sum(W_b / sum W) * target * v_t / mean(|v_{t-w+1..t}|).
Pins: past-only, scale-only (bias kept), ~target once warm, warm-up, the
validator (V13), and that configs without the keys -- every existing config
-- are byte-identical (engine output vs the pre-S3a engine source; transform
ops unchanged).
"""
import importlib.util
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from strategies.registry import TRANSFORM_OPS_REGISTRY, apply_transform_pipeline, standardise_block_forecast
from strategies.strategy_base import MarketRegime
from strategies.strategy_engine import ConfigDrivenStrategyEngine, validate_block_combiner
from tools.validate_config import validate

PE = "strategies.strategy_components.PriceEvolutionComponent"
BASE_COMMIT = "44421b31"  # master before E-060 S3a
TB_ROOT = Path(__file__).resolve().parents[1]


def _ohlcv(n, seed=0, drift=0.0):
    rng = np.random.default_rng(seed)
    close = 100.0 * np.exp(np.cumsum(rng.normal(drift, 0.01, n)))
    return pd.DataFrame({"timestamp": pd.date_range("2024-01-01", periods=n, freq="h"),
                         "open": close, "high": close * 1.001, "low": close * 0.999,
                         "close": close, "volume": 1.0})


def _std_series(values, window):
    """The engine's formula applied bar by bar to a plain list (reference)."""
    out = []
    for t in range(len(values)):
        h = pd.Series(values[max(0, t - window + 1): t + 1])
        out.append(standardise_block_forecast(h, 10.0))
    return out


# --- the standardisation function ------------------------------------------

def test_past_only_future_bars_never_change_past_values():
    rng = np.random.default_rng(1)
    v = list(rng.normal(0.5, 2.0, 600))
    full = _std_series(v, 200)
    short = _std_series(v[:350], 200)
    assert full[:350] == short  # exact: nothing after bar t enters bar t


def test_scale_only_keeps_directional_bias_and_zeros():
    rng = np.random.default_rng(2)
    v = list(np.abs(rng.normal(3.0, 1.0, 400)) * np.where(rng.random(400) < 0.85, 1, -1))
    v[10] = 0.0
    s = _std_series(v, 100)
    assert all(np.sign(a) == np.sign(b) for a, b in zip(v, s))  # sign preserved bar by bar
    assert sum(x > 0 for x in s[100:]) / len(s[100:]) > 0.75     # mostly positive stays so
    assert s[10] == 0.0


def test_averages_about_ten_once_warm():
    rng = np.random.default_rng(3)
    v = list(rng.normal(0.0, 0.37, 5000))  # arbitrary raw scale
    s = _std_series(v, 500)
    m = float(np.mean(np.abs(s[500:])))
    assert 9.5 < m < 10.5, m


def test_zero_history_gives_zero_not_nan():
    assert standardise_block_forecast(pd.Series([0.0, 0.0, 0.0])) == 0.0
    assert standardise_block_forecast(pd.Series([], dtype=float)) == 0.0


# --- existing transform ops: unchanged (flag-off identity) -----------------

def test_transform_ops_registry_is_unchanged():
    assert sorted(TRANSFORM_OPS_REGISTRY) == sorted([
        "identity", "percentile", "negate_percentile", "zscore", "ratio_to_mean", "ema",
        "scale", "threshold_filter", "clip", "sigmoid", "negate", "vol_normalize",
        "vol_adjusted", "price_normalized", "volume_filter"])
    h = pd.Series([1.0, -2.0, 3.0, 0.5, 4.0])
    assert apply_transform_pipeline(h, [{"op": "ratio_to_mean"}]) == 4.0 / h.abs().mean()
    z = (4.0 - h.mean()) / h.std()
    assert apply_transform_pipeline(h, [{"op": "zscore"}, {"op": "scale", "params": {"factor": 10}}]) \
        == pytest.approx(10 * z, abs=0)


def _old_engine_class():
    try:
        src = subprocess.run(["git", "show", f"{BASE_COMMIT}:trading-bot/strategies/strategy_engine.py"],
                             cwd=TB_ROOT, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        pytest.skip(f"base commit {BASE_COMMIT} not reachable via git: {exc}")
    spec = importlib.util.spec_from_loader("_old_strategy_engine", loader=None)
    mod = importlib.util.module_from_spec(spec)
    exec(compile(src, "old_strategy_engine.py", "exec"), mod.__dict__)
    return mod.ConfigDrivenStrategyEngine


LEGACY_CFG = {
    "warmup": 30,
    "regimes": {
        "unknown": {"components": [
            {"id": "a", "class": PE, "params": {"period": 5}, "weight": 2.0, "lookback": 200,
             "transforms": [{"op": "ratio_to_mean"}, {"op": "scale", "params": {"factor": 10}},
                            {"op": "threshold_filter", "params": {"min_abs": 3}}]},
            {"id": "b", "class": PE, "params": {"period": 20}, "weight": 1.0,
             "transforms": [{"op": "zscore"}, {"op": "clip", "params": {"min": -2, "max": 2}}]},
        ]},
        "trending": {"components": [
            {"id": "c", "class": PE, "params": {"period": 10}, "weight": 1.0,
             "transforms": [{"op": "percentile"}]}]},
        "mean_reversion": None, "chop": None,
    },
}


def test_engine_without_block_keys_matches_pre_s3a_engine_bar_for_bar():
    Old = _old_engine_class()
    new, old = ConfigDrivenStrategyEngine(LEGACY_CFG), Old(LEGACY_CFG)
    df = _ohlcv(400, seed=4)
    n_compared = 0
    for i in range(1, len(df) + 1):
        new.update(df.iloc[:i])
        old.update(df.iloc[:i])
        for regime in (MarketRegime.UNKNOWN, MarketRegime.TRENDING, MarketRegime.CHOP):
            assert new.is_ready(regime) == old.is_ready(regime)
            assert new.forecast(regime) == old.forecast(regime)
            n_compared += 1
    assert n_compared == 1200
    assert new._block_cfgs == {} and new._block_hist == {}


# --- the combiner in the engine --------------------------------------------

def _block_cfg(window=100, min_periods=30, w=(1.0, 3.0)):
    return {
        "warmup": 10,
        "regimes": {
            "unknown": {
                "components": [
                    {"id": "b0__x", "class": PE, "params": {"period": 5}, "weight": 1.0,
                     "transforms": [{"op": "identity"}]},
                    {"id": "b1__y", "class": PE, "params": {"period": 12}, "weight": 2.0,
                     "transforms": [{"op": "identity"}, {"op": "scale", "params": {"factor": 50}}]},
                    {"id": "b1__z", "class": PE, "params": {"period": 3}, "weight": 1.0,
                     "transforms": [{"op": "identity"}]},
                ],
                "blocks": [{"id": "b0", "weight": w[0], "components": ["b0__x"]},
                           {"id": "b1", "weight": w[1], "components": ["b1__y", "b1__z"]}],
                "block_standardisation": {"target": 10.0, "window": window,
                                          "min_periods": min_periods},
            },
            "trending": None, "mean_reversion": None, "chop": None,
        },
    }


def _run(cfg, df):
    eng = ConfigDrivenStrategyEngine(cfg)
    out = []
    for i in range(1, len(df) + 1):
        eng.update(df.iloc[:i])
        out.append((eng.is_ready(MarketRegime.UNKNOWN),) + eng.forecast(MarketRegime.UNKNOWN))
    return eng, out


def test_engine_combines_standardised_final_block_forecasts():
    df = _ohlcv(300, seed=5)
    eng, out = _run(_block_cfg(), df)
    # reference: each block's final (weighted, clipped) forecast, standardised past-only
    raw = {"b0": [], "b1": []}
    hist = eng._block_hist["unknown"]
    assert len(hist["b0"]) == len(hist["b1"]) > 30
    for bid in raw:
        raw[bid] = list(hist[bid])
    ready, f, dbg = out[-1]
    assert ready
    s0 = standardise_block_forecast(pd.Series(raw["b0"]), 10.0)
    s1 = standardise_block_forecast(pd.Series(raw["b1"]), 10.0)
    assert f == pytest.approx(float(np.clip(0.25 * s0 + 0.75 * s1, -20, 20)), rel=1e-12)
    assert dbg["b1"]["post_pipeline_value"] == pytest.approx(s1, rel=1e-12)
    assert dbg["b1"]["weight_normalized"] == 0.75
    # the block's raw value = its components weighted within the block, clipped +-20
    y = apply_transform_pipeline(pd.Series(list(eng._history["unknown"]["b1__y"])),
                                 [{"op": "identity"}, {"op": "scale", "params": {"factor": 50}}])
    z = float(eng._history["unknown"]["b1__z"][-1])
    assert raw["b1"][-1] == pytest.approx(float(np.clip((2 * y + z) / 3, -20, 20)), rel=1e-12)


def test_engine_past_only_prefix_identical_when_bars_are_appended():
    df = _ohlcv(260, seed=6)
    _, long = _run(_block_cfg(window=50, min_periods=20), df)
    _, short = _run(_block_cfg(window=50, min_periods=20), df.iloc[:180])
    assert long[:180] == short


def test_engine_warmup_emits_zero_and_not_ready_until_min_periods():
    df = _ohlcv(200, seed=7)
    eng, out = _run(_block_cfg(min_periods=40), df)
    first_ready = next(i for i, (r, _f, _d) in enumerate(out) if r)
    assert all(f == 0.0 for r, f, _d in out[:first_ready])
    assert all("not_ready_block" in d or d.get("not_ready_component") for r, _f, d in out[:first_ready])
    # ready exactly when both block histories hold min_periods values
    eng2 = ConfigDrivenStrategyEngine(_block_cfg(min_periods=40))
    for i in range(1, first_ready + 2):  # out[k] is after bar k+1
        eng2.update(df.iloc[:i])
    assert min(len(h) for h in eng2._block_hist["unknown"].values()) == 40
    eng.reset_history()
    assert all(len(h) == 0 for h in eng._block_hist["unknown"].values())
    assert not eng.is_ready(MarketRegime.UNKNOWN)


def test_engine_weights_only_change_the_mix():
    df = _ohlcv(200, seed=8)
    eng_a, a = _run(_block_cfg(w=(1.0, 1.0)), df)
    eng_b, b = _run(_block_cfg(w=(5.0, 5.0)), df)
    assert a == b  # weights are normalised


@pytest.mark.parametrize("mutate, needle", [
    (lambda r: r.pop("block_standardisation"), "needs both"),
    (lambda r: r["blocks"][0].update(weight=0), "weight"),
    (lambda r: r["blocks"][0].update(components=["nope"]), "not components"),
    (lambda r: r["blocks"][1].update(components=["b1__y"]), "belong to no block"),
    (lambda r: r["blocks"][1].update(components=["b0__x", "b1__y", "b1__z"]), "more than one block"),
    (lambda r: r["blocks"][1].update(id="b0"), "duplicated"),
    (lambda r: r["blocks"][1].update(id="b0__x"), "component id"),
    (lambda r: r["block_standardisation"].update(min_periods=1), "min_periods"),
    (lambda r: r["block_standardisation"].update(window=10, min_periods=20), "min_periods"),
    (lambda r: r["block_standardisation"].update(target=-1), "target"),
    (lambda r: r["block_standardisation"].update(extra=1), "exactly keys"),
    (lambda r: r["components"][0].update(weight=0.0), "summing to > 0"),
])
def test_malformed_combiner_fails_loud_in_engine_and_validator(mutate, needle):
    cfg = _block_cfg()
    mutate(cfg["regimes"]["unknown"])
    errs = validate_block_combiner("unknown", cfg["regimes"]["unknown"])
    assert errs and any(needle in e for e in errs), errs
    with pytest.raises(ValueError, match="strategies.regimes.unknown"):
        ConfigDrivenStrategyEngine(cfg)
    full = {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                                "default_regime": "unknown"}, "strategies": cfg}
    assert any(v.startswith("VIOLATION V13") for v in validate(full))


def test_validator_silent_without_block_keys():
    full = {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                                "default_regime": "unknown"}, "strategies": LEGACY_CFG}
    assert not [v for v in validate(full) if "V13" in v]
    assert validate_block_combiner("unknown", None) == []
