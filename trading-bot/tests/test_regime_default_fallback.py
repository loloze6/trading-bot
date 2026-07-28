"""
The `default_regime` fall-through in ConfigDrivenRegimeEngine must fail SAFE.

`_classify_threshold_rules()` ends with a lookup of the configured default:

    return _REGIME_MAP.get(self._default_regime, <fallback>)

That `<fallback>` fires only when `default_regime` is a value absent from
_REGIME_MAP — i.e. an explicit `null`, or a name that validate_config's V7 would
reject. It was `MarketRegime.MEAN_REVERSION`, which is the single worst choice
available: mean_reversion is the only regime carrying components in the shipped
config, so it is the only regime that produces a non-zero forecast and trades.

That was a silent bypass of exactly what validator rule V9 exists to prevent. V9
forbids `default_regime` aliasing a real trading regime while `rules` is
non-empty, but it tests only the three literal names — so an explicit `null`
validated with zero errors and then landed on MEAN_REVERSION anyway: every bar
that matched no rule was traded, while every check reported green.

Note the asymmetry: a MISSING key was always safe, because regime_engine.py:70
reads it as `config.get("default_regime", "unknown")` and the *string* maps
correctly. Only an EXPLICIT null was unsafe.

The fix is now two layers, and each is tested where it lives:

  * ENGINE (this file) — the fall-through returns UNKNOWN, matching the veto and
    rule-match paths that already did. This closes the whole class, including a
    typo'd name, and it is the ONLY protection for callers that construct
    ConfigDrivenRegimeEngine directly without validating — which
    strategy-research/tools/validate_regime_detector.py:116 does.
  * VALIDATOR (tests/test_validate_config.py) — V7 rejects an explicit null
    outright, so no such config can construct an AdvancedStrategy at all.

Engine alone was not enough: it made a null config harmless but invisible, still
forecasting 0.0 on every bar with nothing reporting why. Validator alone was not
enough either, because of the unvalidated construction path above. Reverting
either layer breaks tests the other does not cover.
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
    """A mapped name must still resolve to itself, so this change cannot alter any
    existing config. Pins the private helper only — public-path coverage is
    test_null_default_regime_resolves_to_unknown_through_classify below, and
    forecast-level coverage of the ungated pattern is in
    test_ungated_config_pattern.py."""
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


# ----------------------------------------------------------------------------
# Public-path coverage.
#
# Every test above calls the private _classify_threshold_rules() with hand-stuffed
# _history, bypassing update() / is_ready() / classify(). An adversarial review
# proved that gap real by reintroducing this defect one level up inside classify(),
# where NONE of those tests failed. The tests below close it by driving classify()
# — the actual public entry point, and the method that was sabotaged.
#
# The fully-ungated pattern (rules=[] and components=[]) is used deliberately: it
# makes the fall-through fire on the first bar with no warmup, and it is the shape
# where a bad default is most damaging because EVERY bar resolves through it.
# ----------------------------------------------------------------------------

def _ungated_engine(default_regime) -> ConfigDrivenRegimeEngine:
    return ConfigDrivenRegimeEngine({
        "mode": "threshold_rules",
        "components": [],
        "rules": [],
        "default_regime": default_regime,
    })


def test_null_default_regime_resolves_to_unknown_through_classify():
    """THE public-path regression, driven through classify() rather than the private
    helper. Catches a defect reintroduced anywhere in the classification path, which
    the private-helper tests above provably do not."""
    regime, _ = _ungated_engine(None).classify()
    assert regime is MarketRegime.UNKNOWN


def test_the_classify_fixture_is_not_vacuously_unknown():
    """Control for the test above, and it is load-bearing.

    classify() short-circuits to UNKNOWN when not ready, so an UNKNOWN result could
    mean 'correctly defaulted' or 'never ran'. Pointing the default at a real regime
    must yield THAT regime — which is only possible if the engine was ready and the
    fall-through actually executed.
    """
    regime, _ = _ungated_engine("mean_reversion").classify()
    assert regime is MarketRegime.MEAN_REVERSION, (
        "the ungated engine did not reach its default fall-through — the null test "
        "above proves nothing"
    )


def test_advanced_strategy_rejects_a_null_default_regime():
    """The validator layer: since the V7 hardening, a null default_regime cannot get
    as far as the engine through the normal path — AdvancedStrategy refuses to build.

    This is what turns the engine's silent-but-safe behaviour into a loud error for
    every caller that validates. Before both fixes this config constructed happily
    and traded every bar.
    """
    import json
    import os
    import tempfile

    from strategies.main_strategy import AdvancedStrategy

    config = {
        "regime_detector": {
            "mode": "threshold_rules", "components": [], "rules": [], "default_regime": None,
        },
        "strategies": {"warmup": 25, "regimes": {name: None for name in _VALID_REGIMES}},
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config, f)
        tmp_path = f.name
    try:
        with pytest.raises(ValueError, match="invalid strategy_config"):
            AdvancedStrategy(config_path=tmp_path)
    finally:
        os.unlink(tmp_path)
