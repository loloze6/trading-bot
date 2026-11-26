"""Topic 49 proof: in a backtest of an idea that names a market profile, the book is flat outside the profile.

  python3 topics/49_review/profile_book_check.py RECORD PROFILE [--horizon DAYS]

From the coin's own daily closes (local data), independently of the engine: each bar's 60-day return (the trend) and the
rank of its 30-day swing among the past year's (the agitation), as common/market_profile.md defines them. Then, on every
bar of every window: (a) the engine's regime is the idea's regime exactly when the bar is in the profile; (b) the forecast is 0 on every bar outside the profile (a bet,
a rise of the forecast, is made only inside it); (c) a position held outside the profile is held at most the idea's
horizon after the last bar in it (the holding period, common/forecast.md 7), apart from a remainder too small for the
engine to trade (its rebalance minimum), whose size is printed. Prints one line per coin and the totals.
"""
import argparse, glob, os, sys
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "..", "..", "trading-bot", "local_data")
sys.path.insert(0, os.path.join(HERE, "..", "..", "common"))
from lib import profile_name  # noqa: E402

TREND = {"rising": lambda r: r > 10, "choppy": lambda r: (r >= -10) & (r <= 10), "falling": lambda r: r < -10}
AGIT = {"agitated": lambda k: k > 0.5, "calm": lambda k: k <= 0.5}


def in_profile(close, profile):
    trend = (close / close.shift(60) - 1) * 100
    ret = close.diff() / close                      # one-bar returns as the component reads them
    vol = ret.rolling(30).std()
    rank = vol.rolling(365 + 1).apply(lambda w: (w <= w[-1]).mean(), raw=True)
    ok = pd.Series(True, index=close.index)
    for w in profile.split():
        ok &= TREND[w](trend) if w in TREND else AGIT[w](rank)
    return ok


def main():
    a = argparse.ArgumentParser()
    a.add_argument("record"); a.add_argument("profile"); a.add_argument("--horizon", type=int, default=5)
    args = a.parse_args()
    profile = profile_name(args.profile)
    tot = {"bars": 0, "in_profile": 0, "regime_mismatch": 0, "forecast_outside": 0, "held_outside_beyond_horizon": 0,
           "days_in_position": 0, "days_in_position_in_profile": 0}
    beyond = []
    for coin in sorted(os.listdir(args.record)):
        files = sorted(glob.glob(os.path.join(args.record, coin, "w*", "bars.csv.gz")))
        if not files:
            continue
        d = pd.read_csv(os.path.join(DATA, f"kraken_{coin}_1d.csv"), usecols=["timestamp", "close"])
        d["timestamp"] = pd.to_datetime(d["timestamp"]).dt.strftime("%Y-%m-%d")
        close = d.set_index("timestamp")["close"]
        inside = in_profile(close, profile)
        c = dict.fromkeys(tot, 0)
        for f in files:
            b = pd.read_csv(f, usecols=["timestamp", "regime", "forecast", "postRebalance_current_allocation"])
            b["timestamp"] = pd.to_datetime(b["timestamp"]).dt.strftime("%Y-%m-%d")
            ins = b["timestamp"].map(inside).fillna(False).astype(bool).values
            pos = b["postRebalance_current_allocation"].fillna(0).abs().values
            regime_in = (b["regime"] != "chop").values      # the flat regime the code sends a bar outside to
            ready = b["regime"].notna().values
            c["bars"] += len(b); c["in_profile"] += ins.sum()
            c["regime_mismatch"] += (ready & (regime_in != ins)).sum()
            c["forecast_outside"] += ((b["forecast"].fillna(0).abs().values > 1e-9) & ~ins).sum()
            last_in = -10**9
            for i in range(len(b)):
                if ins[i]:
                    last_in = i
                elif pos[i] > 1e-9 and i - last_in > args.horizon:
                    c["held_outside_beyond_horizon"] += 1
                    beyond.append(pos[i])
            c["days_in_position"] += (pos > 1e-9).sum(); c["days_in_position_in_profile"] += ((pos > 1e-9) & ins).sum()
        print(coin, {k: int(v) for k, v in c.items()})
        for k in tot:
            tot[k] += int(c[k])
    print("total", tot)
    if beyond:
        print(f"held beyond the horizon: median position {np.median(beyond):.3f}, 90th percentile {np.quantile(beyond, 0.9):.3f} "
              f"(of the capital; inside the profile the median position is the record's own)")


if __name__ == "__main__":
    main()
