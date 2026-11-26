def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            b["fwd"] = c.shift(-H) / c - 1
            b["r20"] = c / c.shift(20) - 1
            b["r60"] = c / c.shift(60) - 1
            b["r5p"] = c / c.shift(5) - 1
            b["vr"] = np.log(v.rolling(30).mean() / v.rolling(30).mean().shift(30))
            b["vol30"] = r1.rolling(30).std()
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            b["coin"] = coin; b["win"] = w
            g = b.iloc[::H]
            rows.append(g[g["fwd"].notna()])
    d = pd.concat(rows, ignore_index=True)
    d["ex"] = d["fwd"] - d["coin"].map(d.groupby("coin")["fwd"].mean())
    d["trend"] = np.where(d["r60"] > 0.10, "rising", np.where(d["r60"] < -0.10, "falling", "choppy"))
    def ct(x):
        x = x.dropna(subset=["ex"])
        if len(x) < 5: return pd.Series({"n": len(x), "days": 0, "mean%": np.nan, "t_day": np.nan})
        m = x["ex"].mean(); s = (x["ex"] - m).groupby(x["day"]).sum(); D = len(s)
        se = np.sqrt((s ** 2).sum() * D / (D - 1)) / len(x)
        return pd.Series({"n": len(x), "days": D, "mean%": 100 * m, "t_day": m / se})
    out = {}
    for tr in ["rising", "choppy", "falling"]:
        x = d[d.trend == tr].copy()
        for col in ["vr", "r20", "r5p"]:
            x["q"] = pd.qcut(x[col], 5, labels=False, duplicates="drop")
            out[tr + " by " + col + " quintile"] = x.groupby("q").apply(ct)
    x = d[d.trend != "falling"].copy()
    x["q"] = pd.qcut(x["r20"], 5, labels=False)
    out["notfalling r20 q by year"] = x[x.q == 0].groupby("yr").apply(ct)
    out["notfalling r20 q0 by vr half"] = x[x.q == 0].assign(h=lambda z: z.vr < z.vr.median()).groupby("h").apply(ct)
    out["notfalling r20 q0 by agitation half"] = x[x.q == 0].assign(h=lambda z: z.vol30 > x.vol30.median()).groupby("h").apply(ct)
    f = d[d.trend == "falling"].copy()
    f["q"] = pd.qcut(f["vr"], 5, labels=False)
    out["falling vr q0 by year"] = f[f.q == 0].groupby("yr").apply(ct)
    out["falling weekday clustered"] = f.groupby("wd").apply(ct)
    # rank correlations of vr with ex inside each trend, clustered sign
    out["spearman vr-ex by trend"] = d.groupby("trend").apply(lambda z: pd.Series({"rho": z[["vr", "ex"]].corr(method="spearman").iloc[0, 1], "n": z[["vr","ex"]].dropna().shape[0]}))
    out["spearman r20-ex by trend"] = d.groupby("trend").apply(lambda z: pd.Series({"rho": z[["r20", "ex"]].corr(method="spearman").iloc[0, 1], "n": z[["r20","ex"]].dropna().shape[0]}))
    # book: largest loss days and gains, position side
    return out
