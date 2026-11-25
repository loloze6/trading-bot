def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    def clus_t(df, xcol, ycol):
        X = df[xcol].values; Y = df[ycol].values
        xm = X - X.mean(); b = (xm * (Y - Y.mean())).sum() / (xm ** 2).sum()
        e = Y - Y.mean() - b * xm
        s = pd.Series(xm * e).groupby(df["day"].values).sum()
        G = len(s); var = (s ** 2).sum() / (xm ** 2).sum() ** 2 * G / (G - 1)
        return b, b / np.sqrt(var), G
    H = 5
    recs = []
    for c in bars:
        allr = []
        for w in bars[c]:
            cl = bars[c][w]["close"].values
            idx = np.arange(0, len(cl) - H, H); allr.append(cl[idx + H] / cl[idx] - 1)
        mu = np.concatenate(allr).mean()
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True); cl = b["close"]
            hi28 = cl.rolling(28, min_periods=28).max()
            dist = cl / hi28 - 1
            r28 = cl / cl.shift(28) - 1
            r5p = cl / cl.shift(5) - 1
            lr = np.log(cl).diff()
            vol20 = lr.rolling(20).std()
            vol60 = lr.rolling(60, min_periods=20).std()
            f = b["debug_info.components.high_prox.post_pipeline_value"]
            raw = b["debug_info.components.high_prox.last_history_value"]
            al = b["postRebalance_current_allocation"]
            idx = np.arange(0, len(cl) - H, H)
            for i in idx:
                recs.append(dict(coin=c, window=w, day=str(b["timestamp"].iloc[i])[:10],
                                 year=int(str(b["timestamp"].iloc[i])[:4]),
                                 f=f.iloc[i], raw=raw.iloc[i], dist=dist.iloc[i], r28=r28.iloc[i],
                                 r5p=r5p.iloc[i], vr=vol20.iloc[i] / vol60.iloc[i], vol20=vol20.iloc[i],
                                 al=al.iloc[i], x=cl.iloc[i + H] / cl.iloc[i] - 1 - mu,
                                 xa=(cl.iloc[i + H] / cl.iloc[i] - 1) * al.iloc[i]))
    R = pd.DataFrame(recs).dropna()
    res = {}
    for col in ["f", "raw", "dist", "r28", "r5p", "vr", "vol20", "al"]:
        b_, t_, G = clus_t(R, col, "x"); res[col] = {"slope": b_, "t_day": t_, "days": G}
    out["slopes_clustered_h5"] = pd.DataFrame(res).T
    out["n_cases"] = len(R)
    # raw distance quintiles
    R["dq"] = pd.qcut(R["dist"].rank(method="first"), 5, labels=False)
    g = R.groupby("dq")
    out["dist_quintile"] = pd.DataFrame({"dist": g["dist"].mean(), "x": g["x"].mean(),
                                         "t": g["x"].mean() / (g["x"].std() / np.sqrt(g.size())), "n": g.size()})
    # forecast quintiles
    R["fq"] = pd.qcut(R["f"].rank(method="first"), 5, labels=False)
    g = R.groupby("fq")
    out["f_quintile"] = pd.DataFrame({"f": g["f"].mean(), "dist": g["dist"].mean(), "r28": g["r28"].mean(),
                                      "x": g["x"].mean(), "t": g["x"].mean() / (g["x"].std() / np.sqrt(g.size())),
                                      "alloc": g["al"].mean(), "n": g.size()})
    # by 28d return sign: slope of f
    rows = {}
    for nm, sub in [("r28_up", R[R.r28 > 0]), ("r28_down", R[R.r28 <= 0])]:
        b_, t_, G = clus_t(sub, "f", "x"); rows[nm] = {"slope_f": b_, "t": t_, "days": G, "n": len(sub), "x": sub["x"].mean()}
        b_, t_, G = clus_t(sub, "r28", "x"); rows[nm].update({"slope_r28": b_, "t_r28": t_})
    out["by_r28_sign"] = pd.DataFrame(rows).T
    # f slope within each year and coin
    out["f_slope_by_year"] = pd.DataFrame({y: dict(zip(["slope", "t", "days"], clus_t(s, "f", "x")))
                                           for y, s in R.groupby("year")}).T
    out["f_slope_by_coin"] = pd.DataFrame({c: dict(zip(["slope", "t", "days"], clus_t(s, "f", "x")))
                                           for c, s in R.groupby("coin")}).T
    # multivariate: x on f, r28, vr
    Xm = np.column_stack([np.ones(len(R)), (R["f"] - R["f"].mean()) / R["f"].std(),
                          (R["r28"] - R["r28"].mean()) / R["r28"].std(), (R["vr"] - R["vr"].mean()) / R["vr"].std()])
    beta, *_ = np.linalg.lstsq(Xm, R["x"].values, rcond=None)
    out["multi_std_betas_const_f_r28_vr"] = pd.Series(beta, index=["c", "f", "r28", "vr"])
    out["corr"] = R[["f", "raw", "dist", "r28", "vr", "al"]].corr()
    # book concentration: share of book total gain from top 5% days
    br = []
    for c in days:
        for w in days[c]:
            br.append(days[c][w]["book_return"].dropna())
    B = pd.concat(br).sort_values(ascending=False)
    out["top5pct_days_share_of_sum"] = B.head(int(len(B) * 0.05)).sum() / B.sum()
    return out
