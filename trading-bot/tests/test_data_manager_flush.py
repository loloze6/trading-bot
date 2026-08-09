"""
E-012 synthetic regression tests: backtests were silently dropping the last
two fetched bars (data/data_manager.py's replay gate parked the cursor one
row short, and the final row's candle opened but never closed).

Everything here drives DataManager/CandleBuilder directly over tiny synthetic
hourly frames -- no market data, no launcher, fast. Covers the three edits:
  B1 has_more_data gate  (`< len(...)` , was `< len(...) - 1`)
  B2 advance cursor park (`min(new_idx, n)` on overshoot)
  B3 CandleBuilder.flush_final_candle + the DataManager wrapper

Each row gets a unique volume (10.0 * (i+1)) so "the flushed candle matches
the LAST row" is actually pinned to that row's identity, not just to some
row sharing a common constant.

Fixtures wire their OWN 1-arg candle_completion_callback. DataManager's
default (_enrich_and_notify) is 2-arg; CandleBuilder fires callbacks 1-arg
(`candle_completion_callback(symbol)`, matching `_ingest`), so a fixture that
forgets to override the default swallows a TypeError at the same try/except
that guards `_ingest` and silently reads as "0 callbacks fired".
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.data_manager import DataManager  # noqa: E402

SYMBOL = "BTCUSDT"
INTERVAL_SECONDS = 3600


def _hourly_frame(n: int, start: str = "2024-01-01 00:00:00") -> pd.DataFrame:
    """n hourly OHLCV rows with a unique volume per row (10.0 * (i+1))."""
    ts = pd.date_range(start, periods=n, freq="1h")
    return pd.DataFrame({
        "timestamp": ts,
        "open":   [100.0 + i for i in range(n)],
        "high":   [100.5 + i for i in range(n)],
        "low":    [99.5 + i for i in range(n)],
        "close":  [100.2 + i for i in range(n)],
        "volume": [10.0 * (i + 1) for i in range(n)],
    })


class _CallbackRecorder:
    """1-arg candle_completion_callback matching CandleBuilder's call
    convention (`self.candle_completion_callback(symbol)`, _ingest :360).
    Counts calls and snapshots get_candle_history() as seen from inside
    each call."""

    def __init__(self, dm: DataManager, symbol: str):
        self.dm = dm
        self.symbol = symbol
        self.calls = 0
        self.history_snapshots = []

    def __call__(self, symbol: str):
        self.calls += 1
        self.history_snapshots.append(
            self.dm.candle_builder.get_candle_history(symbol, count=1000)
        )


def _make_dm(n_rows: int, symbol: str = SYMBOL, start: str = "2024-01-01 00:00:00"):
    """Backtest-mode DataManager loaded with n_rows of synthetic data and its
    own 1-arg callback wired (see module docstring)."""
    dm = DataManager(symbols=[symbol], interval_seconds=INTERVAL_SECONDS, mode="backtest")
    dm.historical_data[symbol] = _hourly_frame(n_rows, start=start)
    dm.initialize()
    recorder = _CallbackRecorder(dm, symbol)
    dm.candle_builder.candle_completion_callback = recorder
    return dm, recorder


def _replay(dm: DataManager, symbol: str, n_rows: int) -> int:
    """Feed/advance until has_more_data is False, capped at 3*n_rows feeds so
    a reverted cursor park (B2) fails the assertion instead of hanging the
    suite. Returns the number of feeds performed."""
    cap = max(3 * n_rows, 3)
    feeds = 0
    while dm.has_more_data(symbol):
        feeds += 1
        assert feeds <= cap, (
            f"has_more_data still True after {cap} feeds for n_rows={n_rows} -- "
            "the cursor never parked past the end (B2 reverted?)"
        )
        dm.process_next_tick(symbol)
        dm.advance(symbol)
    return feeds


# ---------------------------------------------------------------------------
# Core replay + flush behaviour
# ---------------------------------------------------------------------------

def test_replay_feeds_every_row_exactly_once():
    n = 5
    dm, _recorder = _make_dm(n)
    feeds = _replay(dm, SYMBOL, n)
    assert feeds == n, f"expected {n} feeds (one per row), got {feeds}"


def test_cursor_parks_at_n_and_has_more_data_goes_false():
    n = 4
    dm, _recorder = _make_dm(n)
    _replay(dm, SYMBOL, n)
    assert dm._cursor[SYMBOL] == n, f"cursor should park at n={n}, got {dm._cursor[SYMBOL]}"
    assert dm.has_more_data(SYMBOL) is False


def test_n_rows_yield_exactly_n_completion_callbacks_after_flush():
    """N-1 close in-loop (each row's feed closes the PREVIOUS candle) + 1 flush
    for the final still-open candle == N total. Kills B1 (last row never fed
    -> N-1), B2 (park removed -> infinite loop, cap assertion fails), and B3
    (flush no-op -> N-1)."""
    n = 5
    dm, recorder = _make_dm(n)
    _replay(dm, SYMBOL, n)
    dm.flush_final_candle(SYMBOL)
    assert recorder.calls == n, f"expected {n} completion callbacks, got {recorder.calls}"


def test_flush_completes_the_final_candle_matching_the_last_row():
    n = 4
    dm, _recorder = _make_dm(n)
    _replay(dm, SYMBOL, n)
    final = dm.flush_final_candle(SYMBOL)
    assert final is not None
    assert final.tick_count == 1, "flushed candle should carry exactly the last row's tick"
    assert final.volume == pytest.approx(10.0 * n), (
        "flushed candle volume must equal the LAST row's volume, not any earlier row's "
        f"(row i's volume is 10.0*(i+1)); got {final.volume}"
    )


def test_flush_is_idempotent():
    n = 3
    dm, recorder = _make_dm(n)
    _replay(dm, SYMBOL, n)
    first = dm.flush_final_candle(SYMBOL)
    calls_after_first = recorder.calls
    second = dm.flush_final_candle(SYMBOL)
    assert first is not None
    assert second is None, "a second flush must find no open candle and decline"
    assert recorder.calls == calls_after_first, "the idempotent second flush must not re-fire the callback"


def test_flush_final_bar_visible_in_history_exactly_once():
    """Mirrors _ingest's append-before-callback ordering: the strategy must
    see the just-flushed bar in get_candle_history() from inside the very
    callback that reports it, exactly once (not zero, not duplicated)."""
    n = 3
    dm, recorder = _make_dm(n)
    _replay(dm, SYMBOL, n)
    final = dm.flush_final_candle(SYMBOL)
    snapshot = recorder.history_snapshots[-1]
    assert len(snapshot) == n, f"expected {n} completed candles visible at flush time, got {len(snapshot)}"
    matches = snapshot[snapshot["timestamp"] == final.start_time]
    assert len(matches) == 1, (
        f"the flushed bar's timestamp must appear exactly once in get_candle_history(); "
        f"found {len(matches)}"
    )


def test_flush_declines_loudly_when_no_open_candle(caplog):
    """A symbol that never had a row fed (N=0) has no open candle to flush --
    must decline with a logged warning, not raise or silently no-op."""
    dm, recorder = _make_dm(0)
    with caplog.at_level("WARNING", logger="trading_bot"):
        result = dm.flush_final_candle(SYMBOL)
    assert result is None
    assert any("no open candle" in r.message for r in caplog.records), (
        "flush_final_candle must log a loud decline when there is nothing to flush"
    )
    assert recorder.calls == 0


def test_flush_wrapper_raises_in_live_mode():
    """flush_final_candle must never force-close a candle that may still be
    genuinely forming in live mode. Flip .mode post-construction (constructing
    with mode='live' would open a real Binance client / network ping)."""
    dm, _recorder = _make_dm(1)
    dm.mode = "live"
    with pytest.raises(RuntimeError):
        dm.flush_final_candle(SYMBOL)


# ---------------------------------------------------------------------------
# Edge cases: N=0, N=1
# ---------------------------------------------------------------------------

def test_zero_rows_zero_feeds_zero_callbacks():
    dm, recorder = _make_dm(0)
    feeds = _replay(dm, SYMBOL, 0)
    assert feeds == 0
    assert recorder.calls == 0
    assert dm.flush_final_candle(SYMBOL) is None
    assert recorder.calls == 0


def test_one_row_zero_in_loop_callbacks_one_after_flush():
    """Pre-E-012 a single-row window processed 0 bars; the fix corrects it to 1."""
    dm, recorder = _make_dm(1)
    feeds = _replay(dm, SYMBOL, 1)
    assert feeds == 1
    assert recorder.calls == 0, "a single row never closes in-loop -- only the flush closes it"
    final = dm.flush_final_candle(SYMBOL)
    assert final is not None
    assert recorder.calls == 1
    assert final.volume == pytest.approx(10.0)


# ---------------------------------------------------------------------------
# Multi-symbol
# ---------------------------------------------------------------------------

def test_two_symbols_unequal_lengths_each_flush_once():
    dm = DataManager(symbols=["BTCUSDT", "ETHUSDT"], interval_seconds=INTERVAL_SECONDS, mode="backtest")
    dm.historical_data["BTCUSDT"] = _hourly_frame(4, start="2024-01-01 00:00:00")
    dm.historical_data["ETHUSDT"] = _hourly_frame(2, start="2024-01-01 00:00:00")
    dm.initialize()

    recorders = {}
    for symbol in ("BTCUSDT", "ETHUSDT"):
        recorders[symbol] = _CallbackRecorder(dm, symbol)
    # CandleBuilder has one shared callback slot; route by the symbol argument.
    dm.candle_builder.candle_completion_callback = lambda symbol: recorders[symbol](symbol)

    for symbol, n in (("BTCUSDT", 4), ("ETHUSDT", 2)):
        _replay(dm, symbol, n)

    finals = {}
    for symbol in ("BTCUSDT", "ETHUSDT"):
        finals[symbol] = dm.flush_final_candle(symbol)

    assert recorders["BTCUSDT"].calls == 4
    assert recorders["ETHUSDT"].calls == 2
    assert finals["BTCUSDT"].volume == pytest.approx(40.0)
    assert finals["ETHUSDT"].volume == pytest.approx(20.0)
    # Each symbol's own flush is idempotent independently of the other.
    assert dm.flush_final_candle("BTCUSDT") is None
    assert dm.flush_final_candle("ETHUSDT") is None
