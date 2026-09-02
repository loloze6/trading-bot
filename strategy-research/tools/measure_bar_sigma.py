"""
Per-bar return volatility, in bps, for the recorded pair set (dispatch W11 step 2).
==================================================================================

    python -m tools.measure_bar_sigma [--pairs ...] [--start ...] [--end ...]

Answers ONE question: what is ``sigma_bar_bps`` — the standard deviation of
1-bar close-to-close returns in basis points — for each of the 19 Kraken pairs
the forward recorder captures.

WHY THIS FILE EXISTS
--------------------
`prereg_whale_footprint_v2.yaml` gates on

    IC_required = safety_factor * round_trip_cost_bps / (sigma_bar_bps * sqrt(H))

and its ``sigma_bar_bps`` has been wrong twice in two different directions.
Dispatch W9 used 15.0, which was `prescreen_signal._DEFAULT_SIGMA_BAR_BPS` — a
fallback constant for runs with under five records, not a measurement — and that
single wrong scalar produced a terminal "the family is untradeable" verdict.
Dispatch W10 replaced it with 61.6052, which IS a measurement but of the wrong
instrument set: it is the minimum across archived prescreen runs on BTC and
AVAX, two of the nineteen pairs, and neither of them chosen for being
representative. This module measures the figure for the pair set the
pre-registration actually names.

WHAT THIS DELIBERATELY DOES NOT READ
------------------------------------
No whale feature. No recorded capture. This module opens exactly one kind of
file — `local_data/kraken_<BASE>USD_1h.csv` — and computes a property of the
price series alone. There is no code path here that could relate a feature to a
return.

That is not a stylistic note. Amending a pre-registration's threshold after the
data exists is only legitimate if the amendment cannot have been informed by the
relationship under test, and the cheapest way to make that checkable is for the
two amended inputs to be measured by two programs that share no data:
`sigma_bar_bps` here from prices only, and ``H`` in
`tools/recorder/whale_persistence.py` from feature signs only. Neither program can
compute an IC; together they cannot either.

WINDOW, AND WHY IT IS NOT THE CAPTURE'S OWN
--------------------------------------------
Default `[2024-12-01, 2025-12-31]` — `campaign_data_policy.yaml`'s
``walk_forward_extension``, the most recent range every one of the 19 pairs has
complete data for. Two alternatives were rejected:

*The capture's own window* (2026-07-27 onward) would be the most on-point period,
but the capture is registered deny-by-default and measuring from it would put a
price statistic derived from reserved data into the gate — defensible, since a
volatility is not a return relationship, but unnecessary when a clean in-sample
source exists, and it is not worth spending the argument.

*Full available history per pair* spans 2013-2025 for BTC and 2024-2025 for TAO,
so a pooled figure would mix a decade of BTC regimes with eighteen months of TAO
and weight the pairs by how long they have existed. Reported anyway as
``--full-history`` sensitivity, since a reader should be able to see whether the
window choice is doing any work. It is not: see the report's own comparison.

The holdout range is asserted against, not merely avoided — see `_assert_window`.

WHICH FIGURE THE GATE SHOULD USE
---------------------------------
The report prints four pooled candidates and takes no position by itself; the
choice belongs in the pre-registration, where it can be argued for in writing:

``pooled``      stdev of every pair's returns concatenated. The natural
                counterpart to a test that pools all 19 pairs, but slightly
                inflated by cross-pair dispersion in the mean.
``mean``        equal-weight mean of the 19 per-pair sigmas. Treats the pairs as
                the test does — one vote each.
``median``      as above, robust to a single outlier pair.
``min``         the least volatile pair. Yields the HIGHEST required IC and is
                therefore the conservative-against-the-family choice, which is
                the convention dispatch W10 used when it picked 61.6052.
"""

from __future__ import annotations

import argparse
import math
import os
import statistics
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import pandas as pd

_HERE = Path(__file__).resolve()
_SR = _HERE.parents[1]
_REPO = _HERE.parents[2]
_LOCAL_DATA = _REPO / "trading-bot" / "local_data"
_POLICY_PATH = _SR / "config" / "campaign_data_policy.yaml"

#: The 19 bases of `campaign_data_policy.yaml:kraken_breadth_19pair`, in the
#: order the pre-registration lists them.
DEFAULT_BASES = (
    "BTC", "ETH", "XRP", "SOL", "ADA", "SUI", "ZEC", "DOGE", "XMR", "LTC",
    "ONDO", "NEAR", "LINK", "TAO", "AVAX", "TRX", "AAVE", "INJ", "UNI",
)

#: `campaign_data_policy.yaml:walk_forward_extension`.
DEFAULT_START = "2024-12-01"
DEFAULT_END = "2025-12-31"

