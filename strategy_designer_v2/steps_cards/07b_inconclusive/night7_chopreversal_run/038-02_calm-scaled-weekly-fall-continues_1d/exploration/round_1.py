import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            dr = c.pct_change()
            sd = dr.rolling(30, min_periods=20).std()
            r7 = c / c.shift(7) - 1
            sc = r7 / (sd * np.sqrt(7))
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in (2, 5, 10):
                idx = np.arange(0, len(df) - h, h)
                fr = (c.shift(-h) / c - 1).values
                for i in idx:
                    rows.append(dict(coin=coin, w=w, h=h, day=str(df["timestamp"].iloc[i])[:10],
                                     year=yr.iloc[i], regime=df["regime"].iloc[i],
                                     sc=sc.iloc[i], fc=df["forecast"].iloc[i], r=fr[i]))
    d = pd.DataFrame(rows).dropna(subset=["r"])
    d["drift"] = d.groupby(["coin", "h"])["r"].transform("mean")
    d["u"] = d["r"] - d["drift"]
    d["calm"] = np.where(d["regime"] == "chop", "agit", "calm")
    d = d.dropna(subset=["sc"])
    d["side"] = np.where(d["sc"] < 0, "fall", "rise")
    # direction-of-continuation unusual move
    d["cu"] = np.where(d["side"] == "fall", -d["u"], d["u"])

    def tday(g, col="cu"):
        s = g.groupby("day")[col].sum()
        n = len(s)
        m = g[col].mean()
        t = s.mean() / (s.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series(dict(n=len(g), days=n, mean=m, t=t))

    out = {}
    out["by_h_regime_side"] = d.groupby(["h", "calm", "side"]).apply(tday)
    d5 = d[(d.h == 5)].copy()
    d5["q"] = d5.groupby(["calm", "side"])["sc"].transform(lambda x: pd.qcut(x.abs(), 3, labels=False, duplicates="drop"))
    out["h5_by_size_tercile"] = d5.groupby(["calm", "side", "q"]).apply(tday)
    cf = d5[(d5.calm == "calm") & (d5.side == "fall")]
    out["h5_calm_fall_by_coin"] = cf.groupby("coin").apply(tday)
    out["h5_calm_fall_by_year"] = cf.groupby("year").apply(tday)
    out["h5_calm_fall_by_window"] = cf.groupby("w").apply(tday)
    # raw return and drift for calm falls
    out["h5_calm_fall_raw_mean_r"] = float(cf["r"].mean())
    out["h5_calm_fall_mean_drift"] = float(cf["drift"].mean())
    # forecast<0 cases specifically
    fneg = d5[d5["fc"] < 0]
    out["h5_fc_neg"] = tday(fneg)
    return out
