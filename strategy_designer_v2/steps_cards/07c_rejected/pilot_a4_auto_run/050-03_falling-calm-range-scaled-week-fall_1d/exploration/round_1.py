def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; rng = (b["high"] - b["low"]) / c
            b["r7"] = c / c.shift(7) - 1
            b["mrng"] = rng.rolling(30).mean()
            b["sc"] = b["r7"] / b["mrng"]
            b["inprof"] = b["regime"].isin(["trending", "unknown"])
            for h in [1, 3, 5, 10]:
                b[f"f{h}"] = c.shift(-h) / c - 1
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","win","pos","year","r7","sc","inprof","regime","f1","f3","f5","f10"]])
    d = pd.concat(rows, ignore_index=True)
    out = {}
    out["regime counts"] = d.groupby(["coin","regime"]).size().unstack(fill_value=0)
    # normal drift per coin per h on grid
    drift = {}
    for h in [1,3,5,10]:
        g = d[d.pos % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
    p = d[d.inprof & d.sc.notna()].copy()
    p["q"] = pd.qcut(p["sc"], 5, labels=["q1 big fall","q2","q3","q4","q5 big rise"])
    res = []
    for h in [1,3,5,10]:
        g = p[p.pos % h == 0].copy()
        g["ab"] = g[f"f{h}"] - g["coin"].map(drift[h])
        for q, gg in g.groupby("q", observed=True):
            x = gg["ab"].dropna()
            res.append({"h": h, "q": q, "n": len(x), "mean_ab_long": x.mean(),
                        "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                        "mean_total": gg[f"f{h}"].mean(), "sc_mean": gg.sc.mean()})
        x = g.dropna(subset=["ab"])
        r, pv = stats.spearmanr(x.sc, x.ab)
        res.append({"h": h, "q": "spearman sc vs ab", "n": len(x), "mean_ab_long": r, "t": pv})
    out["in falling calm, by scaled 7d quintile (long dir)"] = pd.DataFrame(res)
    # by coin, h=3, falls vs rises
    g = p[p.pos % 3 == 0].copy(); g["ab"] = g.f3 - g.coin.map(drift[3])
    g["side"] = np.where(g.sc < 0, "fell", "rose")
    out["h3 by coin/side"] = g.groupby(["coin","side"]).ab.agg(["count","mean"])
    g5 = p[p.pos % 5 == 0].copy(); g5["ab"] = g5.f5 - g5.coin.map(drift[5])
    g5["side"] = np.where(g5.sc < 0, "fell", "rose")
    out["h5 by year/side"] = g5.groupby(["year","side"]).ab.agg(["count","mean"]).unstack()
    out["drift"] = pd.DataFrame(drift)
    return out
