"""
Every example config in strategy-research/docs/STRATEGY_DESIGN_GUIDE.md is executed here, and the property the
guide states about it is asserted on a seeded synthetic price path (no market data).

An example is a fenced ```json block right after an HTML comment ``<!-- example: <name> -->``. For each one:
  1. `validate_config.validate()` returns no violations;
  2. `ConfigDrivenStrategyEngine(config["strategies"])` is fed the synthetic path bar by bar;
  3. the guide's claim about it holds (exact weighted-mean identities, sign, range, gradedness).
A marked example with no property function here fails the suite, so a new example cannot ship untested.

The rest of the file pins the factual claims the guide makes about the engine (first-forecast bars, ignored
`strategies.warmup`, silent behaviours, the score-product arithmetic, the production component snippet).
"""
import copy
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TRADING_BOT = REPO_ROOT / "trading-bot"
GUIDE_PATH = REPO_ROOT / "strategy-research" / "docs" / "STRATEGY_DESIGN_GUIDE.md"

for _p in (TRADING_BOT / "tools", TRADING_BOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import validate_config as _vc  # noqa: E402  (trading-bot/tools/validate_config.py)
from strategies.strategy_engine import ConfigDrivenStrategyEngine  # noqa: E402
from strategies.regime_engine import ConfigDrivenRegimeEngine  # noqa: E402
from strategies.strategy_base import MarketRegime  # noqa: E402

COMP = "strategies.strategy_components."
_EXAMPLE_RE = re.compile(r"<!-- example: (\w+) -->\s*```json\n(.*?)\n```", re.DOTALL)


# ---------------------------------------------------------------------------
# Synthetic data and the engine loop
# ---------------------------------------------------------------------------

def _synthetic_bars(n: int = 1500, seed: int = 7) -> pd.DataFrame:
    """Up-trend, down-trend, up-trend with noise; hourly timestamps."""
    rng = np.random.default_rng(seed)
    third = n // 3
    drift = np.r_[np.full(third, 0.001), np.full(third, -0.001), np.full(n - 2 * third, 0.001)]
    close = 100.0 * np.exp(np.cumsum(drift + rng.normal(0.0, 0.01, n)))
    high = close * (1.0 + np.abs(rng.normal(0.0, 0.004, n)))
    low = close * (1.0 - np.abs(rng.normal(0.0, 0.004, n)))
    df = pd.DataFrame({
        "timestamp": pd.date_range("2020-01-01", periods=n, freq="h"),
        "open": close, "high": high, "low": low, "close": close,
        "volume": rng.uniform(50.0, 150.0, n),
    })
    df["stddev_24"] = df["close"].rolling(24).std()
    return df


BARS = _synthetic_bars()
WINDOW = 700  # bars handed to the engine per step (the real strategy hands required_bars + 100)


def _forecasts(config: dict, regime: MarketRegime = MarketRegime.UNKNOWN) -> dict:
    """{bar index: forecast} for every bar on which the engine is ready."""
    engine = ConfigDrivenStrategyEngine(copy.deepcopy(config["strategies"]))
    out = {}
    for t in range(len(BARS)):
        window = BARS.iloc[max(0, t + 1 - WINDOW): t + 1].reset_index(drop=True)
        engine.update(window)
        if engine.is_ready(regime):
            out[t] = engine.forecast(regime)[0]
    return out


def _ungated(components: list) -> dict:
    return {
        "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
        "strategies": {"regimes": {"unknown": {"components": components},
                                   "trending": None, "mean_reversion": None, "chop": None}},
    }


def _alone(component: dict, transforms=None) -> dict:
    c = copy.deepcopy(component)
    c["weight"] = 1.0
    if transforms is not None:
        c["transforms"] = transforms
    return _ungated([c])


def _values(f: dict) -> np.ndarray:
    return np.array([f[t] for t in sorted(f)], dtype=float)


def _components(config: dict) -> dict:
    return {c["id"]: c for c in config["strategies"]["regimes"]["unknown"]["components"]}


def _assert_graded(v: np.ndarray, min_distinct: int = 100) -> None:
    assert np.all(np.isfinite(v))
    assert np.all(np.abs(v) <= 20.0 + 1e-9)
    assert len(np.unique(np.round(v, 8))) >= min_distinct, "output takes too few distinct values to be graded"


def _assert_both_signs(v: np.ndarray) -> None:
    assert (v > 0).any() and (v < 0).any()


def _max_share_at_one_value(v: np.ndarray) -> float:
    """Largest fraction of bars sitting on any single (rounded) value: a graded signal has no mass point."""
    _, counts = np.unique(np.round(v, 8), return_counts=True)
    return counts.max() / len(v)


# ---------------------------------------------------------------------------
# Example extraction
# ---------------------------------------------------------------------------

def _examples() -> dict:
    text = GUIDE_PATH.read_text(encoding="utf-8")
    found = {}
    for name, body in _EXAMPLE_RE.findall(text):
        assert name not in found, f"example {name!r} appears twice"
        found[name] = json.loads(body)
    return found


EXAMPLES = _examples()
EXPECTED_EXAMPLES = {
    "two_trend_horizons", "subtract_short_term_run_up", "centre_one_sided_signal",
    "sign_flip_negate", "long_only_from_signed", "normalised_trend",
}
MAX_SHARE_AT_ONE_VALUE = 0.05


def test_every_expected_example_is_in_the_guide_and_nothing_unexpected():
    assert set(EXAMPLES) == EXPECTED_EXAMPLES


# ---------------------------------------------------------------------------
# Properties, one per example
# ---------------------------------------------------------------------------

def _prop_two_trend_horizons(cfg):
    comps = _components(cfg)
    both = _values(_forecasts(cfg))
    fast = _forecasts(_alone(comps["fast"]))
    slow = _forecasts(_alone(comps["slow"]))
    combined = _forecasts(cfg)
    assert combined and set(combined) <= set(fast) & set(slow)
    assert max(abs(v) for v in list(fast.values()) + list(slow.values())) < 20.0  # neither is clipped alone
    for t, v in combined.items():
        assert v == pytest.approx(0.5 * (fast[t] + slow[t]), abs=1e-9)
    _assert_graded(both)
    _assert_both_signs(both)


def _prop_subtract_short_term_run_up(cfg):
    comps = _components(cfg)
    trend = _forecasts(_alone(comps["trend"]))
    run_up = _forecasts(_alone(comps["run_up"]))
    combined = _forecasts(cfg)
    assert combined
    for t, v in combined.items():
        assert v == pytest.approx(float(np.clip(2.0 * trend[t] - run_up[t], -20.0, 20.0)), abs=1e-9)
    vals = _values(combined)
    _assert_graded(vals)
    _assert_both_signs(vals)


def _prop_centre_one_sided_signal(cfg):
    comps = _components(cfg)
    rank = _forecasts(_alone(comps["rank"], transforms=[{"op": "percentile"},
                                                        {"op": "scale", "params": {"factor": 20.0}}]))
    rank_vals = _values(rank)
    assert rank_vals.min() > 0.0 and rank_vals.max() <= 20.0 + 1e-9  # one-sided: (0, 20]
    # graded across the whole range: no bar share piles up on a boundary (or any other single) value
    assert _max_share_at_one_value(rank_vals) <= MAX_SHARE_AT_ONE_VALUE
    combined = _forecasts(cfg)
    assert combined
    for t, v in combined.items():
        assert v == pytest.approx(rank[t] - 10.0, abs=1e-9)
    vals = _values(combined)
    assert vals.min() >= -10.0 - 1e-9 and vals.max() <= 10.0 + 1e-9
    _assert_graded(vals)
    _assert_both_signs(vals)
    assert _max_share_at_one_value(vals) <= MAX_SHARE_AT_ONE_VALUE


def _prop_sign_flip_negate(cfg):
    comps = _components(cfg)
    plain = _forecasts(_alone(comps["range"], transforms=[{"op": "identity"}]))
    flipped = _forecasts(cfg)
    assert flipped
    for t, v in flipped.items():
        assert v == pytest.approx(-plain[t], abs=1e-9)
    # the same thing through a negative scaling_factor
    neg = copy.deepcopy(comps["range"])
    neg["params"]["scaling_factor"] = -neg["params"]["scaling_factor"]
    via_sf = _forecasts(_alone(neg, transforms=[{"op": "identity"}]))
    for t, v in flipped.items():
        assert v == pytest.approx(via_sf[t], abs=1e-9)
    vals = _values(flipped)
    _assert_graded(vals, min_distinct=50)
    _assert_both_signs(vals)


def _prop_long_only_from_signed(cfg):
    comps = _components(cfg)
    signed = _forecasts(_alone(comps["trend"], transforms=[{"op": "identity"}]))
    assert min(signed.values()) < 0 < max(signed.values())  # the raw signal has both sides
    clipped = _forecasts(cfg)
    assert clipped
    for t, v in clipped.items():
        assert v == pytest.approx(max(signed[t], 0.0), abs=1e-9)
    vals = _values(clipped)
    assert vals.min() >= 0.0
    assert (vals == 0.0).any() and len(np.unique(np.round(vals[vals > 0], 8))) >= 100  # graded on the long side


def _prop_normalised_trend(cfg):
    f = _forecasts(cfg)
    vals = _values(f)
    _assert_graded(vals)
    _assert_both_signs(vals)
    tail = vals[500:]
    assert 7.0 <= np.mean(np.abs(tail)) <= 13.0, np.mean(np.abs(tail))
    # the component's scaling_factor cancels under ratio_to_mean
    big = copy.deepcopy(cfg)
    big["strategies"]["regimes"]["unknown"]["components"][0]["params"]["scaling_factor"] = 99.0
    big_vals = _values(_forecasts(big))
    assert np.allclose(vals, big_vals, atol=1e-9)


PROPERTIES = {
    "two_trend_horizons": _prop_two_trend_horizons,
    "subtract_short_term_run_up": _prop_subtract_short_term_run_up,
    "centre_one_sided_signal": _prop_centre_one_sided_signal,
    "sign_flip_negate": _prop_sign_flip_negate,
    "long_only_from_signed": _prop_long_only_from_signed,
    "normalised_trend": _prop_normalised_trend,
}


def test_every_example_has_a_property_test():
    assert set(PROPERTIES) == set(EXAMPLES)


@pytest.mark.parametrize("name", sorted(EXAMPLES))
def test_example_validates(name):
    assert _vc.validate(copy.deepcopy(EXAMPLES[name])) == []


@pytest.mark.parametrize("name", sorted(EXAMPLES))
def test_example_property_holds_on_synthetic_bars(name):
    PROPERTIES[name](copy.deepcopy(EXAMPLES[name]))


# ---------------------------------------------------------------------------
# Other examples and claims in the guide
# ---------------------------------------------------------------------------

def test_production_component_snippet_matches_strategy_config_json_without_its_dead_zone():
    """The guide shows the production component WITHOUT its last transform (the threshold_filter dead zone, no
    longer allowed in `strategies`) and says so."""
    text = GUIDE_PATH.read_text(encoding="utf-8")
    head = text.index("### The production mean_reversion component")
    m = re.search(r"```json\n(.*?)\n```", text[head:], re.DOTALL)
    snippet = json.loads(m.group(1))
    prod = copy.deepcopy(json.loads((TRADING_BOT / "strategy_config.json").read_text(encoding="utf-8"))
                         ["strategies"]["regimes"]["mean_reversion"]["components"][0])
    dropped = prod["transforms"].pop()
    assert dropped["op"] == "threshold_filter"
    assert snippet == prod
    assert not any(step["op"] in ("threshold_filter", "volume_filter") for step in snippet["transforms"])
    assert _vc.validate(_ungated([copy.deepcopy(snippet)])) == []
    assert "threshold_filter" in text[head:head + text[head:].index("```json")]  # the prose names the omitted step


def _score_product_detector() -> dict:
    text = GUIDE_PATH.read_text(encoding="utf-8")
    head = text.index("### Score-product mode")
    m = re.search(r"```json\n(\"regime_detector\": \{.*?)\n```", text[head:], re.DOTALL)
    return json.loads("{" + m.group(1) + "}")["regime_detector"]


def _fill(engine: ConfigDrivenRegimeEngine, values: dict) -> None:
    for cid, v in values.items():
        h = engine._history[cid]
        h.clear()
        h.extend([v] * h.maxlen)


def test_score_product_example_arithmetic_and_validity():
    det = _score_product_detector()
    cfg = {"regime_detector": det,
           "strategies": {"regimes": {"trending": {"components": [
               {"id": "x", "class": COMP + "PriceEvolutionComponent", "params": {}, "weight": 1.0,
                "transforms": [{"op": "identity"}]}]}, "unknown": None, "chop": None, "mean_reversion": None}}}
    assert _vc.validate(cfg) == []
    eng = ConfigDrivenRegimeEngine(copy.deepcopy(det))
    _fill(eng, {"er": 0.5, "vr": 2.0})
    assert eng.classify()[0] == MarketRegime.TRENDING      # 0.5 x (2.0 / 2.0) = 0.5 >= 0.4
    eng = ConfigDrivenRegimeEngine(copy.deepcopy(det))
    _fill(eng, {"er": 0.6, "vr": 0.8})
    assert eng.classify()[0] == MarketRegime.UNKNOWN       # 0.6 x (0.8 / 2.0) = 0.24 < 0.4


def _er_detector(mode: str, rule_op: str = "gte") -> dict:
    er = {"id": "er", "class": COMP + "EfficiencyRatioRegimeComponent", "params": {"period": 24}}
    return {
        "mode": mode, "components": [er],
        "rules": [{"regime": "trending", "any_of": [[{"id": "er", "op": rule_op, "value": 0.1}]]}],
        "regimes": {"trending": {"components": [{"id": "er", "weight": 1.0, "transforms": [{"op": "identity"}]}]}},
        "default_regime": "chop",
    }


def test_unknown_mode_silently_runs_score_mode():
    bogus = ConfigDrivenRegimeEngine(_er_detector("not_a_mode"))
    score = ConfigDrivenRegimeEngine(_er_detector("score"))
    for eng in (bogus, score):
        _fill(eng, {"er": 0.5})
    assert bogus.classify()[0] == score.classify()[0] == MarketRegime.TRENDING


def test_unknown_rule_op_silently_evaluates_false():
    good = ConfigDrivenRegimeEngine(_er_detector("threshold_rules", "gte"))
    bad = ConfigDrivenRegimeEngine(_er_detector("threshold_rules", ">="))
    for eng in (good, bad):
        _fill(eng, {"er": 0.5})
    assert good.classify()[0] == MarketRegime.TRENDING
    assert bad.classify()[0] == MarketRegime.CHOP           # falls through to default_regime


def test_detector_component_weight_lookback_history_transforms_are_ignored():
    plain = _er_detector("threshold_rules")
    decorated = copy.deepcopy(plain)
    decorated["components"][0].update({"weight": 99.0, "lookback": 3,
                                       "history_transforms": [{"op": "scale", "params": {"factor": 1000.0}}]})
    a, b = ConfigDrivenRegimeEngine(plain), ConfigDrivenRegimeEngine(decorated)
    assert a._history["er"].maxlen == b._history["er"].maxlen
    for t in range(60):
        window = BARS.iloc[: t + 30].reset_index(drop=True)
        a.update(window)
        b.update(window)
    assert list(a._history["er"]) == list(b._history["er"])


def test_ungated_default_regime_may_be_any_of_the_four_names_when_components_hold_that_regime():
    comp = {"id": "t", "class": COMP + "PriceEvolutionComponent", "params": {}, "weight": 1.0,
            "transforms": [{"op": "identity"}]}
    for name in ("trending", "mean_reversion", "chop", "unknown"):
        cfg = _ungated([copy.deepcopy(comp)])
        cfg["strategies"]["regimes"] = {r: None for r in ("trending", "mean_reversion", "chop", "unknown")}
        cfg["strategies"]["regimes"][name] = {"components": [copy.deepcopy(comp)]}
        cfg["regime_detector"]["default_regime"] = name
        assert _vc.validate(cfg) == [], name


def test_ungated_default_regime_pointing_at_a_null_regime_is_v10():
    cfg = _ungated([{"id": "t", "class": COMP + "PriceEvolutionComponent", "params": {}, "weight": 1.0,
                     "transforms": [{"op": "identity"}]}])
    cfg["regime_detector"]["default_regime"] = "trending"
    assert any("V10" in v for v in _vc.validate(cfg))


def test_empty_components_regime_is_v8_and_negative_weights_are_allowed():
    cfg = _ungated([])
    assert any("V8" in v for v in _vc.validate(cfg))
    neg = _ungated([
        {"id": "a", "class": COMP + "PriceEvolutionComponent", "params": {}, "weight": 2.0, "transforms": [{"op": "identity"}]},
        {"id": "b", "class": COMP + "PriceEvolutionComponent", "params": {}, "weight": -1.0, "transforms": [{"op": "identity"}]},
    ])
    assert _vc.validate(neg) == []
    neg["strategies"]["regimes"]["unknown"]["components"][0]["weight"] = 0.5      # total -0.5
    assert any("V8" in v for v in _vc.validate(neg))


def test_default_lookback_is_engine_wide_and_warmup_is_capped_by_the_smallest_history():
    """The guide's `lookback` row and readiness bullet: an omitted lookback is the maximum over ALL components of all
    regimes (50 with none), and the warmup is capped by the smallest history size of any component."""
    def ema(cid, fast, slow, **extra):
        c = {"id": cid, "class": COMP + "EMASpreadComponent",
             "params": {"fast_period": fast, "slow_period": slow}, "weight": 1.0,
             "transforms": [{"op": "identity"}]}
        c.update(extra)
        return c

    def cfg(trending, chop):
        return {"regimes": {"trending": {"components": trending}, "chop": {"components": chop},
                            "mean_reversion": None, "unknown": None}}

    eng = ConfigDrivenStrategyEngine(cfg([ema("a", 12, 26)], [ema("b", 50, 200)]))
    assert eng.lookback == 200                                  # the other regime's component sets it
    assert eng._history["trending"]["a"].maxlen == 200          # not its own warmup (26)
    eng.set_warmup(150)
    assert eng._warmup == 150                                   # min(required_bars, smallest history)
    short = ConfigDrivenStrategyEngine(cfg([ema("a", 12, 26, lookback=40)], [ema("b", 50, 200)]))
    assert short._history["trending"]["a"].maxlen == 40 and short._history["chop"]["b"].maxlen == 200
    short.set_warmup(150)
    assert short._warmup == 40                                  # one short history lowers the whole config's warmup
    assert ConfigDrivenStrategyEngine({"regimes": {}}).lookback == 50


def test_lookback_below_op_minimum_is_v6():
    cfg = _ungated([{"id": "a", "class": COMP + "PriceEvolutionComponent", "params": {}, "weight": 1.0,
                     "lookback": 10, "transforms": [{"op": "percentile"}]}])
    assert any("V6" in v for v in _vc.validate(cfg))


# ---------------------------------------------------------------------------
# Claims that need the real AdvancedStrategy (readiness, ignored warmup, missing transforms)
# ---------------------------------------------------------------------------

def _strategy(tmp_path, config: dict):
    from strategies.main_strategy import AdvancedStrategy
    path = tmp_path / "strategy_config.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    return AdvancedStrategy(config_path=str(path))


def _first_ready_bar(strategy, n: int = 400):
    bars = BARS.iloc[:n].drop(columns=["stddev_24"])  # the strategy computes its own
    for t in range(n):
        strategy.update(bars.iloc[t:t + 1])
        if strategy.is_ready():
            return t + 1
    return None


def _rsi(transforms, **extra):
    c = {"id": "r", "class": COMP + "RSIPullbackComponent", "params": {}, "weight": 1.0, "transforms": transforms}
    c.update(extra)
    return c


def test_first_forecast_bars_quoted_in_the_guide(tmp_path):
    assert _first_ready_bar(_strategy(tmp_path, _ungated([_rsi([{"op": "identity"}])]))) == 29
    assert _first_ready_bar(_strategy(tmp_path, _ungated([_rsi([{"op": "ratio_to_mean"}])]))) == 38
    sma = {"id": "s", "class": COMP + "SmaTrendLongOnlyComponent", "params": {}, "weight": 1.0,
           "transforms": [{"op": "identity"}]}
    assert _first_ready_bar(_strategy(tmp_path, _ungated([sma])), n=300) == 201


def test_strategies_warmup_has_no_effect(tmp_path):
    base = _ungated([_rsi([{"op": "identity"}])])
    with_warmup = copy.deepcopy(base)
    with_warmup["strategies"]["warmup"] = 3
    other = copy.deepcopy(base)
    other["strategies"]["warmup"] = 300
    a = _first_ready_bar(_strategy(tmp_path, base))
    assert a == _first_ready_bar(_strategy(tmp_path, with_warmup)) == _first_ready_bar(_strategy(tmp_path, other))


def test_ungated_pattern_is_ready_on_the_same_bar_whatever_default_regime_names(tmp_path):
    bars = set()
    for name in ("trending", "mean_reversion", "chop", "unknown"):
        cfg = _ungated([_rsi([{"op": "identity"}])])
        cfg["strategies"]["regimes"] = {r: None for r in ("trending", "mean_reversion", "chop", "unknown")}
        cfg["strategies"]["regimes"][name] = {"components": [_rsi([{"op": "identity"}])]}
        cfg["regime_detector"]["default_regime"] = name
        bars.add(_first_ready_bar(_strategy(tmp_path, cfg)))
    assert len(bars) == 1 and None not in bars


def test_missing_transforms_key_raises_on_every_bar_and_passes_the_validator(tmp_path):
    comp = _rsi([{"op": "identity"}])
    del comp["transforms"]
    cfg = _ungated([comp])
    assert _vc.validate(copy.deepcopy(cfg)) == []
    strategy = _strategy(tmp_path, cfg)
    assert _first_ready_bar(strategy) is not None
    # the real cause: the forecast reads `transforms` from the component spec. (Asserted on the forecast call, not
    # on generate_signals(), whose except-handler currently fails for an unrelated reason: CUL-353.)
    with pytest.raises(KeyError, match="transforms"):
        strategy.generate_forecast()


def test_centring_a_boundary_heavy_input_is_not_graded():
    """The guide's warning: RSIPullbackComponent(long_only) is exactly 0 on every bar with RSI >= 50, so centred
    by a -10 offset it sits at a constant -10 on all of those bars."""
    cfg = _ungated([
        {"id": "rsi", "class": COMP + "RSIPullbackComponent",
         "params": {"period": 14, "scaling_factor": 0.4, "long_only": True},
         "weight": 1.0, "transforms": [{"op": "identity"}, {"op": "scale", "params": {"factor": 2.0}}]},
        {"id": "offset", "class": COMP + "BuyAndHoldStrategy", "params": {},
         "weight": 1.0, "transforms": [{"op": "scale", "params": {"factor": -2.0}}]},
    ])
    vals = _values(_forecasts(cfg))
    assert np.isclose(vals.min(), -10.0)
    assert (np.isclose(vals, -10.0)).mean() > 0.30
    assert _max_share_at_one_value(vals) > 0.30
