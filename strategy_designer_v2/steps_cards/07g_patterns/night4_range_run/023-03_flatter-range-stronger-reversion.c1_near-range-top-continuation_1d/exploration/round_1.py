def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float)
            hi = c.rolling(30, min_periods=30).max(); lo = c.rolling(30, min_periods=30).min()
            rp = (c - (hi + lo) / 2) / ((hi - lo) / 2)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=20).std()
            ret30 = c / c.shift(30) - 1
            ret10b = c / c.shift(10) - 1
            ret3b = c / c.shift(3) - 1
            width = (hi - lo) / c
            fwd10 = c.shift(-10) / c - 1
            fwd3 = c.shift(-3) / c - 1
            n = len(d)
            for i in range(0, n, 10):
                rows.append(dict(coin=coin, w=w, i=i, fc=d["forecast"].iloc[i], rp=rp.iloc[i],
                                 vol=vol20.iloc[i], ret30=ret30.iloc[i], ret10b=ret10b.iloc[i],
                                 ret3b=ret3b.iloc[i], width=width.iloc[i], fwd10=fwd10.iloc[i],
                                 fwd3=fwd3.iloc[i], wd=pd.Timestamp(d["timestamp"].iloc[i]).weekday(),
                                 year=pd.Timestamp(d["timestamp"].iloc[i]).year))
    g = pd.DataFrame(rows)
    cm = g.groupby("coin")["fwd10"].transform("mean")
    g["ex"] = g["fwd10"] - cm
    g["sdz"] = g.groupby("coin")["fwd10"].transform("std")
    out = {}
    def summ(gr, col="ex"):
        a = gr[col].dropna()
        return pd.Series(dict(n=len(a), mean=a.mean(), t=a.mean() / (a.std() / np.sqrt(len(a))) if len(a) > 2 else np.nan))
    gg = g.dropna(subset=["fc", "ex"])
    gg["fq"] = pd.qcut(gg["fc"], 5, labels=False, duplicates="drop")
    out["fwd10_ex by forecast quintile"] = gg.groupby("fq").apply(summ)
    h = g.dropna(subset=["rp", "ex", "ret30", "vol", "width"]).copy()
    h["rpq"] = pd.qcut(h["rp"], 3, labels=["low", "mid", "top"])
    h["trend"] = pd.qcut(h["ret30"].abs() / (h["vol"] * np.sqrt(30)), 2, labels=["flat", "trend"])
    out["ex by rangepos x trend"] = h.groupby(["trend", "rpq"]).apply(summ)
    h["volq"] = pd.qcut(h.groupby("coin")["vol"].rank(pct=True), 3, labels=["lowvol", "midvol", "hivol"])
    out["ex by rangepos x vol"] = h.groupby(["volq", "rpq"]).apply(summ)
    h["wq"] = pd.qcut(h.groupby("coin")["width"].rank(pct=True), 3, labels=["narrow", "mid", "wide"])
    out["ex by rangepos x width"] = h.groupby(["wq", "rpq"]).apply(summ)
    k = g.dropna(subset=["ret10b", "ex", "vol"]).copy()
    k["z10"] = k["ret10b"] / (k["vol"] * np.sqrt(10))
    k["zq"] = pd.qcut(k["z10"], 5, labels=False)
    out["ex by past 10d z quintile"] = k.groupby("zq").apply(summ)
    k["z30"] = k["ret30"] / (k["vol"] * np.sqrt(30))
    k2 = k.dropna(subset=["z30"]).copy(); k2["zq"] = pd.qcut(k2["z30"], 5, labels=False)
    out["ex by past 30d z quintile"] = k2.groupby("zq").apply(summ)
    k3 = k.dropna(subset=["ret3b"]).copy(); k3["z3"] = k3["ret3b"] / (k3["vol"] * np.sqrt(3))
    k3["zq"] = pd.qcut(k3["z3"], 5, labels=False)
    k3["ex3"] = k3["fwd3"] - k3.groupby("coin")["fwd3"].transform("mean")
    out["ex3 by past 3d z quintile"] = k3.groupby("zq").apply(lambda x: summ(x, "ex3"))
    out["ex by year"] = g.groupby("year").apply(summ)
    out["slope rp->ex by coin"] = h.groupby("coin").apply(lambda x: pd.Series(dict(n=len(x), slope=stats.linregress(x["rp"], x["ex"]).slope, t=stats.linregress(x["rp"], x["ex"]).slope / stats.linregress(x["rp"], x["ex"]).stderr)))
    # book days
    dl = []
    for coin, ws in days.items():
        for w, df in ws.items():
            dd = df.copy(); dd["coin"] = coin; dd["w"] = w
            dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
            dl.append(dd)
    D = pd.concat(dl)
    out["book & coin daily by weekday"] = D.groupby("wd").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book & coin daily by year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    return out
