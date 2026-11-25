def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            lr = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol30 = pd.Series(lr).rolling(30, min_periods=30).std().values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in [1, 5]:
                for t in range(0, n - h, h):
                    tr = c[t] / c[t - 60] - 1 if t >= 60 else np.nan
                    r20 = c[t] / c[t - 20] - 1 if t >= 20 else np.nan
                    rows.append(dict(coin=coin, w=w, h=h, f=f[t], r=c[t + h] / c[t] - 1, yr=yr[t],
                                     tr=tr, half=int(t >= n / 2), vol=vol30[t], r20=r20, n=n))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby(["coin", "h"])["r"].transform("mean")
    # agitation proxy: 30d vol vs coin median 30d vol across explored windows (coarse, uses whole sample)
    d["agit"] = np.where(d["vol"] > d.groupby("coin")["vol"].transform("median"), "agitated", "calm")
    d.loc[d["vol"].isna(), "agit"] = np.nan

    def reg(g):
        g = g.dropna(subset=["f", "ex"])
        if len(g) < 30 or g["f"].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        s = stats.linregress(g["f"], g["ex"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr))

    out = {}
    d5 = d[d.h == 5].copy()
    d5["signed_ex"] = np.sign(d5["f"]) * d5["ex"]
    out["h5_by_half"] = d5.groupby("half").apply(reg)
    out["h5_by_agit"] = d5.groupby("agit").apply(reg)
    out["h5_by_agit_year"] = d5.groupby(["agit", "yr"]).apply(reg)
    d5["absq"] = pd.qcut(d5["f"].abs(), 4, labels=False, duplicates="drop")
    out["h5_signed_ex_by_absf_quartile"] = d5.groupby("absq")["signed_ex"].agg(
        n="size", mean="mean", t=lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    out["h5_signed_ex_by_year"] = d5.groupby("yr")["signed_ex"].agg(
        n="size", mean="mean", t=lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    d5["side"] = np.sign(d5["f"])
    out["h5_side_year_meanex"] = d5.groupby(["side", "yr"])["ex"].agg(
        n="size", mean="mean", t=lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    d1 = d[d.h == 1].copy()
    out["h1_by_year"] = d1.groupby("yr").apply(reg)
    out["h1_by_agit"] = d1.groupby("agit").apply(reg)
    # raw 20d return (not scaled) vs scaled forecast, h5
    g = d5.dropna(subset=["r20", "ex", "f"])
    s1 = stats.linregress(g["r20"], g["ex"]); s2 = stats.linregress(g["f"], g["ex"])
    out["h5_raw_vs_scaled"] = pd.DataFrame({"n": [len(g), len(g)], "slope": [s1.slope, s2.slope],
                                            "t": [s1.slope / s1.stderr, s2.slope / s2.stderr], "r": [s1.rvalue, s2.rvalue]},
                                           index=["raw_r20", "scaled_forecast"])
    return out
