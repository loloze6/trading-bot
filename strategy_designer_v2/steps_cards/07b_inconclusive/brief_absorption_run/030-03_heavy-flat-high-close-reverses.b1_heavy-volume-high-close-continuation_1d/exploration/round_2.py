def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        g = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c)-10, 10):
                g.append(c[i+10]/c[i]-1)
        drift[coin] = np.mean(g)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            v = df["volume"].values
            rng = hi - lo
            cl = np.where(rng > 0, (2*c - hi - lo)/np.where(rng>0,rng,1), 0)
            vr = v / pd.Series(v).shift(1).rolling(20, min_periods=20).mean().values
            r20 = pd.Series(c).pct_change(20).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            for i in range(n):
                rows.append({"coin": coin, "w": w, "i": i, "cell": i//10, "cl": cl[i], "vr": vr[i],
                             "r20": r20[i], "year": yr[i], "f": df["forecast"].values[i],
                             "u10": (c[i+10]/c[i]-1 - drift[coin]) if i+10 < n else np.nan})
    D = pd.DataFrame(rows).dropna(subset=["u10","vr"])
    def summ(x):
        x = x.dropna()
        if len(x) < 3: return pd.Series({"n": len(x), "mean": np.nan, "t": np.nan})
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))})
    out = {}
    # one per cell: heaviest-volume day of each cell
    top = D.sort_values("vr", ascending=False).groupby(["coin","w","cell"]).head(1).copy()
    top["vb"] = pd.cut(top["vr"], [0,1,1.5,2,3,100])
    out["heaviest day per cell, by vr bucket"] = top.groupby("vb")["u10"].apply(summ).unstack()
    hv = top[top["vr"] >= 2].copy()
    out["heavy: high-close(cl>0) minus low-close welch"] = pd.Series({
        "diff": hv[hv.cl>0].u10.mean() - hv[hv.cl<=0].u10.mean(),
        "t": stats.ttest_ind(hv[hv.cl>0].u10, hv[hv.cl<=0].u10, equal_var=False)[0],
        "n_hi": (hv.cl>0).sum(), "n_lo": (hv.cl<=0).sum()})
    hh = hv[hv.cl > 0].copy()
    out["heavy high-close by vr bucket"] = hh.groupby(pd.cut(hh["vr"],[2,2.5,3.5,100]))["u10"].apply(summ).unstack()
    out["heavy high-close by cl bucket"] = hh.groupby(pd.cut(hh["cl"],[0,0.5,0.8,1.01]))["u10"].apply(summ).unstack()
    out["heavy high-close spearman cl*vr vs u10"] = float(stats.spearmanr(hh["cl"]*hh["vr"], hh["u10"])[0])
    out["heavy all spearman vr vs u10"] = float(stats.spearmanr(hv["vr"], hv["u10"])[0])
    out["heavy all by year"] = hv.groupby("year")["u10"].apply(summ).unstack()
    out["heavy all by coin"] = hv.groupby("coin")["u10"].apply(summ).unstack()
    hv["trend"] = np.where(hv["r20"] > 0, "up20", "down20")
    out["heavy by prior 20d trend and cl sign"] = hv.groupby(["trend", hv["cl"]>0])["u10"].apply(summ).unstack()
    out["heavy cells: forecast>=2 share"] = float((hv["f"] >= 2).mean())
    return out
