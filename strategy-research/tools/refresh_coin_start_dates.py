"""
refresh_coin_start_dates.py — E-054 Layer 1 follow-up (fix/layer1-per-coin-start-dates).

PROBLEM this closes: layer1_price_precheck (data_availability_gate.py) has a
per-coin `earliest_ohlcv_utc` gate for Binance symbols, but for Kraken it only
had a venue-WIDE 2013-09-01 floor (`earliest_possible_utc`) plus
`confirmed_universe` membership -- no per-coin date. A confirmed Kraken coin
whose local cache genuinely starts years later (e.g. kraken_SUIUSD_1h.csv:
2023-05-03) looked available all the way back to 2013 at Layer 1, deferring
the decline to a real, network/disk-bound Layer 2 fetch that could have been
avoided for free.

WHAT THIS TOOL DOES: reads ONLY the header and first data row of each local
1h cache file (`trading-bot/local_data/<cache_key>.csv`) for every coin
declared in `strategy-research/config/coin_universe.yaml`, and writes a
per-coin `earliest_ohlcv_utc` entry into `venue_data_capability.yaml`'s
`venues.kraken.spot.symbols` block, in the same shape (key name, per-symbol
ISO-date-at-T00:00:00Z value) Binance's existing entries already use.

Why 1h specifically: it is the finest timeframe any protocol in this
workflow actually requests (coin_universe.yaml's own `default_timeframe: 1h`,
and every Kraken coin_universe.yaml entry pins `cache_key: kraken_<SYM>_1h`
explicitly) -- a coarser cache could start later than the finer one due to a
partial/aggregated ingestion, so 1h is the tightest true bound available on
disk.

Binance coins are READ-ONLY here: venue_data_capability.yaml's existing five
Binance dates (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/AVAXUSDT) come from a live,
read-only probe of Binance's own REST API (a stronger source than a local
cache's observed first row, which merely reflects what THIS codebase happened
to fetch/ingest). This tool never overwrites or adds a Binance
earliest_ohlcv_utc entry; a Binance coin with a local file but no existing
entry is reported (see the `no_file`-shaped report list) for a human to
decide, never written automatically.

SAFETY (per this tool's own task brief):
  - Reads ONLY the CSV header row plus the first data row of each cache file
    -- never the rest of the file, however large. See `first_row_date()`.
  - Never reads anything under `local_data/holdout_sealed/` (this tool never
    constructs a path under that directory at all -- every path it touches is
    `<local_data_dir>/<cache_key>.csv`, a flat, non-recursive lookup against
    cache_key strings drawn from coin_universe.yaml, which never names that
    directory).
  - Refuses to write any date on or after the policy's `holdout_range` start
    (`campaign_data_policy.yaml`, loaded fresh every run, never hardcoded
    here) -- such a coin is reported under `refused`, and no write happens
    for it. This also means `trading-bot/tests/test_no_sealed_date_literals.py`
    can never regress via this tool: the date this tool would refuse to write
    never becomes a string literal in venue_data_capability.yaml *or* in this
    module's own source (it is always a value loaded from disk at runtime,
    never typed into a docstring/comment as a bare literal).
  - Never round-trips venue_data_capability.yaml through a full YAML
    load+dump: that file is a heavily hand-authored, comment-carrying
    reference document, and `yaml.safe_dump` would silently destroy every
    `#`-comment in it. Instead this tool does a targeted text splice, bounded
    by a pair of sentinel marker comments, so a second run replaces exactly
    its own previously-written block and touches nothing else in the file
    (see `_splice_generated_block`).

A coin with no local cache file at all gets no date and keeps today's
behaviour (its existing Layer 1 gates -- confirmed_universe /
earliest_possible_utc / earliest_ohlcv_utc-when-present -- are unchanged).
"""
from __future__ import annotations

import argparse
import csv
import datetime
import os
from typing import NamedTuple, Optional

import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))          # strategy-research/tools/
_SR = os.path.dirname(_HERE)                                  # strategy-research/
_REPO = os.path.dirname(_SR)                                   # repo root
_TBOT = os.path.join(_REPO, "trading-bot")

