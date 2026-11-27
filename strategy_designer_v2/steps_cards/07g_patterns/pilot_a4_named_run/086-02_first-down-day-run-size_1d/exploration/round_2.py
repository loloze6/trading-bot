import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for H in [1, 3, 5, 10]:
            pass
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            sd30 = r1.rolling(30).std().shift(1)
            up = (r1 > 0).astype(int)
            # streak length of up days ending at previous bar
            streak = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            prev_streak = streak.shift(1)
            dip = (r1 < 0) & (prev_streak > 0)
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "inprof": b["regime"] != "chop",
                               "dip": dip, "streak": prev_streak, "r1z": r1 / sd30,
                               "alloc": b["postRebalance_current_allocation"],
                               "regime": b["regime"]})
            for H in [1, 3, 5, 10]:
                df[f"f{H}"] = c.shift(-H) / c - 1
            recs.append(df)
    d = pd.concat(recs, ignore_index=True)
    # drift per coin and H on grid
    res = []
    for H in [1, 3, 5, 10]:
        dr = d[d.pos % H == 0].groupby("coin")[f"f{H}"].mean()
        d[f"u{H}"] = -(d[f"f{H}"] - d.coin.map(dr))
        for name, m in [("inprof all", d.inprof), ("inprof dip", d.inprof & d.dip),
                        ("inprof nondip", d.inprof & ~d.dip), ("outprof dip", ~d.inprof & d.dip)]:
            x = d[m & (d.pos % H == 0)][f"u{H}"].dropna()
            res.append([H, name, len(x), x.mean(), x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan])
    out["short unusual by H and situation"] = pd.DataFrame(res, columns=["H", "set", "n", "mean", "t"])
    # dip in profile: by streak length (all dips, not grid, for 3d)
    x = d[d.inprof & d.dip].dropna(subset=["u3"])
    x["sb"] = x.streak.clip(upper=4)
    g = x.groupby("sb").u3.agg(["size", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["dip in profile: streak length -> 3d short unusual (overlapping)"] = g
    x["zb"] = pd.qcut(x.r1z, 4, labels=False, duplicates="drop")
    g = x.groupby("zb").agg(lo=("r1z", "min"), n=("u3", "size"), mean=("u3", "mean"), sd=("u3", "std"))
    g["t"] = g["mean"] / (g["sd"] / np.sqrt(g["n"]))
    out["dip in profile: dip size z -> 3d"] = g.drop(columns="sd")
    # book days: by window and largest losses
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin, win=w))
    dd = pd.concat(dd, ignore_index=True).dropna(subset=["book_return"])
    bw = dd.groupby("win").book_return.agg(["size", "mean", "sum"])
    out["book by window"] = bw
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    tr = pd.concat(tr, ignore_index=True)
    out["trades"] = pd.Series({"n": len(tr), "mean net %": tr.net_profit_loss_percent.mean(),
                               "win share": (tr.net_profit_loss_percent > 0).mean(),
                               "median net %": tr.net_profit_loss_percent.median(),
                               "worst 5 share of total loss": tr.net_profit_loss_percent.nsmallest(5).sum() / tr.net_profit_loss_percent.sum()})
    return out
