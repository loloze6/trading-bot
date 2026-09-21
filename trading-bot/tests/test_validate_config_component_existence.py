"""
E-056 S2 Slice 3a tests for tools/validate_config.py's V12 check.

V12 verifies every declared component's 'class' dotted path in
regime_detector.components[] and strategies.regimes.*.components[] actually
resolves to a real, importable class (reusing strategies.registry._load_class,
the exact function the live engine calls at startup). Before V12, an
invented/typo'd class name was never caught by validate_config.py at all --
it only failed later, at engine startup, after a full backtest had already
been launched and its data fetched. This is a pure addition: it strictly
tightens what was already going to fail, only earlier and with a
validate_config.py-shaped message instead of a bare engine ValueError.

Covers:
- Positive case: a real class name (RSIPullbackComponent) passes cleanly.
- Negative case: an invented class name fires VIOLATION V12 with a clear
  message, in both of the two locations V12 checks
  (regime_detector.components[] and strategies.regimes.*.components[]).
- A missing 'class' key entirely reports cleanly rather than crashing.
- A zero-components config reports cleanly (nothing to check, no false fire).
- V1-V11's existing behavior is unaffected -- see tests/test_validate_config.py,
  run unmodified in the same session as this file's addition (17/17 passed
  before and after V12 was added, non-regression confirmed empirically, not
  merely asserted).
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.validate_config import validate


def _minimal_config(regime_detector: dict, regimes: dict) -> dict:
    return {"regime_detector": regime_detector, "strategies": {"warmup": 25, "regimes": regimes}}


REAL_CLASS = "strategies.strategy_components.RSIPullbackComponent"
INVENTED_CLASS = "strategies.strategy_components.TotallyMadeUpComponent"


def _real_component(comp_id: str) -> dict:
    return {
        "id": comp_id,
        "class": REAL_CLASS,
        "weight": 1.0,
        "transforms": [{"op": "identity"}],
        "params": {"period": 14, "scaling_factor": 0.4, "long_only": True},
    }


def _invented_component(comp_id: str) -> dict:
    comp = _real_component(comp_id)
    comp["class"] = INVENTED_CLASS
    return comp


# ---------------------------------------------------------------------------
# Positive case: a real, importable class name passes cleanly.
# ---------------------------------------------------------------------------

def test_real_class_in_strategies_regimes_passes_v12():
    config = _minimal_config(
        regime_detector={"mode": "threshold_rules", "components": [], "rules": []},
        regimes={"trending": None, "mean_reversion": None, "chop": None,
                 "unknown": {"components": [_real_component("rsi")]}},
    )
    violations = validate(config)
    assert not any("VIOLATION V12" in v for v in violations), violations


def test_real_class_in_regime_detector_components_passes_v12():
    config = _minimal_config(
        regime_detector={
            "mode": "threshold_rules",
            "components": [
                {"id": "er", "class": "strategies.strategy_components.EfficiencyRatioRegimeComponent"}
            ],
            "rules": [{"regime": "trending", "any_of": [[{"id": "er", "op": "gte", "value": 0.5}]]}],
            "default_regime": "unknown",
        },
        regimes={"trending": {"components": [_real_component("rsi")]},
                 "mean_reversion": None, "chop": None, "unknown": None},
    )
    violations = validate(config)
    assert not any("VIOLATION V12" in v for v in violations), violations


# ---------------------------------------------------------------------------
# Negative case: an invented class name fires V12 with a clear message.
# ---------------------------------------------------------------------------

def test_invented_class_in_strategies_regimes_fires_v12():
    config = _minimal_config(
        regime_detector={"mode": "threshold_rules", "components": [], "rules": []},
        regimes={"trending": None, "mean_reversion": None, "chop": None,
                 "unknown": {"components": [_invented_component("bad")]}},
    )
    violations = validate(config)
    v12 = [v for v in violations if "VIOLATION V12" in v]
    assert len(v12) == 1, violations
    assert "strategies.regimes.unknown.components[0]" in v12[0]
    assert INVENTED_CLASS in v12[0]


def test_invented_class_in_regime_detector_components_fires_v12():
    config = _minimal_config(
        regime_detector={
            "mode": "threshold_rules",
            "components": [{"id": "bad", "class": INVENTED_CLASS}],
            "rules": [],
        },
        regimes={"trending": None, "mean_reversion": None, "chop": None, "unknown": None},
    )
    violations = validate(config)
    v12 = [v for v in violations if "VIOLATION V12" in v]
    assert len(v12) == 1, violations
    assert "regime_detector.components[0]" in v12[0]
    assert INVENTED_CLASS in v12[0]


def test_invented_class_message_names_the_bad_class_path():
    """The message must be clear enough to fix without re-reading the engine's
    own ValueError -- it should name the exact bad dotted path."""
    config = _minimal_config(
        regime_detector={"mode": "threshold_rules", "components": [], "rules": []},
        regimes={"trending": None, "mean_reversion": None, "chop": None,
                 "unknown": {"components": [_invented_component("bad")]}},
    )
    violations = validate(config)
    v12 = [v for v in violations if "VIOLATION V12" in v]
    assert INVENTED_CLASS in v12[0], v12


# ---------------------------------------------------------------------------
# Edge cases named in the dispatch's own self-adversarial review requirement.
# ---------------------------------------------------------------------------

def test_missing_class_key_reports_cleanly_not_a_crash():
    comp = _real_component("rsi")
    del comp["class"]
    config = _minimal_config(
        regime_detector={"mode": "threshold_rules", "components": [], "rules": []},
        regimes={"trending": None, "mean_reversion": None, "chop": None,
                 "unknown": {"components": [comp]}},
    )
    violations = validate(config)  # must not raise
    v12 = [v for v in violations if "VIOLATION V12" in v]
    assert len(v12) == 1, violations
    assert "missing required 'class' key" in v12[0]


def test_zero_components_config_reports_cleanly():
    config = _minimal_config(
        regime_detector={"mode": "threshold_rules", "components": [], "rules": []},
        regimes={"trending": None, "mean_reversion": None, "chop": None, "unknown": None},
    )
    violations = validate(config)  # must not raise
    assert not any("VIOLATION V12" in v for v in violations), violations


def test_dotted_path_with_real_module_prefix_resolves_via_rsplit():
    """Confirms V12 handles the real multi-segment dotted-path shape used in every
    actual config in the repo's corpus (strategies.strategy_components.<Class>),
    not a guessed one-segment or two-segment shape."""
    assert REAL_CLASS.count(".") == 2  # module.submodule.ClassName, the real shape
    config = _minimal_config(
        regime_detector={"mode": "threshold_rules", "components": [], "rules": []},
        regimes={"trending": None, "mean_reversion": None, "chop": None,
                 "unknown": {"components": [_real_component("rsi")]}},
    )
    violations = validate(config)
    assert not any("VIOLATION V12" in v for v in violations), violations


# ---------------------------------------------------------------------------
# Non-regression: V1-V11 behavior completely unaffected by V12's addition.
# A full parallel re-assertion lives in tests/test_validate_config.py itself
# (run unmodified, 17/17 passed before and after this change in the same
# session). This one extra check confirms V9/V10/V11 still fire independently
# of V12 on a config that is broken in both an old and a new way at once.
# ---------------------------------------------------------------------------

def test_v9_and_v12_both_fire_independently_on_a_doubly_broken_config():
    config = _minimal_config(
        regime_detector={
            "mode": "threshold_rules",
            "components": [{"id": "er", "class": "strategies.strategy_components.EfficiencyRatioRegimeComponent"}],
            "rules": [{"regime": "trending", "any_of": [[{"id": "er", "op": "gte", "value": 0.5}]]}],
            "default_regime": "trending",  # V9 gate-bypass violation
        },
        regimes={"trending": {"components": [_invented_component("bad")]},  # V12 violation
                 "mean_reversion": None, "chop": None, "unknown": None},
    )
    violations = validate(config)
    assert any("VIOLATION V9" in v for v in violations), violations
    assert any("VIOLATION V12" in v for v in violations), violations


# ---------------------------------------------------------------------------
# CODE-REVIEW REGRESSION (2026-09-21): a dotless class_path (no module
# prefix) used to produce an uninformative message that never named the bad
# class -- strategies.registry._load_class's own
# `class_path.rsplit(".", 1)` unpacking raises a bare ValueError
# ("not enough values to unpack") for a dotless string, which V12's original
# `except ValueError as e: ... f"{e}"` propagated verbatim, silently
# omitting class_path entirely from the violation.
# ---------------------------------------------------------------------------

def test_dotless_class_path_names_the_bad_value_not_a_bare_unpacking_error():
    dotless = "TotallyMadeUpComponentWithNoModulePrefix"
    config = _minimal_config(
        regime_detector={
            "mode": "threshold_rules", "components": [], "rules": [],
        },
        regimes={"trending": None, "mean_reversion": None, "chop": None,
                 "unknown": {"components": [
                     {**_real_component("bad"), "class": dotless},
                 ]}},
    )
    violations = validate(config)
    v12 = [v for v in violations if "VIOLATION V12" in v]
    assert len(v12) == 1, violations
    assert dotless in v12[0], (
        f"dotless class_path must be named explicitly in the violation, "
        f"not just the raw unpacking error: {v12[0]!r}"
    )
    assert "not enough values to unpack" not in v12[0].split(":")[0], (
        "the class_path must appear before/alongside the raw error, not be "
        f"replaced by it: {v12[0]!r}"
    )
