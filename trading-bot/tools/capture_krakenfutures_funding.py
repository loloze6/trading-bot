"""
Kraken Futures funding-rate capture
===================================
Standalone operator tool: captures perpetual-futures funding rates from the
`krakenfutures` ccxt exchange into a local cache slot, reusing the existing
`FundingRateFetcher` fetch/merge/gap-guard plumbing verbatim. Nothing in the
engine imports this file — it is a manual-invocation script in the mold of
`tools/ingest_kraken_archive.py`.

Why a dedicated venue and cadence
---------------------------------
Funding lives on the `krakenfutures` exchange, NOT spot `kraken` (which has no
funding capability at all). Kraken Futures settles HOURLY today, so the
parametrized `FundingRateFetcher(exchange_id="krakenfutures")` resolves
interval_seconds=3600 and the cache slot `krakenfutures_BTCUSD_funding_1h.csv`
— venue-honest and cadence-honest, distinct from Binance's 8h default.

Rolling-window hazard (why capture is time-critical)
----------------------------------------------------
The public endpoint serves a rolling ~366-day window and ignores `since`
server-side; ccxt filters client-side. History before the window is
unobtainable via the API, and the window slides forward daily — every day of
delay permanently loses a day of history. This tool banks whatever the window
currently serves; run it periodically to keep the cache growing forward.

Append, never overwrite
-----------------------
Capture goes through `FundingRateFetcher.get_data()`, which loads the existing
cache, identifies only the missing periods, fetches those, and merges via
`BaseFetcher._merge_and_store` under the `_assert_no_new_gap` continuity guard.
A second run therefore UNIONS new settlements into the existing cache rather
than replacing it — the merge path is reused, not reimplemented.

Holdout discipline
------------------
The rolling window reaches "now", so the captured cache WILL contain rows past
2025-12-31 — exactly as the existing Binance funding cache already does. The
cache filename is gitignored (never committed) and this tool never writes under
`holdout_sealed/`. The seal is enforced at the experiment-window level, not by
truncating live caches. No date literal appears in this file; the window is
computed at runtime.

Run:
    python trading-bot/tools/capture_krakenfutures_funding.py
    python trading-bot/tools/capture_krakenfutures_funding.py --symbol BTCUSD --lookback-days 400
"""

import argparse
import contextlib
import datetime
import sys
from pathlib import Path
from typing import cast

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # tools/ -> trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.funding_rate_fetcher import FundingRateFetcher  # noqa: E402

# CUL-213: the emoji status prints in this module crash on a Windows cp1252
# console (UnicodeEncodeError) the moment stdout is redirected/piped/captured
# (e.g. run as a captured subprocess). Degrade unencodable glyphs to '?' rather
# than raising — same fix as setup_run.py (CUL-12). getattr because typeshed
# types sys.stdout as TextIO (no reconfigure); contextlib.suppress because a
# captured stream may reject it (OSError) — never crash a context the raw prints
# already survived.
_reconfigure = getattr(sys.stdout, "reconfigure", None)
if _reconfigure is not None:
    with contextlib.suppress(OSError):
        _reconfigure(errors="replace")

# Kraken Futures is the funding venue; the fetcher maps it to a 3600s cadence and
# hence the `krakenfutures_<symbol>_funding_1h` cache slot.
EXCHANGE_ID = "krakenfutures"
DEFAULT_SYMBOL = "BTCUSD"
# The public window is ~366 days; ask for a little more so the whole of it is
# requested. A start earlier than the window's first served row is harmless —
# the endpoint simply returns what it has, and the first capture into an empty
# slot has no continuity to break.
DEFAULT_LOOKBACK_DAYS = 400


def build_fetcher(symbol: str, start, end, data_dir: str,
                  exchange_id: str = EXCHANGE_ID) -> FundingRateFetcher:
    """Construct the parametrized fetcher for the funding venue.

    localStorage=True so the fetch loads the existing cache, merges, and writes
    back through the gap-guarded `_merge_and_store` path.
    """
    return FundingRateFetcher(
        start_date=start,
        end_date=end,
        symbols=[symbol],
        exchange_id=exchange_id,
        localStorage=True,
        data_dir=data_dir,
    )


def capture(fetcher: FundingRateFetcher, symbol: str) -> dict:
    """Run the capture for one symbol and return a summary of the merged cache.

    Delegates the whole load -> identify-missing -> fetch -> merge -> gap-guard
    cycle to `FundingRateFetcher.get_data()`. The returned frame is the merged
    cache (existing rows unioned with newly fetched settlements), so a repeat
    call appends rather than overwrites.
    """
    # get_data(symbol) returns the symbol's DataFrame; cast narrows the
    # DataFrame | dict union its unannotated signature otherwise infers.
    data = cast(pd.DataFrame, fetcher.get_data(symbol))
    ts = data["timestamp"]
    summary = {
        "symbol": symbol,
        "exchange_id": fetcher.exchange_id,
        "interval_seconds": fetcher.interval_seconds,
        "cache_key": fetcher.cache_key(symbol),
        "dest": fetcher._csv_path(symbol),
        "rows": len(data),
        "first": None if data.empty else ts.iloc[0],
        "last": None if data.empty else ts.iloc[-1],
    }
    return summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Capture Kraken Futures funding rates into a local cache "
                    "slot (append/merge, gap-guarded). Manual invocation only."
    )
    parser.add_argument(
        "--symbol", default=DEFAULT_SYMBOL,
        help=f"Store symbol (default {DEFAULT_SYMBOL}); resolves the perp market "
             f"on {EXCHANGE_ID} and the cache slot krakenfutures_<symbol>_funding_1h.",
    )
    parser.add_argument(
        "--lookback-days", type=int, default=DEFAULT_LOOKBACK_DAYS,
        help=f"Days of history to request back from now (default "
             f"{DEFAULT_LOOKBACK_DAYS}); the endpoint serves at most its "
             f"~366-day rolling window regardless.",
    )
    parser.add_argument(
        "--data-dir", default=str(PROJECT_ROOT / "local_data"),
        help="Cache directory (default trading-bot/local_data).",
    )
    args = parser.parse_args(argv)

    # Naive-UTC window, matching the cache convention. Computed at runtime so no
    # date literal ever appears in this file (the seal scanner reads it).
    end = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
    start = end - datetime.timedelta(days=args.lookback_days)

    fetcher = build_fetcher(args.symbol, start, end, args.data_dir)
    if fetcher.exchange is None:
        print(f"[FAIL] {EXCHANGE_ID} exchange not initialised (ccxt missing or "
              f"init error) — nothing captured.", file=sys.stderr)
        return 1

    summary = capture(fetcher, args.symbol)
    if summary["rows"] == 0:
        print(f"[WARN] no funding rows captured for {args.symbol} on "
              f"{EXCHANGE_ID} — cache unchanged.", file=sys.stderr)
        return 1

    print(f"[OK] {summary['cache_key']}  rows={summary['rows']}  "
          f"{summary['first']} -> {summary['last']}")
    print(f"     dest: {summary['dest']} (gitignored; holdout-carrying)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
