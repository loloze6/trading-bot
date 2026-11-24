def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H_list = [10, 20, 30, 45, 60, 90]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            raw = df.get("debug_info.components.fall90.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            fc = df["forecast"].values
            # trailing 180-day return as a trend regime, inside window
            for H in H_list:
                for t in range(0, n - H, H):
                    r = c[t + H] / c[t] - 1
                    tr = c[t] / c[t - 30] - 1 if t >= 30 else np.nan
                    rows.append(dict(coin=coin, win=w, H=H, t=t, day=str(df["timestamp"].iloc[t])[:10],
                                     year=str(df["timestamp"].iloc[t])[:4], ret=r, fc=fc[t], raw=raw[t], r30=tr))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin", "H"])["ret"].transform("mean")
    out = {}

    def clus_slope(g, x="fc", y="ex"):
        g = g.dropna(subset=[x, y])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        X = g[x].values - g[x].mean(); Y = g[y].values
        b = (X * Y).sum() / (X * X).sum()
        a = Y.mean() - b * g[x].mean()
        e = Y - a - b * g[x].values
        s = pd.Series(X * e).groupby(g["day"].values).sum()
        G = len(s)
        var = (s ** 2).sum() / (X * X).sum() ** 2 * G / max(G - 1, 1)
        return pd.Series(dict(n=len(g), days=G, slope=b, t=b / np.sqrt(var)))

    out["slope fc by horizon"] = d.groupby("H").apply(clus_slope)
    out["slope raw (both sides) by horizon"] = d.groupby("H").apply(lambda g: clus_slope(g, "raw"))
    d45 = d[d.H == 45].copy()
    d45["fcbin"] = pd.cut(d45["fc"], [-0.01, 0.001, 3, 6, 10, 21])
    out["45d excess by forecast bin"] = d45.groupby("fcbin")["ex"].agg(["count", "mean", "median"])
    d45["rawbin"] = pd.qcut(d45["raw"], 6, duplicates="drop")
    out["45d excess by raw sextile"] = d45.groupby("rawbin")["ex"].agg(["count", "mean", "median"])
    pos = d45[d45.fc > 0]
    out["45d excess fc>0 by coin"] = pos.groupby("coin")["ex"].agg(["count", "mean"])
    out["45d excess fc>0 by year"] = pos.groupby("year")["ex"].agg(["count", "mean"])
    out["slope by year 45"] = d45.groupby("year").apply(clus_slope)
    for H in [20, 45, 90]:
        dd = d[(d.H == H) & (d.fc > 0)].copy()
        dd["r30s"] = np.where(dd.r30 > 0, "last30 up", "last30 down")
        out[f"fc>0 by last-30d sign H{H}"] = dd.groupby("r30s")["ex"].agg(["count", "mean"])
        out[f"slope fc>0 by last-30d sign H{H}"] = dd.groupby("r30s").apply(clus_slope)
    return out
