import pandas as pd, numpy as np

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
                "coin": coin, "win": w, "date": ts.dt.normalize(),
                "wd_next": (ts + pd.Timedelta(days=1)).dt.weekday,
                "fwd": c.shift(-1) / c - 1,
                "r1z": r / vol,
                "r3lag1z": (c.shift(1) / c.shift(4) - 1) / vol.shift(1),
                "r5z": (c / c.shift(5) - 1) / vol,
                "vol": vol,
                "lowdist60": (c / c.rolling(60, min_periods=60).min() - 1) / vol,
                "brk60": (c < c.shift(1).rolling(60, min_periods=60).min()).astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["fwd"].transform("mean")
    D["ex"] = D["fwd"] - mu

    def ct(v, dates):
        m = v.notna()
        v, dates = v[m], dates[m]
        n = len(v)
        if n < 10: return (np.nan, np.nan, n, 0)
        dev = (v - v.mean()).groupby(dates).sum()
        G = len(dev)
        se = np.sqrt(G / (G - 1) * (dev ** 2).sum()) / n
        return (v.mean(), v.mean() / se, n, G)

    out = {}
    # 1 weekday of target day
    res = {}
    for wd in range(7):
        s = D[D.wd_next == wd]
        res[wd] = ct(s["ex"], s["date"])
    out["excess next-day return by target weekday (0=Mon)"] = pd.DataFrame(res, index=["mean", "t", "n", "dates"]).T

    # 2 grading of signals by target weekday: mean of sign-free product z*ex (z clipped)
    for name in ["r3lag1z", "r1z", "r5z"]:
        res = {}
        for wd in list(range(7)) + ["all"]:
            s = D if wd == "all" else D[D.wd_next == wd]
            z = s[name].clip(-4, 4)
            res[wd] = ct(z * s["ex"], s["date"])
        out[f"{name} x next excess, by target weekday"] = pd.DataFrame(res, index=["mean", "t", "n", "dates"]).T

    # 3 quintiles of r1z: next excess
    q = D.dropna(subset=["r1z", "ex"]).copy()
    q["qq"] = pd.qcut(q["r1z"], 5, labels=False)
    res = {k: ct(g["ex"], g["date"]) for k, g in q.groupby("qq")}
    out["next excess by prev-day z quintile"] = pd.DataFrame(res, index=["mean", "t", "n", "dates"]).T

    # 4 vol level relative to coin's median vol
    q = D.dropna(subset=["vol", "ex"]).copy()
    q["vr"] = q["vol"] / q.groupby("coin")["vol"].transform("median")
    q["qq"] = pd.qcut(q["vr"], 5, labels=False)
    res = {k: ct(g["ex"], g["date"]) for k, g in q.groupby("qq")}
    out["next excess by vol quintile"] = pd.DataFrame(res, index=["mean", "t", "n", "dates"]).T

    # 5 distance to 60d low, and breaks
    q = D.dropna(subset=["lowdist60", "ex"]).copy()
    q["qq"] = pd.qcut(q["lowdist60"], 5, labels=False)
    res = {k: ct(g["ex"], g["date"]) for k, g in q.groupby("qq")}
    res["break"] = ct(q.loc[q.brk60 == 1, "ex"], q.loc[q.brk60 == 1, "date"])
    out["next excess by distance to 60d low (vol units) quintile"] = pd.DataFrame(res, index=["mean", "t", "n", "dates"]).T

    # 6 book: daily, weekday of its largest days
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["win"] = w; bk.append(dd)
    B = pd.concat(bk).groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    B["wd"] = pd.to_datetime(B["day"]).dt.weekday
    out["book by weekday"] = B.groupby("wd")["book_return"].agg(["mean", "std", "count"])
    top = B.nlargest(20, "book_return"); bot = B.nsmallest(20, "book_return")
    out["weekday of 20 best/worst book days"] = pd.DataFrame({"best": top.wd.value_counts(), "worst": bot.wd.value_counts()}).fillna(0)
    return out
