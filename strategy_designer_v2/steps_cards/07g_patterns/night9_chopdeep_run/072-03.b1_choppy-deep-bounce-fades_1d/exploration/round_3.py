def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; out = {}
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            hi20 = b["high"].rolling(20).max()
            sd20 = r1.rolling(20).std()
            depth = (hi20 - cl) / hi20 / sd20
            sd30 = r1.rolling(30).std()
            ret60 = cl / cl.shift(60) - 1
            n = len(b)
            for h in (5, 10):
                fwd = cl.shift(-h) / cl - 1
                idx = np.arange(0, n, h)
                rows.append(pd.DataFrame({"coin": c, "w": w, "h": h,
                    "depth": depth.iloc[idx].values, "up": (r1.iloc[idx] > 0).values,
                    "chop": (b["regime"].iloc[idx] != "chop").values,
                    "sd30": sd30.iloc[idx].values, "ret60": ret60.iloc[idx].values,
                    "day": pd.to_datetime(b["timestamp"].iloc[idx]).dt.floor("D").values,
                    "yr": pd.to_datetime(b["timestamp"].iloc[idx]).dt.year.values,
                    "fwd": fwd.iloc[idx].values}))
    D = pd.concat(rows).dropna(subset=["fwd", "depth", "sd30"])
    D["drift"] = D.groupby(["coin", "h"])["fwd"].transform("mean")
    D["un"] = D["fwd"] - D["drift"]
    D["vr"] = D.groupby(["coin", "h"])["sd30"].transform(lambda s: s.rank(pct=True))
    D["dz"] = D.groupby(["coin", "h"])["depth"].transform(lambda s: (s - s.mean()) / s.std())
    D["vz"] = D.groupby(["coin", "h"])["vr"].transform(lambda s: (s - s.mean()) / s.std())
    D["agit"] = D["vr"] > 0.5
    D["trend"] = np.where(D["chop"], "choppy", np.where(D["ret60"] > 0, "rising", "falling"))
    def ct(g, xcol):
        n = len(g); m = g["un"].mean()
        dev = g.assign(d=g["un"] - m).groupby("day")["d"].sum()
        se = np.sqrt((dev**2).sum()) / n * np.sqrt(len(dev) / max(len(dev) - 1, 1))
        x = g[xcol]; y = g["un"]
        if n < 6: return pd.Series({"n": n})
        b1 = np.cov(x, y)[0, 1] / x.var()
        res = y - y.mean() - b1 * (x - x.mean())
        sb = np.sqrt((res**2).sum() / (n - 2) / ((x - x.mean())**2).sum())
        return pd.Series({"n": n, "days": len(dev), "mean_un": m, "t": m / se, "slope": b1, "t_slope": b1 / sb})
    Dc = D[D.chop]
    out["choppy: slope on swing rank, by h"] = Dc.groupby("h").apply(ct, "vz").round(4)
    Dc5 = Dc[Dc.h == 5].copy()
    Dc5["vq"] = pd.qcut(Dc5["vr"], 4, labels=False)
    out["choppy h5: by swing-rank quartile"] = Dc5.groupby("vq").apply(ct, "vz").round(4)
    out["choppy h5 swing slope by year"] = Dc5.groupby("yr").apply(ct, "vz").round(4)
    out["choppy h5 swing slope by coin"] = Dc5.groupby("coin").apply(ct, "vz").round(4)
    out["depth slope by trend x agit, h5/h10"] = D.groupby(["h", "trend", "agit"]).apply(ct, "dz").round(4)
    Dcc = Dc[(~Dc.agit)]
    out["choppy calm depth slope by h x year"] = Dcc.groupby(["h", "yr"]).apply(ct, "dz").round(4)
    out["choppy calm depth slope by h x up"] = Dcc.groupby(["h", "up"]).apply(ct, "dz").round(4)
    return out
