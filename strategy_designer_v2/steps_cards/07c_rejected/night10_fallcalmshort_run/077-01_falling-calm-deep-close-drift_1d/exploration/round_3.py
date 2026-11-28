def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float)
            r = c.pct_change(); sd = r.rolling(20).std()
            feats = {}
            for k in [5, 10, 20]:
                Hk = h.rolling(k).max()
                feats[f"d{k}"] = ((c - Hk) / Hk) / sd
            for k in [3, 5, 10]:
                feats[f"r{k}s"] = (c / c.shift(k) - 1) / (sd * np.sqrt(k))
            n = len(b)
            for hz in [3, 5]:
                fwd = c.shift(-hz) / c - 1
                for i in range(0, n, hz):
                    if np.isnan(fwd.iloc[i]) or np.isnan(sd.iloc[i]) or i < 20:
                        continue
                    row = dict(coin=coin, hz=hz, ret=fwd.iloc[i], regime=b["regime"].iloc[i],
                               day=str(b["timestamp"].iloc[i])[:10])
                    for kk, v in feats.items(): row[kk] = v.iloc[i]
                    rows.append(row)
    df = pd.DataFrame(rows)
    drift = df.groupby(["coin", "hz"])["ret"].mean().rename("drift")
    df = df.join(drift, on=["coin", "hz"]); df["ex"] = df["ret"] - df["drift"]
    def ct(d, x, y="ex"):
        d = d.dropna(subset=[x, y])
        if len(d) < 15: return np.nan, np.nan, len(d), np.nan
        X = d[x].values; Y = d[y].values
        xm = X - X.mean(); b1 = (xm * (Y - Y.mean())).sum() / (xm**2).sum()
        e = Y - Y.mean() - b1 * xm
        s = pd.Series(xm * e).groupby(d["day"].values).sum()
        G = len(s); v = (s**2).sum() / (xm**2).sum()**2 * G / (G - 1)
        return b1, b1 / np.sqrt(v), len(d), G
    out = {}
    res = []
    for reg in ["unknown", "chop"]:
        for hz in [3, 5]:
            d = df[(df.regime == reg) & (df.hz == hz)]
            for x in ["d5", "d10", "d20", "r3s", "r5s", "r10s"]:
                s, t, nn, G = ct(d, x)
                res.append(dict(reg=reg, hz=hz, x=x, n=nn, days=G, slope=s, t_cl=t))
    out["slopes"] = pd.DataFrame(res)
    fc = df[(df.regime == "unknown")].copy()
    fc["year"] = fc["day"].str[:4]
    res = []
    for hz in [3, 5]:
        for x in ["d5", "r5s"]:
            for grp in ["coin", "year"]:
                for g, d in fc[fc.hz == hz].groupby(grp):
                    s, t, nn, G = ct(d, x)
                    res.append(dict(hz=hz, x=x, grp=g, n=nn, slope=s, t_cl=t))
    out["split"] = pd.DataFrame(res)
    d3 = fc[fc.hz == 3].copy(); d3["q"] = pd.qcut(d3["d5"], 4, labels=False)
    out["fc3_by_d5"] = d3.groupby("q").agg(dep=("d5", "mean"), ex=("ex", "mean"), tot=("ret", "mean"), n=("ex", "size"))
    d5 = fc[fc.hz == 5].copy(); d5["q"] = pd.qcut(d5["r5s"], 4, labels=False)
    out["fc5_by_r5s"] = d5.groupby("q").agg(r=("r5s", "mean"), ex=("ex", "mean"), tot=("ret", "mean"), n=("ex", "size"))
    return out