_DEFAULT_COIN_UNIVERSE_PATH = os.path.join(_SR, "config", "coin_universe.yaml")
_DEFAULT_VENUE_CAPABILITY_PATH = os.path.join(_SR, "config", "venue_data_capability.yaml")
_DEFAULT_POLICY_PATH = os.path.join(_SR, "config", "campaign_data_policy.yaml")
_DEFAULT_LOCAL_DATA_DIR = os.path.join(_TBOT, "local_data")

TIMEFRAME = "1h"  # the finest timeframe the protocols use -- see module docstring

_BEGIN_MARKER = "        # BEGIN GENERATED: refresh_coin_start_dates.py (kraken earliest_ohlcv_utc)"
_END_MARKER = "        # END GENERATED: refresh_coin_start_dates.py"

# Unique two-line anchor identifying the Kraken (not Binance) `symbols:`
# block's `pattern:` key -- both venues declare a `pattern:` key under
# `symbols:`, so matching on this key alone would be ambiguous. The new
# block is inserted immediately before this anchor on a first run.
_KRAKEN_PATTERN_ANCHOR = (
    "        pattern: >\n"
    "          19-pair breadth universe currently declared in\n"
)


class CoinEntry(NamedTuple):
    symbol: str          # coin_universe.yaml's own `symbol` field, e.g. "SUIUSDT"
    exchange: str
    cache_key: str        # e.g. "kraken_SUIUSD_1h" or "DOTUSDT_1h"


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def holdout_start(policy_path: Optional[str] = None) -> datetime.date:
    policy = load_yaml(policy_path or _DEFAULT_POLICY_PATH)
    lo_str, _hi_str = policy["holdout_range"]
    return datetime.date.fromisoformat(lo_str)


def iter_coin_universe_entries(coin_universe: dict) -> list:
    """
    Every coin declared under `categories.*.coins`, with exchange/cache_key
    resolved exactly the way the rest of the pipeline resolves them:
    coin_universe.yaml's own `default_exchange`/`default_timeframe` are the
    fallback, an explicit per-coin `exchange:`/`cache_key:` always wins, and
    the derived cache_key for a Binance-default coin mirrors
    CcxtFetcher.cache_key()'s own empty-prefix-for-binance rule
    (ccxt_fetcher.py:101-124): "" prefix for binance, "{exchange}_" otherwise.
    """
    default_exchange = coin_universe.get("default_exchange", "binance")
    default_timeframe = coin_universe.get("default_timeframe", "1h")
    entries = []
    for category in (coin_universe.get("categories") or {}).values():
        for coin in category.get("coins") or []:
            symbol = coin["symbol"]
            exchange = coin.get("exchange", default_exchange)
            cache_key = coin.get("cache_key")
            if cache_key is None:
                prefix = "" if exchange == "binance" else f"{exchange}_"
                cache_key = f"{prefix}{symbol}_{default_timeframe}"
            entries.append(CoinEntry(symbol=symbol, exchange=exchange, cache_key=cache_key))
    return entries


def kraken_symbol_from_cache_key(cache_key: str) -> Optional[str]:
    """'kraken_SOLUSD_1h' -> 'SOLUSD'. None if not kraken-shaped or malformed."""
    if not cache_key.startswith("kraken_"):
        return None
    rest = cache_key[len("kraken_"):]
    base, sep, _timeframe = rest.rpartition("_")
    return base if sep and base else None


def first_row_date(csv_path: str) -> Optional[str]:
    """
    Read ONLY the header row and the first data row of `csv_path` -- never
    anything past it, regardless of file size. Returns the `timestamp`
    column's date part (first 10 chars, 'YYYY-MM-DD') for the first data row,
    or None if the file doesn't exist, has no data rows, or has no
    `timestamp` column.
    """
    if not os.path.exists(csv_path):
        return None
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return None
        try:
            row = next(reader)
        except StopIteration:
            return None
    try:
        ts_index = header.index("timestamp")
    except ValueError:
        return None
    if ts_index >= len(row):
        return None
    raw = row[ts_index].strip()
    if len(raw) < 10:
        return None
    return raw[:10]


