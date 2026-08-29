"""
What every recorded per-trade record does and does not carry.

Evidence for E-029. Reads only archived `trade_diagnostics.json` files; changes
nothing and re-runs nothing.

Usage:  python engineering/roadmap/E-029/artifacts/measure_trade_records.py
        (cwd = strategy-research/)
"""

import collections
import glob
import json
import os
import statistics as st

ABSENT = (
    "regime_at_exit",
    "forecast_at_entry",
    "forecast_at_exit",
    "allocation_before",
    "allocation_after",
    "move_shape",
    "entry_reason",
)


def main():
    trades, sources = [], []
    for path in sorted(glob.glob("runs/**/trade_diagnostics.json", recursive=True)):
        recs = json.load(open(path, encoding="utf-8")).get("trades", [])
        sources.append((os.path.relpath(path, "runs").replace(os.sep, "/"), len(recs)))
        trades += recs

    n = len(trades)
    print(f"source files: {len(sources)}   total trades: {n}")
    for p, c in sources:
        print(f"  {p}  n={c}")
    print()

    counts = collections.Counter(t.get("exit_reason", "<missing>") for t in trades)
    print("exit_reason distribution:")
    for k, v in counts.most_common():
        print(f"  {k:16s}: {v} ({100.0 * v / n:.1f}%)")
    print()

    print("F7 -- does exit_reason separate outcomes? (if it did not at all, low")
    print("      cardinality would still be tolerable; it does, for one category)")
    for reason in counts:
        rets = [t["net_portfolio_return_pct"] for t in trades if t.get("exit_reason") == reason]
        holds = [t["holding_bars"] for t in trades if t.get("exit_reason") == reason]
        print(
            f"  {reason:14s} n={len(rets):5d} median_ret={st.median(rets):+.4f}% "
            f"mean={st.mean(rets):+.4f}% median_hold={st.median(holds):.0f} bars"
        )
    print()

    for field in ("regime_at_entry", "direction", "symbol"):
        c = collections.Counter(t.get(field) for t in trades)
        print(f"{field}: {dict(c.most_common())}")
    hist = collections.Counter(min(t.get("holding_bars") or 0, 10) for t in trades)
    print(f"holding_bars histogram (10 = 10+): {dict(sorted(hist.items()))}")
    print()

    present = collections.Counter()
    for t in trades:
        present.update(t.keys())
    print("fields present on trade records:")
    print("  " + ", ".join(sorted(present)))
    print()
    print("ABSENT and load-bearing (E-029 Done-when 1):")
    for f in ABSENT:
        print(f"  {f}")


if __name__ == "__main__":
    main()
