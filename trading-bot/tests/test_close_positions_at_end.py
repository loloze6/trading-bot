"""
Regression guard for TradingBot._close_all_positions_at_end (core/trading_bot.py).

Two NameErrors lived in that method, both dormant because the method only runs when a
backtest ends holding an OPEN position -- the reference window (2024-04-01 -> 2024-05-30)
ends flat, so every baseline in this fork was measured without executing the body.
(Anchors below are names rather than line numbers, which rot on the first edit.)

  1. The `postRebalance_current_allocation` ternary read `previous_allocation`, a name
     bound nowhere in the method; the in-scope name holding the pre-rebalance allocation
     is `actual_allocation`. Python evaluates only the taken branch of a ternary, so the
     undefined name stayed invisible until the close rebalance FAILS -- exactly the path
     that matters, since it is the one that has to record what the portfolio still holds.

  2. The `else:` of `if abs(allocation_change) != 0.0:` (position open but the computed
     change is zero) never bound `success_execute_portfolio_rebalance` or
     `debug_execute_portfolio_rebalance`, which the post-rebalance block and the
     record_state call below it read unconditionally.

Neither NameError propagates: the per-symbol body is wrapped in a blanket
`except Exception`, which logs and moves on. So on those two paths the damage is silent --
the close bar is simply never recorded into portfolio_states.csv.

Every other close was already correct before the fix: a SUCCEEDING forced close takes the
ternary's other arm, so the undefined name is never evaluated. Measured on this window,
pre-fix vs post-fix runs are byte-identical across all five artifacts and the pre-fix run
records the close row correctly (503 rows, allocation +2.002210281267678 -> 0.0). That is
why the faults below are injected: without one, this window proves nothing.

The assertions check both that the close bar is recorded AND what it contains. Existence
alone is too weak -- it passes for a value that is defined but wrong, which is the class
the original defect belonged to.

Both tests drive the real engine through run_backtest. Faults are injected at public
collaborator methods (MockExecutionHandler._execute_portfolio_rebalance,
ForecastManager.calculate_allocation_change) and scoped to the close by a flag raised
around TradingBot.stop() -- the private method under test is never called directly, and
every value it reads is one the engine actually produced.
"""
import logging
import sys
from pathlib import Path

import pytest
from _cache_guard import cache_skip_reason

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Measured window (E-012 re-anchor, 2026-08-09): the last bar the engine now processes
# for this window is 2025-04-15 23:00 (E-012 relaxed the replay gate + added the
# end-of-backtest flush, so the final fetched bar is fed and closed instead of dropped),
# at which the default strategy_config.json holds a LONG BTCUSDT position -- so
# _close_all_positions_at_end runs for real. The previous window (2024-09-15..2024-10-05)
# self-exits one bar before its old forced-close bar under the fix and ends flat, which is
# exactly the fix working (the stale forced close at the dropped bar is replaced by the
# strategy's own exit) but leaves this file's fixtures vacuous, so it needed a new anchor.
# Found by probing bar-by-bar open-position state across 2024-2025; no config tweak
# needed. Well clear of the sealed 2026 holdout, and the window is ~20 days (~480 bars,
# ~2.5s) rather than marking these tests slow.
# test_window_still_ends_with_an_open_position below fails loudly if this ever stops
# holding, since a flat ending would make both regression tests vacuously pass.
START_DATE = "2025-03-26"
END_DATE = "2025-04-15"
SYMBOL = "BTCUSDT"

_NEEDED_CACHES = ("BTCUSDT_1h.csv", "BTCUSDT_funding_8h.csv", "fear_greed_daily.csv")
_CACHE_SKIP = cache_skip_reason(PROJECT_ROOT / "local_data", _NEEDED_CACHES, START_DATE, END_DATE)
# CUL-275 (2026-09-07): both module-scoped fixtures below (rejected_close,
# zero_change_close) each drive one full real-engine run_backtest() -- measured
# 7.5-7.7s each on a warm disk cache, but the ticket's original report measured
# 32-45s, well past pytest.ini's global --timeout=30 for the default (fast)
# suite, causing pytest-timeout to fire mid-run at an unrelated call site with a
# misleading traceback. Likely disk-cache-state dependent (cold vs warm CSV
# reads) rather than fixed, which makes it exactly the class pytest.ini's own
# `slow` marker docstring describes ("tests that take more than a few
# seconds") -- every test in this file depends on one of these two fixtures,
# so the whole module moves to the slow lane rather than the default one.
# Run explicitly via `pytest -m slow --timeout=0` (see pytest.ini's own note).
pytestmark = [
    pytest.mark.skipif(_CACHE_SKIP is not None, reason=_CACHE_SKIP or "local_data caches usable"),
    pytest.mark.slow,
]


