"""A one-table summary of a backtests folder, for the readings: per plan, the coins and windows run, the trades, and the
engine's forecast-against-next-return correlation (all bars) per window. It reads only metrics.json files (the engine's
figures); it reads no bars and judges nothing (that is step 5).

  python summarise_backtests.py BACKTESTS_DIR
"""
import glob, json, os, sys
from pathlib import Path


def main():
    root = Path(sys.argv[1])
    print("| plan | coin | windows | trades (sum) | forecast vs next return, all bars, per window |")
    print("|---|---|---|---|---|")
    for plan in sorted(p for p in root.iterdir() if p.is_dir()):
        for coin in sorted(c for c in plan.iterdir() if c.is_dir()):
            ws = sorted(coin.glob("w*/metrics.json"), key=lambda p: int(p.parent.name[1:]))
            cores = [json.loads(w.read_text())["core"] for w in ws]
            trades = sum(c.get("trade_count") or 0 for c in cores)
            corr = ", ".join(f"{c.get('forecast_return_corr_all_bars'):+.3f}" if isinstance(c.get("forecast_return_corr_all_bars"), (int, float)) else "n/a" for c in cores)
            print(f"| {plan.name} | {coin.name} | {len(ws)} | {trades} | {corr} |")


if __name__ == "__main__":
    main()
