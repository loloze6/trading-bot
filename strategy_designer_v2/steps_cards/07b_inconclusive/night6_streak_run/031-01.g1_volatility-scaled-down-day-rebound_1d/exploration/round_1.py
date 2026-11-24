def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            r1 = pd.Series(c).pct_change()
            vol = r1.rolling(60, min_periods=20).std()
            z = (r1 / vol).values
            ret60 = pd.Series(c).pct_change(30).values
            f = df["forecast"].values.astype(float)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in (1, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append((coin, w, h, i, f[i], z[i], ret60[i], yr[i], c[i + h] / c[i] - 1))
    D = pd.DataFrame(rows, columns=["coin", "w", "h", "i", "f", "z", "r30", "yr", "ret"])
    g = D.groupby(["coin", "h"])["ret"]
    D["u"] = (D["ret"] - g.transform("mean")) / g.transform("std")
    out = {}

    def slope(d):
        d = d.dropna(subset=["f", "u"])
        if len(d) < 30 or d["f"].std() == 0:
            return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        s = stats.linregress(d["f"], d["u"])
        return pd.Series({"n": len(d), "slope": s.slope, "t": s.slope / s.stderr})

    out["slope by horizon"] = D.groupby("h").apply(slope)
    d3 = D[D.h == 3]
    out["slope by coin h3"] = d3.groupby("coin").apply(slope)
    out["slope by year h3"] = d3.groupby("yr").apply(slope)
    d3 = d3.copy()
    d3["fb"] = pd.cut(d3["f"], [-0.1, 0.0001, 5, 10, 15, 21])
    out["u by forecast bin h3"] = d3.groupby("fb")["u"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    d3["zb"] = pd.cut(d3["z"], [-20, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3, 20])
    out["u by raw z h3"] = d3.groupby("zb")["u"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    d3["trend"] = np.where(d3["r30"] > 0, "up30", "down30")
    out["slope by 30d trend h3"] = d3[d3.f > 0].groupby("trend").apply(slope)
    out["slope f>0 only by horizon"] = D[D.f > 0].groupby("h").apply(slope)
    return out
