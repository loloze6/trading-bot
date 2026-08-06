"""
WhaleFootprintFetcher
=====================
Bar-level whale-footprint features (roadmap Phase 2.3) from the Kraken WS v2
forward capture.

Output columns added to the candle DataFrame — see
`strategy-research/tools/recorder/whale_features.py` for the exact definition of each:

    whale_lt_imbalance   [-1,+1]  signed share of the bar's LARGE-trade notional
    whale_lt_count       count    trades at or above the pair's own size threshold
    whale_cvd_delta      quote    per-bar signed notional (taker buys - sells)
    whale_size_shift     log      ln(bar median notional / trailing median)
    whale_trade_count    count    trades in the bar
    whale_attested       0/1      1 iff the coverage journal attests the whole bar

WHY THIS IS A `BaseFetcher` AND NOT A NEW LOADER
------------------------------------------------
The bot already has exactly one way to get a non-price series onto a bar:
subclass `BaseFetcher`, name a `cache_key`, return a DataFrame with `timestamp`
plus named float columns, and register the name in `feed_registry`
(`data/ADDING_A_FEED.md`). `DataManager._premerge_aux_feeds`
(data_manager.py:601-651) then `merge_asof(direction='backward')`s it onto the
candles. This class is that, and nothing else — no parallel data path.

The registration goes in `RESERVED_FEED_REGISTRY`, NOT `FEED_REGISTRY`, because
`launcher.py:290` and `launcher.py:596` pass the whole of the latter as
`extra_feeds`: membership there means "loaded by every backtest", which is the
one thing reserved data must not be. See the comment in `feed_registry.py`.

ONE REGISTRY ENTRY PER COLUMN. `_premerge_aux_feeds` attaches only the column
whose name EQUALS the registered feed name (data_manager.py:622,
`if feed_data.empty or name not in feed_data.columns`), so a multi-column feed
reaches the strategy only if each column is registered under its own name. All
six entries share one `cache_key`, so the CSV is computed once and re-read.

`BaseFetcher`'s `interval_seconds` gap arithmetic is APPLICABLE HERE, unlike on
the raw capture (`campaign_data_policy.yaml`:
`gap_semantics.base_fetcher_gap_arithmetic_applies: false`). That flag is about
the EVENT STREAM, which has no expected interval. What this class emits is the
aggregated bar grid — a regular grid by construction, with a row for every bar
including unattested ones — so the grid arithmetic is meaningful and there are
no timestamp gaps for it to trip on. Coverage is carried in a COLUMN
(`whale_attested`), never by omitting a row.

DENY BY DEFAULT — CONSTRUCTION FAILS ON UNDESIGNATED DATA
----------------------------------------------------------
The capture is registered `status: configured_reserved_undesignated`
(`campaign_data_policy.yaml:kraken_ws_forward_recorder`): "No stage, tool,
prescreen, diagnostic or backtest may read ANY window of this capture until an
explicit, separately-committed designation releases a named window."

So `__init__` calls :func:`assert_designated` and RAISES
:class:`ReservedDataError` unless the policy releases the requested window. It
raises at construction rather than inside `_fetch_remote` on purpose:
`_fetch_remote`'s contract is "return an empty DataFrame on failure, do not
raise", and a refusal that degrades to an empty DataFrame is a refusal a caller
can miss. There is deliberately NO override argument — an override would be a
designation granted by whoever happened to be writing the call, which is the
one thing the policy says a designation must not be. Releasing a window means
editing the policy file, which is a reviewed commit.

Registering the feed names in `RESERVED_FEED_REGISTRY` does NOT release the
data. The entries exist so the wiring is real and testable; the gate is what
decides.
"""

from __future__ import annotations

import datetime
import logging
import sys
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd

from data.fetchers.base_fetcher import BaseFetcher

_REPO_ROOT = Path(__file__).resolve().parents[3]

# The recorder's read side lives with the recorder. Importing it is deliberate:
# the alternative is a second definition of "what a shard is" inside the bot
# tree, and two definitions drift — which is the failure the reader's
# deny-by-default record handling exists to prevent. Precedent for the
# cross-tree path insert: trading-bot/tests/test_funding_rate_component.py:27.
_RESEARCH_ROOT = str(_REPO_ROOT / "strategy-research" / "tools")
if _RESEARCH_ROOT not in sys.path:
    sys.path.insert(0, _RESEARCH_ROOT)

from recorder.shard_reader import ShardReader  # noqa: E402
from recorder.whale_features import (  # noqa: E402
    DEFAULT_BAR_SECONDS,
    DEFAULT_BASELINE_SECONDS,
    DEFAULT_LARGE_QUANTILE,
    DEFAULT_MIN_BAR_TRADES,
    DEFAULT_MIN_BASELINE_TRADES,
    FEATURE_COLUMNS,
    whale_bar_features,
)

logger = logging.getLogger("trading_bot")

#: Policy entry governing the capture.
POLICY_PATH = _REPO_ROOT / "strategy-research" / "config" / "campaign_data_policy.yaml"
POLICY_KEY = "kraken_ws_forward_recorder"

