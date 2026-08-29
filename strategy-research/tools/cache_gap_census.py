"""
Timestamp-continuity census over the local OHLCV caches.

Written for the issue #50 policy decision (docs/analysis-reports/
PRESCREEN_GAP_POLICY_20260829.md). Every number quoted in that document is
reproduced by running this file, so the policy's evidence is re-checkable
rather than asserted.

Reports, per symbol x research window:
  - gap pairs: consecutive rows whose timestamp step != the timeframe step.
    These are the pairs prescreen_signal._extract_forecasts currently scores as
    one-bar returns regardless of their true horizon.
  - the contiguous-run structure, which decides how many bootstrap blocks can
    actually be placed without a block spanning a gap.
  - nominal vs gap-aware n_eff, i.e. how much prescreen_signal.
    _block_adjusted_significance's `n_active_bars // block_size` overstates the
    achievable block count.

Read-only. Never touches the sealed holdout store: it globs an explicit
timeframe suffix inside `local_data/` and does not recurse.

Usage (from strategy-research/):
    ../.venv/bin/python tools/cache_gap_census.py
    ../.venv/bin/python tools/cache_gap_census.py --timeframe 1d --warmup 120
"""

from __future__ import annotations

import argparse
import csv
import glob
import math
import os
import statistics
from datetime import datetime, timedelta

# Research windows (CLAUDE.fork.md "Data splits"). The holdout is deliberately
# absent: it is single-use and reading it is spending it.
WINDOWS = {
    "train": (datetime(2018, 1, 1), datetime(2023, 12, 31, 23, 59, 59)),
    "valid": (datetime(2024, 1, 1), datetime(2025, 12, 31, 23, 59, 59)),
}

_STEPS = {"1h": timedelta(hours=1), "4h": timedelta(hours=4), "1d": timedelta(days=1)}

_DEFAULT_DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "trading-bot",
    "local_data",
)


def _load(path: str) -> list[tuple[datetime, float | None]]:
    """Rows as (timestamp, close), sorted. Unparseable timestamps are counted by
    the caller, never silently folded into the series."""
    rows, bad_ts = [], 0
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            raw = (r.get("timestamp") or "").strip()
            try:
                t = datetime.fromisoformat(raw)
            except ValueError:
                bad_ts += 1
                continue
            try:
                c = float(r["close"])
            except (TypeError, ValueError, KeyError):
                c = None
            rows.append((t, c))
    rows.sort(key=lambda x: x[0])
    return rows, bad_ts


def _runs(times: list[datetime], step: timedelta) -> list[int]:
    """Lengths of maximal contiguous runs (consecutive rows exactly `step` apart)."""
    if not times:
        return []
    out, cur = [], 1
    for i in range(len(times) - 1):
        if times[i + 1] - times[i] == step:
            cur += 1
        else:
            out.append(cur)
            cur = 1
    out.append(cur)
    return out


