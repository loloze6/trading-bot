def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; rng = (b["high"] - b["low"]) / c
            b["mrng"] = rng.rolling(30).mean()
            for L in [3, 7, 14]:
                b[f"sc{L}"] = (c / c.shift(L) - 1) / b["mrng"]
            b["inprof"] = b["regime"].isin(["trending", "unknown"])
            for h in [3, 5, 7, 10]:
                b[f"f{h}"] = c.shift(-h) / c - 1
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    drift = {h: d[d.pos % h == 0].groupby("coin")[f"f{h}"].mean() for h in [3,5,7,10]}
    p = d[d.inprof].copy()
    out = {}
    res = []
    for L in [3, 7, 14]:
        for h in [3, 5, 7, 10]:
            g = p[(p.pos % h == 0)].dropna(subset=[f"sc{L}", f"f{h}"]).copy()
            g["ab"] = g[f"f{h}"] - g.coin.map(drift[h])
            for side, gg in [("rise", g[g[f"sc{L}"] > 0]), ("fall", g[g[f"sc{L}"] < 0])]:
                if len(gg) < 8: continue
                # graded: weighted mean ab by |sc|, per-day summed
                wgt = gg[f"sc{L}"].abs()
                wm = (gg.ab * wgt).sum() / wgt.sum()
                dd = gg.groupby("day").ab.sum()
                r, pv = stats.spearmanr(gg[f"sc{L}"].abs(), gg.ab)
                top = gg[wgt >= wgt.median()].ab; bot = gg[wgt < wgt.median()].ab
                res.append({"L": L, "h": h, "side": side, "n": len(gg),
                            "mean_ab": gg.ab.mean(), "t_day": dd.mean()/(dd.std()/np.sqrt(len(dd))),
                            "w_by_size": wm, "spear_|sc|": r, "p": pv,
                            "top-bot": top.mean() - bot.mean()})
    out["long dir, falling calm, by lookback/horizon/side"] = pd.DataFrame(res)
    g = p[p.pos % 5 == 0].dropna(subset=["sc7","f5"]).copy()
    g["ab"] = g.f5 - g.coin.map(drift[5])
    g = g[g.sc7 > 0]
    g["big"] = np.where(g.sc7 >= g.sc7.median(), "big rise", "small rise")
    out["h5 rises by coin"] = g.groupby(["coin","big"]).ab.agg(["count","mean"]).unstack()
    out["h5 rises by year"] = g.groupby(["year","big"]).ab.agg(["count","mean"]).unstack()
    gf = p[p.pos % 5 == 0].dropna(subset=["sc7","f5"]).copy()
    gf["ab"] = gf.f5 - gf.coin.map(drift[5])
    gf = gf[gf.sc7 < 0]
    gf["big"] = np.where(gf.sc7 <= gf.sc7.median(), "big fall", "small fall")
    out["h5 falls by coin"] = gf.groupby(["coin","big"]).ab.agg(["count","mean"]).unstack()
    return out
