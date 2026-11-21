import pandas as pd, numpy as np
from scipy import stats

def tstat(v):
    v = pd.Series(v).dropna()
    return v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan

def explore(data):
    out = {}
    D = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20).std().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "p1": r1, "z": r1 / vol,
                               "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1,
                               "f10": c.shift(-10) / c - 1,
                               "year": ts.dt.year, "wd": ts.dt.weekday,
                               "alloc": b["postRebalance_current_allocation"],
                               "dhi30": c / c.rolling(30).max() - 1})
            df["pos"] = np.arange(len(df))
            D.append(df)
    D = pd.concat(D)
    for h in ["f1", "f3", "f10"]:
        n = int(h[1:])
        grid = D[D["pos"] % n == 0]
        drift = grid.groupby("coin")[h].mean()
        D["x" + h] = D[h] - D["coin"].map(drift)
    D["zq"] = D.groupby("coin")["z"].transform(lambda v: pd.qcut(v.rank(method="first"), 20, labels=False))
    res = {}
    for h in ["xf1", "xf3"]:
        n = int(h[2:])
        x = D[D["pos"] % n == 0]
        t = x.groupby("zq")[h].agg(["mean", "count"])
        t["t"] = x.groupby("zq")[h].apply(tstat)
        res[h] = t
    out["by_z_vigintile_next1"] = res["xf1"]
    out["by_z_vigintile_next3"] = res["xf3"]
    low = D[D["zq"] <= 1]
    out["worst10pct_by_coin"] = low.groupby("coin")["xf1"].agg(["mean", "count", tstat])
    out["worst10pct_by_year"] = low.groupby("year")["xf1"].agg(["mean", "count", tstat])
    wl = low.groupby("win")["xf1"].mean()
    out["worst10pct_windows_pos_share"] = float((wl > 0).mean())
    # graded within negative days
    neg = D[D["z"] < 0].dropna(subset=["z", "xf1"])
    out["neg_days_spearman_z_vs_next1_by_coin"] = neg.groupby("coin").apply(lambda d: stats.spearmanr(d["z"], d["xf1"])[0])
    # weekday excess per coin share positive
    wd = D.dropna(subset=["xf1"]).groupby(["wd", "coin"])["xf1"].mean().unstack()
    out["weekday_next1_excess_by_coin"] = wd
    # near-high momentum by year
    g10 = D[D["pos"] % 10 == 0].dropna(subset=["dhi30", "xf10"]).copy()
    g10["q"] = g10.groupby("coin")["dhi30"].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
    top = g10[g10["q"] == 4]
    out["nearhigh_top_by_year"] = top.groupby("year")["xf10"].agg(["mean", "count", tstat])
    # book: next-day return when the book is in vs out, after worst days
    out["alloc_on_worst_days"] = low.groupby(low["alloc"] > 0)["xf1"].agg(["mean", "count"])
    return out