class _RecordingHandler(logging.Handler):
    """Collects records emitted while the end-of-backtest close runs."""

    def __init__(self, sink):
        super().__init__(level=logging.NOTSET)
        self.sink = sink

    def emit(self, record):
        self.sink.append(record)


class _CloseResult:
    """What one instrumented backtest observed about its end-of-backtest close."""

    def __init__(self):
        self.records = []
        self.open_symbols_at_close = []
        self.close_rows = []
        self.pre_stop_final = {}


def _run_backtest_with_close_fault(monkeypatch, results_dir, install_fault):
    """Run the window end to end with `install_fault` active only during the close."""
    from core.launcher import run_backtest
    from core.trading_bot import TradingBot

    result = _CloseResult()
    closing = {"active": False}
    handler = _RecordingHandler(result.records)
    original_stop = TradingBot.stop

    def stop(self):
        tracker = self.portfolio_state_tracker
        result.open_symbols_at_close = sorted(self.performance_tracker.get_open_positions())
        # The per-bar loop's final row, snapshotted BEFORE the forced close runs. The
        # close now MERGES its post-close numbers onto this row (upstream c5b1dc62's
        # replace_if_same_bar) instead of appending, so this is the pre-merge state the
        # anti-vacuity guards probe.
        result.pre_stop_final = dict(tracker.states[-1]) if tracker.states else {}
        self.logger.addHandler(handler)
        closing["active"] = True
        try:
            return original_stop(self)
        finally:
            closing["active"] = False
            self.logger.removeHandler(handler)
            # Anchor by the final-bar timestamp, not by append position. The forced
            # close now MERGES its post-close snapshot onto the per-bar loop's existing
            # final-bar row (upstream c5b1dc62) rather than appending a duplicate, so a
            # states_before: slice would capture ZERO rows. Selecting by timestamp finds
            # the single final-bar row under BOTH regimes -- merge (the per-bar row
            # existed) and append (the per-bar loop never recorded the bar) -- which is
            # what makes the len == 1 assertions a true one-row-per-bar invariant. The
            # rows' CONTENT, not just the count, is what distinguishes the fix from a
            # defined-but-wrong value.
            final_ts = result.pre_stop_final.get("timestamp")
            result.close_rows = [r for r in tracker.states if r.get("timestamp") == final_ts]

    monkeypatch.setattr(TradingBot, "stop", stop)
    install_fault(monkeypatch, closing)

    run_backtest(
        config_path=str(PROJECT_ROOT / "strategy_config.json"),
        symbol=SYMBOL,
        start=START_DATE,
        end=END_DATE,
        results_root=str(results_dir),
        # Keep the tracker's interim trades.json out of the shared results dir; the
        # session-wide guard in conftest.py fails the run if a test dirties a tracked
        # file under trading-bot/results/.
        trades_log_file=str(Path(results_dir) / "interim_trades.json"),
    )
    return result


def _reject_the_close_order(monkeypatch, closing):
    """Make the close rebalance report failure, as a rejected order would."""
    from execution.execution_handler import MockExecutionHandler

    original = MockExecutionHandler._execute_portfolio_rebalance

    def _execute_portfolio_rebalance(self, *args, **kwargs):
        if closing["active"]:
            return False, {"error": "injected: close order rejected"}
        return original(self, *args, **kwargs)

    monkeypatch.setattr(
        MockExecutionHandler, "_execute_portfolio_rebalance", _execute_portfolio_rebalance
    )


def _zero_the_close_allocation_change(monkeypatch, closing):
    """Make the close compute a zero allocation change against an open position.

    Reached for real when the pre-close allocation is already 0.0 while the tracker still
    holds the position -- a wiped-out total portfolio value (the `total_value > 0` guard in
    MockPortfolioInfo._calculate_actual_allocation returns 0.0 flat) or tracker/balance
    divergence. Both are hard to stage end to end, so the arithmetic that selects the
    branch is forced here instead; everything else in the run is real.
    """
    from execution.forecast_manager import ForecastManager

    original = ForecastManager.calculate_allocation_change

    def calculate_allocation_change(self, target_allocation, current_allocation):
        if closing["active"]:
            return 0.0
        return original(self, target_allocation, current_allocation)

    monkeypatch.setattr(
        ForecastManager, "calculate_allocation_change", calculate_allocation_change
    )


