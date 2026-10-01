"""
CUL-161 — the aux-feed read path must not mutate a tracked cache on a pure read.

CUL-26 closed the OHLCV read path (fetch_historical_data(localStorage=False)).
The SAME BaseFetcher._load_all/_merge_and_store mutate-on-read mechanism is
reached a second time through the aux-feed path
(DataManager._premerge_aux_feeds -> feed.fetcher.get_data() -> _load_all), whose
fetchers are built by the factory lambdas in data/feed_registry.py — every one of
which hardcoded localStorage=True with no way to override it.

This suite proves the fix threads a `localStorage` opt-out end to end:

  * test_every_registry_factory_threads_localStorage — all 8 factory entries in
    both registries (2 in FEED_REGISTRY, 6 in RESERVED_FEED_REGISTRY) forward the
    flag to their fetcher. Per-factory: reverting the threading in one lambda
    turns exactly this test red for that feed. Uses recorder stubs, so no reserved
    designation gate and no network are touched.
  * test_load_data_threads_flag_and_default_call_is_unchanged — the
    BacktestEngine.load_data -> factory(...) hop forwards feed_local_storage:
    False passes localStorage=False into the factory; the default omits the kwarg
    entirely, so a factory predating the flag (the existing tests') is called
    byte-identically.
  * test_pure_read_does_not_mutate_funding_cache / _default_write_through — the
    load-bearing differential: a gapped-window read through the REAL funding
    factory. localStorage=False leaves the on-disk cache bytes untouched while the
    default write-through path rewrites the gap-filled cache. NO NETWORK:
    FundingRateFetcher._fetch_remote is monkeypatched to a fixture-returning
    tripwire; a `fired` list asserts the mock — never a socket — served the fetch.

Matches CUL-26's docstring honesty: the flag closes cache-mutation-on-read, NOT
fetch-on-read (the mocked remote is still allowed to fire on localStorage=False).
"""

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import logging  # noqa: E402

import data.feed_registry as feed_registry  # noqa: E402
from core.backtester import BacktestEngine  # noqa: E402
from data.feed_registry import FEED_REGISTRY, RESERVED_FEED_REGISTRY  # noqa: E402
from data.fetchers.funding_rate_fetcher import FundingRateFetcher  # noqa: E402

TEST_LOGGER = logging.getLogger("trading_bot_test_aux_localstorage")

T0 = pd.Timestamp("2020-01-01 00:00:00")  # far from any seal


# ---------------------------------------------------------------------------
# 1) Every factory entry in both registries threads the flag to its fetcher
# ---------------------------------------------------------------------------


class _Recorder:
    """Stand-in fetcher class: records the localStorage it was constructed with."""

    def __init__(self, *args, **kwargs):
        self.localStorage = kwargs.get("localStorage")


def test_every_registry_factory_threads_localStorage(monkeypatch):
    # Replace the three real fetcher classes the lambdas close over. Whale's
    # reserved-designation gate lives in its real __init__; the recorder skips it.
    monkeypatch.setattr(feed_registry, "FundingRateFetcher", _Recorder)
    monkeypatch.setattr(feed_registry, "FearGreedFetcher", _Recorder)
    monkeypatch.setattr(feed_registry, "WhaleFootprintFetcher", _Recorder)

    factories = list(FEED_REGISTRY.items()) + list(RESERVED_FEED_REGISTRY.items())
    assert len(factories) == 8, "expected 2 FEED_REGISTRY + 6 RESERVED_FEED_REGISTRY entries"

    for name, factory in factories:
        built_false = factory(["BTCUSD"], T0, T0 + pd.Timedelta(8, unit="h"), "d", localStorage=False)
        assert built_false.localStorage is False, f"{name}: localStorage=False not threaded to fetcher"

        built_default = factory(["BTCUSD"], T0, T0 + pd.Timedelta(8, unit="h"), "d")
        assert built_default.localStorage is True, f"{name}: default localStorage must stay True (bit-identical)"


# ---------------------------------------------------------------------------
# 2) load_data -> factory hop forwards the flag; default call is byte-identical
# ---------------------------------------------------------------------------


