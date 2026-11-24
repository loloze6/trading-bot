def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            hi = c.rolling(20, min_periods=20).max(); lo = c.rolling(20, min_periods=20).min()
            rp = 2 * (c - lo) / (hi - lo) - 1
            r20 = c / c.shift(20) - 1
            vol20 = c.pct_change().rolling(20, min_periods=10).std()
            for h in H:
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(df), h)
                for i in idx:
                    if i + h >= len(df): continue
                    rows.append(dict(coin=coin, win=w, h=h, i=i, ts=pd.Timestamp(df["timestamp"].iloc[i]),
                                     fc=df["forecast"].iloc[i], rp=rp.iloc[i], fwd=fwd.iloc[i],
                                     r20=r20.iloc[i], vol=vol20.iloc[i]))
    d = pd.DataFrame(rows)
    d["day"] = d["ts"].dt.floor("D")
    d["year"] = d["ts"].dt.year
    # drift per coin per h
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    out = {}

    def slope_t(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 30: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        X = g[x].values; y = g["ex"].values
        Xc = X - X.mean(); b = (Xc * (y - y.mean())).sum() / (Xc ** 2).sum()
        a = y.mean() - b * X.mean(); e = y - a - b * X
        sc = pd.Series(Xc * e).groupby(g["day"].values).sum()
        G = len(sc); se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (Xc ** 2).sum()
        return pd.Series(dict(n=len(g), days=G, slope=b, t=b / se))

    out["by_horizon_fc"] = d.groupby("h").apply(slope_t)
    out["by_horizon_rawpos"] = d.groupby("h").apply(lambda g: slope_t(g, "rp"))
    d5 = d[d.h == 5].copy()
    out["h5_by_coin"] = d5.groupby("coin").apply(slope_t)
    out["h5_by_window"] = d5.groupby("win").apply(slope_t)
    out["h5_by_year"] = d5.groupby("year").apply(slope_t)
    d5["fcb"] = pd.cut(d5["fc"], [-21, -15, -10, -5, 0, 5, 10, 15, 21])
    out["h5_by_fc_bucket"] = d5.groupby("fcb")["ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    d5["rpb"] = pd.cut(d5["rp"], [-1.01, -0.6, -0.2, 0.2, 0.6, 0.99, 1.01])
    out["h5_by_rawpos_bucket"] = d5.groupby("rpb")["ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    d5["trend"] = pd.cut(d5["r20"], [-10, -0.1, 0.1, 10], labels=["fall20", "flat20", "rise20"])
    out["h5_by_trend20"] = d5.groupby("trend").apply(slope_t)
    d5["volq"] = d5.groupby("coin")["vol"].transform(lambda s: s.rank(pct=True) > 0.5).map({True: "hiVol", False: "loVol"})
    out["h5_by_vol"] = d5.groupby("volq").apply(slope_t)
    d5["side"] = np.where(d5["fc"] > 0, "long", "short")
    out["h5_side_mean_ex_signed"] = d5.groupby("side").apply(lambda g: pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(), t=g["ex"].mean() / g["ex"].std() * np.sqrt(len(g)))))
    d10 = d[d.h == 10].copy(); d10["fcb"] = pd.cut(d10["fc"], [-21, -10, -5, 0, 5, 10, 21])
    out["h10_by_fc_bucket"] = d10.groupby("fcb")["ex"].agg(["count", "mean"])
    return out
