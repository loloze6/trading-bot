def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            for h in (7, 10, 14, 21):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, f=f[i], ret=c[i + h] / c[i] - 1,
                                     year=yr[i], day=day[i]))
    d = pd.DataFrame(rows)
    d["dret"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")

    def reg(g):
        g = g.dropna(subset=["f", "dret"])
        if len(g) < 10 or g["f"].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g["f"], g["dret"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))

    out["by_h"] = d.groupby("h").apply(reg)
    d7 = d[d.h == 7]
    out["h7_by_coin"] = d7.groupby("coin").apply(reg)
    out["h7_by_year"] = d7.groupby("year").apply(reg)

    def tmean(x):
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / x.std() * np.sqrt(len(x))))

    for h in (7, 14):
        g = d[d.h == h].copy()
        g["fq"] = pd.qcut(g["f"], 5, labels=False, duplicates="drop")
        out[f"quintile_h{h}_signed_dret"] = g.groupby("fq")["dret"].apply(tmean).unstack()
        g["top"] = g["fq"] == 4
        out[f"top_vs_rest_h{h}"] = g.groupby("top")["dret"].apply(tmean).unstack()
        top = g[g.fq == 4]
        out[f"top_h{h}_by_coin"] = top.groupby("coin")["dret"].apply(tmean).unstack()
        out[f"top_h{h}_by_year"] = top.groupby("year")["dret"].apply(tmean).unstack()
        # signed move in forecast direction, per day aggregated t
        g["sdev"] = np.sign(g["f"]) * g["dret"]
        pd_ = g.groupby("day")["sdev"].sum()
        out[f"signed_dev_h{h}_daily_t"] = pd.Series(dict(days=len(pd_), mean_case=g["sdev"].mean(),
                                                     t=pd_.mean() / pd_.std() * np.sqrt(len(pd_))))
        # graded within positive side only
        pos = g[g.f > 0]
        out[f"pos_side_reg_h{h}"] = reg(pos)
        neg = g[g.f < 0]
        out[f"neg_side_reg_h{h}"] = reg(neg)
    return out
