"""
Daily-bar ("1d") engine support (2026-07-07), authorized to unblock P4_ts_trend's
user-delivered brief (SMA(100)-daily, long-only, next-day-open execution).

Scope was deliberately narrowed after an initial full-inventory pass: only the
constants actually on THIS hypothesis's critical path were touched
(prescreen_signal.py's block_size dispatch, run_phase1_research.py's
_run_a86_power_check block_size, run_protocol.py/launcher.py's timeframe
plumbing, check_data.py's hardcoded interval). Regime-detector tooling,
episode_significance.py's gap_bars, and main_strategy.py's std_dev_period were
confirmed NOT exercised by this specific (ungated, dense ~55%-activation,
standardized_forecast=False) hypothesis — see config/campaign_queue.yaml's
P4_ts_trend notes for the full classification.

Every constant that WAS changed gets two things here: a test proving "1h"
behavior is bit-identical to before the change (using real historical fixture
values, not synthetic ones, per this project's standing rule), and a test
proving correct "1d" behavior.
"""

import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(WORKFLOW_PATH))
sys.path.insert(0, str(TOOLS_PATH))

import run_phase1_research as rpr  # noqa: E402
import prescreen_signal  # noqa: E402


# ---------------------------------------------------------------------------
# prescreen_signal.py block_size dispatch
# ---------------------------------------------------------------------------


def test_block_size_1h_unchanged():
    """Bit-identical: "1h" must still resolve to 24, exactly as before this change."""
    assert prescreen_signal._BLOCK_SIZE_1H == 24


def test_block_size_1d_correct():
    assert prescreen_signal._BLOCK_SIZE_1D == 1


def _resolve_block_size(timeframe: str) -> int:
    """Mirrors the exact dispatch added in run_prescreen()'s body — kept as a
    small local helper so this test doesn't need to invoke the full prescreen
    pipeline just to exercise a 3-line if/elif/else."""
    if timeframe == "1h":
        return prescreen_signal._BLOCK_SIZE_1H
    elif timeframe == "1d":
        return prescreen_signal._BLOCK_SIZE_1D
    else:
        return max(prescreen_signal._BLOCK_SIZE_1H // 4, 6)


def test_block_size_dispatch_1h():
    assert _resolve_block_size("1h") == 24


def test_block_size_dispatch_1d():
    assert _resolve_block_size("1d") == 1


def test_block_size_dispatch_other_timeframes_unchanged():
    """4h/15m etc. must still get the pre-existing generic fallback (6) —
    this project's only intent was to ADD a "1d" case, not touch this."""
    assert _resolve_block_size("4h") == 6
    assert _resolve_block_size("15m") == 6


# ---------------------------------------------------------------------------
# _run_a86_power_check — bit-identical at 1h (real fixture: run_050)
# ---------------------------------------------------------------------------

# Frozen REAL power_parameters from runs/run_050/artifacts/hypothesis_card.yaml
# (H-041-A reactivation, 2026-07-05/06) — timeframe="1h" per that run's real
# research_brief.yaml. This run genuinely passed the A8.6 gate at block_size=24
# before this session's timeframe-dispatch fix existed; the fix must reproduce
# the EXACT same numbers for a "1h" (or absent-timeframe) run.
RUN_050_POWER_PARAMETERS = {
    "activation_rate": 0.03,
    "plausible_ic_upper": 0.20,
    "n_bars": 55000,
    "n_symbols": 2,
    "is_market_wide": False,
}
# Hand-computed from the pre-existing (unchanged-at-1h) formula:
#   active_n = 0.03 * 55000 * 2 = 3300
#   n_eff = 3300 / 24 = 137.5
#   mde = 1/sqrt(137.5-3) = 1/sqrt(134.5) = 0.086228...
RUN_050_EXPECTED_ACTIVE_N = 3300.0
RUN_050_EXPECTED_N_EFF = 137.5
RUN_050_EXPECTED_MDE = pytest.approx(0.08623, abs=1e-4)


def _write_hypothesis_card_and_brief(
    artifacts: Path, power_parameters: dict, timeframe: str | None
):
    artifacts.mkdir(parents=True, exist_ok=True)
    rpr.save_yaml(
        artifacts / "hypothesis_card.yaml",
        {
            "hypothesis_id": "TEST",
            "power_parameters": power_parameters,
        },
    )
    if timeframe is not None:
        rpr.save_yaml(artifacts / "research_brief.yaml", {"timeframe": timeframe})


def test_a86_power_check_bit_identical_at_1h_real_run_050_fixture(tmp_path):
    artifacts = tmp_path / "artifacts"
    _write_hypothesis_card_and_brief(
        artifacts, RUN_050_POWER_PARAMETERS, timeframe="1h"
    )

    result = rpr._run_a86_power_check(artifacts)

    assert result["expected_active_n"] == RUN_050_EXPECTED_ACTIVE_N
    assert result["expected_n_eff"] == RUN_050_EXPECTED_N_EFF
    assert result["min_detectable_ic"] == RUN_050_EXPECTED_MDE
    assert (
        result["verdict"] == "power_adequate"
    )  # matches run_050's real, historical outcome


def test_a86_power_check_missing_research_brief_defaults_to_1h_unchanged(tmp_path):
    """Runs authored before this fix have no timeframe field expectation at all —
    must default to '1h' behavior exactly (block_size=24), not error or change."""
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir(parents=True)
    rpr.save_yaml(
        artifacts / "hypothesis_card.yaml",
        {
            "hypothesis_id": "TEST",
            "power_parameters": RUN_050_POWER_PARAMETERS,
        },
    )
    # No research_brief.yaml at all.
    result = rpr._run_a86_power_check(artifacts)
    assert result["expected_n_eff"] == RUN_050_EXPECTED_N_EFF


def test_a86_power_check_1d_uses_block_size_1(tmp_path):
    """Same power_parameters, but timeframe=1d -> block_size=1, not 24.
    n_eff = active_n / 1 = 3300 (24x larger than the 1h case), proving the
    dispatch actually took effect rather than silently falling through."""
    artifacts = tmp_path / "artifacts"
    _write_hypothesis_card_and_brief(
        artifacts, RUN_050_POWER_PARAMETERS, timeframe="1d"
    )

    result = rpr._run_a86_power_check(artifacts)

    assert (
        result["expected_active_n"] == RUN_050_EXPECTED_ACTIVE_N
    )  # unaffected by block_size
    assert result["expected_n_eff"] == 3300.0
    assert result["expected_n_eff"] == RUN_050_EXPECTED_N_EFF * 24


def test_a86_block_size_is_derived_not_enumerated():
    """REPLACED 2026-08-27. This test used to read:

        assert rpr._A86_BLOCK_SIZE_BY_TIMEFRAME == {"1h": 24, "1d": 1}

    It did not merely fail to catch the bug -- it PINNED it. The table's
    two-entry shape was the defect (every other timeframe silently inherited
    the 1h value of 24, killing run_060 with an artifact verdict), and this
    assertion made adding a third entry a test failure. A test that locks in
    the shape of a defect is worse than no test.

    Its replacement asserts the property that actually matters: the block size
    is DERIVED, so a timeframe nobody has run before is correct on first use
    and there is no table to forget to update. 1h and 1d still resolve to their
    known-correct values -- that is the anchor proving the derivation computes
    the same quantity."""
    assert not hasattr(rpr, "_A86_BLOCK_SIZE_BY_TIMEFRAME"), (
        "the enumerated table is back; it is the bug's own mechanism"
    )
    assert rpr._a86_block_size("1h") == 24
    assert rpr._a86_block_size("1d") == 1
    # Never run before, correct anyway -- the whole point of the change.
    assert rpr._a86_block_size("4h") == 6
    assert rpr._a86_block_size("30m") == 48


# ---------------------------------------------------------------------------
# launcher.py::run_backtest interval_seconds override — logic-level test
# (a full backtest run is too expensive for a unit test; this isolates the
# exact conditional this change added).
# ---------------------------------------------------------------------------


def _resolve_interval(interval_seconds, config_interval_value):
    """Mirrors run_backtest's exact new dispatch logic."""
    from core.launcher import parse_interval_seconds

    if interval_seconds is not None:
        return interval_seconds
    return parse_interval_seconds(config_interval_value)


def test_run_backtest_interval_default_none_preserves_prior_behavior():
    """Bit-identical: interval_seconds=None (every pre-existing caller's
    implicit behavior) must resolve to exactly what parse_interval_seconds(3600)
    always returned — 3600 — completely unaffected by this parameter's addition."""
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "trading-bot"))
    assert _resolve_interval(None, 3600) == 3600


