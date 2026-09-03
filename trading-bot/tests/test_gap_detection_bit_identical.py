"""
CUL-261 / E-039: off-by-default gap detection at candle completion.

E-039's prescreen-removal parity check found a hard blocker: gap detection
(`_contiguous_segments`/`gap_skipped_pct`) exists ONLY inside
`strategy-research/tools/prescreen_signal.py`, reaching only the prescreen kill
path. The real engine's own `data_manager.py::validate_data_continuity` only logs
a console warning -- never structured, never counted, never reaching any
artifact. This closes that gap at the source: `TradingBot._process_symbol_
candle_completion` (core/trading_bot.py), the SAME callback live trading uses.

Three things are proven here:
  1. `_check_and_record_gap` unit-level: first candle never flags, an exact-step
     candle never flags, a mismatched delta does -- and never mutates state it
     shouldn't.
  2. `suppress_allocation_after_gap=True` zeroes allocation_change for the ONE
     bar immediately following a detected gap, and only that bar -- driven
     through the real `_process_symbol_candle_completion` with lightweight real
     collaborators (ForecastManager, MockPortfolioInfo) and mocked I/O boundaries
     (data_manager, execution_handler, risk_manager, strategy), not through a
     full backtest, since manufacturing a real data-cache gap on demand isn't
     reliable.
  3. FLAG OFF is byte-identical, driven through the real engine end to end
     (`core/launcher.py::run_backtest`), same reference window and cache-guard
     convention as tests/test_model_funding_bit_identical.py.

NOT verified this session (flagged for review, not silently assumed): whether a
REAL gap in the shipped local_data caches actually gets detected end-to-end
through a full run_backtest() call. The unit-level proof (item 1) and the
wiring proof below (data_quality key appears when the flag is on) stand in for
it, but a run against a known-gapped window is the stronger proof and should be
done before relying on this in the campaign loop.
"""
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.trading_bot import TradingBot
from execution.forecast_manager import ForecastManager
from execution.portfolio_info import MockPortfolioInfo


# ---------------------------------------------------------------------------
# 1. _check_and_record_gap, unit level -- no I/O, no collaborators needed.
# ---------------------------------------------------------------------------

def _bare_bot(**kwargs) -> TradingBot:
    """A TradingBot with only what _check_and_record_gap touches: logger,
    candle_interval_seconds, and the gap_detection/suppress flags. Every other
    collaborator stays None/default -- this method never reads them."""
    import logging
    return TradingBot(
        data_manager=None, strategy=None, execution_handler=None,
        logger=logging.getLogger("test_gap_detection"),
        candle_interval_seconds=kwargs.pop("candle_interval_seconds", 3600),
        symbols=["BTCUSDT"],
        **kwargs,
    )


def test_first_candle_for_a_symbol_never_flags():
    bot = _bare_bot(gap_detection=True)
    assert bot._check_and_record_gap("BTCUSDT", pd.Timestamp("2024-01-01 00:00:00")) is False
    assert bot.gap_events == []
    assert bot._last_candle_time["BTCUSDT"] == pd.Timestamp("2024-01-01 00:00:00")


def test_exact_expected_step_never_flags():
    bot = _bare_bot(gap_detection=True, candle_interval_seconds=3600)
    bot._check_and_record_gap("BTCUSDT", pd.Timestamp("2024-01-01 00:00:00"))
    flagged = bot._check_and_record_gap("BTCUSDT", pd.Timestamp("2024-01-01 01:00:00"))
    assert flagged is False
    assert bot.gap_events == []


def test_mismatched_delta_flags_and_records_a_structured_event():
    bot = _bare_bot(gap_detection=True, candle_interval_seconds=3600)
    bot._check_and_record_gap("BTCUSDT", pd.Timestamp("2024-01-01 00:00:00"))
    flagged = bot._check_and_record_gap("BTCUSDT", pd.Timestamp("2024-01-01 05:00:00"))
    assert flagged is True
    assert len(bot.gap_events) == 1
    event = bot.gap_events[0]
    assert event["symbol"] == "BTCUSDT"
    assert event["expected_step_seconds"] == 3600
    assert event["actual_delta_seconds"] == 5 * 3600


