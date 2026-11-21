def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 26
    rows = []; dl = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); n = len(b); ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            past26 = c / c.shift(26) - 1
            past52 = c / c.shift(52) - 1
            vol60 = r1.rolling(60).std() * np.sqrt(26)
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, year=ts[i].year, cell=ts[i].strftime("%Y%m"),
                                 fwd=c.iloc[i+H]/c.iloc[i]-1, regime=b["regime"].iloc[i],
                                 past26=past26.iloc[i], past52=past52.iloc[i], vol=vol60.iloc[i]))
            dl.append(pd.DataFrame(dict(coin=coin, day=ts.dt.floor("D"), year=ts.dt.year, wd=ts.dt.weekday, r1=r1)))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["fwd"].transform("mean"); g["ex"] = g["fwd"] - g["drift"]
    g["sdc"] = g.groupby("coin")["fwd"].transform("std")
    out = {}
    def clus_t(df, v):
        x = df[v].rank(pct=True).values - 0.5; y = df["ex"].values
        beta = (x*y).sum()/(x*x).sum(); e = y - beta*x
        s = pd.DataFrame(dict(c=df["cell"].values, xe=x*e)).groupby("c")["xe"].sum()
        se = np.sqrt((s**2).sum())/(x*x).sum()
        return "beta %.4f t_clustered %.2f n %d cells %d" % (beta, beta/se, len(df), s.shape[0])
    a = g.dropna(subset=["past26", "vol"]).copy()
    a["z26"] = a["past26"] / a["vol"]
    out["all_clus_z26"] = clus_t(a, "z26")
    a52 = g.dropna(subset=["past52"]).copy()
    out["all_clus_past52"] = clus_t(a52, "past52")
    a["era"] = np.where(a["year"] <= 2021, "<=2021", ">=2022")
    a["q"] = a.groupby("coin")["z26"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False) if len(x) >= 9 else np.nan)
    aa = a.dropna(subset=["q"])
    out["z26_tercile_by_era"] = aa.groupby(["era", "q"])["ex"].agg(["count", "mean"]).unstack()
    out["z26_tercile_strength"] = (aa.assign(s=aa["ex"]/aa["sdc"])).groupby("q")["s"].agg(["count", "mean"])
    out["z26_top_minus_bottom_by_year"] = aa.groupby(["year", "q"])["ex"].mean().unstack()
    pc = aa.groupby(["coin", "q"])["ex"].mean().unstack()
    out["coins_top_gt_bottom"] = "%d of %d" % (((pc[2.0] - pc[0.0]) > 0).sum(), pc.dropna().shape[0])
    d = pd.concat(dl).dropna(subset=["r1"])
    dm = d.groupby(["day", "wd", "year"])["r1"].mean().reset_index()
    out["sat_minus_rest_by_year"] = dm.groupby("year").apply(lambda x: pd.Series(dict(
        sat=x.loc[x.wd == 5, "r1"].mean(), rest=x.loc[x.wd != 5, "r1"].mean(),
        t=stats.ttest_ind(x.loc[x.wd == 5, "r1"], x.loc[x.wd != 5, "r1"], equal_var=False)[0])))
    pcs = d.groupby("coin").apply(lambda x: x.loc[x.wd == 5, "r1"].mean() - x.loc[x.wd != 5, "r1"].mean())
    out["coins_sat_gt_rest"] = "%d of %d" % ((pcs > 0).sum(), len(pcs))
    return out
