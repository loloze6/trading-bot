import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            for h in (5, 10, 20, 40):
                for i in range(0, n, h):
                    if i + h >= n:
                        break
                    r20 = c[i]/c[i-20]-1 if i >= 20 else np.nan
                    r60 = c[i]/c[i-60]-1 if i >= 60 else np.nan
                    rows.append((coin, w, h, i, yr[i], f[i], c[i+h]/c[i]-1, r20, r60))
    d = pd.DataFrame(rows, columns=["coin","win","h","i","year","fc","fwd","r20","r60"])
    d["drift"] = d.groupby(["coin","h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]

    def slope_t(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan, "corr": np.nan})
        X = g[x] - g[x].mean()
        b = (X*g["ex"]).sum()/(X**2).sum()
        res = g["ex"] - g["ex"].mean() - b*X
        se = np.sqrt((res**2).sum()/(len(g)-2)/(X**2).sum())
        return pd.Series({"n": len(g), "slope": b, "t": b/se, "corr": np.corrcoef(X, g["ex"])[0,1]})

    out = {}
    out["by horizon, fc"] = d.groupby("h").apply(slope_t)
    d10 = d[d.h == 10]
    out["h10 by coin"] = d10.groupby("coin").apply(slope_t)
    out["h10 by year"] = d10.groupby("year").apply(slope_t)
    d10q = d10.copy()
    d10q["q"] = pd.qcut(d10q["fc"].rank(method="first"), 5, labels=False)
    out["h10 by fc quintile: mean fc, mean ex, signed ex, n"] = d10q.groupby("q").agg(
        fc=("fc","mean"), ex=("ex","mean"), n=("ex","size"))
    d10s = d10.copy()
    d10s["side"] = np.sign(d10s["fc"])
    out["h10 by side"] = d10s.groupby("side").apply(slope_t)
    out["by horizon, r60"] = d.groupby("h").apply(lambda g: slope_t(g, "r60"))
    out["by horizon, r20 raw"] = d.groupby("h").apply(lambda g: slope_t(g, "r20"))
    return out
