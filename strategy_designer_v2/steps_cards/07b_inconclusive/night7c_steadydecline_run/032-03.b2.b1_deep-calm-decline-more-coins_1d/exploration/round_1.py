def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 10
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            v = df["volume"].astype(float).values
            n = len(df)
            r28 = pd.Series(c).pct_change(28).values
            rng = ((df["high"] - df["low"]) / df["close"]).astype(float)
            rng_ratio = (rng.rolling(28).mean() / rng.rolling(90).mean().shift(28)).values
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, ts=df["timestamp"].iloc[i],
                                     ret=c[i + h] / c[i] - 1, fc=df["forecast"].iloc[i],
                                     reg=df["regime"].iloc[i], r28=r28[i], rr=rng_ratio[i]))
    d = pd.DataFrame(rows)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["adj"] = d["ret"] - d["drift"]
    d["short_adj"] = -d["adj"]
    out = {}

    def tstat(x):
        x = x.dropna()
        return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan

    def slope_t(g):
        g = g.dropna(subset=["adj", "fc"])
        if len(g) < 10: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, short_mean=np.nan))
        s = stats.linregress(g["fc"], g["adj"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr, short_mean=g["short_adj"].mean()))

    cases = d[(d.reg == "mean_reversion") & (d.fc < 0)]
    out["slope by horizon (cases)"] = cases.groupby("h").apply(slope_t)
    c10 = cases[cases.h == H].copy()
    c10["q"] = pd.qcut(c10["fc"], 5, labels=False, duplicates="drop")
    out["by forecast quintile h10 (0=deepest)"] = c10.groupby("q").agg(n=("adj", "size"), fc=("fc", "mean"),
        r28=("r28", "mean"), short_mean=("short_adj", "mean"), t=("short_adj", tstat))
    out["by coin h10"] = c10.groupby("coin").apply(slope_t)
    out["by window h10"] = c10.groupby("w").apply(slope_t)
    c10["year"] = pd.to_datetime(c10["ts"]).dt.year
    out["by year h10"] = c10.groupby("year").apply(slope_t)
    # falls outside the thin-volume regime (comparison)
    a10 = d[(d.h == H) & (d.r28 < 0)].copy()
    a10["thin"] = a10["reg"] == "mean_reversion"
    out["falls: thin vs not, h10"] = a10.groupby("thin").agg(n=("adj", "size"), r28=("r28", "mean"),
        short_mean=("short_adj", "mean"), t=("short_adj", tstat))
    # slope of adj on r28 within falls, thin vs not
    def sl28(g):
        g = g.dropna(subset=["adj", "r28"])
        s = stats.linregress(g["r28"], g["adj"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr))
    out["slope adj on r28 (falls) thin vs not"] = a10.groupby("thin").apply(sl28)
    # calm range split within cases
    c10["calm_range"] = c10["rr"] < 1
    out["cases by range calm"] = c10.groupby("calm_range").apply(slope_t)
    # regime of the market: coin's r28 cross-sectional? use BTC not allowed; use coin's 90d? split by depth sign of r28 magnitude
    c10["deep"] = pd.qcut(c10["r28"], 3, labels=["deep", "mid", "shallow"])
    out["cases by r28 tercile"] = c10.groupby("deep").agg(n=("adj", "size"), r28=("r28", "mean"),
        short_mean=("short_adj", "mean"), t=("short_adj", tstat), raw=("ret", "mean"))
    return out
