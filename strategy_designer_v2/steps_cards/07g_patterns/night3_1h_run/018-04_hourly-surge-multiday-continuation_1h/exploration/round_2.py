def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]

    def tstat(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

    allrec = {h: [] for h in (24, 48, 72, 120)}
    for coin, wins in bars.items():
        per = {h: [] for h in allrec}
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            ret24 = c / c.shift(24) - 1
            m = ret24 / ret24.abs().rolling(720, min_periods=120).mean()
            near = c / c.rolling(720, min_periods=240).max() - 1
            rng = (c - c.rolling(720, min_periods=240).min()) / (c.rolling(720, min_periods=240).max() - c.rolling(720, min_periods=240).min())
            for h in per:
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(c), h)
                per[h].append(pd.DataFrame({"coin": coin, "w": w, "year": ts.iloc[idx].dt.year.values,
                                            "fwd": fwd.iloc[idx].values, "m": m.iloc[idx].values,
                                            "near": near.iloc[idx].values, "rng": rng.iloc[idx].values}))
        for h in per:
            d = pd.concat(per[h]).dropna(subset=["fwd"])
            d["unus"] = d["fwd"] - d["fwd"].mean()
            d["str"] = d["unus"] / d["fwd"].std()
            allrec[h].append(d)
    G = {h: pd.concat(v) for h, v in allrec.items()}

    def summ(d, by):
        r = d.groupby(by, observed=True).agg(n=("unus", "size"), mean_pct=("unus", lambda x: 100 * x.mean()),
                                             strength=("str", "mean"))
        r["t"] = d.groupby(by, observed=True)["unus"].apply(tstat)
        return r.round(4)

    mb = [-np.inf, -3, -2, -1, -0.5, 0, np.inf]
    for h in (24, 48, 72):
        out[f"{h}h fwd by 24h multiple"] = summ(G[h], pd.cut(G[h]["m"], mb))
    d = G[24]; dn = d[d["m"] <= -2].copy()
    out["24h after m<=-2, by coin"] = summ(dn, "coin")
    dn["half"] = np.where(dn["year"] <= 2021, "2018-21", "2022-25")
    out["24h after m<=-2, by period half"] = summ(dn, "half")
    neg = d[d["m"] < 0].dropna(subset=["m"])
    sl = stats.linregress(neg["m"], neg["str"])
    out["slope strength on m (m<0), 24h"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(neg)}).round(4)

    for h in (72, 120):
        g = G[h].dropna(subset=["rng"])
        out[f"{h}h fwd by position in 30d range"] = summ(g, pd.cut(g["rng"], [-0.01, 0.2, 0.4, 0.6, 0.8, 0.95, 1.0]))
    g = G[120].dropna(subset=["rng"]); top = g[g["rng"] > 0.8].copy()
    out["120h, top of range, by coin"] = summ(top, "coin")
    top["half"] = np.where(top["year"] <= 2021, "2018-21", "2022-25")
    out["120h, top of range, by half"] = summ(top, "half")
    sl2 = stats.linregress(g["rng"], g["str"])
    out["slope strength on range pos, 120h"] = pd.Series({"slope": sl2.slope, "t": sl2.slope / sl2.stderr, "n": len(g)}).round(4)
    return out