#: Capture root, relative to the bot's `local_data` dir.
DEFAULT_CAPTURE_SUBDIR = Path("recorded_reserved") / "kraken_ws_v2"


def _to_utc(when) -> datetime.datetime:
    """
    Any datetime-like -> tz-aware UTC, which is what the reader and the journal
    compare against.

    Accepts BOTH spellings deliberately. `BaseFetcher` stores naive-UTC (its
    `_load_local` raises on a tz-aware `timestamp` column), so the normal call
    arrives naive and is INTERPRETED as UTC — not as local time, which on this
    machine would shift the window by two hours and quietly mis-align every bar
    against the coverage journal. A caller holding a tz-aware value is converted
    rather than rejected.
    """
    ts = pd.Timestamp(when)
    return (ts.tz_localize("UTC") if ts.tzinfo is None else ts.tz_convert("UTC")).to_pydatetime()


def _end_of_day_if_midnight(when: datetime.datetime) -> datetime.datetime:
    """
    A window ending exactly at midnight means THROUGH THAT DAY, not at its first
    instant.

    This is `BaseFetcher`'s own convention, not a local invention: `_load_all`
    trims with ``df["timestamp"] <= self._inclusive_end(self.end_date)``, and
    `BaseFetcher._inclusive_end` applies this same midnight rule, i.e. `end_date`
    is an inclusive DAY. (Until 2026-07-28 that trim read
    ``< self.end_date + timedelta(days=1)``, which widened EVERY end by a day
    rather than only midnight ones — an end of 23:00 admitted the next day's
    bars. `_inclusive_end` differs by a millisecond where this differs by a
    microsecond; both are far below any bar resolution in use.) Callers pass
    dates — ``'2026-07-26'`` parses to midnight — so reading the bound literally
    would return an empty final day while reporting success, which is the
    `FetchGapError` failure shape. Intra-day bounds (which
    `_identify_missing_periods` also produces, at millisecond offsets) are left
    exactly as given.
    """
    if when.time() == datetime.time.min:
        return when + datetime.timedelta(days=1) - datetime.timedelta(microseconds=1)
    return when


class ReservedDataError(RuntimeError):
    """
    Raised when a consumer asks for a window of the forward capture that no
    committed designation has released.

    Sibling of `journal.CoverageGapError` and `base_fetcher.FetchGapError`: the
    refusal is loud and total. A reserved dataset that can be read by anyone who
    imports the right class is not reserved.
    """


def assert_designated(
    start: datetime.datetime,
    end: datetime.datetime,
    policy_path: Path = POLICY_PATH,
) -> None:
    """
    Raise :class:`ReservedDataError` unless the policy releases [start, end].

    A designation is an entry under ``kraken_ws_forward_recorder.designations``
    of the form ``{start: YYYY-MM-DD, end: YYYY-MM-DD, ratified: YYYY-MM-DD}``,
    and it must COVER the requested window — a partial overlap releases nothing,
    because the un-designated remainder would be read alongside it.

    Fails CLOSED at every step: a missing policy file, an unparseable one, a
    missing entry and an absent `designations` key all deny. A gate that cannot
    prove a release is not a gate.
    """
    import yaml

    if not Path(policy_path).exists():
        raise ReservedDataError(
            f"data policy not found at {policy_path}; cannot prove any window of the "
            "forward capture has been designated. Denying."
        )
    try:
        with open(policy_path, "r", encoding="utf-8") as fh:
            policy = yaml.safe_load(fh) or {}
    except yaml.YAMLError as exc:
        raise ReservedDataError(f"{policy_path} did not parse: {exc}. Denying.") from exc

    entry = policy.get(POLICY_KEY)
    if not isinstance(entry, dict):
        raise ReservedDataError(
            f"{policy_path} has no '{POLICY_KEY}' entry. Denying."
        )

    designations = entry.get("designations") or []
    req_start = pd.Timestamp(start).normalize()
    req_end = pd.Timestamp(end).normalize()
    for d in designations:
        if not isinstance(d, dict) or "start" not in d or "end" not in d:
            continue
        if pd.Timestamp(d["start"]) <= req_start and req_end <= pd.Timestamp(d["end"]):
            logger.info(
                "WhaleFootprintFetcher: window %s..%s released by designation "
                "%s..%s (ratified %s)",
                req_start.date(), req_end.date(), d["start"], d["end"],
                d.get("ratified", "?"),
            )
            return

    raise ReservedDataError(
        f"{POLICY_KEY} is '{entry.get('status')}' and no designation covers "
        f"{req_start.date()}..{req_end.date()} "
        f"({len(designations)} designation(s) on file). The forward capture is "
        "deny-by-default: it is the only renewable source of genuinely unseen "
        "out-of-sample this campaign has, and reading an undesignated window "
        "spends that irreversibly. Release a named window by adding a ratified "
        f"entry under {POLICY_KEY}.designations in {policy_path}."
    )


