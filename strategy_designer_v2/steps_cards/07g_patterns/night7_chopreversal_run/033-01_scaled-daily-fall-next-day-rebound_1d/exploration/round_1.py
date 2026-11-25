def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            z = r / sd30.shift(1)
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"], utc=True),
                "r": r, "z": z,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "tr60": c / c.shift(60) - 1,
                "r5": c / c.shift(5) - 1,
                "rng": (b["high"].astype(float) - b["low"].astype(float)) / c,
                "clpos": (c - b["low"].astype(float)) / (b["high"].astype(float) - b["low"].astype(float)).replace(0, np.nan),
                "vol_rel": b["volume"].astype(float) / b["volume"].astype(float).rolling(30, min_periods=10).mean().shift(1),
                "sd30": sd30,
                "sdrel": sd30 / sd30.rolling(90, min_periods=30).median(),
            })
            df["pos"] = np.arange(len(df))
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["f1"].mean()
    D["x1"] = D["f1"] - D["coin"].map(drift)
    D["day"] = D["ts"].dt.floor("D")

    def clus(sub, col="x1"):
        s = sub.dropna(subset=[col])
        if len(s) < 10:
            return pd.Series({"n": len(s), "days": 0, "mean%": np.nan, "t_day": np.nan})
        g = s.groupby("day")[col].agg(["sum", "count"])
        m = s[col].mean()
        dev = s[col] - m
        gs = dev.groupby(s["day"]).sum()
        G = len(gs)
        se = np.sqrt((gs ** 2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"n": len(s), "days": G, "mean%": 100 * m, "t_day": m / se})

    out = {}
    D["zb"] = pd.cut(D["z"], [-np.inf, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3, np.inf])
    out["next-day excess by z bucket"] = D.groupby("zb", observed=True).apply(clus)
    dn = D[D["z"] < 0].copy()
    dn["trb"] = pd.cut(dn["tr60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    dn["zb2"] = pd.cut(dn["z"], [-np.inf, -2, -1, 0], labels=["<-2", "-2..-1", "-1..0"])
    out["down days: trend x z"] = dn.groupby(["trb", "zb2"], observed=True).apply(clus)
    dn["agb"] = np.where(dn["sdrel"] > 1, "agitated", "calm")
    dn.loc[dn["sdrel"].isna(), "agb"] = np.nan
    out["down days: agitation x z"] = dn.groupby(["agb", "zb2"], observed=True).apply(clus)
    dn["cpb"] = pd.cut(dn["clpos"], [-0.01, 0.25, 0.6, 1.01], labels=["close low", "mid", "close high"])
    out["down days z<-1: close position"] = dn[dn["z"] < -1].groupby("cpb", observed=True).apply(clus)
    dn["vb"] = pd.cut(dn["vol_rel"], [0, 0.8, 1.3, np.inf], labels=["low vol", "normal", "high vol"])
    out["down days z<-1: volume"] = dn[dn["z"] < -1].groupby("vb", observed=True).apply(clus)
    dn["r5b"] = pd.cut(dn["r5"], [-np.inf, -0.1, 0, np.inf], labels=["5d<-10%", "5d -10..0", "5d>0"])
    out["down days z<-1: prior 5d"] = dn[dn["z"] < -1].groupby("r5b", observed=True).apply(clus)
    D["wd"] = D["ts"].dt.dayofweek
    out["down z<-1: by weekday"] = D[D["z"] < -1].groupby("wd").apply(clus)
    out["all days: by weekday"] = D.groupby("wd").apply(clus)
    # 3-day horizon after falls, non-overlapping grid
    g3 = D[D["pos"] % 3 == 0].copy()
    d3 = g3.groupby("coin")["f3"].mean()
    g3["x3"] = g3["f3"] - g3["coin"].map(d3)
    out["3d excess by z (grid)"] = g3.groupby(pd.cut(g3["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf]), observed=True).apply(lambda s: clus(s, "x3"))
    out["by coin, z<-1"] = D[D["z"] < -1].groupby("coin").apply(clus)
    out["by window, z<-1"] = D[D["z"] < -1].groupby("win").apply(clus)
    # book side
    days = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; days.append(d)
    DD = pd.concat(days)
    bk = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    hd = DD.groupby(["win", "day"])["coin_return"].mean().dropna()
    out["book by window: mean%, sd%"] = pd.DataFrame({"book_mean%": bk.groupby(level=0).mean() * 100,
                                                      "hold_mean%": hd.groupby(level=0).mean() * 100,
                                                      "book_sd%": bk.groupby(level=0).std() * 100})
    out["corr book vs hold daily"] = float(np.corrcoef(bk.values, hd.reindex(bk.index).fillna(0).values)[0, 1])
    return out
