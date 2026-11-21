def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 26
    rows = []; dl = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b); ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change(); vol20 = r1.rolling(20).std()
            hi52 = hi.rolling(52).max(); lo52 = lo.rolling(52).min()
            pos52 = c / ((hi52 + lo52) / 2) - 1
            rngpos = (c - lo52) / (hi52 - lo52)
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26); sb = ((hi52 + lo52) / 2).shift(26)
            lower = np.minimum(sa, sb); upper = np.maximum(sa, sb)
            dcloud = c / lower - 1
            thick = (upper - lower) / c
            ckij = c / kij - 1
            past26 = c / c.shift(26) - 1
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, year=ts[i].year, cell=ts[i].strftime("%Y%m"),
                                 fwd=c.iloc[i+H]/c.iloc[i]-1, regime=b["regime"].iloc[i],
                                 pos52=pos52.iloc[i], rng=rngpos.iloc[i], dcloud=dcloud.iloc[i],
                                 thick=thick.iloc[i], ckij=ckij.iloc[i], vol20=vol20.iloc[i], past26=past26.iloc[i]))
            dl.append(pd.DataFrame(dict(day=ts.dt.floor("D"), wd=ts.dt.weekday, r1=r1)))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["fwd"].transform("mean"); g["ex"] = g["fwd"] - g["drift"]
    out = {}
    def summ(df, key):
        return df.groupby(key)["ex"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x)) if len(x) > 2 else np.nan])
    def clus_t(df, v):
        # slope of ex on rank of v, t with time-cell clustering
        x = df[v].rank(pct=True).values - 0.5; y = df["ex"].values
        beta = (x*y).sum()/(x*x).sum(); e = y - beta*x
        s = pd.DataFrame(dict(c=df["cell"].values, xe=x*e)).groupby("c")["xe"].sum()
        se = np.sqrt((s**2).sum())/(x*x).sum()
        return "beta %.4f t_clustered %.2f n %d cells %d" % (beta, beta/se, len(df), s.shape[0])
    t = g[g.regime == "trending"].dropna(subset=["pos52", "vol20", "dcloud"]).copy()
    for v in ["pos52", "rng", "dcloud", "ckij", "thick", "vol20", "past26"]:
        tt = t.dropna(subset=[v]).copy()
        tt["q"] = pd.qcut(tt[v].rank(method="first"), 4, labels=False)
        out["tr_q_" + v] = summ(tt, "q")
        out["tr_clus_" + v] = clus_t(tt, v)
    t["early"] = np.where(t["year"] <= 2021, "<=2021", ">=2022")
    t["q"] = t.groupby("early")["pos52"].transform(lambda x: pd.qcut(x.rank(method="first"), 2, labels=False))
    out["tr_pos52_half_by_era"] = t.groupby(["early", "q"])["ex"].agg(["count", "mean"])
    t["qv"] = t.groupby("early")["vol20"].transform(lambda x: pd.qcut(x.rank(method="first"), 2, labels=False))
    out["tr_vol_half_by_era"] = t.groupby(["early", "qv"])["ex"].agg(["count", "mean"])
    out["tr_pos52_vs_dcloud_corr"] = "spearman %.3f" % stats.spearmanr(t["pos52"], t["dcloud"])[0]
    a = g.dropna(subset=["past26"]).copy()
    out["all_clus_past26"] = clus_t(a, "past26")
    a2 = g.dropna(subset=["rng"]).copy()
    out["all_clus_rng"] = clus_t(a2, "rng")
    d = pd.concat(dl).dropna(subset=["r1"]).groupby(["day", "wd"])["r1"].mean().reset_index()
    out["weekday_crossmean"] = d.groupby("wd")["r1"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    d["era"] = np.where(d["day"].dt.year <= 2021, "<=2021", ">=2022")
    out["weekday_by_era"] = d.groupby(["era", "wd"])["r1"].mean().unstack()
    return out
