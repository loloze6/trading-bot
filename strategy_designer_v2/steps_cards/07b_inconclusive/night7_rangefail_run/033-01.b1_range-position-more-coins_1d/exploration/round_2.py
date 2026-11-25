def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            n = len(df)
            hi = c.rolling(20, min_periods=20).max(); lo = c.rolling(20, min_periods=20).min()
            rp = 2 * (c - lo) / (hi - lo) - 1
            r60 = c / c.shift(60) - 1
            ret = c.pct_change()
            v30 = ret.rolling(30, min_periods=20).std()
            vmed = v30.rolling(365, min_periods=60).median()
            for h in [3, 5]:
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    if i + h >= n: continue
                    rows.append(dict(coin=coin, win=w, h=h, ts=pd.Timestamp(df["timestamp"].iloc[i]),
                                     fc=df["forecast"].iloc[i], rp=rp.iloc[i], fwd=fwd.iloc[i],
                                     r60=r60.iloc[i], ag=(v30.iloc[i] > vmed.iloc[i]) if pd.notna(vmed.iloc[i]) else np.nan))
    d = pd.DataFrame(rows)
    d["day"] = d["ts"].dt.floor("D")
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    out = {}

    def slope_t(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 30: return pd.Series(dict(n=len(g), days=np.nan, slope=np.nan, t=np.nan))
        X = g[x].values; y = g["ex"].values
        Xc = X - X.mean(); b = (Xc * (y - y.mean())).sum() / (Xc ** 2).sum()
        a = y.mean() - b * X.mean(); e = y - a - b * X
        sc = pd.Series(Xc * e).groupby(g["day"].values).sum()
        G = len(sc); se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (Xc ** 2).sum()
        return pd.Series(dict(n=len(g), days=G, slope=b, t=b / se))

    def mean_t(g):
        s = g.groupby("day")["ex"].sum(); 
        return pd.Series(dict(n=len(g), days=len(s), mean=g["ex"].mean(), median=g["ex"].median(),
                              t=s.mean() / s.std() * np.sqrt(len(s)) if len(s) > 2 else np.nan))
    d5 = d[d.h == 5].copy()
    d5["trend"] = pd.cut(d5["r60"], [-10, -0.1, 0.1, 100], labels=["falling", "choppy", "rising"])
    d5["agit"] = d5["ag"].map({True: "agitated", False: "calm"})
    out["h5_slope_by_trend60"] = d5.groupby("trend").apply(slope_t)
    out["h5_slope_by_agit"] = d5.groupby("agit").apply(slope_t)
    out["h5_slope_by_profile"] = d5.groupby(["trend", "agit"]).apply(slope_t)
    top = d5[d5.rp > 0.99]
    out["top_close_mean_ex"] = mean_t(top)
    out["top_close_by_coin"] = top.groupby("coin").apply(mean_t)
    out["top_close_by_window"] = top.groupby("win").apply(mean_t)
    out["top_close_trimmed_mean_5_95"] = float(top["ex"].clip(top["ex"].quantile(.05), top["ex"].quantile(.95)).mean())
    out["top_close_by_trend60"] = top.groupby("trend").apply(mean_t)
    bot = d5[d5.rp < -0.99]
    out["bottom_close_mean_ex"] = mean_t(bot)
    out["upper_half_slope_rp"] = slope_t(d5[d5.rp > 0], "rp")
    out["lower_half_slope_rp"] = slope_t(d5[d5.rp <= 0], "rp")
    d3 = d[d.h == 3].copy()
    d3["trend"] = pd.cut(d3["r60"], [-10, -0.1, 0.1, 100], labels=["falling", "choppy", "rising"])
    out["h3_slope_by_trend60"] = d3.groupby("trend").apply(slope_t)
    return out