def _close_path_errors(records):
    """Records emitted by the method's own `except Exception` handler."""
    return [r for r in records if "Error closing" in r.getMessage()]


def _matching(records, fragment):
    return [r for r in records if fragment in r.getMessage()]


def _describe(records):
    return "; ".join(
        f"{r.getMessage()} [{r.exc_info[1]!r}]" if r.exc_info else r.getMessage()
        for r in records
    )


@pytest.fixture(scope="module")
def rejected_close(tmp_path_factory):
    with pytest.MonkeyPatch.context() as monkeypatch:
        yield _run_backtest_with_close_fault(
            monkeypatch, tmp_path_factory.mktemp("rejected_close"), _reject_the_close_order
        )


@pytest.fixture(scope="module")
def zero_change_close(tmp_path_factory):
    with pytest.MonkeyPatch.context() as monkeypatch:
        yield _run_backtest_with_close_fault(
            monkeypatch,
            tmp_path_factory.mktemp("zero_change_close"),
            _zero_the_close_allocation_change,
        )


def test_window_still_ends_with_an_open_position(rejected_close):
    """Anti-vacuity guard: a flat ending would skip the method these tests cover."""
    assert rejected_close.open_symbols_at_close == [SYMBOL], (
        f"{START_DATE}..{END_DATE} no longer ends holding {SYMBOL}, so "
        "_close_all_positions_at_end returns early and the two regression tests below "
        "prove nothing. Re-probe for a window whose final bar holds a position."
    )


def test_rejected_close_fixture_reaches_the_failed_close_branch(rejected_close):
    """Guard: proves the injected failure lands on the close, not somewhere harmless.

    Without this, a refactor that de-targets the injection (renaming the handler method,
    moving the call, changing when `closing` is active) leaves every other test in this
    fixture passing against a SUCCEEDING close -- the happy path, tested twice, proving
    nothing about the branch these tests exist for.
    """
    assert _matching(rejected_close.records, "close failed"), (
        "the close rebalance never reported failure, so the failed-close branch was "
        "never taken; the fault injection no longer reaches the close"
    )


def test_close_survives_a_rejected_close_order(rejected_close):
    errors = _close_path_errors(rejected_close.records)
    assert not errors, (
        "_close_all_positions_at_end raised when the close rebalance reported failure: "
        f"{_describe(errors)}"
    )


def test_rejected_close_order_still_records_the_close_bar(rejected_close):
    assert len(rejected_close.close_rows) == 1, (
        "exactly one row for the final bar after the forced close merges onto it "
        "(upstream c5b1dc62 dedup); a second row would mean the close appended a "
        f"duplicate instead of merging; found {len(rejected_close.close_rows)}"
    )


def test_rejected_close_pre_close_row_did_not_already_carry_the_failure_flag(rejected_close):
    """Guard: protects the is-False write-proof from passing without a close write.

    If the per-bar final row already recorded succcess=False, the merged row would
    carry False whether or not the forced close wrote onto it, so
    test_rejected_close_records_the_handler_failure_flag would hold even under a
    merge-skipping NameError. Fail loudly and re-probe when that happens.
    """
    assert rejected_close.pre_stop_final["succcess_execute_portfolio_rebalance"] is not False, (
        "the per-bar final row already records succcess=False, so "
        "test_rejected_close_records_the_handler_failure_flag would hold even if the forced "
        "close never wrote (a merge-skipping NameError). Re-probe for a window whose final "
        "per-bar rebalance did not itself fail."
    )


def test_rejected_close_pre_close_allocation_is_non_zero(rejected_close):
    """Guard: a zero pre-close allocation makes the sign check below trivially true."""
    assert rejected_close.close_rows[0]["previous_allocation"] != 0.0, (
        "the recorded pre-close allocation is 0.0, so "
        "test_rejected_close_records_the_allocation_unchanged_including_sign would hold "
        "for every value the ternary could produce, sign errors included. Re-probe the "
        "window for one that ends holding a non-zero allocation."
    )


