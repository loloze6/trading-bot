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
    """A mapped name must still resolve to itself, so this change cannot alter any
    existing config. Note this pins the private helper only — the end-to-end
    coverage for the ungated pattern lives in test_ungated_config_pattern.py and in
    test_null_default_regime_is_flat_end_to_end below."""
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
# End-to-end coverage.
#
# Every test above calls _classify_threshold_rules() directly and hand-stuffs
# _history, which bypasses update() / is_ready() / classify() — the only path
# main_strategy.py actually uses. An adversarial review proved that gap real by
# reintroducing this exact defect one level up, inside classify(), where NONE of
# the tests above failed. The test below closes it by driving the public path.
#
# It uses the fully-ungated pattern (rules=[] and components=[]), where the
# default fall-through fires on every single bar rather than only on unmatched
# ones — see test_ungated_config_pattern.py. The signal is parked in
# mean_reversion, so a regression that routes the default there produces real
# forecasts, while the fixed behaviour routes to the null `unknown` entry and
# stays flat.
# ----------------------------------------------------------------------------

_EMA_COMPONENT = {
    "id": "ema_spread",
    "class": "strategies.strategy_components.EMASpreadComponent",
    "weight": 1.0,
    "transforms": [{"op": "identity"}],
    "params": {"fast_period": 9, "slow_period": 21, "scaling_factor": 5.0},
}


def _ungated_config_with_signal_in_mean_reversion(default_regime) -> dict:
    regimes = {name: None for name in _VALID_REGIMES}
    regimes["mean_reversion"] = {"components": [_EMA_COMPONENT]}
    return {
        "regime_detector": {
            "mode": "threshold_rules",
            "components": [],
            "rules": [],
            "default_regime": default_regime,
        },
        "strategies": {"warmup": 25, "regimes": regimes},
    }


def _forecasts(config: dict) -> list:
    """Feed deterministic synthetic bars one at a time through the real public
    path and collect every forecast produced once ready."""
    import json
    import os
    import tempfile

    import numpy as np
    import pandas as pd

    from strategies.main_strategy import AdvancedStrategy

    rng = np.random.default_rng(42)
    close = 100.0 + rng.normal(loc=0.05, scale=1.0, size=70).cumsum()
    bars = pd.DataFrame({
        "timestamp": pd.date_range("2024-01-01", periods=70, freq="h", tz="UTC"),
        "open": close, "high": close + 0.5, "low": close - 0.5,
        "close": close, "volume": 1.0,
    })

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config, f)
        tmp_path = f.name
    try:
        strat = AdvancedStrategy(config_path=tmp_path)
        out = []
        for i in range(1, len(bars) + 1):
            strat.update(bars.iloc[:i])
            if strat.is_ready():
                forecast, *_ = strat.generate_forecast()
                out.append(forecast)
        return out
    finally:
        os.unlink(tmp_path)


def test_null_default_regime_is_flat_end_to_end():
    """THE end-to-end regression, driven through AdvancedStrategy rather than the
    private helper.

    Pre-fix this produced real non-zero forecasts off an unclassified default —
    trading every bar while validate_config reported zero violations. Post-fix
    every bar must be flat.
    """
    forecasts = _forecasts(_ungated_config_with_signal_in_mean_reversion(None))
    assert forecasts, "strategy never became ready — fixture is vacuous, not passing"
    nonzero = [f for f in forecasts if f != 0.0]
    assert not nonzero, (
        f"{len(nonzero)} of {len(forecasts)} bars traded off a null default_regime; "
        "an unclassified default must never reach a regime that carries components."
    )


def test_the_end_to_end_fixture_is_not_vacuously_flat():
    """Control for the test above: the same config with the default pointed AT the
    signal must produce real forecasts. Without this, an all-zero result could mean
    'correctly flat' or 'fixture is broken' — and they must not be confusable."""
    forecasts = _forecasts(_ungated_config_with_signal_in_mean_reversion("mean_reversion"))
    assert any(f != 0.0 for f in forecasts), (
        "the signal produced no forecast even when the default pointed straight at "
        "it — the fixture proves nothing about the null case"
    )
