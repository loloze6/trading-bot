def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    pp = "debug_info.components.hpmom.post_pipeline_value"
    rows = []
    # drift per coin per horizon, computed on non-overlapping grid
    H = [1, 3, 5, 10, 20]
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            # rough 30-bar return and distance to 60-bar high, within window (NaN in early rows)
            s = pd.Series(c)
            r30 = s / s.shift(30) - 1
            hi60 = s.rolling(60, min_periods=60).max()
            dist = 1 - s / hi60
            year = pd.to_datetime(df["timestamp"]).dt.year
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=int(year.iloc[i]),
                                     f=df[pp].iloc[i], ret=c[i + h] / c[i] - 1,
                                     r30=r30.iloc[i], dist=dist.iloc[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]

    def slope_t(g, x="f"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 20 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))

    out = {}
    out["by_horizon"] = d.groupby("h").apply(slope_t)
    d5 = d[d.h == 5].copy()
    out["by_coin_h5"] = d5.groupby("coin").apply(slope_t)
    out["by_year_h5"] = d5.groupby("year").apply(slope_t)
    d5["side"] = np.sign(d5["f"])
    out["by_side_h5"] = d5.groupby("side").apply(slope_t)
    # mean excess in direction by forecast quintile
    d5["fq"] = pd.qcut(d5["f"], 5, labels=False, duplicates="drop")
    out["quintile_h5"] = d5.groupby("fq").agg(n=("ex", "size"), fmean=("f", "mean"),
                                              ex_mean=("ex", "mean"),
                                              ex_t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    # raw parts: r30 alone, and r30 by distance tercile
    out["r30_alone_by_h"] = d.groupby("h").apply(lambda g: slope_t(g, "r30"))
    d5["dq"] = pd.qcut(d5["dist"], 3, labels=["near", "mid", "far"])
    out["r30_by_dist_h5"] = d5.groupby("dq").apply(lambda g: slope_t(g, "r30"))
    d10 = d[d.h == 10].copy()
    d10["dq"] = pd.qcut(d10["dist"], 3, labels=["near", "mid", "far"])
    out["r30_by_dist_h10"] = d10.groupby("dq").apply(lambda g: slope_t(g, "r30"))
    out["dist_alone_by_h"] = d.groupby("h").apply(lambda g: slope_t(g, "dist"))
    return out