def test_rejected_close_records_the_allocation_unchanged_including_sign(rejected_close):
    """A close that failed moved nothing, so the post-close allocation IS the pre-close one.

    Pins the sign, not just the magnitude. The close computes
    `allocation_change = 0.0 - actual_allocation`, so a ternary arm reading the change
    instead of the allocation records that same number negated (measured: -2.0022 where
    +2.0022 is correct) -- defined, plausible and wrong, the class the original defect
    belonged to. Equality is exact because the fixed arm records the very object passed
    to record_state as previous_allocation; no arithmetic runs in between.
    """
    row = rejected_close.close_rows[0]
    assert row["postRebalance_current_allocation"] == row["previous_allocation"], (
        "a failed close leaves the position untouched, so the recorded post-close "
        "allocation must equal the pre-close one exactly, sign included; got "
        f"{row['postRebalance_current_allocation']!r} against "
        f"{row['previous_allocation']!r}"
    )


def test_rejected_close_records_the_handler_failure_flag(rejected_close):
    # Three c's: record_state's keyword is misspelled in core/trading_bot.py, so the
    # recorded column carries the typo. Not a typo here.
    assert rejected_close.close_rows[0]["succcess_execute_portfolio_rebalance"] is False, (
        "a close whose rebalance reported failure must record that failure, so a later "
        "reader of portfolio_states.csv can tell the position was NOT flattened"
    )


def test_zero_change_fixture_reaches_the_zero_change_branch(zero_change_close):
    """Guard: proves the forced zero actually selects the else branch. See the
    rejected-close twin above for why an untargeted injection is worth failing on."""
    assert _matching(zero_change_close.records, "was already at 0"), (
        "the zero-allocation-change branch was never taken, so these tests ran against "
        "an ordinary close; the fault injection no longer reaches the close"
    )


def test_close_survives_a_zero_allocation_change(zero_change_close):
    errors = _close_path_errors(zero_change_close.records)
    assert not errors, (
        "_close_all_positions_at_end raised on the zero-allocation-change branch: "
        f"{_describe(errors)}"
    )


def test_zero_allocation_change_still_records_the_close_bar(zero_change_close):
    assert len(zero_change_close.close_rows) == 1, (
        "exactly one row for the final bar after the forced close merges onto it "
        "(upstream c5b1dc62 dedup); a second row would mean the close appended a "
        f"duplicate instead of merging; found {len(zero_change_close.close_rows)}"
    )


def test_zero_change_close_records_the_injected_zero_allocation_change(zero_change_close):
    """Write-proof: the merged row carries the close's own allocation_change=0.0.

    The existing is-None assertion is vacuous under a merge-skipping NameError, since
    the per-bar final row records None too. This reads a value the CLOSE supplied
    (the injected 0.0), so it only holds if the close path actually wrote.
    """
    assert zero_change_close.close_rows[0]["allocation_change"] == 0.0, (
        "the zero-change forced close must record its allocation_change=0.0 onto the final "
        f"bar; got {zero_change_close.close_rows[0].get('allocation_change')!r} -- the close "
        "path did not write (a merge-skipping NameError would do this)"
    )


def test_zero_change_pre_close_allocation_change_is_non_zero(zero_change_close):
    """Guard: keeps the write-proof above non-vacuous.

    If the per-bar final row already carries allocation_change=0.0, the merged row
    would read 0.0 whether or not the close wrote, so the write-proof would hold under
    a NameError. Fail loudly and re-probe when that happens.
    """
    assert zero_change_close.pre_stop_final["allocation_change"] != 0.0, (
        "the per-bar final row already carries allocation_change=0.0, so the write-proof "
        "above is vacuous. Re-probe for a window whose final per-bar bar computes a non-zero "
        "allocation_change."
    )


def test_zero_allocation_change_records_the_skipped_call_as_none(zero_change_close):
    """Pins the None convention so it cannot drift silently.

    None is what the per-bar path records for a bar whose rebalance was never attempted:
    it initialises the flag to None and forces None again at record_state time whenever
    approved_rebalance is falsy. Measured on this window's artifact, 471 of 503 rows carry
    None and 32 carry True, so None is the engine's established word for "not attempted".
    The no-op close makes no call either.

    Both True and False would be defined, plausible, and produce identical numbers -- every
    other recorded value is unchanged whichever is used, because MockPortfolioInfo's
    get_account_balance is pure, so the post-rebalance recompute equals the pre-values.
    They would also pass every other test here, while making the close row the only skipped
    row in the file claiming a rebalance was attempted.

    Asserted against the tracker's in-memory row, which holds the raw object. The CSV
    serialises it as an empty field, which pandas reads back as NaN.
    """
    assert zero_change_close.close_rows[0]["succcess_execute_portfolio_rebalance"] is None, (
        "a skipped no-op close must record None, the per-bar path's convention for a "
        "rebalance that was never attempted -- not a success or a failure that never "
        "happened"
    )