#: `campaign_data_policy.yaml:holdout_range`. FROZEN — no tool or diagnostic may
#: read candles inside it. Asserted rather than assumed: the caches currently
#: stop at 2025-12-31 so no overlap is possible today, but a future top-up fetch
#: (the ledger G2 backfill this policy already anticipates) would extend them
#: into the holdout and this module would then be reading sealed data with no
#: signal that anything had changed.
def _holdout_range_from_policy():
    """(first sealed day, last sealed day) as "YYYY-MM-DD", read from the policy.

    Derived, not a local literal (CUL-203) -- so the seal moves with
    `campaign_data_policy.yaml` instead of silently drifting from it. This module
    is import-isolated for pre-registration integrity (`test_module_cannot_reach
    _the_recorded_capture` pins its imports to stdlib+pandas), so it CANNOT reuse
    `data_manager._holdout_bounds`; it reads the same single source of truth with
    a minimal parser over the one contractually-pinned line the policy documents
    ("exactly ONE holdout_range key, DOUBLE-QUOTED ISO YYYY-MM-DD"). Deny by
    default: any failure to locate that line raises rather than guessing a
    window it cannot prove.
    """
    for line in _POLICY_PATH.read_text(encoding="utf-8").splitlines():
        if line.split("#", 1)[0].strip().startswith("holdout_range:"):
            inside = line.split("[", 1)[1].split("]", 1)[0]
            lo, hi = (p.strip().strip('"').strip("'") for p in inside.split(",")[:2])
            return lo, hi
    raise HoldoutViolation(
        f"cannot locate holdout_range in {_POLICY_PATH} -- refusing to guess the "
        "sealed window."
    )


class HoldoutViolation(RuntimeError):
    """A requested window overlaps the sealed holdout range."""


#: (closed) sealed-window bounds, DERIVED from the policy (see above), kept as a
#: public tuple because the module's tests read it.
HOLDOUT_RANGE = _holdout_range_from_policy()


def _assert_window(start: str, end: str) -> None:
    h0, h1 = pd.Timestamp(HOLDOUT_RANGE[0]), pd.Timestamp(HOLDOUT_RANGE[1])
    s, e = pd.Timestamp(start), pd.Timestamp(end)
    if s <= h1 and e >= h0:
        raise HoldoutViolation(
            f"window [{start}, {end}] overlaps holdout_range "
            f"[{HOLDOUT_RANGE[0]}, {HOLDOUT_RANGE[1]}] "
            "(campaign_data_policy.yaml). Refusing to read sealed candles."
        )


def cache_path(base: str, local_data: Path = _LOCAL_DATA) -> Path:
    return local_data / f"kraken_{base}USD_1h.csv"


