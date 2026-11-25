def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 5, 10, 20]
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in H:
                for t in range(0, n - h, h):
                    tr = c[t] / c[t - 60] - 1 if t >= 60 else np.nan
                    rows.append(dict(coin=coin, w=w, h=h, f=f[t], r=c[t + h] / c[t] - 1, yr=yr[t], tr=tr))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby(["coin", "h"])["r"].transform("mean")

    def reg(g):
        g = g.dropna(subset=["f", "ex"])
        if len(g) < 30 or g["f"].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        s = stats.linregress(g["f"], g["ex"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr))

    out = {}
    out["by_horizon"] = d.groupby("h").apply(reg)
    d5 = d[d.h == 5].copy()
    out["h5_by_coin"] = d5.groupby("coin").apply(reg)
    out["h5_by_window"] = d5.groupby("w").apply(reg)
    out["h5_by_year"] = d5.groupby("yr").apply(reg)
    d5["side"] = np.sign(d5["f"])
    out["h5_by_side_meanex"] = d5.groupby("side")["ex"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["h5_by_side_slope"] = d5.groupby("side").apply(reg)
    d5["q"] = pd.qcut(d5["f"], 5, labels=False, duplicates="drop")
    out["h5_by_fq"] = d5.groupby("q").agg(n=("ex", "size"), fmean=("f", "mean"), exmean=("ex", "mean"))
    d5["trend"] = pd.cut(d5["tr"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    out["h5_by_trend"] = d5.groupby("trend").apply(reg)
    for h in [10, 20]:
        dh = d[d.h == h]
        out[f"h{h}_by_year"] = dh.groupby("yr").apply(reg)
    return out