def census(rows, lo, hi, step, warmup, block):
    w = [r for r in rows if lo <= r[0] <= hi]
    times = [t for t, _ in w]
    pairs = max(len(w) - 1, 0)
    gaps = worst = 0
    gap_rets, ok_rets = [], []
    for i in range(pairs):
        delta = times[i + 1] - times[i]
        c0, c1 = w[i][1], w[i + 1][1]
        ret = abs((c1 - c0) / c0 * 10_000.0) if (c0 and c1) else None
        if delta != step:
            gaps += 1
            worst = max(worst, delta.total_seconds() / 3600.0)
            if ret is not None:
                gap_rets.append(ret)
        elif ret is not None:
            ok_rets.append(ret)

    runs = _runs(times, step)
    total = sum(runs)
    # The strategy warms up ONCE over the whole series (it is never reset), so
    # the warmup is charged against the leading run(s); each run then loses its
    # last bar, which has no in-run successor.
    rem, run_recs = warmup + 1, []
    for length in runs:
        take = min(rem, length)
        rem -= take
        run_recs.append(max(length - take - 1, 0))

    nominal = max(total - warmup - 1, 0) // block
    gap_aware = sum(r // block for r in run_recs)
    ratio = (nominal / gap_aware) if gap_aware else float("inf")

    # Admission-gate simulation (policy doc S5). Reported under BOTH sample
    # models, because which one you use changes the answer and the doc
    # originally quoted the wrong one:
    #   no_rewarm -- the model the policy ADOPTS: one global warmup, blocks
    #                merely have to fit inside a contiguous run.
    #   rewarm    -- option 3's model, which the policy REJECTS: every segment
    #                pays the warmup again.
    blocks_no_rewarm = gap_aware
    blocks_rewarm = sum(max(length - warmup - 1, 0) // block for length in runs)

    return {
        "pairs": pairs,
        "gaps": gaps,
        "pct": (gaps / pairs * 100) if pairs else 0.0,
        "worst_h": worst,
        "med_gap_ret": statistics.median(gap_rets) if gap_rets else None,
        "med_ok_ret": statistics.median(ok_rets) if ok_rets else None,
        "n_runs": len(runs),
        "median_run": statistics.median(runs) if runs else 0,
        "nominal_neff": nominal,
        "gap_aware_neff": gap_aware,
        "ratio": ratio,
        "z_inflation": math.sqrt(ratio) if ratio != float("inf") else float("inf"),
        "blocks_no_rewarm": blocks_no_rewarm,
        "blocks_rewarm": blocks_rewarm,
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--data-dir", default=_DEFAULT_DATA)
    ap.add_argument("--timeframe", default="1h", choices=sorted(_STEPS))
    ap.add_argument(
        "--warmup",
        type=int,
        default=120,
        help="bars the strategy needs before is_ready() (default: 120)",
    )
    ap.add_argument(
        "--block",
        type=int,
        default=24,
        help="bootstrap block size (default: 24, matching "
        "prescreen_signal._BLOCK_SIZE_1H)",
    )
    ap.add_argument(
        "--gate-floor",
        type=int,
        action="append",
        default=None,
        help="simulate the S5 admission gate at this minimum block "
        "count; repeatable (default: 8 = _MIN_N_EPISODES, and "
        "30 = the fork promotion bar)",
    )
    args = ap.parse_args()
    floors = args.gate_floor or [8, 30]

    step = _STEPS[args.timeframe]
    pattern = os.path.join(args.data_dir, f"*_{args.timeframe}.csv")
    files = sorted(glob.glob(pattern))
    if not files:
        raise SystemExit(f"no caches matched {pattern}")

    print(
        f"{len(files)} {args.timeframe} caches | warmup={args.warmup} block={args.block}\n"
    )
    hdr = (
        f"{'symbol':22} {'win':6} {'pairs':>7} {'gaps':>6} {'%':>7} {'worst':>7} "
        f"{'runs':>6} {'medrun':>7} {'nom':>6} {'gapaware':>9} {'z infl':>7}"
    )
    print(hdr)
    print("-" * len(hdr))

    out, gappy, combos, bad_total = [], 0, 0, 0
    for path in files:
        sym = os.path.basename(path)[: -len(f"_{args.timeframe}.csv")]
        rows, bad_ts = _load(path)
        bad_total += bad_ts
        for wname, (lo, hi) in WINDOWS.items():
            c = census(rows, lo, hi, step, args.warmup, args.block)
            if c["pairs"] == 0:
                continue
            combos += 1
            gappy += 1 if c["gaps"] else 0
            out.append((c["pct"], sym, wname, c))

    for _, sym, wname, c in sorted(out, reverse=True):
        worst = f"{c['worst_h']:.0f}h" if c["gaps"] else "-"
        print(
            f"{sym:22} {wname:6} {c['pairs']:7d} {c['gaps']:6d} {c['pct']:6.2f}% "
            f"{worst:>7} {c['n_runs']:6d} {c['median_run']:7.0f} "
            f"{c['nominal_neff']:6d} {c['gap_aware_neff']:9d} {c['z_inflation']:6.2f}x"
        )

    print(
        f"\n{gappy} of {combos} symbol x window combinations contain at least one gap"
    )

    # --- S5 admission-gate simulation -------------------------------------
    print("\nADMISSION GATE (policy doc S5) -- would it reject anything?")
    print("  A block spanning a gap is the defect, so blocks must fit inside a")
    print("  contiguous run. ADMIT iff placeable blocks >= floor.\n")
    for model, key in (
        ("no-re-warm (ADOPTED)", "blocks_no_rewarm"),
        ("re-warm    (REJECTED)", "blocks_rewarm"),
    ):
        for floor in floors:
            stopped = [(sym, wn) for _, sym, wn, c in out if c[key] < floor]
            verdict = (
                ("admits all %d" % combos)
                if not stopped
                else (
                    "stops %d: %s"
                    % (len(stopped), ", ".join(f"{s_} {w_}" for s_, w_ in stopped))
                )
            )
            print(f"  {model}  floor {floor:>3}: {verdict}")
    print("\n  The gate was DROPPED: under the adopted model it rejects nothing at")
    print("  either floor. Raising the floor until it bit would have been the")
    print("  post-hoc threshold-fitting the policy exists to prevent.")
    if bad_total:
        print(
            f"NOTE: {bad_total} row(s) had an unparseable timestamp and were excluded "
            f"from the series (see issue #50's residual on the lexical window filter)."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
