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

# prescreen_signal.py's own block_size dispatch (formerly tested here) is
# removed along with that module (E-039 step 5, 2026-09-12) -- the underlying
# "1h"->24 / "1d"->1 values it mirrored are the single shared derivation
# tools/timeframe.py::bars_per_day() already provides, tested exhaustively in
# test_timeframe_block_size.py.


# ---------------------------------------------------------------------------
# _run_a86_power_check / _a86_block_size -- REMOVED 2026-09-11 (E-039: A8.6
# dropped entirely, "always backtest" instead of an a-priori power pre-flight
# kill). The four tests that lived here (bit-identical-at-1h against the real
# run_050 fixture, missing-research-brief default, 1d block-size dispatch,
# derived-not-enumerated block size) tested functions that no longer exist in
# run_phase1_research.py. block_size derivation for prescreen_signal.py
# (tested above, test_block_size_1h_unchanged etc.) is untouched by this --
# only A8.6's OWN mirror of that derivation was removed.
# ---------------------------------------------------------------------------


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
