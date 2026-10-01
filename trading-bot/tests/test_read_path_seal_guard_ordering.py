"""Aux-feed loads are gated behind the seal-guarded OHLCV read (upstream #49).

The read-path seal guard (`data_manager._assert_no_sealed_rows`) has a single
production call site: `DataManager.fetch_historical_data`. That single guard is
only sufficient if every other data read in a backtest happens AFTER, or
THROUGH, that guarded call -- otherwise an aux feed could read sealed rows a
step before the guard ever runs (the shape of #41, the funding-series read that
had to be window-bounded rather than guarded).

This test pins the load ORDERING in `BacktestEngine.load_data`: the OHLCV fetch
that carries the guard runs before any aux feed is constructed, so a request
reaching into the seal is refused before a single aux row is read. It is coupled
to real ordering, not to a call count -- the accompanying mutation (reorder the
aux-registration loop above the OHLCV fetch in `load_data`) makes the aux factory
record itself before the guard raises, and both assertions below fail.

Self-contained on purpose: it imports only the bot's own `core`/`data` modules
so the diff is cleanly offerable upstream alongside the guard it protects.
"""
import logging
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from core.backtester import BacktestEngine  # noqa: E402
from data.data_manager import (  # noqa: E402
    SealedDataError,
    _assert_no_sealed_rows,
    _holdout_bounds,
)


def _frame(*stamps):
    return pd.DataFrame({"timestamp": [pd.Timestamp(s) for s in stamps],
                         "close": [1.0] * len(stamps)})


def _engine(recording_dm):
    """A BacktestEngine wired with only the attributes load_data touches."""
    engine = BacktestEngine.__new__(BacktestEngine)
    engine.logger = logging.getLogger("cul32-ordering-test")
    engine.historical_data = {}
    engine.data_manager = recording_dm
    engine.symbols = ["BTCUSDT"]
    engine.strategy = None          # no required feeds -> load_data's V1 check is a no-op
    engine.exchange = "binance"
    return engine


class _RecordingDM:
    """Records the order of the two reads load_data drives: the OHLCV fetch
    (which carries the seal guard) and each aux-feed construction."""

    def __init__(self, ohlcv_frame, sealed):
        self.historical_data = None
        self._aux_feeds = {}
        self.candle_builder = None
        self.events = []
        self._ohlcv_frame = ohlcv_frame
        self._sealed = sealed

    def fetch_historical_data(self, symbol, start_date, end_date,
                              exchange="binance", allow_sealed=False):
        self.events.append("ohlcv_fetch")
        # Faithful to production: the guard sits on the returned frame here
        # (data_manager.py:1121). A cache reaching into the seal is refused.
        if self._sealed and not allow_sealed:
            _assert_no_sealed_rows(self._ohlcv_frame, symbol)
        return self._ohlcv_frame

    def register_feed(self, name, fetcher, window_seconds, agg, required, fill="none", delay_seconds=0.0):
        self.events.append(f"register_feed:{name}")

    def initialize(self):
        self.events.append("initialize")


def _aux_factory_recording(dm):
    def factory(symbols, start_date, end_date, data_dir=None, exchange=None):
        dm.events.append("aux_factory")
        return object()
    return factory


def test_a_sealed_ohlcv_request_is_refused_before_any_aux_feed_loads():
    """The seal refusal fires on the OHLCV read and short-circuits load_data, so
    the aux factory never runs -- proving aux reads are gated behind the guard."""
    dm = _RecordingDM(_frame(_holdout_bounds()[0]), sealed=True)
    engine = _engine(dm)

    with pytest.raises(SealedDataError):
        BacktestEngine.load_data(
            engine, "2026-01-01", "2026-02-28",
            extra_feeds={"funding_rate": _aux_factory_recording(dm)},
        )

    assert dm.events == ["ohlcv_fetch"], (
        "an aux feed loaded before, or without, the seal-guarded OHLCV fetch; "
        f"observed order: {dm.events}")


def test_the_clean_path_loads_ohlcv_then_aux_then_initializes():
    """Positive control and the ordering in miniature: on a legitimate pre-seal
    window the OHLCV fetch still precedes aux construction and initialize()."""
    dm = _RecordingDM(_frame("2025-01-01"), sealed=False)
    engine = _engine(dm)

    BacktestEngine.load_data(
        engine, "2024-01-01", "2024-02-01",
        extra_feeds={"funding_rate": _aux_factory_recording(dm)},
    )

    assert dm.events == [
        "ohlcv_fetch", "aux_factory", "register_feed:funding_rate", "initialize",
    ], f"load order regressed: {dm.events}"
