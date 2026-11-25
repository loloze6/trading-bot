import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            L30 = l.shift(1).rolling(30, min_periods=30).min()
            vol30 = r1.rolling(30, min_periods=20).std()
            vol_rel = vol30 / r1.rolling(90, min_periods=60).std()
            rng = (h - l).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n), "day": ts.dt.floor("D").astype("int64"),
                "year": ts.dt.year, "ret60": c / c.shift(60) - 1, "vol_rel": vol_rel,
                "z5": (c / c.shift(5) - 1) / (vol30 * np.sqrt(5)),
                "pr": (l < L30) & (c > L30), "reclaim": (c - L30) / rng,
                "f5": c.shift(-5) / c - 1, "u5": vol30 * np.sqrt(5),
            }))
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % 5 == 0) & A["f5"].notna()].copy()
    drift = G["f5"].mean()
    G["ex"] = G["f5"] - drift
    G["trend"] = np.where(G["ret60"] < -0.1, "fall", np.where(G["ret60"] > 0.1, "rise", "chop"))
    G.loc[G["ret60"].isna(), "trend"] = "na"
    G["agit"] = np.where(G["vol_rel"].isna(), "na", np.where(G["vol_rel"] > 1, "ag", "calm"))

    def clslope(x, y, d):
        x = np.asarray(x, float); y = np.asarray(y, float); d = np.asarray(d)
        xm = x - x.mean(); b = (xm * (y - y.mean())).sum() / (xm ** 2).sum()
        e = y - y.mean() - b * xm
        s = pd.Series(xm * e).groupby(d).sum()
        se = np.sqrt((s ** 2).sum()) / (xm ** 2).sum()
        return b, b / se, len(np.unique(d))

    out = {}
    res = {}
    for tr in ["chop", "fall", "rise", "all"]:
        for ag in ["calm", "ag"]:
            s = G[((G["trend"] == tr) | (tr == "all")) & (G["agit"] == ag) & G["z5"].notna()]
            s = s[s["trend"] != "na"] if tr == "all" else s
            if len(s) < 20: continue
            sz = s["z5"].clip(-3, 3)
            b, t, nd = clslope(sz, s["ex"] / s["u5"], s["day"])
            res[(tr, ag)] = pd.Series({"n": len(s), "slope": b, "t_day": t, "days": nd})
    out["z5 -> next 5d move (in usual moves), clustered by day"] = pd.DataFrame(res).T

    cal = G[(G["agit"] == "calm") & G["z5"].notna() & (G["trend"] != "na")].copy()
    cal["sig"] = np.sign(cal["z5"]) * cal["ex"]
    out["calm: z5-signed excess by window"] = cal.groupby("win")["sig"].agg(["count", "mean"])
    out["calm: z5-signed excess by year"] = cal.groupby("year")["sig"].agg(["count", "mean"])
    cal["q"] = pd.qcut(cal["z5"], 5, labels=False)
    out["calm: excess by z5 quintile"] = cal.groupby("q")["ex"].agg(["count", "mean"])

    P = A[A["pr"] & A["f5"].notna() & (A["ret60"] < -0.1)].sort_values(["coin", "win", "pos"])
    keep, last = [], {}
    for i, r in P.iterrows():
        k = (r["coin"], r["win"])
        if k not in last or r["pos"] - last[k] >= 5:
            keep.append(i); last[k] = r["pos"]
    P = P.loc[keep].copy(); P["ex"] = P["f5"] - drift
    b, t, nd = clslope(P["reclaim"], P["ex"] / P["u5"], P["day"])
    out["falling pierce-reclaim: reclaim slope, clustered"] = pd.Series({"n": len(P), "slope": b, "t_day": t, "days": nd})
    out["falling pr high-reclaim by window"] = P[P["reclaim"] > P["reclaim"].median()].groupby("win")["ex"].agg(["count", "mean"])
    return out
