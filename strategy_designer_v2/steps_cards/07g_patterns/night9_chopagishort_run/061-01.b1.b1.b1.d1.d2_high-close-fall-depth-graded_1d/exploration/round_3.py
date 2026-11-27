def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            rng = (hi - lo).replace(0, np.nan)
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            vol90 = r1.rolling(90, min_periods=60).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "cl": (c - lo) / rng, "r5": c / c.shift(5) - 1, "r20": c / c.shift(20) - 1,
                               "r60": c / c.shift(60) - 1, "vol30": vol30, "vr": vol30 / vol90,
                               "fwd": c.shift(-H) / c - 1, "wd": ts.dt.weekday})
            df["z20"] = df.r20 / (vol30 * np.sqrt(20))
            df["z5"] = df.r5 / (vol30 * np.sqrt(5))
            df["us"] = np.sqrt(H) * vol30
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D[D.pos % H == 0].groupby("coin")["fwd"].mean()
    D["ufwd"] = D["fwd"] - D["coin"].map(drift)
    D["ustr"] = D.ufwd / D.us
    G = D[D.pos % H == 0].dropna(subset=["ufwd", "z20"]).copy()
    G["trend"] = pd.cut(G.r60, [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    G["ag"] = np.where(G.vr > 1, "agit_proxy", np.where(G.vr.notna(), "calm_proxy", "na"))

    def slope(g, x="z20"):
        g = g.dropna(subset=[x, "ufwd"])
        n = len(g)
        if n < 20: return pd.Series({"n": n, "days": g.day.nunique(), "slope": np.nan, "t_day": np.nan})
        xc = g[x] - g[x].mean(); yc = g.ufwd - g.ufwd.mean()
        b = (xc * yc).sum() / (xc ** 2).sum()
        e = yc - b * xc
        s = (xc * e).groupby(g.day).sum()
        se = np.sqrt((s ** 2).sum()) / (xc ** 2).sum()
        return pd.Series({"n": n, "days": g.day.nunique(), "slope": round(b, 5), "t_day": round(b / se, 2)})

    def ct(g):
        n = len(g)
        if n < 5: return pd.Series({"n": n, "days": 0, "mean": np.nan, "str": np.nan, "t_day": np.nan})
        m = g.ufwd.mean(); s = (g.ufwd - m).groupby(g.day).sum()
        se = np.sqrt((s ** 2).sum()) / n
        return pd.Series({"n": n, "days": g.day.nunique(), "mean": round(m, 4), "str": round(g.ustr.mean(), 3), "t_day": round(m / se, 2)})

    out = {}
    out["z20 slope all"] = slope(G)
    out["z20 slope by trend"] = G.dropna(subset=["trend"]).groupby("trend", observed=True).apply(slope)
    out["z20 slope by agit proxy"] = G[G.ag != "na"].groupby("ag").apply(slope)
    out["z20 slope by trend x agit"] = G[(G.ag != "na")].dropna(subset=["trend"]).groupby(["trend", "ag"], observed=True).apply(slope)
    out["z20 slope by half"] = G.groupby(G.w.isin(["w7","w8","w9","w10","w11","w12"])).apply(slope)
    out["z20 slope by coin"] = G.groupby("coin").apply(slope)
    out["z5 slope by trend"] = G.dropna(subset=["trend"]).groupby("trend", observed=True).apply(lambda g: slope(g, "z5"))
    G["hc"] = G.cl >= 0.75
    G["r5s"] = np.where(G.r5 < 0, "neg", "pos")
    out["high close x r5 sign x trend"] = G[G.hc].dropna(subset=["trend"]).groupby(["trend", "r5s"], observed=True).apply(ct)
    out["weekday clustered"] = G.groupby("wd").apply(ct)
    return out