class WhaleFootprintFetcher(BaseFetcher):
    """
    Whale-footprint features per symbol, at the pipeline's bar frequency.

    `symbols` are on-disk spellings matching the capture tree and the price
    caches — ``BTCUSD``, not ``BTC/USD`` and not ``BTCUSDT``.
    """

    #: A complete bar grid is emitted (see the module docstring), so no natural
    #: gaps exist and the default tolerance is the right one.
    expected_gap_tolerance: float = 1.5

    def __init__(
        self,
        start_date,
        end_date,
        symbols: Optional[Sequence[str]] = None,
        localStorage: bool = False,
        data_dir: str = "data",
        capture_root: Optional[Path] = None,
        policy_path: Path = POLICY_PATH,
        bar_seconds: int = DEFAULT_BAR_SECONDS,
        large_quantile: float = DEFAULT_LARGE_QUANTILE,
        baseline_seconds: int = DEFAULT_BASELINE_SECONDS,
        min_baseline_trades: int = DEFAULT_MIN_BASELINE_TRADES,
        min_bar_trades: int = DEFAULT_MIN_BAR_TRADES,
    ):
        if symbols is None:
            symbols = ["BTCUSD"]

        super().__init__(
            start_date=start_date,
            end_date=end_date,
            symbols=list(symbols),
            interval_seconds=int(bar_seconds),
            localStorage=localStorage,
            data_dir=data_dir,
        )

        # Before anything else, and before any path is even resolved.
        assert_designated(self.start_date, self.end_date, policy_path)

        self.capture_root = (
            Path(capture_root) if capture_root else Path(data_dir) / DEFAULT_CAPTURE_SUBDIR
        )
        self.bar_seconds = int(bar_seconds)
        self.large_quantile = float(large_quantile)
        self.baseline_seconds = int(baseline_seconds)
        self.min_baseline_trades = int(min_baseline_trades)
        self.min_bar_trades = int(min_bar_trades)

    # -----------------------------------------------------------------------
    # BaseFetcher interface
    # -----------------------------------------------------------------------

    def cache_key(self, symbol: str) -> str:
        """
        e.g. ``kraken_BTCUSD_whale_1h``.

        Carries the ``kraken_`` exchange qualification of
        `ccxt_fetcher.cache_key` (ccxt_fetcher.py:120-121) and the
        ``_<feed>_<interval>`` suffix of `FundingRateFetcher`
        (funding_rate_fetcher.py:108), so the derived series sits beside
        ``kraken_BTCUSD_1h.csv`` without colliding with it.
        """
        return f"kraken_{symbol}_whale_{self._bar_label()}"

    def _bar_label(self) -> str:
        s = self.bar_seconds
        if s % 3600 == 0:
            return f"{s // 3600}h"
        if s % 60 == 0:
            return f"{s // 60}m"
        return f"{s}s"

    def _fetch_remote(
        self, symbol: str, start: datetime.datetime, end: datetime.datetime
    ) -> pd.DataFrame:
        """
        Read the recorded shards for `symbol` and aggregate them to bars.

        "Remote" is the recorded capture on disk; the method name is
        `BaseFetcher`'s. Per its contract this returns an empty DataFrame when
        there is nothing to read and does not raise — the refusal that MUST be
        loud (an undesignated window) already happened in `__init__`.

        `ShardReader.iter_trades` yields `Gap` markers inline and
        `whale_bar_features` turns them into `whale_attested = 0.0` rows, so an
        uncaptured span arrives at the strategy MARKED rather than either
        missing or silently filled.
        """
        if not self.capture_root.is_dir():
            logger.warning(
                "WhaleFootprintFetcher: no capture at %s", self.capture_root
            )
            return pd.DataFrame()

        reader = ShardReader(self.capture_root)
        if not reader.shard_paths("trades", symbol):
            logger.warning(
                "WhaleFootprintFetcher: no trade shards for %s under %s",
                symbol, self.capture_root,
            )
            return pd.DataFrame()

        window_start = _to_utc(start)
        window_end = _end_of_day_if_midnight(_to_utc(end))

        df = whale_bar_features(
            reader.iter_trades(
                symbols=[symbol], start=window_start, end=window_end, emit_gaps=True
            ),
            bar_seconds=self.bar_seconds,
            large_quantile=self.large_quantile,
            baseline_seconds=self.baseline_seconds,
            min_baseline_trades=self.min_baseline_trades,
            min_bar_trades=self.min_bar_trades,
            start=window_start,
            end=window_end,
        )
        if reader.truncations:
            logger.info(
                "WhaleFootprintFetcher: %d truncated shard tail(s) tolerated for %s",
                len(reader.truncations), symbol,
            )
        if df.empty:
            logger.warning("WhaleFootprintFetcher: no bars produced for %s", symbol)
            return pd.DataFrame()

        logger.info(
            "WhaleFootprintFetcher: %s -> %d bars (%d attested)",
            symbol, len(df), int(df["whale_attested"].sum()),
        )
        return df[["timestamp", *FEATURE_COLUMNS]]
