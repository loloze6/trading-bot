def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            inprof = (b["regime"] == "unknown").values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            for i in range(0, n, 7):
                if i + 7 >= n or i < 7:
                    continue
                past7 = c[i] / c[i-7] - 1
                fut7 = c[i+7] / c[i] - 1
                tr60 = c[i] / c[i-60] - 1 if i >= 60 else np.nan
                vol30 = np.nanstd(r1[max(1, i-29):i+1]) if i >= 30 else np.nan
                rows.append(dict(coin=coin, w=w, past7=past7, fut7=fut7, tr60=tr60, vol30=vol30,
                                 inprof=inprof[i], past1=r1[i]))
            ts = pd.to_datetime(b["timestamp"])
            for i in range(1, n - 1):
                daily.append(dict(coin=coin, w=w, r=r1[i], nxt=c[i+1]/c[i]-1, wd=ts.iloc[i].dayofweek,
                                  rng=(b["high"].iloc[i]-b["low"].iloc[i])/c[i-1],
                                  clpos=(c[i]-b["low"].iloc[i])/max(b["high"].iloc[i]-b["low"].iloc[i],1e-12)))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["fut7"].mean()
    g["ex"] = g["fut7"] - g["coin"].map(drift)
    g["z"] = g.groupby("coin")["past7"].transform(lambda s: s / s.std())
    def corr(d):
        d = d.dropna(subset=["past7", "ex"])
        if len(d) < 10: return pd.Series(dict(n=len(d)))
        r = np.corrcoef(d["past7"], d["ex"])[0, 1]
        t = r * np.sqrt((len(d)-2)/(1-r*r))
        sl = stats.linregress(d["z"], d["ex"]).slope
        return pd.Series(dict(n=len(d), r=r, t=t, slope_per_sd=sl))
    out["all"] = corr(g)
    out["by_inprof"] = g.groupby("inprof").apply(corr)
    g["trend"] = pd.cut(g["tr60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    out["by_trend"] = g.groupby("trend").apply(corr)
    g["side"] = np.where(g["past7"] > 0, "up", "down")
    out["by_side"] = g.groupby("side").apply(corr)
    out["by_trend_side"] = g.groupby(["trend", "side"]).apply(corr)
    g["volq"] = g.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["by_volq"] = g.groupby("volq").apply(corr)
    out["by_coin"] = g.groupby("coin").apply(corr)
    out["by_window"] = g.groupby("w").apply(corr)
    g["pq"] = g.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["quintile_ex"] = g.groupby("pq")["ex"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    d = pd.DataFrame(daily).dropna()
    d["zr"] = d.groupby("coin")["r"].transform(lambda s: s / s.std())
    d["rq"] = d.groupby("coin")["zr"].transform(lambda s: pd.qcut(s, 10, labels=False))
    out["daily_next_by_decile"] = d.groupby("rq")["nxt"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["daily_by_weekday"] = d.groupby("wd")["nxt"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    d["cq"] = pd.cut(d["clpos"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    out["next_by_closepos"] = d.groupby("cq")["nxt"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    return out
