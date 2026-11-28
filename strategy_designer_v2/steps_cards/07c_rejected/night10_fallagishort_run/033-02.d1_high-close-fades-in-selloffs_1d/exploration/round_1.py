def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["clv"] = (b["close"] - b["low"]) / rng
            b["dayret"] = b["close"] / b["open"] - 1
            b["range_rel"] = rng / b["close"]
            for h in (1, 2, 3, 5):
                b[f"r{h}"] = b["close"].shift(-h) / b["close"] - 1
            b["pos"] = np.arange(len(b))
            b["inprof"] = (b["regime"] != "chop")
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["fc"] = b["forecast"]
            rows.append(b[["coin","win","year","pos","clv","dayret","range_rel","r1","r2","r3","r5","inprof","fc","timestamp"]])
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["r1"].mean()
    d["ex1"] = d["r1"] - d["coin"].map(drift)
    for h in (2,3,5):
        dm = {}
        for c in d.coin.unique():
            s = d[(d.coin==c) & (d.pos % h == 0)][f"r{h}"]
            dm[c] = s.mean()
        d[f"ex{h}"] = d[f"r{h}"] - d["coin"].map(dm)
    d["day"] = pd.to_datetime(d["timestamp"]).dt.floor("D")
    out = {}
    p = d[d.inprof & d.clv.notna()].copy()
    out["counts"] = pd.Series({"all": len(d), "inprof": len(p), "inprof_fc_nonzero": int((p.fc < 0).sum())})
    p["q"] = pd.qcut(p["clv"], 5, labels=False)
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean_%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    for h in (1,2,3,5):
        col = f"ex{h}"
        sub = p if h == 1 else p[p.pos % h == 0]
        out[f"inprof_clv_quint_ex{h}"] = sub.groupby("q").apply(lambda g: summ(g, col))
    o = d[(~d.inprof) & d.clv.notna()].copy()
    o["q"] = pd.qcut(o["clv"], 5, labels=False)
    out["outprof_clv_quint_ex1"] = o.groupby("q").apply(lambda g: summ(g, "ex1"))
    # correlation of clv with next-day excess in profile by coin, window-year
    def corr(g):
        x = g[["clv","ex1"]].dropna()
        r = x.corr().iloc[0,1] if len(x)>5 else np.nan
        return pd.Series({"n": len(x), "corr": r, "t": r*np.sqrt((len(x)-2)/(1-r**2)) if len(x)>5 else np.nan})
    out["inprof_corr_by_coin"] = p.groupby("coin").apply(corr)
    out["inprof_corr_by_year"] = p.groupby("year").apply(corr)
    # day return sign / range size interaction
    p["dq"] = pd.qcut(p["dayret"], 5, labels=False)
    out["inprof_dayret_quint_ex1"] = p.groupby("dq").apply(lambda g: summ(g, "ex1"))
    p["rq"] = pd.qcut(p["range_rel"], 3, labels=False)
    out["inprof_range_tercile_x_clvhigh_ex1"] = p.groupby(["rq", p.clv > 0.5]).apply(lambda g: summ(g, "ex1"))
    out["inprof_dayret_quint_ex3"] = p[p.pos%3==0].groupby("dq").apply(lambda g: summ(g, "ex3"))
    return out
