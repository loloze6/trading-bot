"""
Descriptive report over the whale-footprint features.
=====================================================

    python -m recorder.whale_report [--root DIR] [--bar-seconds N] ...

Prints the capture manifest, then per-pair DESCRIPTIVE statistics of the three
features: value ranges, quartiles, NaN counts, gap and attestation counts,
truncated shard tails.

WHAT THIS DELIBERATELY DOES NOT COMPUTE
---------------------------------------
No forward return. No correlation against price. No information coefficient. No
backtest. Not because they are hard, but because the capture is registered
deny-by-default (`campaign_data_policy.yaml:kraken_ws_forward_recorder`) and is
the campaign's only renewable source of genuinely unseen out-of-sample. A
predictive statistic computed at BUILD time is an ungated verdict: it cannot be
un-seen, and every later decision is conditioned on it whether or not anyone
writes it down.

The distinction this report draws is between "does the instrument produce
sane numbers" (answerable from ranges and counts alone, which is what is here)
and "does the instrument predict anything" (a separately gated task).

The report reads recorded data and is therefore itself covered by the policy's
"no stage, tool, prescreen, diagnostic or backtest" language. It exists as a
build-verification tool, run once against the ten-minute baseline capture; the
gate that keeps this data out of a BACKTEST lives on
`WhaleFootprintFetcher.__init__`, which refuses to construct for an
undesignated window.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import List, Optional, Sequence

import numpy as np
import pandas as pd

if __package__ in (None, ""):  # allow direct execution
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recorder.shard_reader import Gap, ShardReader  # type: ignore
    from recorder.whale_features import (  # type: ignore
        DEFAULT_BAR_SECONDS,
        DEFAULT_BASELINE_SECONDS,
        DEFAULT_LARGE_QUANTILE,
        DEFAULT_MIN_BAR_TRADES,
        DEFAULT_MIN_BASELINE_TRADES,
        whale_bar_features,
    )
else:
    from .shard_reader import Gap, ShardReader
    from .whale_features import (
        DEFAULT_BAR_SECONDS,
        DEFAULT_BASELINE_SECONDS,
        DEFAULT_LARGE_QUANTILE,
        DEFAULT_MIN_BAR_TRADES,
        DEFAULT_MIN_BASELINE_TRADES,
        whale_bar_features,
    )

DEFAULT_ROOT = (
    Path(__file__).resolve().parents[3]
    / "trading-bot"
    / "local_data"
    / "recorded_reserved"
    / "kraken_ws_v2"
)


def _fmt(x: float, nd: int = 4) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "-"
    return f"{x:.{nd}f}"


def report(
    root: Path,
    symbols: Optional[Sequence[str]] = None,
    bar_seconds: int = DEFAULT_BAR_SECONDS,
    large_quantile: float = DEFAULT_LARGE_QUANTILE,
    baseline_seconds: int = DEFAULT_BASELINE_SECONDS,
    min_baseline_trades: int = DEFAULT_MIN_BASELINE_TRADES,
    min_bar_trades: int = DEFAULT_MIN_BAR_TRADES,
) -> str:
    reader = ShardReader(root)
    man = reader.manifest()
    out: List[str] = ["=" * 78, "MANIFEST", "=" * 78, man.render(), ""]

    extent = reader.journal_extent()
    if extent is None:
        return "\n".join(out + ["journal is empty; nothing to report"])
    out += [
        f"journal extent  {extent[0].isoformat()} .. {extent[1].isoformat()}",
        f"                {(extent[1] - extent[0]).total_seconds():.1f} s",
        "",
        "=" * 78,
        "PARAMETERS",
        "=" * 78,
        f"bar_seconds={bar_seconds}  large_quantile={large_quantile}  "
        f"baseline_seconds={baseline_seconds}",
        f"min_baseline_trades={min_baseline_trades}  min_bar_trades={min_bar_trades}",
        "",
        "=" * 78,
        "PER-PAIR DESCRIPTIVE OUTPUT  (no forward return, no correlation, no IC)",
        "=" * 78,
    ]

    syms = list(symbols) if symbols else man.streams.get("trades", [])
    header = (
        f"{'pair':<9}{'bars':>5}{'att':>5}{'gap':>4}{'trades':>8}"
        f"{'notional_usd':>14}{'LTI n':>7}{'LTI min':>9}{'LTI max':>9}"
        f"{'CVD min':>13}{'CVD max':>13}{'shift n':>9}{'shift min':>11}{'shift max':>11}"
    )
    out += [header, "-" * len(header)]

    totals = {"bars": 0, "attested": 0, "trades": 0, "notional": 0.0}
    for sym in syms:
        stream = list(reader.iter_trades(symbols=[sym], emit_gaps=True))
        gaps = [x for x in stream if isinstance(x, Gap)]
        trades = [x for x in stream if not isinstance(x, Gap)]
        df = whale_bar_features(
            stream,
            bar_seconds=bar_seconds,
            large_quantile=large_quantile,
            baseline_seconds=baseline_seconds,
            min_baseline_trades=min_baseline_trades,
            min_bar_trades=min_bar_trades,
        )
        if df.empty:
            out.append(f"{sym:<9}{'(no bars)':>20}")
            continue

        lti = df["whale_lt_imbalance"].dropna()
        cvd = df["whale_cvd_delta"].dropna()
        shift = df["whale_size_shift"].dropna()
        notional = float(sum(t.notional for t in trades))
        totals["bars"] += len(df)
        totals["attested"] += int(df["whale_attested"].sum())
        totals["trades"] += len(trades)
        totals["notional"] += notional

        out.append(
            f"{sym:<9}{len(df):>5}{int(df['whale_attested'].sum()):>5}{len(gaps):>4}"
            f"{len(trades):>8}{notional:>14,.0f}"
            f"{len(lti):>7}{_fmt(lti.min() if len(lti) else math.nan, 3):>9}"
            f"{_fmt(lti.max() if len(lti) else math.nan, 3):>9}"
            f"{(f'{cvd.min():,.0f}' if len(cvd) else '-'):>13}"
            f"{(f'{cvd.max():,.0f}' if len(cvd) else '-'):>13}"
            f"{len(shift):>9}{_fmt(shift.min() if len(shift) else math.nan, 3):>11}"
            f"{_fmt(shift.max() if len(shift) else math.nan, 3):>11}"
        )

    out += [
        "-" * len(header),
        f"{'TOTAL':<9}{totals['bars']:>5}{totals['attested']:>5}{'':>4}"
        f"{totals['trades']:>8}{totals['notional']:>14,.0f}",
        "",
        f"truncated shard tails tolerated: {len(reader.truncations)}",
    ]
    for p, n in sorted(reader.truncations.items()):
        out.append(f"  {p.relative_to(root)}  line {n}")
    out += [
        "",
        "att = bars the coverage journal attests IN FULL. gap = inline Gap markers.",
        "LTI n / shift n = bars with a non-NaN value; the rest are unscored, not zero.",
    ]
    return "\n".join(out)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    ap.add_argument("--symbols", nargs="*", default=None)
    ap.add_argument("--bar-seconds", type=int, default=DEFAULT_BAR_SECONDS)
    ap.add_argument("--large-quantile", type=float, default=DEFAULT_LARGE_QUANTILE)
    ap.add_argument("--baseline-seconds", type=int, default=DEFAULT_BASELINE_SECONDS)
    ap.add_argument(
        "--min-baseline-trades", type=int, default=DEFAULT_MIN_BASELINE_TRADES
    )
    ap.add_argument("--min-bar-trades", type=int, default=DEFAULT_MIN_BAR_TRADES)
    args = ap.parse_args(argv)

    print(
        report(
            root=args.root,
            symbols=args.symbols,
            bar_seconds=args.bar_seconds,
            large_quantile=args.large_quantile,
            baseline_seconds=args.baseline_seconds,
            min_baseline_trades=args.min_baseline_trades,
            min_bar_trades=args.min_bar_trades,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
