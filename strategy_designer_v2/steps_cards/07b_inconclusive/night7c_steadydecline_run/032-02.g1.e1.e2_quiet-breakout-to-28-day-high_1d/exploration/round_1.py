def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for H in (1, 3, 5, 10, 20):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rs.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = (np.mean(rs), np.std(rs, ddof=1))
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            hi28 = pd.Series(c).rolling(28, min_periods=1).max().values
            r20 = pd.Series(c).pct_change().rolling(20).std()
            r60 = pd.Series(c).pct_change().rolling(60).std()
            ret28 = pd.Series(c).pct_change(28).values
            n = len(c)
            for H in (1, 3, 5, 10, 20):
                for i in range(0, n - H, H):
                    if df["regime"].iloc[i] != "trending":
                        continue
                    f = df["forecast"].iloc[i]
                    if pd.isna(f):
                        continue
                    m, s = drift[(coin, H)]
                    rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, H=H, f=f,
                                     ex=c[i + H] / c[i] - 1 - m, ex_sd=(c[i + H] / c[i] - 1 - m) / s,
                                     ratio=(r20.iloc[i] / r60.iloc[i]) if not pd.isna(r60.iloc[i]) else np.nan,
                                     ret28=ret28[i]))
    d = pd.DataFrame(rows)

    def slope_t(g):
        g = g.dropna(subset=["f", "ex"])
        if len(g) < 8 or g["f"].std() == 0:
            return pd.Series(dict(n=len(g), t=np.nan, mean_ex=g["ex"].mean() if len(g) else np.nan))
        r = stats.linregress(g["f"], g["ex"])
        tt = r.slope / r.stderr
        q = np.floor(len(g) / 3).astype(int)
        gs = g.sort_values("f")
        tb = gs["ex"].iloc[-q:].mean() - gs["ex"].iloc[:q].mean() if q > 0 else np.nan
        return pd.Series(dict(n=len(g), t=tt, mean_ex=g["ex"].mean(), top_minus_bot=tb,
                              t_mean=stats.ttest_1samp(g["ex"], 0).statistic))

    out = {}
    out["by_horizon"] = d.groupby("H").apply(slope_t)
    d5 = d[d.H == 5]
    out["h5_by_coin"] = d5.groupby("coin").apply(slope_t)
    out["h5_by_year"] = d5.groupby("year").apply(slope_t)
    out["h5_by_window"] = d5.groupby("w").apply(slope_t)
    d5 = d5.copy()
    d5["fbin"] = pd.qcut(d5["f"], 5, labels=False, duplicates="drop")
    out["h5_by_forecast_quintile"] = d5.groupby("fbin").agg(n=("ex", "size"), f=("f", "mean"),
                                                             mean_ex=("ex", "mean"), ratio=("ratio", "mean"))
    d5["side"] = np.where(d5["f"] > 0, "compressed", "expanded")
    out["h5_by_side"] = d5.groupby("side").apply(slope_t)
    d10 = d[d.H == 10].copy()
    d10["fbin"] = pd.qcut(d10["f"], 5, labels=False, duplicates="drop")
    out["h10_by_forecast_quintile"] = d10.groupby("fbin").agg(n=("ex", "size"), mean_ex=("ex", "mean"))
    d20 = d[d.H == 20].copy()
    d20["fbin"] = pd.qcut(d20["f"], 4, labels=False, duplicates="drop")
    out["h20_by_forecast_quartile"] = d20.groupby("fbin").agg(n=("ex", "size"), mean_ex=("ex", "mean"))
    # raw ratio instead of standardised forecast
    g = d5.dropna(subset=["ratio"])
    r = stats.linregress(-g["ratio"], g["ex"])
    out["h5_raw_ratio_slope_t"] = float(r.slope / r.stderr)
    d5["r28bin"] = pd.qcut(d5["ret28"], 3, labels=["low", "mid", "high"])
    out["h5_by_ret28_tercile"] = d5.groupby("r28bin").apply(slope_t)
    return out
