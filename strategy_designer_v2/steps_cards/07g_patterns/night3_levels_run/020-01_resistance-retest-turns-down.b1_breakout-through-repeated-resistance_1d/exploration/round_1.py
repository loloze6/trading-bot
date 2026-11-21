import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 10
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        grid = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-H) / c - 1,
                "p1": r1,
                "p3": c / c.shift(3) - 1,
                "p10": c / c.shift(10) - 1,
                "p30": c / c.shift(30) - 1,
                "vol20": r1.rolling(20).std(),
                "dhi30": c / c.rolling(30).max() - 1,
                "dlo30": c / c.rolling(30).min() - 1,
                "rng": (b["high"] - b["low"]) / c,
                "volu": b["volume"] / b["volume"].rolling(20).mean(),
                "fc": b["forecast"],
            })
            df["pos"] = np.arange(len(df))
            g = df[df["pos"] % H == 0]
            grid.append(g)
            d = pd.DataFrame({"coin": coin, "r": r1.shift(-1), "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                              "p1": r1})
            daily.append(d)
        g = pd.concat(grid)
        drift = g["fwd"].mean()
        sd = g["fwd"].std()
        g["ex"] = g["fwd"] - drift
        g["exs"] = g["ex"] / sd
        rows.append(g)
    G = pd.concat(rows).dropna(subset=["ex"])
    out = {}
    for s in ["p1", "p3", "p10", "p30", "vol20", "dhi30", "dlo30", "rng", "volu"]:
        x = G.dropna(subset=[s]).copy()
        x["q"] = x.groupby("coin")[s].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
        t = x.groupby("q").agg(mean_ex=("ex", "mean"), strength=("exs", "mean"), n=("ex", "size"))
        t["t"] = x.groupby("q")["ex"].apply(lambda v: v.mean() / (v.std() / np.sqrt(len(v))))
        # per-coin spearman
        rc = x.groupby("coin").apply(lambda d: stats.spearmanr(d[s], d["ex"])[0])
        t.loc["coins_rho_pos"] = [ (rc > 0).sum(), rc.mean(), len(rc), np.nan]
        out[s] = t
    D = pd.concat(daily).dropna()
    wt = D.groupby("wd")["r"].agg(["mean", "count", "std"])
    wt["t"] = wt["mean"] / (wt["std"] / np.sqrt(wt["count"]))
    out["weekday_next_day"] = wt
    # big one-day moves: next-day return by p1 decile pooled (per coin rank)
    D["q"] = D.groupby("coin")["p1"].transform(lambda v: pd.qcut(v.rank(method="first"), 10, labels=False))
    nd = D.groupby("q")["r"].agg(["mean", "count", "std"])
    nd["t"] = nd["mean"] / (nd["std"] / np.sqrt(nd["count"]))
    out["next_day_by_p1_decile"] = nd
    return out
