def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    H = 168
    rows = []
    hrows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values.astype(float)
            n = len(cl)
            s = pd.Series(cl)
            r7 = s / s.shift(168) - 1
            r30 = s / s.shift(720) - 1
            r1 = s / s.shift(24) - 1
            hi30 = s.rolling(720, min_periods=720).max()
            near = s / hi30 - 1
            lr = np.log(s).diff()
            vol7 = lr.rolling(168, min_periods=100).std()
            vol30 = lr.rolling(720, min_periods=300).std()
            vrat = vol7 / vol30
            v = b["volume"].astype(float)
            vrel = v.rolling(24).sum() / v.rolling(720, min_periods=300).sum() * 30
            f7 = s.shift(-168) / s - 1
            f1 = s.shift(-24) / s - 1
            idx = np.arange(0, n, H)
            for i in idx:
                rows.append(dict(coin=c, w=w, r7=r7[i], r30=r30[i], r1=r1[i], near=near[i],
                                 vrat=vrat[i], vrel=vrel[i], f7=f7[i], reg=b["regime"].iat[i]))
            idx24 = np.arange(0, n, 24)
            ts = pd.to_datetime(b["timestamp"])
            for i in idx24:
                hrows.append(dict(coin=c, w=w, r1=r1[i], r7=r7[i], r30=r30[i], vrat=vrat[i],
                                  f1=f1[i], wd=ts.iat[i].weekday(), near=near[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["f7"] - g.groupby("coin")["f7"].transform("mean")
    g = g.dropna(subset=["ex"])
    def qtab(df, col, y="ex", q=5):
        d = df.dropna(subset=[col, y]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = d.groupby("q")[y].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.round(4)
    def slope(df, col, y="ex"):
        d = df.dropna(subset=[col, y])
        r = stats.linregress(d[col], d[y]); return pd.Series(dict(slope=r.slope, t=r.slope / r.stderr, n=len(d)))
    up = g[g.r30 > 0]; dn = g[g.r30 <= 0]
    out["7d fwd by r7 quint, r30<=0"] = qtab(dn, "r7")
    out["7d fwd by near quint, all"] = qtab(g, "near")
    out["7d fwd by vrat quint, all"] = qtab(g, "vrat")
    out["7d fwd by vrel quint, all"] = qtab(g, "vrel")
    out["slopes"] = pd.DataFrame({
        "r7|up": slope(up, "r7"), "r7|dn": slope(dn, "r7"), "near|all": slope(g, "near"),
        "near|up": slope(up, "near"), "r30|all": slope(g, "r30"), "vrat|all": slope(g, "vrat"),
        "vrel|all": slope(g, "vrel"), "r1|all": slope(g, "r1")}).T.round(5)
    out["r7|up slope by coin"] = up.groupby("coin").apply(lambda d: slope(d, "r7")).round(4)
    h = pd.DataFrame(hrows)
    h["ex"] = h["f1"] - h.groupby("coin")["f1"].transform("mean")
    h = h.dropna(subset=["ex"])
    out["1d fwd by r1 quint, all"] = qtab(h, "r1")
    out["1d slopes"] = pd.DataFrame({"r1|all": slope(h, "r1"), "r1|up": slope(h[h.r30 > 0], "r1"),
        "r1|dn": slope(h[h.r30 <= 0], "r1"), "r7|all": slope(h, "r7"), "vrat|all": slope(h, "vrat"),
        "near|all": slope(h, "near")}).T.round(5)
    # weekday of daily coin returns, hourly returns by hour
    dd = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"] = c; dd.append(d)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    t = D.groupby("wd")["coin_return"].agg(["mean", "count", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["coin daily ret by weekday"] = t.round(5)
    hr = []
    for c in bars:
        for w, b in bars[c].items():
            r = b["close"].pct_change()
            hr.append(pd.DataFrame({"h": pd.to_datetime(b["timestamp"]).dt.hour, "r": r,
                                    "pos": b["postRebalance_current_allocation"].shift(1)}))
    HR = pd.concat(hr).dropna()
    t = HR.groupby("h")["r"].agg(["mean", "count", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["hourly ret by hour (t only)"] = t[["mean", "t"]].round(6)
    return out
