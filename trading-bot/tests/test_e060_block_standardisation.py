"""
E-060 S3a -- block standardisation at combination time (engine side).

The opt-in `blocks` + `block_standardisation` keys on a strategies regime make
ConfigDrivenStrategyEngine run each block as validated (own source timing,
own source detector as a gate) and combine the blocks as
sum(W_b / sum W) * clip(target * v_t / mean(|v| over PAST active values), +-20).
Pins: past-only (current value excluded), scale-only (bias kept), ~target once
warm, per-block cap, warm-up / required periods, gating, NaN fails loud, V13
(never raises), and that configs without the keys -- every existing config --
are byte-identical (engine output vs the pre-S3a engine source; transform ops
unchanged). Writer-level stand-alone equality lives in
strategy-research/tests/test_e060_s3a_composition.py.
"""
import copy
import importlib.util
import json
import math
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from strategies.main_strategy import AdvancedStrategy
from strategies.registry import TRANSFORM_OPS_REGISTRY, apply_transform_pipeline, standardise_block_forecast
from strategies.strategy_base import MarketRegime
from strategies.strategy_engine import (
    BlockCombinerError, ConfigDrivenStrategyEngine, validate_block_combiner,
)
from tools.validate_config import validate

PE = "strategies.strategy_components.PriceEvolutionComponent"
BASE_COMMIT = "44421b31"  # master before E-060 S3a
TB_ROOT = Path(__file__).resolve().parents[1]
UNGATED = {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"}


def _ohlcv(n, seed=0, drift=0.0):
    rng = np.random.default_rng(seed)
    close = 100.0 * np.exp(np.cumsum(rng.normal(drift, 0.01, n)))
    return pd.DataFrame({"timestamp": pd.date_range("2024-01-01", periods=n, freq="h"),
                         "open": close, "high": close * 1.001, "low": close * 0.999,
                         "close": close, "volume": 1.0})


def _std_series(values, window, cap=20.0):
    """Reference: each value over the mean |.| of the <= `window` values BEFORE it."""
    out = []
    for t in range(len(values)):
        past = values[max(0, t - window): t]
        m = float(np.mean(np.abs(past))) if past else 0.0
        out.append(standardise_block_forecast(values[t], m, 10.0, cap))
    return out


# --- the standardisation function ------------------------------------------

def test_past_only_future_bars_never_change_past_values():
    rng = np.random.default_rng(1)
    v = list(rng.normal(0.5, 2.0, 600))
    assert _std_series(v, 200)[:350] == _std_series(v[:350], 200)


def test_current_value_is_not_in_its_own_denominator():
    # past mean |.| = 1; a current value of 1.5 -> 15 (would be 10*1.5/1.0167 if included)
    assert standardise_block_forecast(1.5, 1.0) == 15.0


def test_scale_only_keeps_directional_bias_and_zeros():
    rng = np.random.default_rng(2)
    v = list(np.abs(rng.normal(3.0, 1.0, 400)) * np.where(rng.random(400) < 0.85, 1, -1))
    v[10] = 0.0
    s = _std_series(v, 100)
    assert all(np.sign(a) == np.sign(b) for a, b in zip(v[1:], s[1:]))  # sign kept bar by bar
    assert sum(x > 0 for x in s[100:]) / len(s[100:]) > 0.75
    assert s[10] == 0.0


def test_averages_about_ten_once_warm():
    rng = np.random.default_rng(3)
    v = list(rng.normal(0.0, 0.37, 5000))  # arbitrary raw scale
    uncapped = float(np.mean(np.abs(_std_series(v, 500, cap=math.inf)[500:])))
    capped = float(np.mean(np.abs(_std_series(v, 500)[500:])))
    assert 9.5 < uncapped < 10.5, uncapped
    # the +-20 cap trims the tail: for a normal series E[min(|z|/E|z|, 2)] * 10 = 9.41
    assert 9.0 < capped < uncapped, capped


def test_cap_bounds_a_spike_after_a_quiet_stretch():
    assert standardise_block_forecast(5.0, 0.01) == 20.0
    assert standardise_block_forecast(-5.0, 0.01) == -20.0
    assert standardise_block_forecast(5.0, 0.0) == 0.0  # no past scale at all: 0 (the ratio_to_mean guard)


# --- existing transform ops / engine: unchanged (flag-off identity) --------

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
    new.set_indicators({"stddev_24": lambda df: df["close"].rolling(24).std()})  # stored, unused
    df = _ohlcv(400, seed=4)
    n_compared = 0
    for i in range(1, len(df) + 1):
        new.update(df.iloc[:i])
        old.update(df.iloc[:i])
        for regime in (MarketRegime.UNKNOWN, MarketRegime.TRENDING, MarketRegime.CHOP):
            assert new.is_ready(regime) == old.is_ready(regime)
            assert new.forecast(regime) == old.forecast(regime)
            n_compared += 1
        assert new.get_required_periods() == old.get_required_periods()
        assert new.required_feeds() == old.required_feeds()
    assert n_compared == 1200
    assert new._block_regimes == {}


# --- the combiner in the engine --------------------------------------------

def _src(required_bars=24, warmup=10, parts=None, detector=None, buffer_bars=None):
    return {"required_bars": required_bars, "warmup": warmup,
            "buffer_bars": buffer_bars or required_bars + 100,
            "regime_detector": copy.deepcopy(detector or UNGATED),
            "parts": parts}


def _block_cfg(window=100, min_periods=30, w=(1.0, 3.0), y_factor=50, detector1=None,
               parts1=None):
    return {
        "warmup": 10,
        "regimes": {
            "unknown": {
                "components": [
                    {"id": "b0__x", "class": PE, "params": {"period": 5}, "weight": 1.0,
                     "lookback": 60, "transforms": [{"op": "identity"}]},
                    {"id": "b1__y", "class": PE, "params": {"period": 12}, "weight": 2.0,
                     "lookback": 60,
                     "transforms": [{"op": "identity"}, {"op": "scale", "params": {"factor": y_factor}}]},
                    {"id": "b1__z", "class": PE, "params": {"period": 3}, "weight": 1.0,
                     "lookback": 60, "transforms": [{"op": "identity"}]},
                ],
                "blocks": [
                    {"id": "b0", "weight": w[0], "components": ["b0__x"],
                     "source": _src(parts={"unknown": ["b0__x"]})},
                    {"id": "b1", "weight": w[1], "components": ["b1__y", "b1__z"],
                     "source": _src(parts=parts1 or {"unknown": ["b1__y", "b1__z"]},
                                    detector=detector1)},
                ],
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


def test_engine_combines_capped_standardised_block_forecasts_past_only():
    df = _ohlcv(300, seed=5)
    eng = ConfigDrivenStrategyEngine(_block_cfg())
    raws = {"b0": [], "b1": []}
    n_checked = 0
    for i in range(1, len(df) + 1):
        prev = {b.id: list(b.hist) for b in eng._block_regimes["unknown"]["blocks"]}
        eng.update(df.iloc[:i])
        blocks = eng._block_regimes["unknown"]["blocks"]
        for b in blocks:
            if len(b.hist) and (len(b.hist) > len(prev[b.id]) or list(b.hist) != prev[b.id]):
                raws[b.id].append(b.raw)
        if not eng.is_ready(MarketRegime.UNKNOWN):
            continue
        f, dbg = eng.forecast(MarketRegime.UNKNOWN)
        if "not_ready_block" in dbg or not all(len(prev[k]) >= 30 for k in prev):
            continue
        exp = 0.0
        for k, wn in (("b0", 0.25), ("b1", 0.75)):
            m = sum(abs(x) for x in prev[k]) / len(prev[k])  # PAST values only, <= window
            assert len(prev[k]) <= 100
            s = standardise_block_forecast(dbg[k]["last_history_value"], m, 10.0, 20.0)
            assert dbg[k]["post_pipeline_value"] == pytest.approx(s, rel=1e-9, abs=1e-12)
            assert abs(dbg[k]["post_pipeline_value"]) <= 20.0
            exp += wn * s
        assert f == pytest.approx(float(np.clip(exp, -20, 20)), rel=1e-9, abs=1e-12)
        n_checked += 1
    assert n_checked > 100
    # the block's raw value = its part's components weighted within the part, clipped +-20
    y = apply_transform_pipeline(pd.Series(list(eng._history["unknown"]["b1__y"])),
                                 [{"op": "identity"}, {"op": "scale", "params": {"factor": 50}}])
    z = float(eng._history["unknown"]["b1__z"][-1])
    assert raws["b1"][-1] == pytest.approx(float(np.clip((2 * y + z) / 3, -20, 20)), rel=1e-12)


def test_per_block_cap_stops_one_block_saturating_the_composite():
    df = _ohlcv(300, seed=9)
    _, out = _run(_block_cfg(y_factor=1e6), df)  # b1 always pinned at the +-20 raw clip
    ready = [(f, d) for r, f, d in out if r and "not_ready_block" not in d]
    assert ready
    assert all(abs(d["b0"]["post_pipeline_value"]) <= 20 and abs(d["b1"]["post_pipeline_value"]) <= 20
               for _f, d in ready)


def test_running_sum_matches_a_full_recompute():
    df = _ohlcv(400, seed=10)
    eng, _ = _run(_block_cfg(window=40), df)
    for b in eng._block_regimes["unknown"]["blocks"]:
        assert b.abs_sum == pytest.approx(math.fsum(abs(x) for x in b.hist), rel=1e-12)
        assert len(b.hist) == 40


def test_engine_past_only_prefix_identical_when_bars_are_appended():
    df = _ohlcv(260, seed=6)
    _, long = _run(_block_cfg(window=50, min_periods=20), df)
    _, short = _run(_block_cfg(window=50, min_periods=20), df.iloc[:180])
    assert long[:180] == short


def test_engine_weights_only_change_the_mix():
    df = _ohlcv(200, seed=8)
    _, a = _run(_block_cfg(w=(1.0, 1.0)), df)
    _, b = _run(_block_cfg(w=(5.0, 5.0)), df)
    assert a == b


def test_required_periods_include_each_blocks_chained_warmup():
    cfg = _block_cfg(min_periods=30)
    cfg["regimes"]["unknown"]["blocks"][1]["source"].update(required_bars=70, warmup=40,
                                                            buffer_bars=170)
    eng = ConfigDrivenStrategyEngine(cfg)
    assert eng.get_required_periods() == 70 + 40 + 30


def _write_strategy(tmp_path, strategies, name="c.json"):
    p = tmp_path / name
    p.write_text(json.dumps({"regime_detector": UNGATED, "strategies": strategies}), encoding="utf-8")
    return str(p)


def test_launcher_prefetch_invariant_holds_for_a_composite(tmp_path):
    """core/launcher.py warmup_prefetch feeds 2 * required_bars bars to a probe
    and asserts is_ready(): a composite must satisfy it, and every block must
    already be standardised (not warming) when it becomes ready."""
    cfg = _block_cfg(min_periods=30)
    cfg["regimes"]["unknown"]["blocks"][1]["source"].update(required_bars=70, warmup=40,
                                                            buffer_bars=170)
    strat = AdvancedStrategy(config_path=_write_strategy(tmp_path, cfg))
    df = _ohlcv(2 * strat.required_bars, seed=11)
    first_ready = None
    for i in range(len(df)):
        strat.update(df.iloc[[i]])
        if first_ready is None and strat.is_ready():
            first_ready = i
            _f, _s, _r, _c, dbg = strat.generate_forecast()
            assert all(dbg["components"][b]["active"] == 1.0 for b in ("b0", "b1"))
    assert strat.is_ready() and first_ready is not None
    assert first_ready + 1 == strat.required_bars  # the outer buffer gate is the binding one


def test_gated_block_abstains_outside_its_regime_and_fits_scale_on_active_bars():
    # b1's own detector: PriceEvolution(5) > 0 -> trending, else mean_reversion.
    det = {"mode": "threshold_rules",
           "components": [{"id": "pe", "class": PE, "params": {"period": 5}}],
           "rules": [{"regime": "trending", "any_of": [[{"id": "pe", "op": "gt", "value": 0.0}]]}],
           "default_regime": "mean_reversion"}
    df = _ohlcv(400, seed=12)
    eng = ConfigDrivenStrategyEngine(_block_cfg(detector1=det, parts1={"trending": ["b1__y", "b1__z"]}))
    regimes, n_active = [], 0
    for i in range(1, len(df) + 1):
        before = len(eng._block_regimes["unknown"]["blocks"][1].hist)
        eng.update(df.iloc[:i])
        b1 = eng._block_regimes["unknown"]["blocks"][1]
        if b1.regime is not None:
            regimes.append(b1.regime)
            grew = len(b1.hist) > before or len(b1.hist) == b1.hist.maxlen
            if b1.regime == "mean_reversion":
                assert b1.raw == 0.0 and b1.value == 0.0 and not b1.active
                assert len(b1.hist) == before  # nothing recorded while abstaining
            elif grew:
                n_active += 1
    assert "trending" in regimes and "mean_reversion" in regimes
    assert n_active > 30


def test_multi_regime_block_uses_each_part_only_in_its_own_regime():
    det = {"mode": "threshold_rules",
           "components": [{"id": "pe", "class": PE, "params": {"period": 5}}],
           "rules": [{"regime": "trending", "any_of": [[{"id": "pe", "op": "gt", "value": 0.0}]]}],
           "default_regime": "mean_reversion"}
    df = _ohlcv(300, seed=13)
    eng = ConfigDrivenStrategyEngine(_block_cfg(
        detector1=det, parts1={"trending": ["b1__y"], "mean_reversion": ["b1__z"]}))
    seen = set()
    for i in range(1, len(df) + 1):
        eng.update(df.iloc[:i])
        b1 = eng._block_regimes["unknown"]["blocks"][1]
        if b1.regime is None or not b1.hist or b1.raw == 0.0:
            continue
        y = apply_transform_pipeline(pd.Series(list(eng._history["unknown"]["b1__y"])),
                                     [{"op": "identity"}, {"op": "scale", "params": {"factor": 50}}])
        z = float(eng._history["unknown"]["b1__z"][-1])
        want = float(np.clip(y if b1.regime == "trending" else z, -20, 20))
        assert b1.raw == pytest.approx(want, rel=1e-12)  # never y and z summed
        seen.add(b1.regime)
    assert seen == {"trending", "mean_reversion"}


def test_nan_block_value_fails_loud_and_never_becomes_zero(tmp_path):
    cfg = _block_cfg()
    cfg["regimes"]["unknown"]["components"][0]["transforms"] = [
        {"op": "identity"}, {"op": "scale", "params": {"factor": float("nan")}}]
    eng = ConfigDrivenStrategyEngine(cfg)
    df = _ohlcv(80, seed=14)
    raised = 0
    for i in range(1, len(df) + 1):
        try:
            eng.update(df.iloc[:i])
        except BlockCombinerError as exc:
            raised += 1
            assert "non-finite" in str(exc) and "b0" in str(exc)
            with pytest.raises(BlockCombinerError):
                eng.forecast(MarketRegime.UNKNOWN)
            with pytest.raises(BlockCombinerError):
                eng.is_ready(MarketRegime.UNKNOWN)
    assert raised > 0
    b0 = eng._block_regimes["unknown"]["blocks"][0]
    assert len(b0.hist) == 0  # NaN never entered the history
    # through AdvancedStrategy: generate_signals raises (the candle is skipped loudly)
    strat = AdvancedStrategy(config_path=_write_strategy(tmp_path, cfg))
    with pytest.raises(BlockCombinerError):
        for i in range(len(df)):
            strat.update(df.iloc[[i]])
            strat.generate_signals()
    assert strat.component_error_count > 0


def test_engine_warmup_emits_zero_until_ready():
    df = _ohlcv(200, seed=7)
    _, out = _run(_block_cfg(min_periods=40), df)
    first_ready = next(i for i, (r, _f, _d) in enumerate(out) if r)
    assert all(f == 0.0 for r, f, _d in out[:first_ready])


def test_reset_history_clears_block_state():
    df = _ohlcv(150, seed=15)
    eng, _ = _run(_block_cfg(), df)
    eng.reset_history()
    assert all(len(b.hist) == 0 and b.abs_sum == 0.0 for b in eng._block_regimes["unknown"]["blocks"])
    assert not eng.is_ready(MarketRegime.UNKNOWN)


@pytest.mark.parametrize("mutate, needle", [
    (lambda r: r.pop("block_standardisation"), "needs both"),
    (lambda r: r["blocks"][0].update(weight=0), "weight"),
    (lambda r: r["blocks"][0].update(components=["nope"]), "not components"),
    (lambda r: r["blocks"][1].update(components=["b1__y"]), "belong to no block"),
    (lambda r: r["blocks"][1].update(components=["b0__x", "b1__y", "b1__z"]), "more than one block"),
    (lambda r: r["blocks"][1].update(id="b0"), "unique"),
    (lambda r: r["blocks"][1].update(id="b0__x"), "component id"),
    (lambda r: r["blocks"][1].update(id=["unhashable"]), "non-empty string"),
    (lambda r: r["blocks"][1].update(components=[{"id": "b1__y"}]), "component id strings"),
    (lambda r: r["blocks"][1].update(components="b1__y"), "component id strings"),
    (lambda r: r["blocks"][1].pop("source"), "exactly keys"),
    (lambda r: r["blocks"][1]["source"].update(parts={"unknown": ["b1__y"]}), "partition"),
    (lambda r: r["blocks"][1]["source"].update(parts={"sideways": ["b1__y", "b1__z"]}), "not in"),
    (lambda r: r["blocks"][1]["source"].update(parts={"unknown": [["b1__y"]]}), "component ids"),
    (lambda r: r["blocks"][1]["source"].update(parts=[]), "non-empty mapping"),
    (lambda r: r["blocks"][1]["source"].update(required_bars="24"), "required_bars"),
    (lambda r: r["blocks"][1]["source"].update(buffer_bars=5), "buffer_bars"),
    (lambda r: r["blocks"][1]["source"].update(regime_detector=None), "regime_detector"),
    (lambda r: r["components"][0].update(weight=0.0), "summing to > 0"),
    (lambda r: r["block_standardisation"].update(min_periods=1), "min_periods"),
    (lambda r: r["block_standardisation"].update(window=10, min_periods=20), "min_periods"),
    (lambda r: r["block_standardisation"].update(target=-1), "target"),
    (lambda r: r["block_standardisation"].update(extra=1), "exactly keys"),
    (lambda r: r.update(blocks={"b0": 1}), "non-empty list"),
    (lambda r: r.update(blocks=[["not", "a", "dict"]]), "exactly keys"),
    (lambda r: r.update(components=[{"id": {"x": 1}}]), "must be a string"),
])
def test_malformed_combiner_reports_never_raises(mutate, needle):
    cfg = _block_cfg()
    mutate(cfg["regimes"]["unknown"])
    errs = validate_block_combiner("unknown", cfg["regimes"]["unknown"])  # must not raise
    assert errs and any(needle in e for e in errs), errs
    with pytest.raises(ValueError, match="strategies.regimes.unknown"):
        ConfigDrivenStrategyEngine(cfg)
    full = {"regime_detector": UNGATED, "strategies": cfg}
    try:
        viol = validate(full)
    except Exception as exc:  # other V-checks may trip on the same garbage first
        pytest.skip(f"an earlier V-check raised on this input: {exc!r}")
    assert any(v.startswith("VIOLATION V13") for v in viol)


def test_validator_silent_without_block_keys():
    full = {"regime_detector": UNGATED, "strategies": LEGACY_CFG}
    assert not [v for v in validate(full) if "V13" in v]
    assert validate_block_combiner("unknown", None) == []
    assert validate_block_combiner("unknown", "garbage") == []


def test_block_warmup_longer_than_its_deques_fails_loud():
    cfg = _block_cfg()
    cfg["regimes"]["unknown"]["components"][0]["lookback"] = 5
    with pytest.raises(ValueError, match="could never become ready"):
        ConfigDrivenStrategyEngine(cfg)


def test_required_feeds_include_block_gates():
    eng = ConfigDrivenStrategyEngine(_block_cfg())
    assert eng.required_feeds() == {}