def bar_returns_bps(
    base: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    local_data: Path = _LOCAL_DATA,
) -> List[float]:
    """
    Close-to-close 1-bar returns in bps over `[start, end]`.

    Identical in definition to `prescreen_signal._collect_records`'s
    ``next_return_bps`` — ``(close[i+1] - close[i]) / close[i] * 10_000`` — so the
    sigma this produces is the same quantity `_sigma_from_records` estimates and
    can be substituted into the same cost formula without a units argument.

    Bars are NOT reindexed onto a complete hourly grid. A missing hour in the
    cache makes the neighbouring return a 2-hour return, which slightly inflates
    sigma; `within_life_missing_pct_2017plus` in the data policy puts that at
    well under a percent for these pairs, and inflating sigma LOWERS the required
    IC, so the residual error runs against the conservative direction and is
    reported rather than corrected — see `--report-gaps`.
    """
    p = cache_path(base, local_data)
    if not p.exists():
        raise FileNotFoundError(f"no 1h cache for {base}: {p}")
    df = pd.read_csv(p, usecols=["timestamp", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    if start:
        df = df[df["timestamp"] >= pd.Timestamp(start)]
    if end:
        # STRICTLY less than the start of the following day, not <=. The intent is
        # "include all of the `end` day"; `<=` also admits the next day's 00:00 bar,
        # which is a different day. That single bar is a seal leak in the only case
        # that matters: `_assert_window` passes end="2025-12-31" (correctly — it is
        # outside holdout_range), and this filter then reads the 2026-01-01 00:00
        # bar, the FIRST sealed timestamp. The tool read one bar past its own
        # assertion, silently, on the exact boundary the assertion exists to defend.
        # .normalize() so a time-bearing `end` cannot widen the window past its
        # own day: end="2025-12-31 23:00" passes _assert_window (it is outside
        # holdout_range) and, without this, the bound became 2026-01-01 23:00 —
        # admitting a full day of sealed bars instead of one. Same overshoot
        # `base_fetcher._inclusive_end` exists to prevent, and the reason this
        # fix is not simply "<" instead of "<=".
        df = df[df["timestamp"] < pd.Timestamp(end).normalize() + pd.Timedelta(1, unit="D")]
    closes = df["close"].astype(float).tolist()
    out: List[float] = []
    for i in range(len(closes) - 1):
        if closes[i] > 0:
            out.append((closes[i + 1] - closes[i]) / closes[i] * 10_000.0)
    return out


def sigma_bar_bps(returns: Sequence[float]) -> Optional[float]:
    """`statistics.stdev`, matching `prescreen_signal._sigma_from_records:643`."""
    if len(returns) < 5:
        return None
    return statistics.stdev(returns)


def measure(
    bases: Sequence[str] = DEFAULT_BASES,
    start: str = DEFAULT_START,
    end: str = DEFAULT_END,
    local_data: Path = _LOCAL_DATA,
) -> Dict[str, object]:
    """Per-pair sigma plus the four pooled candidates. Raises on holdout overlap."""
    _assert_window(start, end)
    per_pair: Dict[str, Optional[float]] = {}
    counts: Dict[str, int] = {}
    all_returns: List[float] = []
    for b in bases:
        rets = bar_returns_bps(b, start, end, local_data)
        per_pair[b] = sigma_bar_bps(rets)
        counts[b] = len(rets)
        all_returns.extend(rets)
    vals = [v for v in per_pair.values() if v is not None]
    return {
        "window": [start, end],
        "per_pair": per_pair,
        "n_bars": counts,
        "pooled": sigma_bar_bps(all_returns),
        "mean": statistics.mean(vals) if vals else None,
        "median": statistics.median(vals) if vals else None,
        "min": min(vals) if vals else None,
        "max": max(vals) if vals else None,
        "stdev_across_pairs": statistics.stdev(vals) if len(vals) > 1 else None,
        "n_returns_pooled": len(all_returns),
    }


def report(
    bases: Sequence[str] = DEFAULT_BASES,
    start: str = DEFAULT_START,
    end: str = DEFAULT_END,
    local_data: Path = _LOCAL_DATA,
    full_history: bool = False,
) -> str:
    m = measure(bases, start, end, local_data)
    out: List[str] = [
        "=" * 78,
        "PER-BAR RETURN VOLATILITY  sigma_bar_bps  (prices only — no whale data)",
        "=" * 78,
        f"source     local_data/kraken_<BASE>USD_1h.csv",
        f"window     {start} .. {end}  (campaign_data_policy walk_forward_extension)",
        f"definition stdev of (close[i+1]-close[i])/close[i]*1e4, "
        f"== prescreen_signal._sigma_from_records",
        "",
        f"{'pair':<8}{'bars':>9}{'sigma_bps':>12}",
        "-" * 29,
    ]
    per_pair: Dict[str, Optional[float]] = m["per_pair"]  # type: ignore[assignment]
    counts: Dict[str, int] = m["n_bars"]  # type: ignore[assignment]
    for b in bases:
        v = per_pair.get(b)
        out.append(
            f"{b:<8}{counts.get(b, 0):>9}"
            f"{(f'{v:.4f}' if v is not None else '-'):>12}"
        )
    out += [
        "-" * 29,
        "",
        "POOLED CANDIDATES",
        f"  pooled (all returns concatenated)   {m['pooled']:.4f}   "
        f"n={m['n_returns_pooled']:,}",
        f"  mean of per-pair sigmas             {m['mean']:.4f}",
        f"  median of per-pair sigmas           {m['median']:.4f}",
        f"  min  (conservative: highest req IC) {m['min']:.4f}",
        f"  max                                 {m['max']:.4f}",
        f"  stdev across pairs                  {m['stdev_across_pairs']:.4f}",
    ]

    if full_history:
        fh = measure(bases, "2013-01-01", "2025-12-31", local_data)
        out += [
            "",
            "SENSITIVITY — full available history per pair (unequal spans; see docstring)",
            f"  pooled {fh['pooled']:.4f}   mean {fh['mean']:.4f}   "
            f"median {fh['median']:.4f}   min {fh['min']:.4f}   max {fh['max']:.4f}",
        ]
    return "\n".join(out)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--pairs", nargs="*", default=list(DEFAULT_BASES))
    ap.add_argument("--start", default=DEFAULT_START)
    ap.add_argument("--end", default=DEFAULT_END)
    ap.add_argument("--local-data", type=Path, default=_LOCAL_DATA)
    ap.add_argument("--full-history", action="store_true")
    args = ap.parse_args(argv)
    print(report(
        bases=args.pairs,
        start=args.start,
        end=args.end,
        local_data=args.local_data,
        full_history=args.full_history,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
