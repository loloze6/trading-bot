def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r28 = c / c.shift(28) - 1
            hi28 = c.rolling(28, min_periods=28).max()
            dist = c / hi28 - 1
            n = len(c)
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, pos=i,
                                     fwd=c.iloc[i + h] / c.iloc[i] - 1,
                                     r28=r28.iloc[i], dist=dist.iloc[i],
                                     fc=b["forecast"].iloc[i], reg=b["regime"].iloc[i],
                                     year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby(["coin", "h"])["fwd"].transform("mean")
    out = {}
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g["ex"].mean(),
                          "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "mean_fwd": g["fwd"].mean()})
    for h in (5, 10, 20):
        dh = d[d.h == h].dropna(subset=["r28", "dist"])
        hi = dh[dh.dist >= 0].copy()
        out[f"h{h} at high vs not"] = dh.groupby(dh.dist >= 0).apply(summ)
        if len(hi) > 10:
            hi["q"] = pd.qcut(hi["r28"], 4, labels=False)
            out[f"h{h} at-high by r28 quartile"] = hi.groupby("q").apply(summ).join(hi.groupby("q")["r28"].mean().rename("r28_mean"))
            s = stats.linregress(hi["r28"], hi["ex"])
            out[f"h{h} at-high slope ex on r28 (slope,t)"] = f"{s.slope:.4f}, t {s.slope/s.stderr:.2f}, n {len(hi)}"
        dh = dh.copy()
        dh["dq"] = pd.qcut(dh["dist"].rank(method="first"), 5, labels=False)
        out[f"h{h} all bars by dist quintile"] = dh.groupby("dq").apply(summ).join(dh.groupby("dq")["dist"].mean().rename("dist_mean"))
    d5 = d[(d.h == 5)].dropna(subset=["r28", "dist"])
    hi5 = d5[d5.dist >= 0]
    out["h5 at-high by coin"] = hi5.groupby("coin").apply(summ)
    out["h5 at-high by window"] = hi5.groupby("win").apply(summ)
    out["h5 at-high by sign of r28"] = hi5.groupby(hi5.r28 > 0).apply(summ)
    return out
