def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    cases = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            f = b["forecast"].values
            lr = pd.Series(np.log(cl)).diff()
            vol168 = lr.rolling(168).std().values
            vol720 = lr.rolling(720).std().values
            r168 = pd.Series(cl).pct_change(168).values
            r24 = pd.Series(cl).pct_change(24).values
            for i in range(0, n-48, 24):
                cases.append((c, w, f[i], cl[i+24]/cl[i]-1, cl[i+48]/cl[i]-1, cl[i+12]/cl[i]-1,
                              vol168[i]/vol720[i] if vol720[i] > 0 else np.nan, r168[i], r24[i],
                              np.min(cl[i:i+25])/cl[i]-1))
    C = pd.DataFrame(cases, columns=["coin","w","f","fwd24","fwd48","fwd12","vr","r168","r24","mae"])
    for h in ["fwd24","fwd48","fwd12"]:
        C["ex"+h[3:]] = C[h] - C.groupby("coin")[h].transform("mean")
    S = C[C.f > 0].copy()
    qs = S.f.quantile([0.8, 0.9, 0.95, 0.99]).values
    def summ(g, col="ex24"):
        return pd.Series({"n": len(g), "mean_fwd24": g["fwd24"].mean(), "mean_ex": g[col].mean(),
                          "t": stats.ttest_1samp(g[col], 0).statistic if len(g) > 2 else np.nan})
    rows = {}
    for lab, q in zip(["top20", "top10", "top5", "top1"], qs):
        g = S[S.f >= q]
        rows[lab] = {"n": len(g), "fwd12": g.fwd12.mean(), "fwd24": g.fwd24.mean(), "fwd48": g.fwd48.mean(),
                     "ex24": g.ex24.mean(), "t24": stats.ttest_1samp(g.ex24, 0).statistic,
                     "ex48": g.ex48.mean(), "t48": stats.ttest_1samp(g.ex48, 0).statistic,
                     "mae24": g.mae.mean(), "f_min": q}
    out["tails"] = pd.DataFrame(rows).T.round(4)
    T = S[S.f >= qs[0]].copy()
    C["vrt"] = pd.qcut(C.vr, 3, labels=["low", "mid", "high"])
    T["vrt"] = C.loc[T.index, "vrt"]
    out["top20_by_vol"] = T.groupby("vrt").apply(summ).round(4)
    out["nosig_by_vol"] = C[C.f <= 0].groupby("vrt").apply(summ).round(4)
    T["tr"] = np.where(T.r168 > 0, "up7d", "down7d")
    out["top20_by_trend7d"] = T.groupby("tr").apply(summ).round(4)
    T["d24"] = np.where(T.r24 > 0, "up24h", "down24h")
    out["top20_by_24h"] = T.groupby("d24").apply(summ).round(4)
    out["top20_by_coin"] = T.groupby("coin").apply(summ).round(4)
    T["wn"] = T.w.str[1:].astype(int)
    out["top20_by_windowgroup"] = T.groupby(pd.cut(T.wn, [0, 6, 12, 18, 24])).apply(summ).round(4)
    # approx book: long only top20 cases, 24h, cost 0.19% per trade, equal over coins, per grid cell
    T["net"] = T.fwd24 - 0.0019
    out["top20_net_mean"] = float(T.net.mean())
    out["top20_net_t"] = float(stats.ttest_1samp(T.net, 0).statistic)
    out["top20_hit"] = float((T.fwd24 > 0).mean())
    # sequential chain: per coin per window ordered by case, value of 1/6 sized trades; approx drawdown
    g = C.copy(); g["pos"] = (g.f >= qs[0]).astype(float)
    g["ret"] = g.pos * (g.fwd24 - 0.0019)
    g["cell"] = g.groupby(["coin", "w"]).cumcount()
    g["wn"] = g.w.str[1:].astype(int)
    P = g.groupby(["wn", "cell"]).ret.mean().sort_index()
    v = (1 + P).cumprod(); dd = (v / v.cummax() - 1).min()
    yrs = len(P) / 365
    out["approx_top20_book"] = {"yearly": float(v.iloc[-1] ** (1 / yrs) - 1), "maxdd": float(dd),
                                "sharpe": float(P.mean() / P.std() * np.sqrt(365)), "share_in": float(g.pos.mean())}
    out["approx_top20_book"] = pd.Series(out["approx_top20_book"]).round(4)
    H = g.groupby(["wn", "cell"]).fwd24.mean().sort_index()
    vh = (1 + H).cumprod()
    out["approx_hold"] = pd.Series({"yearly": float(vh.iloc[-1] ** (1 / yrs) - 1),
                                    "maxdd": float((vh / vh.cummax() - 1).min())}).round(4)
    return out
