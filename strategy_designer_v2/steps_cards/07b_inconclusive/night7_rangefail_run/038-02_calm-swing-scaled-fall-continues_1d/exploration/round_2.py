def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=20).std()
            raw = (c / c.shift(5) - 1) / sd20
            n = len(b)
            for h in (3, 5, 7, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=str(b["timestamp"].iloc[i])[:10],
                                     year=str(b["timestamp"].iloc[i])[:4],
                                     calm=b["regime"].iloc[i] != "chop",
                                     raw=raw.iloc[i], fwd=c.iloc[i + h] / c.iloc[i] - 1))
    df = pd.DataFrame(rows).dropna(subset=["raw", "fwd"])
    df["ex"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    def slope(g):
        if len(g) < 30: return pd.Series(dict(n=len(g)))
        X = g["raw"].values; y = g["ex"].values
        Xc = X - X.mean(); bb = (Xc * (y - y.mean())).sum() / (Xc ** 2).sum()
        e = (y - y.mean() - bb * Xc) * Xc
        s = pd.Series(e).groupby(g["day"].values).sum()
        se = np.sqrt((s ** 2).sum()) / (Xc ** 2).sum()
        return pd.Series(dict(n=len(g), days=g.day.nunique(), slope=bb, t=bb / se))
    def mean_t(g):
        # signed excess in the move's direction, day-clustered t
        v = g["ex"] * np.sign(g["raw"])
        s = v.groupby(g["day"]).sum()
        nd = len(s); m = v.mean()
        se = np.sqrt(((s - v.groupby(g["day"]).size() * m) ** 2).sum()) / len(v)
        return pd.Series(dict(n=len(v), days=nd, mean=m, t=m / se if se > 0 else np.nan))
    out = {}
    out["calm_bothsides_slope_by_h"] = df[df.calm].groupby("h").apply(slope)
    out["agit_bothsides_slope_by_h"] = df[~df.calm].groupby("h").apply(slope)
    out["calm_rise_slope_by_h"] = df[df.calm & (df.raw > 0)].groupby("h").apply(slope)
    out["calm_fall_slope_by_h"] = df[df.calm & (df.raw < 0)].groupby("h").apply(slope)
    big = df[df.calm & (df.raw.abs() >= 2)]
    out["calm_big_dirmove_by_h"] = big.groupby("h").apply(mean_t)
    out["calm_big_dirmove_by_h_side"] = big.assign(side=np.where(big.raw > 0, "rise", "fall")).groupby(["h", "side"]).apply(mean_t)
    d = df[df.calm & (df.h == 5)]
    out["calm_h5_both_by_year"] = d.groupby("year").apply(slope)
    d10 = df[df.calm & (df.h == 10)]
    out["calm_h10_both_by_year"] = d10.groupby("year").apply(slope)
    return out
