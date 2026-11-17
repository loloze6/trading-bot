"""A live session decides what the backtest decides on the same candles (live/runner.py, step 2-3 proof).

A fake Kraken serves recorded hourly candles (local_data/kraken_BTCUSD_1h.csv) up to a simulated clock, the
forming candle included, as the real API does. A live session warms up, polls at an odd period for weeks of
simulated time and stops. Then:
  - no candle was fed before its hour had fully passed (no lookahead);
  - every daily bar was decided at the first poll after midnight UTC;
  - the backtest engine on the session's recorded candles gives a byte-identical local_book.csv.
"""
import datetime
import sys
from pathlib import Path

import pandas as pd
import pytest

BOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOT))

from live import runner  # noqa: E402
from live.proof.replay_session import compare  # noqa: E402

CACHE = BOT / "local_data" / "kraken_BTCUSD_1h.csv"
STRATEGY = (BOT.parent / "strategy_designer_v2" / "steps_cards" / "04_backtest" / "night_013_run" / "backtests"
            / "013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month"
              ".d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d" / "config.json")
pytestmark = pytest.mark.skipif(not CACHE.exists() or not STRATEGY.exists(), reason="cache or strategy missing")

START = pd.Timestamp("2025-06-10 13:27:11")   # inside the cache, before its end; any time of day
POLL = 1789                                    # seconds; deliberately not a divisor of an hour
DAYS = 60


class FakeClock:
    def __init__(self, t):
        self.t = t

    def __call__(self):
        return self.t

    def sleep(self, seconds):
        self.t += datetime.timedelta(seconds=seconds)


class FakeKraken:
    """fetch_ohlcv as Kraken answers it: candles starting at or after the hour holding `since`, up to now,
    the forming one included, 2000 at most."""

    def __init__(self, clock):
        df = pd.read_csv(CACHE, usecols=["timestamp", "open", "high", "low", "close", "volume"],
                         parse_dates=["timestamp"])
        df["ms"] = df["timestamp"].astype("int64") // 1_000_000
        self.df, self.clock = df, clock

    def fetch_ohlcv(self, symbol, timeframe, since=None, limit=2000):
        assert symbol == "BTC/USD:USD" and timeframe == "1h"
        now_ms = int(pd.Timestamp(self.clock()).value // 1_000_000)
        lo = since - since % 3_600_000
        rows = self.df[(self.df["ms"] >= lo) & (self.df["ms"] <= now_ms)].head(limit)
        return rows[["ms", "open", "high", "low", "close", "volume"]].values.tolist()


@pytest.mark.timeout(180)   # ~25 s alone (912 days of hourly warm-up, twice); the suite's 30 s is too tight under -n
def test_live_session_matches_backtest(tmp_path):
    clock = FakeClock(START)
    run_dir, cfg = runner.prepare_run("parity", str(STRATEGY), "BTCUSD", root=tmp_path)
    cfg = dict(cfg, poll_seconds=POLL, start_value=1000.0)
    session = runner.LiveSession(run_dir, cfg, FakeKraken(clock), clock=clock, sleep=clock.sleep)

    fed_late = []
    original_poll = session.poll_once

    def checked_poll():
        n = original_poll()
        last = session.data_manager._last_fed.get("BTCUSD")
        if last is not None and last + datetime.timedelta(hours=1) > clock():
            fed_late.append((last, clock()))
        return n

    session.poll_once = checked_poll
    session.run(max_polls=int(DAYS * 86400 / POLL))

    assert not fed_late, f"candles fed before their hour ended: {fed_late[:3]}"
    real = pd.read_csv(session.session_dir / "real_book.csv", parse_dates=["timestamp", "decided_utc"])
    assert len(real) >= DAYS - 1
    delay = (real["decided_utc"] - real["timestamp"] - datetime.timedelta(days=1)).dt.total_seconds()
    assert delay.between(0, POLL).all(), delay.describe()

    book = pd.read_csv(session.session_dir / "local_book.csv")
    assert (book["succcess_execute_portfolio_rebalance"] == True).sum() >= 1, "no trade: the test proves little"  # noqa: E712
    assert compare(session.session_dir)
