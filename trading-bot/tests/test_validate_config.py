"""
F1 (P1a shakedown, 2026-07-04) regression tests for tools/validate_config.py.

Covers:
- The actual run_043 (attempt 1) failure fixture: an invented regime name ("active")
  outside the four-value enum, produced by backtest_specification when it tried to
  build an "always active" config via a dummy always-true rule. VIOLATION V7 already
  caught this correctly — this is a non-regression check, not a new fix.
- V9 fix: the previous version only ever forbade default_regime="trending", and did so
  UNCONDITIONALLY (even with regime_detector.rules=[], where there is no gate to
  bypass — the rule's own stated rationale). This left mean_reversion/chop unchecked
  in the genuine bypass case (rules non-empty), and incorrectly rejected the fully-
  ungated canonical pattern for "trending" specifically. Both gaps are closed by
  conditioning the check on `rules` being non-empty and covering all three names.
- V10 (new): a fully-ungated regime_detector (components=[] and rules=[]) must not
  point default_regime at a null strategies.regimes entry — that combination silently
  forecasts 0.0 on every bar forever.
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
REPO_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.validate_config import validate

_RUN_043_ATTEMPT_1_CONFIG = (
    REPO_ROOT
    / "strategy-research"
    / "runs"
    / "run_043"
    / "attempt_1_blocked"
    / "candidate_strategy_config.json"
)


def _minimal_config(regime_detector: dict, regimes: dict) -> dict:
    return {
        "regime_detector": regime_detector,
        "strategies": {"warmup": 25, "regimes": regimes},
    }


EMA = {
    "id": "ema_spread",
    "class": "strategies.strategy_components.EMASpreadComponent",
    "weight": 1.0,
    "transforms": [{"op": "identity"}],
    "params": {"fast_period": 9, "slow_period": 21, "scaling_factor": 5.0},
}


# ---------------------------------------------------------------------------
# Non-regression: the actual run_043 attempt-1 failure fixture
# ---------------------------------------------------------------------------


def test_run_043_attempt_1_invented_regime_name_is_still_rejected():
    """Non-regression: V7 must still catch the invented 'active' regime name that
    caused run_043's first blocker (2026-07-04). This test does not depend on F1's
    fixes — it documents that the pre-existing V7 check already worked correctly and
    must keep working after the V9/V10 changes above."""
    if not _RUN_043_ATTEMPT_1_CONFIG.exists():
        import pytest

        pytest.skip("run_043 attempt_1_blocked fixture not present on disk")

    with open(_RUN_043_ATTEMPT_1_CONFIG) as f:
        config = json.load(f)

    violations = validate(config)
    assert any("VIOLATION V7" in v and "active" in v for v in violations), (
        f"Expected VIOLATION V7 citing the invented regime name 'active'; got: {violations}"
    )


# ---------------------------------------------------------------------------
# V9 fix: gate-bypass check now conditioned on rules being non-empty, and covers
# mean_reversion/chop as well as trending.
# ---------------------------------------------------------------------------


def _gated_config(default_regime: str) -> dict:
    """A REAL gate exists here (rules is non-empty) — aliasing default_regime to one
    of the gated regime names is a genuine bypass and must be forbidden."""
    return _minimal_config(
        regime_detector={
            "mode": "threshold_rules",
            "components": [
                {
                    "id": "er",
                    "class": "strategies.strategy_components.EfficiencyRatioRegimeComponent",
                }
            ],
            "rules": [
                {
                    "regime": "trending",
                    "any_of": [[{"id": "er", "op": "gte", "value": 0.5}]],
                }
            ],
            "default_regime": default_regime,
        },
        regimes={
            "trending": {"components": [EMA]},
            "mean_reversion": {"components": [EMA]},
            "chop": {"components": [EMA]},
            "unknown": None,
        },
    )


def test_v9_still_forbids_trending_default_when_gated():
    violations = validate(_gated_config("trending"))
    assert any("VIOLATION V9" in v for v in violations)


def test_v9_now_forbids_mean_reversion_default_when_gated():
    """This is the actual gap: the OLD V9 only checked '== \"trending\"' and would have
    silently let this through despite it being exactly the gate-bypass V9 exists to
    prevent (bars that fail the 'trending' rule get classified as mean_reversion and
    traded unconditionally)."""
    violations = validate(_gated_config("mean_reversion"))
    assert any("VIOLATION V9" in v for v in violations), (
        "V9 did not fire for default_regime='mean_reversion' with non-empty rules — "
        "the gate-bypass gap this fix was meant to close is still open."
    )


def test_v9_now_forbids_chop_default_when_gated():
    violations = validate(_gated_config("chop"))
    assert any("VIOLATION V9" in v for v in violations)


def test_v9_permits_unknown_default_when_gated():
    violations = validate(_gated_config("unknown"))
    assert not any("VIOLATION V9" in v for v in violations)


def _ungated_pattern_a_config(default_regime: str) -> dict:
    regimes = {"trending": None, "mean_reversion": None, "chop": None, "unknown": None}
    regimes[default_regime] = {"components": [EMA]}
    return _minimal_config(
        regime_detector={
            "mode": "threshold_rules",
            "components": [],
            "rules": [],
            "default_regime": default_regime,
        },
        regimes=regimes,
    )


def test_v9_no_longer_blocks_trending_default_when_fully_ungated():
    """The other half of the gap: the OLD V9 rejected default_regime='trending'
    UNCONDITIONALLY, even here, where regime_detector.rules=[] means there is no gate
    to bypass at all (V9's own stated rationale does not apply). This is exactly the
    canonical fully-ungated pattern from
    tests/test_ungated_config_pattern.py::test_pattern_a_unknown_is_the_unique_warmup_safe_choice."""
    violations = validate(_ungated_pattern_a_config("trending"))
    assert not any("VIOLATION V9" in v for v in violations), (
        f"V9 incorrectly fired for a fully-ungated config (rules=[]): {violations}"
    )


def test_v9_permits_mean_reversion_and_chop_default_when_fully_ungated():
    for name in ("mean_reversion", "chop", "unknown"):
        violations = validate(_ungated_pattern_a_config(name))
        assert not any("VIOLATION V9" in v for v in violations), f"{name}: {violations}"


# ---------------------------------------------------------------------------
# V10 (new): fully-ungated config must not point default_regime at a null block
# ---------------------------------------------------------------------------


def test_v10_flags_dead_ungated_config():
    """components=[] and rules=[] means EVERY bar resolves to default_regime — if that
    key's strategies.regimes block is null, the config forecasts 0.0 forever with no
    error anywhere. This is the concrete mistake risk in authoring the canonical
    pattern (moving default_regime without moving its components block)."""
    config = _minimal_config(
        regime_detector={
            "mode": "threshold_rules",
            "components": [],
            "rules": [],
            "default_regime": "mean_reversion",
        },
        regimes={
            "trending": None,
            "mean_reversion": None,
            "chop": None,
            "unknown": None,
        },
    )
    violations = validate(config)
    assert any("VIOLATION V10" in v for v in violations), (
        f"Expected VIOLATION V10 for a dead fully-ungated config; got: {violations}"
    )


def test_v10_permits_correctly_populated_fully_ungated_config():
    for name in ("trending", "mean_reversion", "chop", "unknown"):
        violations = validate(_ungated_pattern_a_config(name))
        assert not any("VIOLATION V10" in v for v in violations), (
            f"{name}: {violations}"
        )


def test_v10_does_not_fire_for_gated_configs():
    """V10 only applies to the components=[]/rules=[] signature — a normal gated
    config with a null default_regime='unknown' block must not be flagged."""
    violations = validate(_gated_config("unknown"))
    assert not any("VIOLATION V10" in v for v in violations)


# ---------------------------------------------------------------------------
# V7 hardening (2026-07-28): an EXPLICIT null default_regime must be rejected.
#
# V7 read `rd.get("default_regime")` and then guarded with `is not None`, so an
# explicit null skipped the enum check entirely. V9 tests membership in a
# three-string tuple, which None fails. V10 guards on `is not None` too. Three
# rules, all blind to the same value — it validated with zero violations.
#
# Before the sibling engine fix (regime_engine.py:137) that config then resolved
# every unmatched bar to MEAN_REVERSION and traded it. After it, the config is
# harmless but silently inert: 0.0 on every bar with nothing reporting why, which
# is the exact failure mode V10 exists to name. Rejecting it at V7 makes it loud.
#
# Note the distinction this must preserve: an ABSENT key is legitimate and safe —
# regime_engine.py:70 reads it as `config.get("default_regime", "unknown")`, so it
# means "unknown", not "null". Only an explicit null is an error.
# ---------------------------------------------------------------------------


def _gated_config_no_default_regime() -> dict:
    detector = _gated_config("unknown")["regime_detector"]
    del detector["default_regime"]
    return _minimal_config(
        regime_detector=detector,
        regimes={
            "trending": {"components": [EMA]},
            "mean_reversion": {"components": [EMA]},
            "chop": {"components": [EMA]},
            "unknown": None,
        },
    )


def test_v7_rejects_explicit_null_default_regime_when_gated():
    """THE regression. A null default_regime previously validated clean."""
    violations = validate(_gated_config(None))
    assert any("VIOLATION V7" in v and "default_regime" in v for v in violations), (
        f"Expected VIOLATION V7 for an explicit null default_regime; got: {violations}"
    )


def test_v7_rejects_explicit_null_default_regime_when_fully_ungated():
    """The fully-ungated pattern is where a null default is most dangerous: the
    fall-through fires on EVERY bar, so the whole config is inert."""
    config = _minimal_config(
        regime_detector={
            "mode": "threshold_rules",
            "components": [],
            "rules": [],
            "default_regime": None,
        },
        regimes={
            "trending": None,
            "mean_reversion": {"components": [EMA]},
            "chop": None,
            "unknown": None,
        },
    )
    violations = validate(config)
    assert any("VIOLATION V7" in v and "default_regime" in v for v in violations), (
        f"Expected VIOLATION V7 for a null default_regime in a fully-ungated config; "
        f"got: {violations}"
    )


def test_absent_default_regime_key_is_still_accepted():
    """Regression guard on the distinction that makes this fix safe rather than
    merely strict. An omitted key is NOT an error — the engine reads it as
    "unknown". If this ever fails, the fix has become a breaking change."""
    violations = validate(_gated_config_no_default_regime())
    assert not any("default_regime" in v for v in violations), (
        f"An absent default_regime key must remain valid (engine reads it as "
        f"'unknown'); got: {violations}"
    )


def test_null_default_regime_reports_v7_only_and_not_a_garbled_v10():
    """V10's `is not None` guard is message hygiene, not the hole, and must stay.

    validate() collects every violation without short-circuiting, so if V10's guard
    were also removed a single null fault would emit the correct V7 plus a nonsense
    V10 naming `strategies.regimes.None`. One fault, one clear violation.
    """
    config = _minimal_config(
        regime_detector={
            "mode": "threshold_rules",
            "components": [],
            "rules": [],
            "default_regime": None,
        },
        regimes={
            "trending": None,
            "mean_reversion": None,
            "chop": None,
            "unknown": None,
        },
    )
    violations = validate(config)
    assert any("VIOLATION V7" in v and "default_regime" in v for v in violations)
    assert not any("V10" in v and "None" in v for v in violations), (
        f"V10 emitted a violation naming the null default_regime — its `is not None` "
        f"guard was removed and now double-reports one fault; got: {violations}"
    )


def test_valid_default_regime_names_still_pass_v7():
    """The fix must not become over-strict: all four mapped names stay clean."""
    for name in ("trending", "mean_reversion", "chop", "unknown"):
        violations = validate(_gated_config(name))
        assert not any(
            "VIOLATION V7" in v and "default_regime" in v for v in violations
        ), f"{name}: V7 wrongly rejected a valid default_regime; got: {violations}"


def test_v10_flags_a_dead_ungated_config_that_omits_default_regime():
    """The other half of the same fault: V10 judged the RAW default_regime, so an
    absent key (which the engine reads as "unknown") skipped the dead-config check.

    This config validated completely clean and forecast 0.0 on every bar forever —
    verbatim the failure V10's own message describes. V9/V10 now judge the regime the
    engine will actually resolve to, so it is caught.
    """
    detector = {"mode": "threshold_rules", "components": [], "rules": []}
    config = _minimal_config(
        regime_detector=detector,
        regimes={
            "trending": None,
            "mean_reversion": None,
            "chop": None,
            "unknown": None,
        },
    )
    assert "default_regime" not in detector, "fixture must omit the key, not null it"
    violations = validate(config)
    assert any("VIOLATION V10" in v for v in violations), (
        f"Expected VIOLATION V10 for a fully-ungated config that omits default_regime "
        f"and whose implied 'unknown' block is null; got: {violations}"
    )


def test_v10_still_permits_an_omitted_default_regime_with_a_populated_unknown_block():
    """Guard against the fix becoming over-strict: omitting the key is legal whenever
    the implied 'unknown' regime actually carries components."""
    config = _minimal_config(
        regime_detector={"mode": "threshold_rules", "components": [], "rules": []},
        regimes={
            "trending": None,
            "mean_reversion": None,
            "chop": None,
            "unknown": {"components": [EMA]},
        },
    )
    violations = validate(config)
    assert not violations, f"Expected a clean config; got: {violations}"
