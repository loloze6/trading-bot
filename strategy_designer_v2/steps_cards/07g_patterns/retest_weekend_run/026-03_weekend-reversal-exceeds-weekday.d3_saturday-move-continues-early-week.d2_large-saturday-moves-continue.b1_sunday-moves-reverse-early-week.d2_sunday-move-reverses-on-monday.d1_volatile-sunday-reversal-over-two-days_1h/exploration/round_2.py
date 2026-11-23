def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp","close"]].copy()
            b["timestamp"] = pd.to_datetime(b["timestamp"], utc=True)
            b = b.reset_index(drop=True)
            c = b["close"]
            r24 = c / c.shift(24) - 1
            scale = r24.abs().rolling(720, min_periods=360).mean()
            r1 = c.pct_change()
            vol = r1.rolling(720, min_periods=360).std()
            df = pd.DataFrame({"ts": b["timestamp"], "z": r24/scale, "r24": r24, "vol": vol,
                               "f24": c.shift(-24)/c - 1, "f12": c.shift(-12)/c - 1})
            df = df.iloc[::24].dropna()
            df["coin"] = coin; df["w"] = w
            df["hr"] = df["ts"].dt.hour; df["wd"] = df["ts"].dt.weekday; df["year"] = df["ts"].dt.year
            rows.append(df)
    d = pd.concat(rows)
    d["f24x"] = d["f24"] - d.groupby("coin")["f24"].transform("mean")
    d["volq"] = d.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    def slope(g, y="f24x", x="z"):
        g = g.dropna(subset=[x, y])
        if len(g) < 30: return pd.Series({"n": len(g), "slope%": np.nan, "t": np.nan})
        s = stats.linregress(g[x], g[y]*100)
        return pd.Series({"n": len(g), "slope%": s.slope, "t": s.slope/s.stderr})
    res = {}
    res["grid24_all"] = slope(d)
    res["grid24_by_volthird"] = d.groupby("volq").apply(slope)
    res["grid24_by_year"] = d.groupby("year").apply(slope)
    res["grid24_by_coin"] = d.groupby("coin").apply(slope)
    res["grid24_by_weekday_of_start"] = d.groupby("wd").apply(slope)
    up = d[d["z"] > 0]; dn = d[d["z"] < 0]
    res["grid24_rises_only"] = slope(up); res["grid24_falls_only"] = slope(dn)
    d["zq"] = d.groupby("coin")["z"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    res["grid24_zquintile_f24x%"] = d.groupby("zq").agg(n=("z","size"), z=("z","mean"), f24x=("f24x", lambda x: x.mean()*100), t=("f24x", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    # volatility-scaled: does slope in % grow with vol? interaction
    d["zv"] = d["z"] * d["vol"] / d.groupby("coin")["vol"].transform("mean")
    res["grid24_z_times_relvol"] = slope(d, x="zv")
    # book daily returns by weekday
    dd = pd.concat([t.assign(coin=c) for c, ws in data["days"].items() for t in ws.values()])
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    res["book_by_weekday"] = dd.groupby("wd").agg(n=("book_return","count"), mean_bp=("book_return", lambda x: x.mean()*1e4), t=("book_return", lambda x: x.mean()/(x.std()/np.sqrt(x.count()))))
    return res
