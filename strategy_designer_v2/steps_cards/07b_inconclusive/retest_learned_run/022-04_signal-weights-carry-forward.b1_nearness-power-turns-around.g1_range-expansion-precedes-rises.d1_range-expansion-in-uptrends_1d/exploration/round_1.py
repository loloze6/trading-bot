def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for h in [1, 3, 5, 10]:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(rs)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]; rng = (df["high"] - df["low"]) / df["close"]
            ratio = (df["high"] - df["low"]) / (df["high"] - df["low"]).rolling(30, min_periods=30).mean()
            r20 = c / c.shift(20) - 1
            day = c / c.shift(1) - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            n = len(df)
            for h in [1, 3, 5, 10]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, year=yr.iloc[i], fc=df["forecast"].iloc[i],
                                     reg=df["regime"].iloc[i], ratio=ratio.iloc[i], r20=r20.iloc[i],
                                     day=day.iloc[i], fwd=c.iloc[i + h] / c.iloc[i] - 1))
    R = pd.DataFrame(rows)
    R["ex"] = R["fwd"] - [drift[(a, b)] for a, b in zip(R.coin, R.h)]

    def slope(d, x="fc"):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 20 or d[x].std() == 0: return pd.Series(dict(n=len(d), slope=np.nan, t=np.nan, mean_ex=np.nan))
        res = stats.linregress(d[x], d["ex"])
        return pd.Series(dict(n=len(d), slope=res.slope, t=res.slope / res.stderr, mean_ex=d["ex"].mean()))

    T = R[(R.reg == "trending")]
    out = {}
    out["by_horizon_trending_fc"] = T.groupby("h").apply(slope)
    out["by_horizon_trending_ratio"] = T.groupby("h").apply(lambda d: slope(d, "ratio"))
    out["by_horizon_downtrend_ratio"] = R[R.r20 <= 0].groupby("h").apply(lambda d: slope(d, "ratio"))
    out["by_horizon_all_ratio"] = R.groupby("h").apply(lambda d: slope(d, "ratio"))
    T5 = T[T.h == 5]
    out["h5_by_coin"] = T5.groupby("coin").apply(slope)
    out["h5_by_year"] = T5.groupby("year").apply(slope)
    T5 = T5.copy()
    T5["upday"] = np.where(T5["day"] > 0, "up", "down")
    out["h5_by_dayside"] = T5.groupby("upday").apply(lambda d: slope(d, "ratio"))
    T5["r20q"] = pd.qcut(T5["r20"], 3, labels=["low", "mid", "high"])
    out["h5_by_r20_tercile"] = T5.groupby("r20q").apply(lambda d: slope(d, "ratio"))
    T5["fq"] = pd.qcut(T5["fc"].rank(method="first"), 5, labels=False)
    out["h5_fc_quintiles"] = T5.groupby("fq").agg(n=("ex", "size"), mean_ex=("ex", "mean"), fc=("fc", "mean"))
    return out