def test_per_symbol_isolation_one_symbols_gap_does_not_flag_the_other():
    bot = _bare_bot(gap_detection=True, candle_interval_seconds=3600)
    bot._check_and_record_gap("BTCUSDT", pd.Timestamp("2024-01-01 00:00:00"))
    bot._check_and_record_gap("ETHUSDT", pd.Timestamp("2024-01-01 00:00:00"))
    # BTCUSDT jumps 5h (gap); ETHUSDT advances exactly one step (no gap).
    assert bot._check_and_record_gap("BTCUSDT", pd.Timestamp("2024-01-01 05:00:00")) is True
    assert bot._check_and_record_gap("ETHUSDT", pd.Timestamp("2024-01-01 01:00:00")) is False
    assert len(bot.gap_events) == 1 and bot.gap_events[0]["symbol"] == "BTCUSDT"


def test_suppress_without_gap_detection_raises_loud():
    with pytest.raises(ValueError, match="requires gap_detection=True"):
        _bare_bot(gap_detection=False, suppress_allocation_after_gap=True)


def test_gap_detection_off_by_default_state_is_inert():
    bot = _bare_bot()
    assert bot.gap_detection is False
    assert bot.suppress_allocation_after_gap is False
    assert bot.gap_events == []


# ---------------------------------------------------------------------------
# 2. suppress_allocation_after_gap, driven through the real per-bar method with
#    lightweight real collaborators + mocked I/O boundaries.
# ---------------------------------------------------------------------------

class _RecordingTracker:
    def __init__(self):
        self.calls = []

    def record_state(self, **kwargs):
        self.calls.append(kwargs)


def _make_bot(*, gap_detection: bool, suppress: bool) -> tuple[TradingBot, _RecordingTracker]:
    import logging

    data_manager = MagicMock()
    data_manager.candle_builder = MagicMock()
    df1 = pd.DataFrame({"close": [100.0], "timestamp": [pd.Timestamp("2024-01-01 00:00:00")]})
    # 5h jump against a 1h expected step -- a real gap, not just "no trade".
    df2 = pd.DataFrame({"close": [101.0], "timestamp": [pd.Timestamp("2024-01-01 05:00:00")]})
    data_manager.get_data_history.side_effect = [df1, df2]

    strategy = MagicMock()
    strategy.update.return_value = None
    strategy.generate_signals.return_value = SimpleNamespace(forecast=10.0)

    execution_handler = MagicMock()
    execution_handler._execute_portfolio_rebalance.return_value = (True, {})

    risk_manager = MagicMock()
    risk_manager.approve_allocation_change.return_value = (True, {})

    portfolio_info = MockPortfolioInfo(initial_balance={"USDT": {"free": 10000.0, "locked": 0.0}})
    forecast_manager = ForecastManager()
    tracker = _RecordingTracker()

    bot = TradingBot(
        data_manager=data_manager,
        strategy=strategy,
        execution_handler=execution_handler,
        logger=logging.getLogger("test_gap_detection"),
        portfolio_info=portfolio_info,
        portfolio_state_tracker=tracker,
        forecast_manager=forecast_manager,
        risk_manager=risk_manager,
        performance_tracker=None,
        candle_interval_seconds=3600,
        symbols=["BTCUSDT"],
        gap_detection=gap_detection,
        suppress_allocation_after_gap=suppress,
    )
    return bot, tracker


def test_suppress_off_allocation_change_nonzero_on_gap_bar():
    bot, tracker = _make_bot(gap_detection=True, suppress=False)
    bot._process_symbol_candle_completion("BTCUSDT")
    bot._process_symbol_candle_completion("BTCUSDT")
    assert len(tracker.calls) == 2
    assert tracker.calls[1]["allocation_change"] != 0.0


def test_suppress_on_zeroes_only_the_gap_bar():
    bot, tracker = _make_bot(gap_detection=True, suppress=True)
    bot._process_symbol_candle_completion("BTCUSDT")
    bot._process_symbol_candle_completion("BTCUSDT")
    assert len(tracker.calls) == 2
    # First bar has no prior candle to compare against -- never a gap, never
    # suppressed, must match the suppress=False run's first-bar behavior.
    assert tracker.calls[0]["allocation_change"] != 0.0
    # Second bar (the manufactured 5h jump) is suppressed to exactly 0.0.
    assert tracker.calls[1]["allocation_change"] == 0.0


