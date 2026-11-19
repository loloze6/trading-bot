def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = []; G = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            p24 = c / c.shift(24) - 1
            vol24 = r1.rolling(168).std()
            nxt2 = c.shift(-2) / c - 1  # return over hours 21 and 22 when taken at close of hour 20
            sel = (ts.dt.hour == 20).values
            H.append(pd.DataFrame({"coin": coin, "year": ts.dt.year[sel].values,
                                   "p24z": (p24 / (vol24 * np.sqrt(24)))[sel].values,
                                   "vol": vol24[sel].values, "y": nxt2[sel].values}))
            past = c / c.shift(72) - 1; vol = r1.rolling(72).std()
            gain = r1.clip(lower=0); sg = gain.rolling(72).sum()
            top3g = gain.rolling(72).apply(lambda x: np.sort(x)[-3:].sum(), raw=True)
            fwd = c.shift(-72) / c - 1
            idx = np.arange(0, len(b), 72)
            G.append(pd.DataFrame({"coin": coin, "past": past.iloc[idx].values, "fwd": fwd.iloc[idx].values,
                                   "zp": (past / (vol * np.sqrt(72))).iloc[idx].values,
                                   "grindG": (1 - top3g / sg).iloc[idx].values}))
    def tt(x):
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    h = pd.concat(H).dropna()
    h["ynorm"] = h["y"] / h["vol"]
    h["pq"] = h.groupby("coin")["p24z"].transform(lambda x: pd.qcut(x, 5, labels=False))
    h["vq"] = h.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 4, labels=False))
    out["h21-22 return by prior 24h z quintile"] = h.groupby("pq")["y"].apply(tt).unstack()
    out["h21-22 return by vol quartile"] = h.groupby("vq")["y"].apply(tt).unstack()
    out["h21-22 vol-normalised by vol quartile"] = h.groupby("vq")["ynorm"].apply(tt).unstack()
    out["h21-22 by coin (non-overlapping, daily)"] = h.groupby("coin")["y"].apply(tt).unstack()
    g = pd.concat(G).dropna()
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    up = g[g.past > 0].copy()
    up["gq"] = pd.qcut(up["grindG"], 4, labels=False)
    up["zq"] = pd.qcut(up["zp"], 3, labels=False)
    out["up: mean ex by zp tercile x grind quartile"] = up.pivot_table(index="zq", columns="gq", values="ex", aggfunc="mean")
    r = stats.spearmanr(g["zp"], g["ex"])
    out["all grid: spearman zp vs ex"] = pd.Series({"rho": r.correlation, "p": r.pvalue, "n": len(g)})
    return out
