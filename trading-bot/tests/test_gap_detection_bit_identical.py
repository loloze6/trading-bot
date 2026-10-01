"""
CUL-261 / E-039: off-by-default gap detection at candle completion.

E-039's prescreen-removal parity check found a hard blocker: gap detection
(`_contiguous_segments`/`gap_skipped_pct`) exists ONLY inside
`strategy-research/tools/prescreen_signal.py`, reaching only the prescreen kill
path. The real engine's own `data_manager.py::validate_data_continuity` only logs
a console warning -- never structured, never counted, never reaching any
artifact. This closes that gap at the source: `TradingBot._process_symbol_
candle_completion` (core/trading_bot.py), the SAME callback live trading uses.

Four things are proven here:
  1. `_check_and_record_gap` unit-level: first candle never flags, an exact-step
     candle never flags, a mismatched delta does -- and never mutates state it
     shouldn't.
  2. CUL-271's `gap_policy` tiers -- replacing the single-bar
     `suppress_allocation_after_gap` this ticket originally shipped with, per
     the design spec's own Step 1/2 investigation (see core/trading_bot.py's
     constructor docstring: every strategy component already exposes
     get_required_periods()/is_ready(), but the LIVE engines actually wired
     into AdvancedStrategy collapse readiness to one shared warmup value, not a
     true per-indicator check, and CompositeStrategy's per-indicator pattern is
     never instantiated in the live path -- so the fixed-tier fallback is what
     the spec's mechanical rule dictates, not a preference). "ignore" (<=
     ignore_max_bars) does nothing special; "middle" blocks a NEW entry
     (flat -> nonzero) until bars_since_gap reaches the strategy's own
     required_bars, keeping any existing position untouched; "large" forces an
     immediate flatten (reusing the same direct-execute bypass PR-2's risk-gate
     kill-switch uses) plus AdvancedStrategy.reset_history() (a real segment
     split), after which the engine's own pre-existing is_ready() gate
     withholds new entries for free until re-warmed. Driven through the real
     `_process_symbol_candle_completion` with lightweight real collaborators
     (ForecastManager, MockPortfolioInfo, a real int strategy.required_bars)
     and mocked I/O boundaries, not a full backtest, since manufacturing a real
     data-cache gap of an exact chosen size on demand isn't reliable.
  3. No fabricated bars: a missing period is never forward-filled, NaN-padded,
     or interpolated into the strategy's update stream -- a documented
     judgment call (see CUL-271's Linear issue) made because 23 heterogeneous
     components' pandas operations were not written with NaN-handling in mind,
     and inserting NaNs generically risks silently corrupting an unaudited
     subset of them. Only real observed bars are ever fed through.
  4. FLAG OFF is byte-identical, driven through the real engine end to end
     (`core/launcher.py::run_backtest`), same reference window and cache-guard
     convention as tests/test_model_funding_bit_identical.py.

VERIFIED this session (2026-09-04, CUL-261 follow-up): a real backtest against
a genuine gap in `local_data/BTCUSDT_1h.csv` (2018-01-04 03:00->05:00) with
gap_detection=True correctly detected and recorded it end to end -- see
CUL-261's Linear issue and PR #142 for the reproduction. gap_policy's own tier
behavior is proven at the unit level above, not yet re-verified against that
same real gap; the manufactured-timestamp tests are the evidence for the
tier logic itself.
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


def test_gap_policy_without_gap_detection_raises_loud():
    """CUL-271: gap_policy replaces suppress_allocation_after_gap."""
    with pytest.raises(ValueError, match="requires gap_detection=True"):
        _bare_bot(gap_detection=False, gap_policy={"ignore_max_bars": 2})


def test_gap_detection_off_by_default_state_is_inert():
    bot = _bare_bot()
    assert bot.gap_detection is False
    assert bot.gap_policy is None
    assert bot.gap_events == []
    assert bot._active_gap_tier == {}


# ---------------------------------------------------------------------------
# 2. CUL-271 gap_policy tiers, driven through the real per-bar method with
#    lightweight real collaborators (ForecastManager, MockPortfolioInfo,
#    strategy.required_bars a real int) + mocked I/O boundaries.
# ---------------------------------------------------------------------------

class _RecordingTracker:
    def __init__(self):
        self.calls = []

    def record_state(self, **kwargs):
        self.calls.append(kwargs)


def _make_bot(*, gap_detection: bool, gap_policy: dict | None,
              initial_balance: dict | None = None,
              timestamps: list | None = None,
              closes: list | None = None) -> tuple[TradingBot, _RecordingTracker]:
    import logging

    data_manager = MagicMock()
    data_manager.candle_builder = MagicMock()
    timestamps = timestamps or [pd.Timestamp("2024-01-01 00:00:00"), pd.Timestamp("2024-01-01 05:00:00")]
    closes = closes or [100.0, 101.0]
    data_manager.get_data_history.side_effect = [
        pd.DataFrame({"close": [c], "timestamp": [t]}) for c, t in zip(closes, timestamps)
    ]

    strategy = MagicMock()
    strategy.update.return_value = None
    strategy.generate_signals.return_value = SimpleNamespace(forecast=10.0)
    strategy.required_bars = 5  # a real int: gap_policy math compares against it directly
    strategy.reset_history = MagicMock()

    execution_handler = MagicMock()
    execution_handler._execute_portfolio_rebalance.return_value = (True, {})

    risk_manager = MagicMock()
    risk_manager.approve_allocation_change.return_value = (True, {})

    portfolio_info = MockPortfolioInfo(
        initial_balance=initial_balance or {"USDT": {"free": 10000.0, "locked": 0.0}}
    )
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
        gap_policy=gap_policy,
    )
    return bot, tracker


def test_1bar_gap_ignore_tier_trading_continues():
    """1-bar gap (2h delta vs 1h step -> 1 bar missed) is <= ignore_max_bars=2:
    no special handling, allocation_change stays nonzero exactly like the
    no-gap-policy baseline."""
    bot, tracker = _make_bot(
        gap_detection=True, gap_policy={"ignore_max_bars": 2, "large_min_bars": 5},
        timestamps=[pd.Timestamp("2024-01-01 00:00:00"), pd.Timestamp("2024-01-01 02:00:00")],
    )
    bot._process_symbol_candle_completion("BTCUSDT")
    bot._process_symbol_candle_completion("BTCUSDT")
    assert len(tracker.calls) == 2
    assert tracker.calls[1]["allocation_change"] != 0.0
    assert bot._active_gap_tier == {}  # ignore tier records nothing to act on


def test_middle_tier_blocks_new_entry_keeps_no_position_flat():
    """A gap of 3 bars (4h delta) with ignore_max_bars=2, large_min_bars=5 is
    "middle": flat -> nonzero is a NEW entry and must be blocked to exactly 0.0."""
    bot, tracker = _make_bot(
        gap_detection=True, gap_policy={"ignore_max_bars": 2, "large_min_bars": 5},
        timestamps=[pd.Timestamp("2024-01-01 00:00:00"), pd.Timestamp("2024-01-01 04:00:00")],
    )
    bot._process_symbol_candle_completion("BTCUSDT")
    assert bot._active_gap_tier.get("BTCUSDT") is None  # first bar: nothing to compare against yet
    bot._process_symbol_candle_completion("BTCUSDT")
    assert bot._active_gap_tier.get("BTCUSDT") == "middle"
    assert tracker.calls[1]["allocation_change"] == 0.0
    strategy = bot.strategy
    strategy.reset_history.assert_not_called()  # middle tier never resets history


def test_middle_tier_recovery_after_required_bars():
    """Once bars_since_gap reaches strategy.required_bars, the middle tier
    lifts and a new entry is allowed again."""
    timestamps = [pd.Timestamp("2024-01-01 00:00:00"), pd.Timestamp("2024-01-01 04:00:00")] + [
        pd.Timestamp("2024-01-01 04:00:00") + pd.Timedelta(hours=h) for h in range(1, 7)
    ]
    bot, tracker = _make_bot(
        gap_detection=True, gap_policy={"ignore_max_bars": 2, "large_min_bars": 50},
        timestamps=timestamps, closes=[100.0] * len(timestamps),
    )
    for _ in range(8):
        bot._process_symbol_candle_completion("BTCUSDT")
    # strategy.required_bars=5; by the 5th post-gap real bar the tier must be lifted.
    assert bot._active_gap_tier.get("BTCUSDT") is None
    assert tracker.calls[-1]["allocation_change"] != 0.0


def test_large_tier_flattens_open_position_and_resets_history():
    """A 10-bar gap (>= large_min_bars=5) with an existing BTC position must
    force target_allocation to 0 (flatten) and call strategy.reset_history()
    -- the segment split."""
    bot, tracker = _make_bot(
        gap_detection=True, gap_policy={"ignore_max_bars": 2, "large_min_bars": 5},
        initial_balance={"USDT": {"free": 5000.0, "locked": 0.0}, "BTC": {"free": 1.0, "locked": 0.0}},
        timestamps=[pd.Timestamp("2024-01-01 00:00:00"), pd.Timestamp("2024-01-01 11:00:00")],
        closes=[100.0, 100.0],
    )
    bot._process_symbol_candle_completion("BTCUSDT")  # establishes previous_allocation from the seeded BTC balance
    prev_alloc_before = bot.portfolio_info._calculate_actual_allocation(
        100.0, bot.portfolio_info.get_account_balance(), 5100.0, "BTCUSDT"
    )
    assert prev_alloc_before != 0.0, "test setup must start from a real open position"
    bot._process_symbol_candle_completion("BTCUSDT")
    assert bot._active_gap_tier.get("BTCUSDT") == "large"
    bot.strategy.reset_history.assert_called_once()
    # The rebalance call closed the existing position: previous_allocation was
    # the real open position, and allocation_change moved target all the way
    # to 0 (allocation_change == -previous_allocation exactly proves
    # target_allocation was forced to 0.0, since calculate_allocation_change
    # is target - previous). execution_handler is mocked, so it never writes
    # back into portfolio_info -- postRebalance_* reflects unchanged balances,
    # not a real fill; that isn't this test's concern.
    call = tracker.calls[1]
    assert call["previous_allocation"] != 0.0
    assert call["allocation_change"] == pytest.approx(-call["previous_allocation"])


def test_no_fabricated_bars_added_across_a_gap():
    """CUL-271 does not synthesize placeholder/interpolated bars for a missing
    period (judgment call, documented on the Linear issue) -- only real
    observed bars are ever fed to the strategy. Proven directly: strategy.update
    is called exactly once per REAL candle, never once per missing bar."""
    bot, tracker = _make_bot(
        gap_detection=True, gap_policy={"ignore_max_bars": 2, "large_min_bars": 50},
        timestamps=[pd.Timestamp("2024-01-01 00:00:00"), pd.Timestamp("2024-01-01 10:00:00")],
    )
    bot._process_symbol_candle_completion("BTCUSDT")
    bot._process_symbol_candle_completion("BTCUSDT")
    # 9 bars were missing (10h delta - 1h step); if any were fabricated and fed
    # through, update() would have been called more than twice.
    assert bot.strategy.update.call_count == 2


def test_gap_policy_flag_off_default_is_byte_identical_unit_level():
    """gap_policy=None (default): no tier classification runs at all, exactly
    the pre-CUL-271 code path -- _active_gap_tier and _bars_since_gap never
    populate regardless of how large a gap fires."""
    bot, tracker = _make_bot(gap_detection=True, gap_policy=None)
    bot._process_symbol_candle_completion("BTCUSDT")
    bot._process_symbol_candle_completion("BTCUSDT")
    assert bot._active_gap_tier == {}
    assert bot._bars_since_gap == {}
    assert tracker.calls[1]["allocation_change"] != 0.0


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


@pytest.fixture(scope="module")
def gap_explicit_default_policy(tmp_path_factory):
    from core.launcher import DEFAULT_GAP_POLICY
    return _run(tmp_path_factory.mktemp("gap_default_policy"), gap_detection=True,
                gap_policy=dict(DEFAULT_GAP_POLICY))


@pytest.mark.slow
@pytest.mark.timeout(180)
@_needs_cache
def test_default_omitted_is_gap_detection_on_with_the_default_policy(gap_default, gap_explicit_default_policy):
    """DECLARED CHANGE (operator 2026-10-01): the gap rule is ON by default for
    every run_backtest() call -- omitting both arguments equals passing
    gap_detection=True and DEFAULT_GAP_POLICY, byte for byte."""
    import json
    assert (gap_default / "metrics.json").read_text() == (
        gap_explicit_default_policy / "metrics.json").read_text()
    assert "data_quality" in json.loads((gap_default / "metrics.json").read_text())


@pytest.mark.slow
@pytest.mark.timeout(180)
@_needs_cache
def test_default_omitted_matches_explicit_false_portfolio_states(gap_default, gap_explicit_false):
    """This reference window has no gap, so the default (gap rule on) trades
    exactly like the rule switched off: identical portfolio states."""
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
def test_gap_policy_without_gap_detection_raises_through_run_backtest(tmp_path_factory):
    with pytest.raises(ValueError, match="requires gap_detection=True"):
        _run(tmp_path_factory.mktemp("gap_bad"), gap_detection=False,
             gap_policy={"ignore_max_bars": 2})


def test_the_backtest_default_gap_policy():
    """Option B (operator 2026-10-01): ignore <= 3 missing bars; 'large' left to
    the strategy's own required_bars; large gaps flatten. run_backtest() and
    Launcher.simulate() both turn the engine tiers on; neither turns the
    indicator fill on (simulate's strategy is built without ignore_max_bars)."""
    import inspect
    from core import launcher
    assert launcher.DEFAULT_GAP_POLICY == {"ignore_max_bars": 3, "on_large_gap": "flatten"}
    params = inspect.signature(launcher.run_backtest).parameters
    assert params["gap_detection"].default is True
    assert params["indicator_fill"].default is False
    sim = inspect.getsource(launcher.Launcher.simulate)
    assert "gap_detection=True" in sim and "gap_policy=dict(DEFAULT_GAP_POLICY)" in sim
    assert "ignore_max_bars" not in sim