def _render_generated_block(kraken_dates: dict, generated_at: str) -> str:
    """
    Render the `earliest_ohlcv_utc` + `earliest_ohlcv_utc_basis` block, in
    the exact shape/indentation (8-space key, 10-space entries) Binance's
    existing entries already use (venue_data_capability.yaml:137-157),
    wrapped in the sentinel markers so a later run can find and replace it.
    """
    lines = [_BEGIN_MARKER, "        earliest_ohlcv_utc:"]
    for symbol in sorted(kraken_dates):
        lines.append(f'          {symbol}: "{kraken_dates[symbol]}"')
    lines.append("        earliest_ohlcv_utc_basis: >")
    lines.append(
        f"          Added {generated_at} (fix/layer1-per-coin-start-dates). Each date is"
    )
    lines.append(
        "          the first row's timestamp of the coin's OWN local"
    )
    lines.append(
        "          local_data/kraken_<SYM>_1h.csv cache (the finest timeframe any"
    )
    lines.append(
        "          protocol here requests), read by"
    )
    lines.append(
        "          strategy-research/tools/refresh_coin_start_dates.py (header + first"
    )
    lines.append(
        "          data row only, never the rest of the file). This is OUR CACHE's"
    )
    lines.append(
        "          observed start, not an independently venue-audited listing date --"
    )
    lines.append(
        "          same caveat as the `unconfirmed` note below and coin_universe.yaml's"
    )
    lines.append(
        "          own per-pair notes -- but it is real and load-bearing: it closes the"
    )
    lines.append(
        "          gap where a Kraken coin with no per-symbol gate looked available all"
    )
    lines.append(
        "          the way back to the venue-wide 2013-09-01 floor regardless of when"
    )
    lines.append(
        "          OUR data (or the coin itself) actually begins. A symbol with a local"
    )
    lines.append(
        "          kraken_<SYM>_1h.csv cache is listed here; one without a cache file is"
    )
    lines.append(
        "          NOT listed and keeps declining via only the venue-wide"
    )
    lines.append(
        "          floor/confirmed_universe gates above (see layer1_price_precheck)."
    )
    lines.append(_END_MARKER)
    return "\n".join(lines) + "\n"


def _splice_generated_block(text: str, block: str) -> str:
    """
    Replace the text between `_BEGIN_MARKER`/`_END_MARKER` with `block` if
    the markers are already present (idempotent re-run); otherwise insert
    `block` immediately before the Kraken `symbols:` block's `pattern:` key
    (see `_KRAKEN_PATTERN_ANCHOR`). Raises ValueError if neither the markers
    nor the anchor can be found -- fail loud rather than silently no-op.
    """
    if _BEGIN_MARKER in text:
        begin_idx = text.index(_BEGIN_MARKER)
        end_marker_idx = text.index(_END_MARKER, begin_idx)
        end_idx = end_marker_idx + len(_END_MARKER)
        # Consume the trailing newline after the end marker, if present, so
        # we don't accumulate a blank line on repeated runs.
        if end_idx < len(text) and text[end_idx] == "\n":
            end_idx += 1
        return text[:begin_idx] + block + text[end_idx:]

    anchor_idx = text.find(_KRAKEN_PATTERN_ANCHOR)
    if anchor_idx == -1:
        raise ValueError(
            "Could not find the Kraken symbols: block's `pattern:` anchor in "
            "venue_data_capability.yaml -- the file's structure has changed "
            "since this tool was written; refusing to guess where to insert."
        )
    return text[:anchor_idx] + block + text[anchor_idx:]


class RefreshResult(NamedTuple):
    written: dict            # kraken_symbol -> date written (YYYY-MM-DD)
    no_local_file: list       # [(symbol, exchange, cache_key), ...]
    refused_sealed: list      # [(symbol, exchange, cache_key, date), ...]
    binance_reported_not_written: list  # [(symbol, cache_key), ...]


