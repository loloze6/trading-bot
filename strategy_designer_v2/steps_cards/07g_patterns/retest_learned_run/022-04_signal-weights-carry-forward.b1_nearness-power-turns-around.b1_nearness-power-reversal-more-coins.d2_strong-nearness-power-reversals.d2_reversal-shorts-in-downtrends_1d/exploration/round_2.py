def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            ret20 = c / c.shift(20) - 1
            ret5 = c / c.shift(5) - 1
            rng = (b["high"] - b["low"]) / c
            ts = pd.to_datetime(b["timestamp"])
            wd = ts.dt.weekday
            yr = ts.dt.year
            vol60 = r1.rolling(60).std()
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, wi=int(w[1:]), yr=yr.iloc[i], fwd=c.iloc[i + H] / c.iloc[i] - 1,
                                 r1=r1.iloc[i], r5=ret5.iloc[i], r20=ret20.iloc[i], rng=rng.iloc[i],
                                 vol60=vol60.iloc[i], wd=wd.iloc[i]))
            dd = pd.DataFrame(dict(coin=coin, w=w, yr=yr, wd=wd, r=r1, nxt=r1.shift(-1),
                                   r5=ret5, r20=ret20, vol60=vol60))
            daily.append(dd)
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby("coin")["fwd"].transform("mean")
    df["ex"] = df["fwd"] - df["drift"]
    df["r5z"] = df["r5"] / (df["vol60"] * np.sqrt(5))
    D = pd.concat(daily).dropna(subset=["r"])
    D["ex"] = D["r"] - D.groupby("coin")["r"].transform("mean")

    def tstat(s):
        s = s.dropna(); return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean() / (s.std() / np.sqrt(len(s)))))

    out = {}
    # weekday on all daily coin returns, by year
    out["daily_ex_by_weekday"] = D.groupby("wd")["ex"].apply(tstat).unstack().round(5)
    sun = D[D["wd"] == 6].groupby("yr")["ex"].apply(tstat).unstack().round(5)
    out["daily_sunday_ex_by_year"] = sun
    out["daily_tuesday_ex_by_year"] = D[D["wd"] == 1].groupby("yr")["ex"].apply(tstat).unstack().round(5)
    out["daily_sunday_ex_by_coin"] = D[D["wd"] == 6].groupby("coin")["ex"].apply(tstat).unstack().round(5)

    # rebound within downtrend, graded
    neg = df[(df["r20"] < 0)].dropna(subset=["r5z", "ex"]).copy()
    neg["b"] = pd.qcut(neg["r5z"].rank(method="first"), 8, labels=False)
    g = neg.groupby("b").agg(lo=("r5z", "min"), hi=("r5z", "max"))
    g = g.join(neg.groupby("b")["ex"].apply(tstat).unstack())
    out["r20neg_by_r5z_octile"] = g.round(4)
    sp = stats.spearmanr(neg["r5z"], neg["ex"])
    out["r20neg_spearman_r5z_ex"] = f"rho={sp.correlation:.4f} p={sp.pvalue:.4g} n={len(neg)}"
    pos5 = neg[neg["r5z"] > 0]
    sp2 = stats.spearmanr(pos5["r5z"], pos5["ex"])
    out["r20neg_r5pos_spearman"] = f"rho={sp2.correlation:.4f} p={sp2.pvalue:.4g} n={len(pos5)}"
    out["r20neg_r5pos_short_by_year"] = pos5.groupby("yr")["ex"].apply(lambda s: tstat(-s)).unstack().round(4)
    out["r20neg_r5pos_short_by_coin"] = pos5.groupby("coin")["ex"].apply(lambda s: tstat(-s)).unstack().round(4)
    # same in rising coins
    pos = df[(df["r20"] >= 0)].dropna(subset=["r5z", "ex"])
    sp3 = stats.spearmanr(pos["r5z"], pos["ex"])
    out["r20pos_spearman_r5z_ex"] = f"rho={sp3.correlation:.4f} p={sp3.pvalue:.4g} n={len(pos)}"
    # rebound relative to the 20-day fall: r5 / |r20|
    neg["ratio"] = neg["r5"] / neg["r20"].abs()
    sp4 = stats.spearmanr(neg["ratio"], neg["ex"])
    out["r20neg_spearman_rebound_share_ex"] = f"rho={sp4.correlation:.4f} p={sp4.pvalue:.4g}"
    # range day split by sign of day's return
    d = df.dropna(subset=["rng", "r1", "ex"]).copy()
    d["rq"] = pd.qcut(d["rng"].rank(method="first"), 5, labels=False)
    d["up"] = d["r1"] > 0
    out["range_q_by_daysign"] = d.groupby(["rq", "up"])["ex"].apply(tstat).unstack().round(4)
    out["range_top_by_year"] = d[d["rq"] == 4].groupby("yr")["ex"].apply(tstat).unstack().round(4)
    return out
