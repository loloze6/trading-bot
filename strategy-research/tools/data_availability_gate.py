"""
data_availability_gate.py — E-054 Layer 2: the real, per-window data-touch
check that decides whether a fully-specified variant's data can actually be
assembled before the engine is ever invoked on it.

Outcome model (pre-registered, E-054 project description, 2026-09-11):
  - validate — every needed series is fully available for the whole window.
  - refine   — partially available in a way a variant can be narrowed around
               (drop a bad window, drop an aux feed, narrow the date range).
               Stated explicitly: which series/window, and why.
  - decline  — something required does not exist at all, no workaround.

Two layers:
  * Layer 1 (venue_data_capability.yaml, already built) — a cheap, zero-network
    capability audit: could this (venue, symbol, timeframe, aux-feed)
    combination possibly exist at all. Consulted here BEFORE any fetch, so a
    structurally-impossible combination declines instantly without spending a
    real data touch.
  * Layer 2 (this module) — the real per-window fetch: for what SURVIVES
    Layer 1, is the actual cached/fetchable data clean enough within each
    specific window it needs. No audit can answer this in advance (internal
    gaps are a property of what actually happened to the data over time).

Three confirmed-required fixes this module implements (see E-054 Phase 1
characterization in the project's Linear description):
  1. Symbols/timeframe/windows come from the RESOLVED protocol (the one
     signal_prescreen/protocol_execution will actually run against, via
     tools/protocol_resolution.py's shared resolver when a protocol needs
     resolving from a run's state), never from hypothesis-level fields.
  2. Exchange resolution mirrors tools/run_protocol.py's exact "Option Y"
     order: explicit override -> protocol.get("exchange") -> "binance".
  3. Every window is checked INDIVIDUALLY (not the full protocol span in one
     call) — this is what makes a `refine` outcome possible (narrow around
     the bad part instead of declining the whole candidate).

Gap-tolerance threshold (confirmed by Jeremy, 2026-09-11): 5%. A window (or
aux-feed's own native-cadence series) with <= 5% of its expected observations
missing -> refine; 0% missing -> validate; > 5% missing, or no data at all
-> decline (for THAT window/feed only — see `evaluate_variant` for how
per-window/per-feed outcomes aggregate to one overall outcome).

Aux-feed handling (confirmed 2026-09-11), two distinct rules:
  1. Venue-less/symbol-less feeds (Layer 1's `non_exchange_feeds` section,
     e.g. fear_greed) skip venue/symbol matching entirely — just a date-range
     coverage check against the global series.
  2. A feed coarser than the strategy's own candle interval (e.g. daily
     fear_greed under an hourly strategy) has its gap tolerance measured in
     the FEED'S OWN native update cadence, never in units of the trading
     candle interval — measuring in candle units would make every normal
     daily feed look ~95%+ "missing" by construction. This is a different
     question from the backtest's own forward-fill merge behavior (agg='last',
     already built, not in question here): forward-fill spreads a KNOWN value
     across finer bars; this check asks whether the feed's OWN observations
     have real holes that forward-fill would otherwise silently paper over.

Scope: HISTORICAL/BACKTEST retrieval only (this repo forbids live trading;
live and backtest are architecturally different data paths — see
venue_data_capability.yaml's own header for the full reasoning). Nothing here
touches DataManager.add_tick()/the live poll path.

Deliberately runs under the trading-bot venv (imports data.data_manager,
data.feed_registry) — mirrors check_data.py's own sys.path setup. Uses
tools/protocol_resolution.py (dependency-light, no claude_agent_sdk /
google-genai) rather than importing run_phase1_research.py directly — see
that module's docstring for why.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

_HERE = os.path.dirname(os.path.abspath(__file__))    # strategy-research/tools/
_SR = os.path.dirname(_HERE)                            # strategy-research/
_REPO = os.path.dirname(_SR)                            # repo root
_TBOT = os.path.join(_REPO, "trading-bot")

if _TBOT not in sys.path:
    sys.path.insert(0, _TBOT)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import pandas as pd
import yaml

from data.data_manager import DataManager  # noqa: E402
from data.feed_registry import (  # noqa: E402
    FEED_REGISTRY,
    RESERVED_FEED_REGISTRY,
)

# CUL-213-style console-encoding guard (same fix as check_data.py / setup_run.py):
# degrade unencodable glyphs rather than crash a captured/piped stdout.
_reconfigure = getattr(sys.stdout, "reconfigure", None)
if _reconfigure is not None:
    with contextlib.suppress(OSError):
        _reconfigure(errors="replace")

_DEFAULT_LAYER1_PATH = os.path.join(_SR, "config", "venue_data_capability.yaml")
_DEFAULT_GAP_TOLERANCE = 0.05  # confirmed by Jeremy, 2026-09-11

_TIMEFRAME_SECONDS = {
    "1m": 60, "3m": 180, "5m": 300, "15m": 900, "30m": 1800,
    "1h": 3600, "2h": 7200, "4h": 14400, "6h": 21600, "8h": 28800,
    "12h": 43200, "1d": 86400, "3d": 259200, "1w": 604800, "1M": 2592000,
}
_TIMEFRAME_UNIT_SECONDS = {"m": 60, "h": 3600, "d": 86400, "w": 604800}
_TIMEFRAME_PATTERN = re.compile(r"^(\d+)(m|h|d|w)$")


def _timeframe_to_seconds(timeframe: str) -> Optional[int]:
    """
    Parse ANY '<N><unit>' timeframe string to seconds, not just the fixed set
    of standard/ccxt-native tokens in `_TIMEFRAME_SECONDS`. Bug found
    2026-09-11 (Jeremy's spot-check, 'Binance BTC 7m'): the aggregation
    fallback added earlier this session was correct in principle (420s
    divides evenly into 1m's 60s, so a 7m request should be reachable by
    aggregating 1m data) but never got a chance to evaluate it, because
    looking `timeframe` up in the fixed dict returned None for any string
    that isn't one of the ~15 enumerated tokens -- silently treating "not a
    named venue timeframe" as "not a real interval at all". CandleBuilder's
    real aggregation mechanism has no such restriction: DataManager just
    buckets rows into `interval_seconds`-sized windows (see its
    fetch_interval_seconds docstring) -- the number never has to correspond
    to a venue-native/"standard" token. '1M' (calendar month) is
    deliberately excluded from the regex fallback -- months have variable
    length in seconds, so it is ONLY ever resolved via the fixed table.
    """
    if timeframe in _TIMEFRAME_SECONDS:
        return _TIMEFRAME_SECONDS[timeframe]
    match = _TIMEFRAME_PATTERN.match(timeframe)
    if not match:
        return None
    n, unit = match.groups()
    return int(n) * _TIMEFRAME_UNIT_SECONDS[unit]

# Feed name -> "how it's checked". 'reserved' feeds decline unconditionally
# here (E-054 scope: a policy gate, not a data-availability fact -- see
# venue_data_capability.yaml's whale_footprint_kraken_ws_v2 entry).
_RESERVED_FEED_NAMES = frozenset(RESERVED_FEED_REGISTRY.keys())
_VENUE_LESS_FEED_NAMES = frozenset({"fear_greed"})
# Every other FEED_REGISTRY name (today: funding_rate) is venue/symbol-scoped.


# ---------------------------------------------------------------------------
# Exchange resolution -- mirrors tools/run_protocol.py's "Option Y" (locked
# 2026-08-09) EXACTLY: explicit override -> protocol.get("exchange") ->
# "binance". Never falls through to any ambient config.json read.
# ---------------------------------------------------------------------------

def resolve_exchange(protocol: dict, cli_override: Optional[str] = None) -> str:
    exchange = cli_override
    if exchange is None:
        exchange = protocol.get("exchange")
    if exchange is None:
        exchange = "binance"
    return exchange


# ---------------------------------------------------------------------------
# Layer 1 -- cheap, zero-network capability audit
# ---------------------------------------------------------------------------

def load_layer1(path: Optional[str] = None) -> dict:
    path = path or _DEFAULT_LAYER1_PATH
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _finer_interval_covers(requested_seconds: Optional[int], available_seconds: set) -> bool:
    """
    True if some interval strictly finer than `requested_seconds` is in
    `available_seconds` and divides it evenly -- i.e. the requested (coarser)
    timeframe is reachable by aggregating an already-available finer one
    (CandleBuilder/DataManager's real, wired mechanism: CUL-250's
    `fetch_interval_seconds` opt-in fetches at the finer resolution and
    aggregates up during replay). This is a CAPABILITY question only (could
    it possibly work) -- whether the opt-in is actually set for a given run,
    and whether the finer data is actually present, is Layer 2's real check.
    """
    if not requested_seconds:
        return False
    return any(
        s < requested_seconds and requested_seconds % s == 0
        for s in available_seconds
    )


def layer1_price_precheck(layer1: dict, exchange: str, symbol: str, timeframe: str,
                           window_start: datetime.datetime, window_end: datetime.datetime,
                           now: Optional[datetime.datetime] = None) -> tuple[bool, str]:
    """
    Cheap, zero-network structural check for PRICE data: could (exchange,
    'spot', symbol, timeframe, window) possibly exist at all. `spot` is
    hardcoded because CcxtFetcher's price path always constructs
    defaultType="spot" regardless of protocol/venue framing (confirmed by
    reading ccxt_fetcher.py and venue_data_capability.yaml's own binance.spot
    entry) -- this is not a parameter this check needs to accept.

    A venue can offer the SAME data through more than one MECHANISM with
    different limits (venue_data_capability.yaml's own header names this
    explicitly -- Kraken spot's live_rest_api vs. downloadable_archive is
    its own worked example). Fixed 2026-09-11 (Jeremy's review: Layer 1 was
    only ever consulting live_rest_api and hard-declining a window the
    moment THAT ONE mechanism couldn't reach it, even though the YAML had
    already documented a second mechanism -- the Kraken bulk-archive
    ingestion already performed for the 19-pair universe, local_data/
    kraken_*.csv, some of which reach back to 2013 -- that could. This check
    now asks "does ANY declared mechanism cover this timeframe" before
    declining, plus a venue-agnostic aggregation fallback (see
    `_finer_interval_covers`) for a coarser timeframe derivable from an
    already-available finer one. Whether the data is ACTUALLY there right
    now (vs. just structurally reachable) is still Layer 2's question,
    never this file's -- local_data/*.csv coverage is mutable, environment-
    dependent state, not a durable capability fact this audit should encode.

    Returns (ok, reason). ok=False means "decline this window without
    touching real data" -- a structural impossibility Layer 2 doesn't need
    to spend a fetch confirming.

    DECLARED BEHAVIOUR CHANGE (fix/layer1-per-coin-start-dates, 2026-09-28):
    Kraken symbols now also have a per-coin `earliest_ohlcv_utc` gate,
    populated for the 19-pair confirmed_universe by
    tools/refresh_coin_start_dates.py from each coin's own local cache's
    first row (mirroring binance.spot's existing per-coin gate below, though
    -- unlike Binance -- an absent entry does not decline by default; see the
    inline comment at the gate itself for why). Before this, a Kraken window
    was checked only against the venue-WIDE 2013-09-01 floor
    (`earliest_possible_utc`), so a coin whose OWN data starts much later
    (e.g. SUIUSD: 2023-05-03) passed Layer 1 for any window back to 2013 and
    deferred the decline to a real Layer 2 fetch. Some early windows for
    populated coins now decline at Layer 1 (no network) instead.
    """
    venues = layer1.get("venues") or {}
    venue_block = (venues.get(exchange) or {}).get("spot")
    if not venue_block:
        return False, (
            f"venue={exchange!r} product=spot is not in the Layer 1 capability "
            f"audit -- unconfirmed, decline by default (silence never resolves "
            f"to available)."
        )

    timeframes = venue_block.get("timeframes") or {}
    interval_seconds = _timeframe_to_seconds(timeframe)

    if exchange == "kraken":
        symbols_block = venue_block.get("symbols") or {}

        # Fix 2026-09-11 (Jeremy's catch: 'SHIBUSD 2010-01-15' passed
        # unconditionally): the archive-mechanism rescue above has no
        # per-symbol or per-date bound of its own -- these two checks are
        # both venue-wide facts (never "what we've fetched"), independent of
        # which mechanism/timeframe is being evaluated, so they run first.
        confirmed_universe = set(symbols_block.get("confirmed_universe") or [])
        if confirmed_universe and symbol not in confirmed_universe:
            return False, (
                f"{symbol!r} is not in kraken spot's Layer 1 confirmed_universe "
                f"({sorted(confirmed_universe)}) -- unconfirmed symbols decline "
                f"by default (silence never resolves to available), same policy "
                f"as binance.spot's earliest_ohlcv_utc gate."
            )

        earliest_possible = symbols_block.get("earliest_possible_utc")
        if earliest_possible:
            earliest_possible_dt = pd.Timestamp(earliest_possible).to_pydatetime().replace(tzinfo=None)
            if window_end < earliest_possible_dt:
                return False, (
                    f"window end {window_end} is entirely before kraken's own "
                    f"public launch ({earliest_possible_dt}) -- impossible on "
                    f"this venue for ANY symbol or mechanism, not just gappy in "
                    f"our cache."
                )

        # Per-coin gate (fix/layer1-per-coin-start-dates, 2026-09-28): uses
        # the SAME field name/shape as binance.spot's earliest_ohlcv_utc gate
        # below (populated for the 19-pair confirmed_universe by
        # tools/refresh_coin_start_dates.py, from each coin's own local
        # kraken_<SYM>_1h.csv first row). Before this, a confirmed Kraken
        # symbol with no per-coin date looked available all the way back to
        # the venue-WIDE 2013-09-01 floor above regardless of when that
        # specific coin's own data (or the coin itself) actually begins --
        # e.g. SUIUSD's real cache starts 2023-05-03, not 2013.
        #
        # UNLIKE binance's gate, a MISSING entry here does NOT decline by
        # default -- only a PRESENT entry that the window predates does.
        # Binance's stricter "decline if unconfirmed" policy is deliberately
        # not mirrored here yet: doing so would decline every Kraken symbol
        # this tool hasn't been run for (including this module's own existing
        # fixture-based tests, none of which declare this field), for no
        # additional data-availability information over what
        # confirmed_universe/earliest_possible_utc above already enforce.
        # Populate earliest_ohlcv_utc for a symbol to get the tighter bound.
        earliest_ohlcv = symbols_block.get("earliest_ohlcv_utc") or {}
        earliest_ohlcv_str = earliest_ohlcv.get(symbol)
        if earliest_ohlcv_str:
            earliest_ohlcv_dt = pd.Timestamp(earliest_ohlcv_str).to_pydatetime().replace(tzinfo=None)
            if window_end < earliest_ohlcv_dt:
                return False, (
                    f"window end {window_end} is entirely before {symbol}'s confirmed "
                    f"earliest OHLCV date {earliest_ohlcv_dt} on {exchange} (per-coin "
                    f"earliest_ohlcv_utc, venue_data_capability.yaml) -- impossible at "
                    f"the source, not just gappy in cache."
                )

        live_rest = timeframes.get("live_rest_api") or {}
        archive = timeframes.get("downloadable_archive") or {}
        interval_minutes = (interval_seconds or 0) // 60

        live_minutes = set(live_rest.get("intervals_minutes") or [])
        archive_minutes = set(archive.get("intervals_minutes") or [])
        all_minutes = live_minutes | archive_minutes

        if interval_minutes in all_minutes:
            # Directly covered by at least one declared mechanism. The
            # live-REST 720-candle recency cap only bites when live_rest_api
            # is the ONLY mechanism able to serve this interval -- if
            # downloadable_archive also lists it, a one-time archive
            # ingestion may already cover an old window regardless of that
            # cap (Layer 2's real fetch/cache check resolves whether it
            # actually does for THIS symbol).
            covered_only_by_live_rest = (
                interval_minutes in live_minutes and interval_minutes not in archive_minutes
            )
            if covered_only_by_live_rest:
                # CUL-<TBD> fix (2026-09-11): read the cap as a NUMBER
                # (history_depth_candles) rather than pattern-matching a
                # descriptive string -- see git history for the earlier
                # string-match version this replaced.
                history_depth_candles = live_rest.get("history_depth_candles")
                if history_depth_candles and interval_seconds:
                    now = now or datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
                    cutoff = now - datetime.timedelta(seconds=history_depth_candles * interval_seconds)
                    if window_start < cutoff:
                        return False, (
                            f"window start {window_start} is older than {exchange} "
                            f"spot's live REST {history_depth_candles}-candle cap at "
                            f"{timeframe} resolution (cutoff ~{cutoff}), and no other "
                            f"declared mechanism (e.g. downloadable_archive) lists "
                            f"this interval -- structurally unreachable via this "
                            f"codebase (Layer 1 audit, load_bearing_finding)."
                        )
            return True, "ok"

        # Not directly covered by any mechanism at this exact interval --
        # check the aggregation fallback before declining.
        if _finer_interval_covers(interval_seconds, {m * 60 for m in all_minutes}):
            return True, (
                "ok (not directly listed, but reachable via aggregation from a "
                "finer available interval -- Layer 2 confirms)"
            )
        return False, (
            f"timeframe={timeframe!r} not in any declared kraken spot mechanism's "
            f"intervals_minutes (live_rest_api={sorted(live_minutes)}, "
            f"downloadable_archive={sorted(archive_minutes)}), and no finer "
            f"available interval evenly divides it (Layer 1 audit)."
        )

    # binance and any other venue modeled with a flat timeframes.available list.
    available = timeframes.get("available") or []
    available_seconds = {_TIMEFRAME_SECONDS[tf] for tf in available if tf in _TIMEFRAME_SECONDS}
    if timeframe not in available and not _finer_interval_covers(interval_seconds, available_seconds):
        return False, (
            f"timeframe={timeframe!r} not in {exchange}.spot's Layer 1 "
            f"timeframes.available={available}, and no finer available interval "
            f"evenly divides it."
        )
    earliest = ((venue_block.get("symbols") or {}).get("earliest_ohlcv_utc") or {})
    earliest_str = earliest.get(symbol)
    if earliest_str is None:
        return False, (
            f"{symbol} has no confirmed earliest_ohlcv_utc entry for "
            f"{exchange}.spot in the Layer 1 audit -- unconfirmed symbols "
            f"decline by default, per that file's own closing policy."
        )
    earliest_dt = pd.Timestamp(earliest_str).to_pydatetime().replace(tzinfo=None)
    if window_end < earliest_dt:
        return False, (
            f"window end {window_end} is entirely before {symbol}'s confirmed "
            f"earliest OHLCV date {earliest_dt} on {exchange} -- impossible at "
            f"the source, not just gappy in cache."
        )
    return True, "ok"


# ---------------------------------------------------------------------------
# Layer 2 -- real per-window / per-feed data touch
# ---------------------------------------------------------------------------

def _measure_end(window_end) -> datetime.datetime:
    """CUL-369 (D-058): the exclusive bound to MEASURE a window to. `test.end`
    is the LAST INCLUDED DAY -- the engine loads every bar of a date-only end
    (base_fetcher._inclusive_end) -- so the window is measured to the next
    midnight and a gap on its last day counts as missing (before CUL-369 the
    gate stopped at the end day's midnight and never looked at that day). Like
    the engine (base_fetcher._inclusive_end: `ts == ts.normalize()`), any
    midnight end counts as the whole day; an end with another time of day is
    taken literally."""
    ts = pd.Timestamp(window_end)
    if ts == ts.normalize():
        ts = ts + pd.Timedelta(days=1)
    return ts.to_pydatetime()


def _expected_bar_count(start: datetime.datetime, end: datetime.datetime, interval_seconds: int) -> int:
    total_seconds = (end - start).total_seconds()
    return max(int(total_seconds // interval_seconds), 0)


# Real single-writer fetchers in this codebase occasionally serialize a
# timestamp with a spurious sub-second offset (observed directly, 2026-09-11:
# BTCUSDT_funding_8h.csv / ETHUSDT_funding_8h.csv carry a literal ".001000"ms
# tail on some rows) -- an artifact of the writer, not a missing observation.
# Left unguarded this shows up as a ~1e-8 "missing_fraction" on EVERY window
# uniformly, which is noise wearing the shape of a signal: it would classify
# a fully-available series as "refine" forever, never "validate". Any real
# missing observation is at minimum one whole interval (minutes to hours);
# 2 seconds is generous headroom above millisecond-scale serialization noise
# while orders of magnitude below the smallest real gap this tool cares about.
_TIMESTAMP_NOISE_EPSILON_SECONDS = 2.0


def _missing_fraction(df: pd.DataFrame, start: datetime.datetime, end: datetime.datetime,
                       interval_seconds: int) -> float:
    """
    Fraction of expected observations missing in [start, end] at
    `interval_seconds` native cadence -- accounts for a totally empty frame
    (1.0), leading/trailing boundary shortfall, AND internal gaps, all in the
    same unit (expected-bar count), so a single 5% threshold means the same
    thing regardless of which shape the missing data takes. Sub-
    `_TIMESTAMP_NOISE_EPSILON_SECONDS` boundary/step deltas are treated as
    exactly on-grid (see that constant's docstring) so serialization noise
    can never manufacture a spurious "refine"/"decline" on fully-available data.
    """
    expected = _expected_bar_count(start, end, interval_seconds)
    if expected <= 0:
        return 0.0
    if df.empty:
        return 1.0

    ts = pd.to_datetime(df["timestamp"]).sort_values()
    ts = ts[(ts >= pd.Timestamp(start)) & (ts <= pd.Timestamp(end))]
    if ts.empty:
        return 1.0

    missing_bars = 0.0
    eps = _TIMESTAMP_NOISE_EPSILON_SECONDS

    # Leading shortfall: whole intervals between `start` and the first row.
    lead_gap = (ts.iloc[0] - pd.Timestamp(start)).total_seconds()
    if lead_gap > eps:
        missing_bars += lead_gap / interval_seconds

    # Trailing shortfall: whole intervals between the last row and `end`.
    trail_gap = (pd.Timestamp(end) - ts.iloc[-1]).total_seconds()
    if trail_gap > interval_seconds + eps:
        missing_bars += (trail_gap - interval_seconds) / interval_seconds

    # Internal gaps: any step > 1 interval (+ noise floor) implies
    # (step/interval - 1) missing bars. Worked entirely in float seconds
    # (.total_seconds() on each Timedelta) to avoid numpy's deprecated
    # bare-integer/"generic unit" timedelta coercion when dividing a diff
    # Series against a plain int interval.
    diff_seconds = ts.diff().dropna().dt.total_seconds()
    for d_seconds in diff_seconds:
        if d_seconds > interval_seconds + eps:
            missing_bars += (d_seconds - interval_seconds) / interval_seconds

    return max(min(missing_bars / expected, 1.0), 0.0)


def classify_missing_fraction(fraction: float, gap_tolerance: float = _DEFAULT_GAP_TOLERANCE) -> str:
    if fraction <= 0.0:
        return "validate"
    if fraction <= gap_tolerance:
        return "refine"
    return "decline"


_DEFAULT_TBOT_CONFIG_PATH = os.path.join(_TBOT, "config.json")


def _read_ambient_fetch_interval_seconds(config_path: Optional[str] = None) -> Optional[int]:
    """
    CUL-250 (PR #133, 2026-09-03) fidelity: the real engine's coarser-from-finer
    derivation is an explicit, off-by-default opt-in read from
    trading-bot/config.json's `trading.fetch_interval_seconds` -- NOT automatic
    "closest available cache" detection (see strategy-research/docs/
    DATA_AVAILABILITY.md §2). Default (key absent/None) means "fetch at the
    exact declared timeframe," byte-identical to every run before CUL-250 --
    this function mirrors that default exactly so Layer 2 neither invents a
    derivation the engine wouldn't perform, nor false-declines a timeframe the
    engine would legitimately serve from a finer cache when the operator HAS
    opted in.
    """
    path = config_path or _DEFAULT_TBOT_CONFIG_PATH
    try:
        with open(path, encoding="utf-8") as f:
            cfg = json.load(f)
    except (OSError, ValueError):
        return None
    return (cfg.get("trading") or {}).get("fetch_interval_seconds")


def check_price_window(symbol: str, exchange: str, timeframe: str,
                        window_start: str, window_end: str,
                        gap_tolerance: float = _DEFAULT_GAP_TOLERANCE,
                        fetch_interval_seconds: Optional[int] = "AMBIENT") -> dict:
    """
    The real, per-window data touch for PRICE. Uses the exact same
    DataManager.fetch_historical_data() call the real backtest path uses
    (core/backtester.py's own load_data()), including its default
    `localStorage=True` -- so "available" here means the same thing it means
    to the engine, AND this check contributes to (rather than bypasses) the
    same on-disk cache a real backtest would build up. `localStorage=False`
    was tried and reverted (2026-09-11): `_load_all` (base_fetcher.py) gates
    the CACHE READ on this same flag (`existing = self._load_local(symbol)
    if self.localStorage else pd.DataFrame()`), not only the write -- passing
    False makes the fetcher ignore an already-complete local cache entirely
    and always attempt a live fetch, which is a strictly WORSE availability
    check (forces a network round-trip this project's own fast-test suite
    correctly blocks, and would silently reclassify a fully-cached window as
    unavailable the moment the network is unreachable). A fetch/network
    failure is caught and classified as a decline for THIS window with a
    distinct `fetch_error` flag -- Decision B means one window's failure
    never stops the others from being checked.

    KNOWN HAZARD, not fixed here (out of E-054's scope -- core fetch-path
    code needs its own dedicated review): `BaseFetcher._merge_and_store`'s
    cache write (`combined.to_csv(path, index=False)`, base_fetcher.py) is
    NOT atomic (no temp-file+os.replace, unlike this project's own
    `save_yaml` convention). Reproduced directly this session (2026-09-11): a
    single, non-concurrent gate run against run_048's 95-window protocol,
    interrupted (SIGTERM) mid-run, truncated ETHUSDT_1h.csv from 74,529 rows
    to 6,630 -- losing years of cache, not just the newest increment. Because
    Decision B means this gate fires MANY more fetch calls than a normal
    backtest, it raises the odds of ever hitting this pre-existing hazard.
    Operational mitigation until fixed: never interrupt a running gate
    process; let it finish or fail on its own.

    `fetch_interval_seconds`: the CUL-250 opt-in (see
    `_read_ambient_fetch_interval_seconds`'s docstring). The sentinel
    "AMBIENT" (default) reads trading-bot/config.json exactly as the real
    engine would; pass an explicit int (or None) to override for a test or a
    campaign that pins its own value.
    """
    interval_seconds = _timeframe_to_seconds(timeframe)
    if interval_seconds is None:
        raise ValueError(
            f"timeframe={timeframe!r} is not a parseable interval (expected a "
            f"standard token or '<N><m|h|d|w>') -- Layer 1 should have declined "
            f"this before Layer 2 was ever called; a caller invoking this "
            f"function directly with a bad timeframe is a real bug, fail loud."
        )
    start_dt = pd.Timestamp(window_start).to_pydatetime()
    end_dt = _measure_end(window_end)  # CUL-369: through the end day's last bar

    if fetch_interval_seconds == "AMBIENT":
        fetch_interval_seconds = _read_ambient_fetch_interval_seconds()

    dm = DataManager(symbols=[symbol], interval_seconds=interval_seconds, mode="backtest",
                      fetch_interval_seconds=fetch_interval_seconds)
    try:
        df = dm.fetch_historical_data(symbol, window_start, window_end, exchange=exchange)
    except Exception as e:  # SealedDataError included -- must never be papered over
        return {
            "outcome": "decline",
            "missing_fraction": 1.0,
            "fetch_error": f"{type(e).__name__}: {e}",
            "reason": f"fetch raised {type(e).__name__}: {e}",
        }

    # The dataframe's actual native cadence is dm.fetch_interval_seconds (the
    # CUL-250 opt-in resolution when set, else interval_seconds itself) -- NOT
    # necessarily the declared strategy timeframe. Measuring gap % in the
    # wrong unit would either manufacture a false gap (checking a 1h-native
    # series in 4h units) or hide a real one (the reverse).
    native_interval_seconds = dm.fetch_interval_seconds
    frac = _missing_fraction(df, start_dt, end_dt, native_interval_seconds)
    outcome = classify_missing_fraction(frac, gap_tolerance)
    reason = (
        "fully available" if outcome == "validate" else
        f"{frac:.1%} of expected bars missing (<= {gap_tolerance:.0%} tolerance)" if outcome == "refine" else
        (f"no data returned for {symbol} {window_start}..{window_end}" if df.empty
         else f"{frac:.1%} of expected bars missing (> {gap_tolerance:.0%} tolerance)")
    )
    return {"outcome": outcome, "missing_fraction": frac, "reason": reason, "rows": len(df)}


def check_aux_feed_window(feed_name: str, exchange: str, symbols: list,
                           window_start: str, window_end: str,
                           gap_tolerance: float = _DEFAULT_GAP_TOLERANCE) -> dict:
    """
    Real per-window aux-feed touch. Branches per the two confirmed rules:
      1. venue-less/symbol-less (fear_greed): date-range coverage only, no
         venue/symbol matching.
      2. everything else (funding_rate): venue/symbol-scoped, gap % measured
         in the FEED'S OWN native cadence (fetcher.interval_seconds), never
         the trading candle interval.
    Reserved feeds (whale_*) decline unconditionally -- a data-POLICY gate
    (campaign_data_policy.yaml designation), not a data-availability fact;
    Layer 2 is not the place to grant or check that designation.
    """
    if feed_name in _RESERVED_FEED_NAMES:
        return {
            "outcome": "decline",
            "missing_fraction": 1.0,
            "reason": (
                f"'{feed_name}' is a RESERVED feed (deny-by-default; requires an "
                f"explicit, committed campaign_data_policy.yaml designation). "
                f"E-054 Layer 2 does not grant or evaluate that designation -- "
                f"decline until a human ratifies it outside this check."
            ),
        }

    if feed_name not in FEED_REGISTRY:
        return {
            "outcome": "decline",
            "missing_fraction": 1.0,
            "reason": f"'{feed_name}' is not a known feed (not in FEED_REGISTRY or "
                      f"RESERVED_FEED_REGISTRY) -- was never built.",
        }

    data_dir = os.path.join(_TBOT, "local_data")
    start_dt = pd.Timestamp(window_start).to_pydatetime()
    end_dt = _measure_end(window_end)  # CUL-369: through the end day's last bar

    if feed_name in _VENUE_LESS_FEED_NAMES:
        try:
            factory = FEED_REGISTRY[feed_name]
            # localStorage=False: see check_price_window's docstring for why
            # localStorage default (True): see check_price_window's docstring
            # -- localStorage=False also disables the CACHE READ, not only
            # the write, which was tried and reverted.
            fetcher = factory([], window_start, window_end, data_dir=data_dir)
            df = fetcher.get_data()
            if isinstance(df, dict):
                df = next(iter(df.values()), pd.DataFrame())
        except Exception as e:
            return {"outcome": "decline", "missing_fraction": 1.0,
                    "fetch_error": f"{type(e).__name__}: {e}",
                    "reason": f"fetch raised {type(e).__name__}: {e}"}
        interval_seconds = getattr(fetcher, "interval_seconds", 86400)
        frac = _missing_fraction(df, start_dt, end_dt, interval_seconds)
        outcome = classify_missing_fraction(frac, gap_tolerance)
        return {
            "outcome": outcome, "missing_fraction": frac,
            "cadence_seconds": interval_seconds,
            "reason": (
                "fully available" if outcome == "validate" else
                f"{frac:.1%} missing in {feed_name}'s own {interval_seconds}s cadence"
            ),
        }

    # Venue/symbol-scoped feed (funding_rate today): check per symbol, roll
    # up to the worst outcome (a required feed missing for ANY declared
    # symbol is a real problem for that symbol's leg of the strategy).
    per_symbol = {}
    worst_outcome = "validate"
    worst_frac = 0.0
    for symbol in symbols:
        try:
            factory = FEED_REGISTRY[feed_name]
            fetcher = factory([symbol], window_start, window_end, data_dir=data_dir, exchange=exchange)
            df = fetcher.get_data(symbol)
        except Exception as e:
            per_symbol[symbol] = {"outcome": "decline", "missing_fraction": 1.0,
                                   "fetch_error": f"{type(e).__name__}: {e}"}
            worst_outcome, worst_frac = "decline", 1.0
            continue
        interval_seconds = getattr(fetcher, "interval_seconds", 28800)
        frac = _missing_fraction(df, start_dt, end_dt, interval_seconds)
        outcome = classify_missing_fraction(frac, gap_tolerance)
        per_symbol[symbol] = {"outcome": outcome, "missing_fraction": frac,
                               "cadence_seconds": interval_seconds}
        if _outcome_rank(outcome) > _outcome_rank(worst_outcome):
            worst_outcome, worst_frac = outcome, frac

    return {
        "outcome": worst_outcome, "missing_fraction": worst_frac,
        "per_symbol": per_symbol,
        "reason": (
            "fully available for all symbols" if worst_outcome == "validate"
            else f"see per_symbol detail for {feed_name}"
        ),
    }


def _outcome_rank(outcome: str) -> int:
    return {"validate": 0, "refine": 1, "decline": 2}[outcome]


# ---------------------------------------------------------------------------
# Top-level: evaluate a whole variant (protocol windows + declared aux feeds)
# ---------------------------------------------------------------------------

def evaluate_variant(config: dict, protocol: dict, gap_tolerance: float = _DEFAULT_GAP_TOLERANCE,
                      exchange_override: Optional[str] = None, layer1: Optional[dict] = None) -> dict:
    """
    The E-054 Layer 2 outcome for one fully-specified variant: resolves the
    exchange (Option Y), then checks every symbol x window individually
    (Decision B), then every declared aux feed, then aggregates to exactly
    one of validate/refine/decline (E-039's outcome model).

    Aggregation:
      - decline (whole variant) iff EVERY window declines (nothing to salvage
        by narrowing) OR any aux feed/symbol is structurally impossible per
        Layer 1 for ALL windows (a series that does not exist at all, no
        workaround) OR a reserved/unbuilt feed is declared.
      - refine iff at least one window/feed is refine or decline while at
        least one window still validates or refines (narrow around the bad
        part).
      - validate iff every window and every aux feed fully validates.

    Known scope boundary (narrowed 2026-09-11 by the mechanism-aware +
    aggregation-fallback fix in `layer1_price_precheck`, but not fully
    closed): Layer 1 now recognizes that a coarser DECLARED protocol
    `timeframe` may be reachable by aggregating an already-available finer
    one (see `_finer_interval_covers`), so it no longer false-declines that
    case outright. What remains unautomated: Layer 2's real fetch still only
    honors the CUL-250 `fetch_interval_seconds` opt-in when an operator has
    actually set it in `trading.json`/passed it explicitly -- there is no
    auto-selection of "the correct finer resolution for this protocol" per
    variant. So a Layer-1-permitted, aggregation-only-reachable window can
    still legitimately DECLINE at Layer 2 if nobody opted in for that run;
    that is the correct, honest outcome (structurally possible in principle
    is not the same as configured to happen), not a bug to silently paper
    over here.
    """
    layer1 = layer1 if layer1 is not None else load_layer1()
    exchange = resolve_exchange(protocol, exchange_override)
    symbols = protocol.get("symbols") or []
    timeframe = protocol.get("timeframe", "1h")
    windows = protocol.get("windows") or []

    window_results = []
    for w in windows:
        label = w.get("label", "")
        test = w.get("test", {})
        w_start, w_end = test.get("start"), test.get("end")
        for symbol in symbols:
            start_dt = pd.Timestamp(w_start).to_pydatetime()
            end_dt = pd.Timestamp(w_end).to_pydatetime()
            ok, l1_reason = layer1_price_precheck(layer1, exchange, symbol, timeframe, start_dt, end_dt)
            if not ok:
                window_results.append({
                    "label": label, "symbol": symbol, "start": w_start, "end": w_end,
                    "layer": 1, "outcome": "decline", "missing_fraction": 1.0, "reason": l1_reason,
                })
                continue
            result = check_price_window(symbol, exchange, timeframe, w_start, w_end, gap_tolerance)
            result.update({"label": label, "symbol": symbol, "start": w_start, "end": w_end, "layer": 2})
            window_results.append(result)

    aux_feed_names = config.get("aux_feeds") or []
    aux_results = []
    for feed_name in aux_feed_names:
        for w in windows:
            label = w.get("label", "")
            test = w.get("test", {})
            w_start, w_end = test.get("start"), test.get("end")
            result = check_aux_feed_window(feed_name, exchange, symbols, w_start, w_end, gap_tolerance)
            result.update({"feed": feed_name, "label": label, "start": w_start, "end": w_end})
            aux_results.append(result)

    outcome = _aggregate(window_results, aux_results, len(windows) * max(len(symbols), 1))

    return {
        "schema_version": 1,
        "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "exchange": exchange,
        "timeframe": timeframe,
        "symbols": symbols,
        "gap_tolerance": gap_tolerance,
        "outcome": outcome["overall"],
        "reasons": outcome["reasons"],
        "windows": window_results,
        "aux_feeds": aux_results,
    }


def _aggregate(window_results: list, aux_results: list, n_price_checks: int) -> dict:
    reasons = []

    if not window_results:
        return {"overall": "decline", "reasons": ["no windows/symbols to check -- empty protocol"]}

    bad_windows = [w for w in window_results if w["outcome"] != "validate"]
    good_windows = [w for w in window_results if w["outcome"] == "validate"]
    all_windows_bad = len(good_windows) == 0

    declined_aux = [a for a in aux_results if a["outcome"] == "decline"]
    refine_aux = [a for a in aux_results if a["outcome"] == "refine"]

    # An aux feed that declines on EVERY window it was checked against is a
    # structurally-missing series -- no workaround by narrowing the window.
    aux_names = {a["feed"] for a in aux_results}
    fully_declined_feeds = [
        name for name in aux_names
        if all(a["outcome"] == "decline" for a in aux_results if a["feed"] == name)
    ]

    if all_windows_bad and bad_windows:
        for w in bad_windows[:5]:
            reasons.append(f"{w['symbol']} {w['label']}: {w['reason']}")
        return {"overall": "decline", "reasons": reasons or ["every window declined"]}

    if fully_declined_feeds:
        for name in fully_declined_feeds:
            reasons.append(f"aux feed '{name}' is unavailable for every window checked -- "
                            f"no workaround (see aux_feeds detail).")
        return {"overall": "decline", "reasons": reasons}

    if bad_windows or refine_aux or declined_aux:
        for w in bad_windows[:10]:
            reasons.append(f"{w['symbol']} {w['label']} ({w['outcome']}): {w['reason']}")
        for a in declined_aux + refine_aux:
            reasons.append(f"aux feed '{a['feed']}' {a['label']} ({a['outcome']}): {a.get('reason', '')}")
        return {"overall": "refine", "reasons": reasons}

    return {"overall": "validate", "reasons": ["all windows and aux feeds fully available"]}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="E-054 Layer 2 data-availability gate: per-window, per-feed "
                    "real data-touch check for a fully-specified variant."
    )
    parser.add_argument("config_path", help="candidate_strategy_config.json path")
    parser.add_argument("protocol_path", help="resolved protocol JSON path "
                         "(the SAME file signal_prescreen/protocol_execution will run against)")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--out-dir", default=None, help="Where to write data_availability_gate.yaml")
    parser.add_argument("--exchange", default=None, help="Override exchange (Option Y precedence)")
    parser.add_argument("--gap-tolerance", type=float, default=_DEFAULT_GAP_TOLERANCE)
    parser.add_argument("--layer1-path", default=None)
    args = parser.parse_args()

    with open(args.config_path, encoding="utf-8") as f:
        config = json.load(f)
    with open(args.protocol_path, encoding="utf-8") as f:
        protocol = json.load(f)

    layer1 = load_layer1(args.layer1_path)
    result = evaluate_variant(
        config, protocol,
        gap_tolerance=args.gap_tolerance,
        exchange_override=args.exchange,
        layer1=layer1,
    )
    result["run_id"] = args.run_id
    result["protocol_path"] = str(args.protocol_path)

    print(f"E-054 Layer 2 outcome: {result['outcome'].upper()}")
    for r in result["reasons"][:20]:
        print(f"  - {r}")

    out_dir = Path(args.out_dir) if args.out_dir else Path(".")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "data_availability_gate.yaml"
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(result, f, sort_keys=False, allow_unicode=True)
    print(f"Wrote {out_path}")

    sys.exit({"validate": 0, "refine": 3, "decline": 2}[result["outcome"]])


if __name__ == "__main__":
    main()
