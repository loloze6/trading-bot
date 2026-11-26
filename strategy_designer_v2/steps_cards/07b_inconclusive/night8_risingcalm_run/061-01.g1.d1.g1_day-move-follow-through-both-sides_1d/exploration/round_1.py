def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            ret60 = c / c.shift(60) - 1
            for h in (1, 3, 5, 10):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                for i in idx:
                    if i + h >= len(b):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, year=pd.Timestamp(b.loc[i, "timestamp"]).year,
                                     f=float(b.loc[i, "forecast"]), z=r.iloc[i] / sd30.iloc[i] if sd30.iloc[i] > 0 else np.nan,
                                     sd30=sd30.iloc[i], ret60=ret60.iloc[i], fwd=fwd.iloc[i]))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    med = df[df.h == 1].groupby("coin")["sd30"].median()
    df["agit"] = np.where(df["sd30"] > df["coin"].map(med), "agitated", "calm")
    df.loc[df["sd30"].isna(), "agit"] = np.nan
    df["trend"] = pd.cut(df["ret60"], [-np.inf, -0.10, 0.10, np.inf], labels=["falling", "choppy", "rising"])

    def slope(g, x="f"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 30 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, top5=np.nan, top5_t=np.nan))
        res = stats.linregress(g[x], g["ex"])
        thr = g[x].abs().quantile(0.8)
        top = g[g[x].abs() >= thr]
        v = np.sign(top[x]) * top["ex"]
        return pd.Series(dict(n=len(g), slope=res.slope, t=res.slope / res.stderr,
                              top5=v.mean(), top5_t=v.mean() / (v.std() / np.sqrt(len(v)))))
    out = {}
    d5 = df[df.h == 5]
    out["by_horizon"] = df.groupby("h").apply(slope)
    out["h5_by_agit"] = d5.groupby("agit").apply(slope)
    out["by_h_agit"] = df.groupby(["h", "agit"]).apply(slope)
    out["h5_by_trend"] = d5.groupby("trend").apply(slope)
    out["h5_by_trend_agit"] = d5.groupby(["trend", "agit"]).apply(slope)
    out["h5_by_coin"] = d5.groupby("coin").apply(slope)
    out["h5_by_year"] = d5.groupby("year").apply(slope)
    d5s = d5.copy(); d5s["side"] = np.where(d5s.f > 0, "up", "down")
    out["h5_by_side_agit"] = d5s.groupby(["side", "agit"]).apply(slope)
    out["h5_by_window"] = d5.groupby("w").apply(slope)
    return out
