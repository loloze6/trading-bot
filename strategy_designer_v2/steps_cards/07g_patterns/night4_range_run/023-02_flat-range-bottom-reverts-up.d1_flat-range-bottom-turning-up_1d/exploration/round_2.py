def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"]; h = d["high"]; l = d["low"]
            hh = h.rolling(30).max(); ll = l.rolling(30).min()
            rng = hh - ll
            d["ratio"] = (c - c.shift(29)).abs() / rng
            d["dmid"] = (c - (hh + ll) / 2) / rng
            d["r1"] = c / c.shift(1) - 1
            d["r30"] = c / c.shift(29) - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["f5"] = c.shift(-5) / c - 1
            d["f1"] = c.shift(-1) / c - 1
            d["pos"] = np.arange(len(d))
            ts = pd.to_datetime(d["timestamp"])
            d["wd"] = ts.dt.weekday; d["yr"] = ts.dt.year
            d["coin"] = coin; d["win"] = w
            d["wn"] = int(w[1:])
            d["alloc"] = d["postRebalance_current_allocation"]
            rows.append(d[["coin","win","wn","pos","ratio","dmid","r1","r30","vol20","f5","f1","wd","yr","alloc"]])
    A = pd.concat(rows, ignore_index=True)
    G0 = A[A.pos % 5 == 0]
    drift5 = G0.groupby("coin")["f5"].mean(); sd5 = G0.groupby("coin")["f5"].std()
    A["z5"] = (A["f5"] - A["coin"].map(drift5)) / A["coin"].map(sd5)
    G = A[A.pos % 5 == 0].dropna(subset=["z5","ratio","dmid","vol20"]).copy()
    out = {}
    T = G[G.ratio > 0.3]
    def slope(g):
        if len(g) < 20: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g.dmid, g.z5)
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})
    out["trend_dmid_by_coin"] = T.groupby("coin").apply(slope)
    out["trend_dmid_by_year"] = T.groupby("yr").apply(slope)
    out["trend_dmid_by_ratio_band"] = G.groupby(pd.cut(G.ratio, [0, 0.3, 0.5, 0.7, 1.01])).apply(slope)
    # graded in ratio: interaction slope
    G["x"] = G.dmid * G.ratio
    X = np.column_stack([np.ones(len(G)), G.dmid, G.ratio, G.x])
    beta, res, *_ = np.linalg.lstsq(X, G.z5.values, rcond=None)
    e = G.z5.values - X @ beta
    cov = np.linalg.inv(X.T @ X) * (e @ e) / (len(G) - 4)
    out["interaction_dmid_x_ratio"] = pd.Series(beta / np.sqrt(np.diag(cov)), index=["c","dmid","ratio","dmid*ratio"])
    # Weekday robustness: z of daily returns
    B = A.dropna(subset=["r1","vol20"]).copy()
    B["r1z"] = B.r1 / B.vol20
    def tm(s):
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s)))})
    out["sat_by_coin"] = B[B.wd == 5].groupby("coin")["r1"].apply(tm).unstack()
    out["sat_by_year"] = B[B.wd == 5].groupby("yr")["r1"].apply(tm).unstack()
    out["nonsat_by_year"] = B[B.wd != 5].groupby("yr")["r1"].apply(tm).unstack()
    out["wd_r1z"] = B.groupby("wd")["r1z"].apply(tm).unstack()
    # Saturday graded by the past-5-day return?
    A["r5p"] = A.groupby(["coin","win"])["r1"].transform(lambda s: s.rolling(5).sum())
    S = A[(A.wd == 4)].dropna(subset=["f1","r5p","vol20"])  # Friday close -> Saturday
    S = S.assign(q=pd.qcut(S.r5p / S.vol20, 4, labels=["q1","q2","q3","q4"]))
    out["sat_ret_by_prior5d_q"] = S.groupby("q")["f1"].apply(tm).unstack()
    # book on weekdays
    out["book_alloc_by_wd"] = A.groupby("wd")["alloc"].mean()
    return out
