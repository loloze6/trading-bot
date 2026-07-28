"""
The `default_regime` fall-through in ConfigDrivenRegimeEngine must fail SAFE.

`_classify_threshold_rules()` ends with a lookup of the configured default:

    return _REGIME_MAP.get(self._default_regime, <fallback>)

That `<fallback>` fires only when `default_regime` is a value absent from
_REGIME_MAP — i.e. an explicit `null`, or a name that validate_config's V7 would
reject. It was `MarketRegime.MEAN_REVERSION`, which is the single worst choice
available: mean_reversion is the only regime carrying components in the shipped
config, so it is the only regime that produces a non-zero forecast and trades.

The result was a silent bypass of exactly what validator rule V9 exists to
prevent. V9 forbids `default_regime` aliasing a real trading regime while
`rules` is non-empty, but it only tests the three literal names
("trending" / "mean_reversion" / "chop"). An explicit `null` passes the
validator with zero errors and then lands on MEAN_REVERSION anyway — so every
bar that matches no rule gets traded, while every check reports green.

Note the asymmetry this closes: a MISSING `default_regime` key was always safe,
because regime_engine.py reads it as `config.get("default_regime", "unknown")`
and the *string* "unknown" maps correctly. Only an EXPLICIT null was unsafe.

Fixing the fallback rather than extending V9 is deliberate: it closes the whole
class (any unmapped value, including a typo'd name that reaches the engine
without validation) instead of the one known instance, and it makes the two
sibling fallbacks in the same file consistent — the veto path and the
rule-match path already fall back to MarketRegime.UNKNOWN.

Whether V9 should ALSO reject null is tracked separately as an optional
follow-up; with the engine failing safe it is a second control on an already
neutralised fault.
"""
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent          # trading-bot/ (inner)
sys.path.insert(0, str(PROJECT_ROOT))

from strategies.regime_engine import ConfigDrivenRegimeEngine
from strategies.strategy_base import MarketRegime

_VALID_REGIMES = ["trending", "mean_reversion", "chop", "unknown"]

# er=0.22 / vr=1.5 / vol=0.5 satisfies none of the three rule blocks below, so
# classification is forced all the way through to the default fall-through.
_NO_RULE_MATCH = {"er": 0.22, "vr": 1.5, "vol": 0.5}


def _gated_detector(default_regime) -> dict:
    """A real gate: non-empty rules, so unmatched bars reach the default."""
    return {
        "mode": "threshold_rules",
        "components": [
            {"id": "er", "class": "strategies.strategy_components.EfficiencyRatioRegimeComponent",
             "params": {"period": 24, "smooth_period": 5}},
            {"id": "vr", "class": "strategies.strategy_components.VarianceRatioComponent",
             "params": {"k": 5, "window": 100}},
            {"id": "vol", "class": "strategies.strategy_components.VolatilityPercentileRegimeComponent",
             "params": {"vol_period": 20, "lookback_period": 100, "smooth_period": 5}},
        ],
        "vetoes": [],
        "rules": [
            {"regime": "trending", "any_of": [
                [{"id": "er", "op": "gte", "value": 0.25}, {"id": "vr", "op": "gte", "value": 1.10}]]},
            {"regime": "mean_reversion", "any_of": [
                [{"id": "er", "op": "lte", "value": 0.20}, {"id": "vr", "op": "lte", "value": 0.90}]]},
            {"regime": "chop", "any_of": [
                [{"id": "er", "op": "lte", "value": 0.15}, {"id": "vol", "op": "lte", "value": 0.35}]]},
        ],
        "default_regime": default_regime,
    }


def _classify_unmatched_bar(default_regime) -> MarketRegime:
    """Drive one bar that matches no rule and return the regime it resolves to."""
    engine = ConfigDrivenRegimeEngine(_gated_detector(default_regime))
    engine._history = {cid: [_NO_RULE_MATCH[cid]] for cid in engine._components}
    return engine._classify_threshold_rules()


def test_explicit_null_default_regime_does_not_resolve_to_a_trading_regime():
    """THE regression. An explicit null must not silently become mean_reversion.

    Before the fix this returned MarketRegime.MEAN_REVERSION — the one regime
    that carries components and trades — while validate_config reported zero
    violations.
    """
    assert _classify_unmatched_bar(None) is MarketRegime.UNKNOWN


def test_unmapped_default_regime_does_not_resolve_to_a_trading_regime():
    """The same fallback guards typo'd names that reach the engine unvalidated.

    V9 could never catch this case; fixing the fallback does.
    """
    assert _classify_unmatched_bar("mean-reversion") is MarketRegime.UNKNOWN


@pytest.mark.parametrize("name", _VALID_REGIMES)
def test_valid_default_regime_names_are_unaffected(name):
    """Guards the ungated pattern (see test_ungated_config_pattern.py), where the
    default fall-through is the hot path on every bar: a mapped name must still
    resolve to itself, so this change cannot alter any existing config."""
    expected = {
        "trending": MarketRegime.TRENDING,
        "mean_reversion": MarketRegime.MEAN_REVERSION,
        "chop": MarketRegime.CHOP,
        "unknown": MarketRegime.UNKNOWN,
    }[name]
    assert _classify_unmatched_bar(name) is expected


def test_missing_default_regime_key_remains_safe():
    """The pre-existing safe path, pinned so it cannot regress: an absent key is
    read as the string "unknown" by regime_engine, not as None."""
    detector = _gated_detector(None)
    del detector["default_regime"]
    engine = ConfigDrivenRegimeEngine(detector)
    engine._history = {cid: [_NO_RULE_MATCH[cid]] for cid in engine._components}
    assert engine._classify_threshold_rules() is MarketRegime.UNKNOWN
