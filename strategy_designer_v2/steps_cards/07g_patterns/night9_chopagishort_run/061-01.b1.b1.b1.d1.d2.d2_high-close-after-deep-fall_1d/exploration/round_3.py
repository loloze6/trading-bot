def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            cl = (b["close"] - b["low"]) / rng
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            p20 = c / c.shift(20) - 1
            p60 = c / c.shift(60) - 1
            vol20 = r1.rolling(20).std()
            vs = p20 / (vol20 * np.sqrt(20))
            vrel = r1.rolling(30).std() / r1.rolling(60).std()
            fwd5 = c.shift(-5) / c - 1
            fwd2 = c.shift(-2) / c - 1
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, day=ts[i].normalize(), fwd=fwd5[i], fwd2=fwd2[i],
                                 cl=cl[i], p20=p20[i], p60=p60[i], vs=vs[i], vrel=vrel[i], yr=ts[i].year))
    d = pd.DataFrame(rows)
    for f in ["fwd", "fwd2"]:
        d["u_" + f] = d[f] - d["coin"].map(d.groupby("coin")[f].mean())
    def pooled(g, col="u_fwd"):
        x = g[[col, "day"]].dropna()
        n = len(x)
        if n < 5:
            return pd.Series(dict(n=n, days=np.nan, mean=np.nan, t=np.nan))
        m = x[col].mean()
        s = (x[col] - m).groupby(x["day"]).sum()
        D = len(s)
        se = np.sqrt((s ** 2).sum() * D / (D - 1)) / n
        return pd.Series(dict(n=n, days=D, mean=m, t=m / se))
    def slope(g, col="u_fwd", xcol="vs"):
        x = g[[col, xcol, "day"]].dropna()
        if len(x) < 20:
            return pd.Series(dict(n=len(x), slope=np.nan, t=np.nan))
        xc = x[xcol] - x[xcol].mean()
        b = (xc * x[col]).sum() / (xc ** 2).sum()
        e = x[col] - x[col].mean() - b * xc
        s = (xc * e).groupby(x["day"]).sum()
        D = len(s)
        se = np.sqrt((s ** 2).sum() * D / (D - 1)) / (xc ** 2).sum()
        return pd.Series(dict(n=len(x), days=D, slope=b, t=b / se))
    out = {}
    d["trend"] = pd.cut(d["p60"], [-10, -0.1, 0.1, 100], labels=["fall", "chop", "rise"])
    d["agit"] = np.where(d["vrel"] > 1, "agit", "calm")
    d.loc[d["vrel"].isna(), "agit"] = np.nan
    out["slope_vs_all"] = slope(d)
    out["slope_vs_by_trend"] = d.groupby("trend").apply(slope)
    out["slope_vs_by_trend_agit"] = d.groupby(["trend", "agit"]).apply(slope)
    out["slope_vs_chop_by_year"] = d[d.trend == "chop"].groupby("yr").apply(slope)
    ch = d[d.trend == "chop"]
    out["chop_vs_tercile"] = ch.groupby(pd.qcut(ch["vs"], 3, labels=False)).apply(pooled)
    out["chop_vs_tercile_fwd2"] = ch.groupby(pd.qcut(ch["vs"], 3, labels=False)).apply(lambda g: pooled(g, "u_fwd2"))
    hc = d[d["cl"] >= 0.8]
    out["hc_slope_p20"] = slope(hc, xcol="p20")
    out["hc_slope_p20_by_year"] = hc.groupby("yr").apply(lambda g: slope(g, xcol="p20"))
    out["hc_slope_p20_by_trend"] = hc.groupby("trend").apply(lambda g: slope(g, xcol="p20"))
    out["nonhc_slope_p20"] = slope(d[d["cl"] < 0.8], xcol="p20")
    return out
