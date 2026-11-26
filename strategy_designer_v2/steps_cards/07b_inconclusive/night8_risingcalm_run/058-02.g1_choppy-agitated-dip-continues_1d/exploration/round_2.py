def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            sd365med = sd.rolling(365, min_periods=120).median()
            mx = c.rolling(5, min_periods=5).max()
            depth = (c - mx) / mx / sd
            tr60 = c / c.shift(60) - 1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            n = len(b)
            for h in (3, 5):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    rows.append(dict(coin=coin, w=w, h=h, depth=depth.iloc[i], fwd=fwd.iloc[i],
                                     tr=tr60.iloc[i], ag=(sd.iloc[i] > sd365med.iloc[i]) if pd.notna(sd365med.iloc[i]) else np.nan,
                                     yr=yr.iloc[i], day=str(pd.to_datetime(b["timestamp"].iloc[i]).date())))
    df = pd.DataFrame(rows).dropna(subset=["fwd", "depth"])
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["adj"] = df["fwd"] - df["drift"]
    def slope(g):
        if len(g) < 10 or g["depth"].std() == 0: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        s = stats.linregress(g["depth"], g["adj"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr))
    out = {}
    d5 = df[df.h == 5].copy()
    out["h5_all"] = slope(d5)
    out["h5_by_coin"] = d5.groupby("coin").apply(slope)
    out["h5_by_year"] = d5.groupby("yr").apply(slope)
    out["h5_by_window"] = d5.groupby("w").apply(slope)
    d5["trb"] = pd.cut(d5["tr"], [-10, -0.1, 0.1, 10], labels=["falling", "choppy", "rising"])
    d5a = d5.dropna(subset=["ag", "trb"])
    out["h5_by_profile"] = d5a.groupby(["trb", "ag"]).apply(slope)
    dip = d5[d5.depth < 0]
    out["h5_dips_only"] = slope(dip)
    at = d5[d5.depth == 0]
    out["at_high_vs_dip_mean_adj"] = pd.Series(dict(at_high=at["adj"].mean(), n_at=len(at), dip=dip["adj"].mean(), n_dip=len(dip)))
    # day-clustered t for the slope (sum residual-weighted per day)
    x = d5["depth"] - d5["depth"].mean(); y = d5["adj"]
    b1 = (x * y).sum() / (x ** 2).sum(); e = y - y.mean() - b1 * x
    sc = (x * e).groupby(d5["day"]).sum()
    se = np.sqrt((sc ** 2).sum()) / (x ** 2).sum()
    out["h5_all_day_clustered"] = pd.Series(dict(slope=b1, t=b1 / se, days=sc.size))
    out["h3_all"] = slope(df[df.h == 3])
    return out
