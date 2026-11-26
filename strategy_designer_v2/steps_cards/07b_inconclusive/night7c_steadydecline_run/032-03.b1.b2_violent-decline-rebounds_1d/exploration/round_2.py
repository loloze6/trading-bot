def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            r28 = pd.Series(c).pct_change(28).values
            r7 = pd.Series(c).pct_change(7).values
            fc = df["forecast"].values
            reg = df["regime"].values
            ts = pd.to_datetime(df["timestamp"])
            yr = ts.dt.year.values
            dk = ts.dt.floor("D").astype("int64").values
            for h in [1, 2, 3, 5]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i], dk=dk[i], fc=fc[i], reg=reg[i],
                                     r28=r28[i], r7=r7[i], ret=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]
    out = {}

    def slope_t(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 8 or g[x].std() == 0:
            return pd.Series({"n": len(g)})
        s = stats.linregress(g[x], g["ex"])
        # day-clustered mean t
        dd = g.groupby("dk")["ex"].sum()
        tm = g["ex"].mean() / (np.sqrt((dd ** 2).sum()) / len(g))
        return pd.Series({"n": len(g), "days": g["dk"].nunique(), "mean_ex": g["ex"].mean(),
                          "t_mean_day": tm, "slope": s.slope, "t_slope": s.slope / s.stderr})

    inr = d[d["fc"] > 0]
    out["inregime_h_by_year"] = inr.groupby(["h", "year"]).apply(slope_t)
    out["inregime_h1_by_coin"] = inr[inr["h"] == 1].groupby("coin").apply(slope_t)
    # within regime: short-term 7-day return as grader
    out["inregime_r7_slope_by_h"] = inr.groupby("h").apply(lambda g: slope_t(g, "r7"))
    # all bars with 28d fall: momentum strength graded by fall, by h
    allf = d[d["r28"] < 0].copy()
    allf["neg"] = -allf["r28"]
    out["all_falls_graded_by_h"] = allf.groupby("h").apply(lambda g: slope_t(g, "neg"))
    # in-regime quintiles at h1 and h3
    for h in [1, 3]:
        g = inr[inr["h"] == h].copy()
        g["q"] = pd.qcut(g["fc"], 5, labels=False, duplicates="drop")
        out[f"inregime_quint_h{h}"] = g.groupby("q").agg(n=("ex", "size"), fc=("fc", "mean"),
                                                        mean_ex=("ex", "mean"), sd=("ex", "std"))
    return out
