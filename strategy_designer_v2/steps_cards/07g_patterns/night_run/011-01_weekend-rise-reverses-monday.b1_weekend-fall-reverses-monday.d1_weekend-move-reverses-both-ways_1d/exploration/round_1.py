import pandas as pd, numpy as np
from scipy import stats

def tstat(x):
    x = pd.Series(x).dropna()
    if len(x) < 3: return np.nan
    return x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "wd": ts.dt.weekday, "year": ts.dt.year,
                "r": r, "z": r/vol, "vol": vol,
                "volrel": b["volume"]/b["volume"].rolling(20, min_periods=10).mean(),
                "vollvl": vol/vol.rolling(120, min_periods=60).median(),
                "f1": c.shift(-1)/c-1, "f2": c.shift(-2)/c-1,
                "r5": c/c.shift(5)-1,
                "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    m1 = D.groupby("coin")["f1"].mean()
    g2 = D[D["pos"] % 2 == 0]
    m2 = g2.groupby("coin")["f2"].mean()
    D["f1x"] = D["f1"] - D["coin"].map(m1)
    D["f2x"] = D["f2"] - D["coin"].map(m2)
    D["rev2"] = -np.sign(D["z"]) * D["f2x"]
    D["rev1"] = -np.sign(D["z"]) * D["f1x"]
    out = {}
    # reversal after each weekday's move (each weekday's samples are 7 days apart)
    rw = []
    for wd, g in D.groupby("wd"):
        g = g.dropna(subset=["z", "f2x", "f1x"])
        big = g[g["z"].abs() > g["z"].abs().median()]
        rw.append({"wd": wd, "n": len(g),
                   "rev1": g["rev1"].mean(), "t_rev1": tstat(g["rev1"]),
                   "rev2": g["rev2"].mean(), "t_rev2": tstat(g["rev2"]),
                   "rev2_big": big["rev2"].mean(), "t_rev2_big": tstat(big["rev2"]),
                   "corr_z_f2": g["z"].corr(g["f2x"])})
    out["reversal_by_weekday"] = pd.DataFrame(rw)
    # mean next-day return by weekday of the next day (f1 of bar wd -> next day wd+1)
    nd = D.dropna(subset=["f1x"]).groupby("wd")["f1x"].agg(["mean", "count", tstat])
    out["next_day_excess_by_bar_wd"] = nd
    # Sunday cases by relative volume tercile
    s = D[(D["wd"] == 6)].dropna(subset=["rev2", "volrel"]).copy()
    s["vt"] = pd.qcut(s["volrel"], 3, labels=["lowvol", "mid", "highvol"])
    out["sunday_rev2_by_volume"] = s.groupby("vt")["rev2"].agg(["mean", "count", tstat])
    # all bars: next-day excess by z quintile (all bars, 1-day non overlapping)
    a = D.dropna(subset=["z", "f1x"]).copy()
    a["zq"] = pd.qcut(a["z"], 5, labels=False)
    out["f1x_by_z_quintile"] = a.groupby("zq")["f1x"].agg(["mean", "count", tstat])
    # by vol level quintile: next-day raw return and its abs
    v = D.dropna(subset=["vollvl", "f1x"]).copy()
    v["vq"] = pd.qcut(v["vollvl"], 5, labels=False)
    out["f1x_by_vollevel"] = v.groupby("vq")["f1x"].agg(["mean", "count", tstat])
    # 5-day return quintile, next 2 days (grid 2)
    q = D[D["pos"] % 2 == 0].dropna(subset=["r5", "f2x"]).copy()
    q["q"] = pd.qcut(q["r5"], 5, labels=False)
    out["f2x_by_r5_quintile"] = q.groupby("q")["f2x"].agg(["mean", "count", tstat])
    # by year
    out["f1x_by_year"] = D.dropna(subset=["f1x"]).groupby("year")["f1x"].agg(["mean", "count", tstat])
    # book daily returns by weekday
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin
            br.append(x)
    B = pd.concat(br)
    B["wd"] = pd.to_datetime(B["day"]).dt.weekday
    out["book_by_weekday"] = B.dropna(subset=["book_return"]).groupby("wd")["book_return"].agg(["mean", "count", tstat])
    out["coin_by_weekday"] = B.dropna(subset=["coin_return"]).groupby("wd")["coin_return"].agg(["mean", "count", tstat])
    return out