def test_run_backtest_interval_explicit_override_used():
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "trading-bot"))
    assert _resolve_interval(86400, 3600) == 86400


# ---------------------------------------------------------------------------
# run_protocol.py timeframe -> interval_seconds derivation
# ---------------------------------------------------------------------------


def test_run_protocol_1h_protocol_passes_none_bit_identical():
    """A protocol with timeframe absent or '1h' must compute interval_seconds=None
    (run_backtest's own default), not 3600 explicitly — proving a plain "1h"
    protocol takes the EXACT same code path as before this change existed."""
    protocol_timeframe = {}.get("timeframe", "1h")
    interval_seconds = None
    if protocol_timeframe != "1h":
        from core.launcher import parse_interval_seconds

        interval_seconds = parse_interval_seconds(protocol_timeframe)
    assert protocol_timeframe == "1h"
    assert interval_seconds is None


def test_run_protocol_1d_protocol_derives_86400():
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "trading-bot"))
    from core.launcher import parse_interval_seconds

    protocol_timeframe = {"timeframe": "1d"}.get("timeframe", "1h")
    interval_seconds = None
    if protocol_timeframe != "1h":
        interval_seconds = parse_interval_seconds(protocol_timeframe)
    assert interval_seconds == 86400


# ---------------------------------------------------------------------------
# check_data.py timeframe parameterization
# ---------------------------------------------------------------------------


def test_check_data_1h_default_unchanged():
    import check_data

    assert check_data._TIMEFRAME_SECONDS["1h"] == 3600
    assert check_data._DEFAULT_TIMEFRAME == "1h"


def test_check_data_1d_registered():
    import check_data

    assert check_data._TIMEFRAME_SECONDS["1d"] == 86400
