def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=20).std()
            raw = (c / c.shift(5) - 1) / sd20
            ret60 = c / c.shift(60) - 1
            n = len(b)
            for h in (2, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=str(b["timestamp"].iloc[i])[:10],
                                     year=str(b["timestamp"].iloc[i])[:4],
                                     calm=b["regime"].iloc[i] != "chop",
                                     fc=b["forecast"].iloc[i], raw=raw.iloc[i],
                                     t60=ret60.iloc[i],
                                     fwd=c.iloc[i + h] / c.iloc[i] - 1))
    df = pd.DataFrame(rows).dropna(subset=["raw", "fwd"])
    df["ex"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["trend"] = np.where(df.t60 > 0.10, "rising", np.where(df.t60 < -0.10, "falling",
                  np.where(df.t60.notna(), "choppy", "na")))
    def slope(g, x="raw"):
        if len(g) < 30: return pd.Series(dict(n=len(g)))
        X = g[x].values; y = g["ex"].values
        Xc = X - X.mean(); b = (Xc * (y - y.mean())).sum() / (Xc ** 2).sum()
        e = (y - y.mean() - b * Xc) * Xc
        s = pd.Series(e).groupby(g["day"].values).sum()
        se = np.sqrt((s ** 2).sum()) / (Xc ** 2).sum()
        return pd.Series(dict(n=len(g), days=g.day.nunique(), slope=b, t=b / se))
    out = {}
    # continuation: slope of excess on raw (positive slope = continuation), all signs
    out["slope_by_h_calm_side"] = df.assign(side=np.where(df.raw < 0, "fall", "rise")).groupby(["h", "calm", "side"]).apply(slope)
    d5 = df[df.h == 5]
    out["slope_h5_calm_fall_by_trend"] = d5[d5.calm & (d5.raw < 0)].groupby("trend").apply(slope)
    out["slope_h5_calm_rise_by_trend"] = d5[d5.calm & (d5.raw > 0)].groupby("trend").apply(slope)
    out["slope_h5_calm_all_by_year"] = d5[d5.calm].groupby("year").apply(slope)
    out["slope_h5_calm_all_by_coin"] = d5[d5.calm].groupby("coin").apply(slope)
    # quintile of raw in calm, mean excess
    q = d5[d5.calm].copy(); q["qq"] = pd.qcut(q.raw, 5, labels=False)
    out["calm_h5_quintiles"] = q.groupby("qq").agg(raw=("raw", "mean"), ex=("ex", "mean"), n=("ex", "size"))
    q = d5[~d5.calm].copy(); q["qq"] = pd.qcut(q.raw, 5, labels=False)
    out["agit_h5_quintiles"] = q.groupby("qq").agg(raw=("raw", "mean"), ex=("ex", "mean"), n=("ex", "size"))
    return out