class _RecordingDataManager:
    """Serves one bar, records register_feed(), never touches the network."""

    def __init__(self):
        self.historical_data = {}
        self._aux_feeds = {}

    def fetch_historical_data(self, symbol, start_date, end_date, exchange="binance"):
        return pd.DataFrame({"timestamp": [pd.Timestamp("2022-01-01")], "close": [1.0]})

    def register_feed(self, name, fetcher, window_seconds, agg, required=False, fill="none", delay_seconds=0.0):
        self._aux_feeds[name] = fetcher

    def initialize(self):
        pass


def _run_load_data(feed_local_storage_kwargs):
    captured = {}

    def recording_factory(symbols, start, end, data_dir, exchange="binance", **kwargs):
        captured["kwargs"] = kwargs
        return object()

    dm = _RecordingDataManager()
    engine = BacktestEngine(data_manager=dm, logger=TEST_LOGGER, symbols=["BTCUSD"])
    engine.load_data(
        start_date="2022-01-01",
        end_date="2022-01-02",
        extra_feeds={"funding_rate": recording_factory},
        **feed_local_storage_kwargs,
    )
    return captured["kwargs"]


def test_load_data_threads_flag_and_default_call_is_unchanged():
    # Opt-out: the factory receives localStorage=False.
    assert _run_load_data({"feed_local_storage": False}) == {"localStorage": False}

    # Default: NO localStorage kwarg is passed, so a factory predating the flag
    # (the fixed (symbols, start, end, data_dir, exchange=...) contract every
    # existing aux-feed test uses) is called byte-identically.
    assert _run_load_data({}) == {}


# ---------------------------------------------------------------------------
# 3) Differential: a pure aux-feed read must not write the on-disk cache
# ---------------------------------------------------------------------------


def _funding_bars(timestamps) -> pd.DataFrame:
    ts = pd.DatetimeIndex(timestamps)
    return pd.DataFrame(
        {
            "timestamp": ts,
            "funding_rate": 0.0001,
            "mark_price": 100.0,
        }
    )


def _seed_gapped_funding_cache(path: Path) -> None:
    """8h settlements 0,8,16 then 40,48,56 (24h & 32h missing -> a >16h gap)."""
    kept = [T0 + pd.Timedelta(h, unit="h") for h in (0, 8, 16, 40, 48, 56)]
    _funding_bars(kept).to_csv(path, index=False)


def _install_remote(monkeypatch, fired):
    def _remote(self, symbol, start, end):
        rng = pd.date_range(start=pd.Timestamp(start), end=pd.Timestamp(end), freq="8h")
        fired.append((symbol, str(start), str(end)))
        return _funding_bars(rng)

    monkeypatch.setattr(FundingRateFetcher, "_fetch_remote", _remote)


def test_pure_read_does_not_mutate_funding_cache(tmp_path, monkeypatch):
    cache = tmp_path / "BTCUSDT_funding_8h.csv"
    _seed_gapped_funding_cache(cache)
    before = cache.read_bytes()

    fired: list = []
    _install_remote(monkeypatch, fired)

    fetcher = FEED_REGISTRY["funding_rate"](
        ["BTCUSDT"],
        T0,
        T0 + pd.Timedelta(56, unit="h"),
        str(tmp_path),
        exchange="binance",
        localStorage=False,
    )
    df = fetcher.get_data("BTCUSDT")

    assert fired, "tripwire: the mocked remote never fired — real network path?"
    assert not df.empty
    assert cache.read_bytes() == before, "localStorage=False rewrote the on-disk aux-feed cache"


def test_default_write_through_does_mutate_funding_cache(tmp_path, monkeypatch):
    """Differential control: the default (localStorage omitted -> True) rewrites."""
    cache = tmp_path / "BTCUSDT_funding_8h.csv"
    _seed_gapped_funding_cache(cache)
    before = cache.read_bytes()

    fired: list = []
    _install_remote(monkeypatch, fired)

    fetcher = FEED_REGISTRY["funding_rate"](
        ["BTCUSDT"],
        T0,
        T0 + pd.Timedelta(56, unit="h"),
        str(tmp_path),
        exchange="binance",  # localStorage omitted -> default True
    )
    df = fetcher.get_data("BTCUSDT")

    assert fired, "tripwire: the mocked remote never fired — real network path?"
    assert not df.empty
    assert cache.read_bytes() != before, "default write-through path did not rewrite the gap-filled cache"