def test_suppress_on_first_bar_is_identical_to_suppress_off_first_bar():
    """Suppression must never touch a bar that wasn't the gap bar."""
    bot_off, tracker_off = _make_bot(gap_detection=True, suppress=False)
    bot_on, tracker_on = _make_bot(gap_detection=True, suppress=True)
    bot_off._process_symbol_candle_completion("BTCUSDT")
    bot_on._process_symbol_candle_completion("BTCUSDT")
    assert tracker_off.calls[0]["allocation_change"] == tracker_on.calls[0]["allocation_change"]


# ---------------------------------------------------------------------------
# 3. Flag-off byte-identity through the real engine, same convention as
#    tests/test_model_funding_bit_identical.py.
# ---------------------------------------------------------------------------

from _cache_guard import cache_skip_reason  # noqa: E402

IDENT_START, IDENT_END = "2024-04-01", "2024-05-30"
SYMBOL = "BTCUSDT"
_NEEDED = ("BTCUSDT_1h.csv", "BTCUSDT_funding_8h.csv", "fear_greed_daily.csv")
_CACHE_SKIP = cache_skip_reason(PROJECT_ROOT / "local_data", _NEEDED, IDENT_START, IDENT_END)
# Scoped to the integration tests below ONLY -- a bare module-level `pytestmark`
# would also skip the fast unit tests above when local_data is unavailable,
# which is wrong: they need no cache at all.
_needs_cache = pytest.mark.skipif(_CACHE_SKIP is not None, reason=_CACHE_SKIP or "local_data caches usable")


def _run(tmp_dir, **kwargs) -> Path:
    from core.launcher import run_backtest

    run_dir = run_backtest(
        config_path=str(PROJECT_ROOT / "strategy_config.json"),
        symbol=SYMBOL,
        start=IDENT_START,
        end=IDENT_END,
        results_root=str(tmp_dir),
        trades_log_file=str(Path(tmp_dir) / "interim_trades.json"),
        **kwargs,
    )
    return Path(run_dir)


# Module-scoped fixtures: each configuration's backtest runs ONCE and is reused
# across every assertion below -- mirrors test_model_funding_bit_identical.py's
# fixture pattern. Calling _run() fresh inside every test (the first draft of
# this file) reran the ~1400-bar window up to twice per test and blew past
# pytest.ini's 30s per-test timeout; sharing the fixture is what keeps this
# fast enough to run as `slow` rather than something worse.

@pytest.fixture(scope="module")
def gap_default(tmp_path_factory):
    return _run(tmp_path_factory.mktemp("gap_default"))


@pytest.fixture(scope="module")
def gap_explicit_false(tmp_path_factory):
    return _run(tmp_path_factory.mktemp("gap_false"), gap_detection=False)


@pytest.fixture(scope="module")
def gap_on(tmp_path_factory):
    return _run(tmp_path_factory.mktemp("gap_on"), gap_detection=True)


@pytest.mark.slow
@pytest.mark.timeout(180)
@_needs_cache
def test_default_omitted_matches_explicit_false_metrics(gap_default, gap_explicit_false):
    assert (gap_default / "metrics.json").read_text() == (gap_explicit_false / "metrics.json").read_text()


@pytest.mark.slow
@pytest.mark.timeout(180)
@_needs_cache
def test_default_omitted_matches_explicit_false_portfolio_states(gap_default, gap_explicit_false):
    assert (gap_default / "portfolio_states.csv").read_text() == (
        gap_explicit_false / "portfolio_states.csv"
    ).read_text()


@pytest.mark.slow
@pytest.mark.timeout(180)
@_needs_cache
def test_gap_detection_on_adds_data_quality_key_wiring_only(gap_on, gap_explicit_false):
    """Wiring proof, not a claim of a real detected gap on this clean window:
    the key must appear (possibly with zero events) when the flag is on, and
    must be absent when it's off."""
    import json

    on_metrics = json.loads((gap_on / "metrics.json").read_text())
    off_metrics = json.loads((gap_explicit_false / "metrics.json").read_text())
    assert "data_quality" in on_metrics
    assert "gaps_detected" in on_metrics["data_quality"]
    assert "data_quality" not in off_metrics


@pytest.mark.slow
@_needs_cache
def test_suppress_without_gap_detection_raises_through_run_backtest(tmp_path_factory):
    with pytest.raises(ValueError, match="requires gap_detection=True"):
        _run(tmp_path_factory.mktemp("gap_bad"), suppress_allocation_after_gap=True)
