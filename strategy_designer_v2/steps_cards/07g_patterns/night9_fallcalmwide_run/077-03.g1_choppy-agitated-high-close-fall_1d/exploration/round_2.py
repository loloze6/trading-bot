def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1) / c - 1).dropna())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            v = b["volume"].astype(float)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "loc": ((c - l) / (h - l).replace(0, np.nan)).values,
                "rngv": (((h - l) / c) / sd).values,
                "ret1": (r / sd).values,
                "tr60": (c / c.shift(60) - 1).values,
                "sd": sd.values,
                "vol": (v / v.rolling(30, min_periods=20).mean()).values,
                "ux": (nxt - drift).values, "ux2": (nxt2 - 2 * drift).values,
                "inprof": (b["regime"] != "chop").values,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D").values,
            })
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["ux", "loc", "rngv"])
    D["sdrel"] = D["sd"] / D.groupby("coin")["sd"].transform("median")

    def ct(x, days):
        x = pd.Series(x.values); dd = pd.Series(days.values)
        m = x.mean(); g = (x - m).groupby(dd).sum(); n = len(g)
        se = np.sqrt((g ** 2).sum()) / len(x) * np.sqrt(n / (n - 1))
        return m / se if se > 0 else np.nan

    def st(g, col="ux"):
        return pd.Series({"n": len(g), "mean_%": 100 * g[col].mean(), "t": ct(g[col], g["day"])})

    res = {}
    D["rq"] = D.groupby("coin")["rngv"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    D["vq"] = D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    D["tr"] = pd.cut(D["tr60"], [-10, -0.1, 0.1, 100], labels=["falling", "choppy", "rising"])
    D["ag"] = np.where(D["sdrel"] > 1, "agit", "calm")
    low = D[D["loc"] <= .25]
    high = D[D["loc"] >= .75]
    res["low close: range tercile x volume tercile"] = low.groupby(["rq", "vq"]).apply(st).round(3)
    res["low close wide (rq2): trend x agitation"] = low[low.rq == 2].groupby(["tr", "ag"]).apply(st).round(3)
    res["high close: trend x agitation"] = high.groupby(["tr", "ag"]).apply(st).round(3)
    res["high close wide (rq>=1): trend x agitation, 2-day"] = high[high.rq >= 1].groupby(["tr", "ag"]).apply(lambda g: st(g, "ux2")).round(3)
    # graded within profile: product score
    P = D[D.inprof & (D["loc"] >= .75)].copy()
    P["score"] = (2 * P["loc"] - 1) * P["rngv"]
    P["sq"] = pd.qcut(P["score"], 3, labels=False, duplicates="drop")
    res["in profile high close by score tercile"] = P.groupby("sq").apply(st).round(3)
    # low close wide: next day vs day 2 (is it spent?)
    lw = low[low.rq == 2]
    res["wide low close: day1 vs 2-day"] = pd.DataFrame({"d1": st(lw), "d2": st(lw, "ux2")}).round(3)
    # 1-day return quintile, by trend
    D["r1q"] = D.groupby("coin")["ret1"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    res["bottom 1d return quintile by trend x agitation"] = D[D.r1q == 0].groupby(["tr", "ag"]).apply(st).round(3)
    res["top 1d return quintile by trend x agitation"] = D[D.r1q == 4].groupby(["tr", "ag"]).apply(st).round(3)
    return res