def refresh(coin_universe_path: Optional[str] = None,
            venue_capability_path: Optional[str] = None,
            policy_path: Optional[str] = None,
            local_data_dir: Optional[str] = None,
            dry_run: bool = False,
            now: Optional[datetime.date] = None) -> RefreshResult:
    coin_universe_path = coin_universe_path or _DEFAULT_COIN_UNIVERSE_PATH
    venue_capability_path = venue_capability_path or _DEFAULT_VENUE_CAPABILITY_PATH
    local_data_dir = local_data_dir or _DEFAULT_LOCAL_DATA_DIR

    coin_universe = load_yaml(coin_universe_path)
    holdout_lo = holdout_start(policy_path)

    existing_binance_dates = load_yaml(venue_capability_path).get(
        "venues", {}).get("binance", {}).get("spot", {}).get(
        "symbols", {}).get("earliest_ohlcv_utc", {}) or {}

    written: dict = {}
    no_local_file = []
    refused_sealed = []
    binance_reported_not_written = []

    for entry in iter_coin_universe_entries(coin_universe):
        csv_path = os.path.join(local_data_dir, f"{entry.cache_key}.csv")
        date_str = first_row_date(csv_path)
        if date_str is None:
            no_local_file.append((entry.symbol, entry.exchange, entry.cache_key))
            continue

        found_date = datetime.date.fromisoformat(date_str)
        if found_date >= holdout_lo:
            refused_sealed.append((entry.symbol, entry.exchange, entry.cache_key, date_str))
            continue

        if entry.exchange == "kraken":
            kraken_symbol = kraken_symbol_from_cache_key(entry.cache_key) or entry.symbol
            written[kraken_symbol] = date_str
        elif entry.exchange == "binance":
            if entry.symbol not in existing_binance_dates:
                binance_reported_not_written.append((entry.symbol, entry.cache_key))
        else:
            no_local_file.append((entry.symbol, entry.exchange, entry.cache_key))

    if written and not dry_run:
        generated_at = (now or datetime.date.today()).isoformat()
        kraken_dates = {sym: f"{d}T00:00:00Z" for sym, d in written.items()}
        block = _render_generated_block(kraken_dates, generated_at)
        with open(venue_capability_path, "r", encoding="utf-8") as f:
            text = f.read()
        text = _splice_generated_block(text, block)
        with open(venue_capability_path, "w", encoding="utf-8") as f:
            f.write(text)

    return RefreshResult(
        written=written,
        no_local_file=no_local_file,
        refused_sealed=refused_sealed,
        binance_reported_not_written=binance_reported_not_written,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Refresh venue_data_capability.yaml's Kraken per-coin "
                     "earliest_ohlcv_utc dates from local cache files."
    )
    parser.add_argument("--dry-run", action="store_true",
                         help="Compute and report, but do not write the yaml file.")
    args = parser.parse_args()

    result = refresh(dry_run=args.dry_run)

    print(f"Written ({len(result.written)} kraken symbols):")
    for symbol, date in sorted(result.written.items()):
        print(f"  {symbol}: {date}")

    if result.binance_reported_not_written:
        print(f"\nBinance coins with a local file but no existing earliest_ohlcv_utc "
              f"entry (reported only, never written -- see module docstring):")
        for symbol, cache_key in result.binance_reported_not_written:
            print(f"  {symbol} ({cache_key})")

    if result.no_local_file:
        print(f"\nCoins with no local cache file ({len(result.no_local_file)}, unchanged behaviour):")
        for symbol, exchange, cache_key in result.no_local_file:
            print(f"  {symbol} ({exchange}, expected {cache_key}.csv)")

    if result.refused_sealed:
        print(f"\nREFUSED -- first row falls at/after the sealed holdout start "
              f"({len(result.refused_sealed)}, nothing written for these):")
        for symbol, exchange, cache_key, date in result.refused_sealed:
            print(f"  {symbol} ({exchange}, {cache_key}): {date}")

    if args.dry_run:
        print("\n[dry run] venue_data_capability.yaml was NOT modified.")


if __name__ == "__main__":
    main()
