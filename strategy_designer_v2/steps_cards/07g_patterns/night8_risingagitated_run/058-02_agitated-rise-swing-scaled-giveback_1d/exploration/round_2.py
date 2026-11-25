def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    def build(H, step=None):
        rows = []
        for coin, wins in bars.items():
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                c = df["close"].astype(float)
                r = c.pct_change()
                sma = c.rolling(20).mean()
                sd = r.rolling(20).std()
                stretch = (c / sma - 1) / sd
                ret60 = c / c.shift(60) - 1
                fwd = c.shift(-H) / c - 1
                ts = pd.to_datetime(df["timestamp"])
                for i in range(0, len(df), H):
                    rows.append(dict(coin=coin, w=w, stretch=stretch.iloc[i], ret60=ret60.iloc[i],
                                     fwd=fwd.iloc[i], regime=df["regime"].iloc[i],
                                     year=ts.iloc[i].year, day=ts.iloc[i].normalize()))
        g = pd.DataFrame(rows).dropna(subset=["fwd"])
        g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        g["exn"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")
        g["trend"] = np.where(g["regime"] == "unknown", "rising_agit",
                      np.where(g["ret60"] > 0.10, "rising_calm", np.where(g["ret60"] < -0.10, "falling",
                      np.where(g["ret60"].isna(), "na", "choppy"))))
        return g.dropna(subset=["stretch"])
    def clus(x):
        # day-clustered slope t of exn on stretch
        n = len(x)
        if n < 15: return pd.Series(dict(n=n, slope=np.nan, t_clu=np.nan, days=np.nan))
        X = x["stretch"].values - x["stretch"].mean(); y = x["exn"].values
        b = (X * y).sum() / (X ** 2).sum()
        e = y - y.mean() - b * X
        sc = pd.Series(X * e).groupby(x["day"].values).sum()
        G = len(sc)
        v = (sc ** 2).sum() / (X ** 2).sum() ** 2 * G / (G - 1)
        return pd.Series(dict(n=n, slope=b, t_clu=b / np.sqrt(v), days=G))
    for H in [3, 5, 10]:
        g = build(H)
        out[f"H{H}_slope_by_trend"] = g.groupby("trend").apply(clus)
    g = build(5)
    ch = g[g["trend"] == "choppy"]
    out["choppy_H5_by_year"] = ch.groupby("year").apply(clus)
    out["choppy_H5_by_coin"] = ch.groupby("coin").apply(clus)
    ch = ch.assign(side=np.where(ch["stretch"] > 0, "above", "below"))
    out["choppy_H5_side"] = ch.groupby("side").agg(n=("exn", "size"), strength=("exn", "mean"),
                                                   mean_ex=("ex", "mean"), sd=("ex", "std"))
    out["choppy_H5_side_slope"] = ch.groupby("side").apply(clus)
    rc = g[g["trend"] == "rising_calm"]
    out["risingcalm_H5_by_year"] = rc.groupby("year").apply(clus)
    return out
