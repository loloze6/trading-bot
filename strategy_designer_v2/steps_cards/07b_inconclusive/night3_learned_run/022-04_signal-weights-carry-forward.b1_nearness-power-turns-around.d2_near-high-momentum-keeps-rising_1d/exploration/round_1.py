def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [5, 10, 20]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            f = df["forecast"].values
            nh = df.get("debug_info.components.near_high.post_pipeline_value", pd.Series(np.nan, index=df.index)).values
            r20 = df.get("debug_info.components.ret20.post_pipeline_value", pd.Series(np.nan, index=df.index)).values
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, year=yr[i], h=h, f=f[i], nh=nh[i], r20=r20[i],
                                     ret=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")

    def slope(g, x="f"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 20 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))

    out = {}
    out["by_h_forecast"] = d.groupby("h").apply(slope)
    out["by_h_nh"] = d.groupby("h").apply(lambda g: slope(g, "nh"))
    out["by_h_r20"] = d.groupby("h").apply(lambda g: slope(g, "r20"))
    d5 = d[d.h == 5]
    out["h5_by_coin"] = d5.groupby("coin").apply(slope)
    out["h5_by_year"] = d5.groupby("year").apply(slope)
    out["h5_by_side"] = d5.assign(side=np.sign(d5.f)).groupby("side").apply(slope)
    d5q = d5.dropna(subset=["f"]).copy()
    d5q["q"] = pd.qcut(d5q["f"], 5, labels=False)
    out["h5_quintiles"] = d5q.groupby("q").agg(n=("ex", "size"), fmean=("f", "mean"), ex_mean=("ex", "mean"),
                                               ex_std=("ex", "std"))
    d10 = d[d.h == 10]
    out["h10_by_coin"] = d10.groupby("coin").apply(slope)
    d20 = d[d.h == 20]
    out["h20_by_year"] = d20.groupby("year").apply(slope)
    out["fcorr_nh_r20"] = float(d5[["nh", "r20"]].corr().iloc[0, 1])
    return out
