def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            b["fwd"] = c.shift(-H) / c - 1
            b["r1"] = c.pct_change()
            b["r5p"] = c / c.shift(5) - 1
            b["r20"] = c / c.shift(20) - 1
            b["r60"] = c / c.shift(60) - 1
            b["vr"] = np.log(v.rolling(30).mean() / v.rolling(30).mean().shift(30))
            b["vol30"] = b["r1"].rolling(30).std()
            b["vol5"] = b["r1"].rolling(5).std()
            b["vr5"] = np.log(v.rolling(5).mean() / v.rolling(30).mean())
            b["falling"] = (b["regime"] == "unknown").astype(int)
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            b["coin"] = coin; b["win"] = w
            g = b.iloc[::H]
            g = g[g["fwd"].notna()]
            rows.append(g)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["fwd"].mean()
    d["ex"] = d["fwd"] - d["coin"].map(drift)
    def summ(x, col="ex"):
        s = x[col].dropna()
        return pd.Series({"n": len(s), "mean%": 100 * s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out = {}
    out["by regime"] = d.groupby("falling").apply(summ)
    f = d[d.falling == 1].copy(); nf = d[d.falling == 0].copy()
    for name, col in [("vr", "vr"), ("r20", "r20"), ("r5p", "r5p"), ("vol30", "vol30"), ("vr5", "vr5"), ("r60", "r60")]:
        f["q"] = pd.qcut(f[col], 5, labels=False, duplicates="drop")
        out["falling by " + name + " quintile"] = f.groupby("q").apply(summ)
        nf["q"] = pd.qcut(nf[col], 5, labels=False, duplicates="drop")
        out["notfalling by " + name + " quintile"] = nf.groupby("q").apply(summ)
    out["all by r5p quintile"] = d.assign(q=pd.qcut(d["r5p"], 5, labels=False)).groupby("q").apply(summ)
    out["falling by weekday"] = f.groupby("wd").apply(summ)
    out["falling by year"] = f.groupby("yr").apply(summ)
    out["falling by coin"] = f.groupby("coin").apply(summ)
    # book daily returns
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window"] = bk.groupby(level=0).agg(["mean", "std", "count"]) * 1
    return out
