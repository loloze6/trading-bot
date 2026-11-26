def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            r = pd.Series(c).pct_change()
            vol30 = r.rolling(30, min_periods=20).std()
            raw = df.get("debug_info.components.dip.last_history_value")
            for h in (1, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                                     ret=c[i + h] / c[i] - 1,
                                     fc=df["forecast"].iloc[i],
                                     reg=df["regime"].iloc[i],
                                     raw=(raw.iloc[i] if raw is not None else np.nan),
                                     vol30=vol30.iloc[i]))
    d = pd.DataFrame(rows)
    drift = d.groupby(["coin", "h"])["ret"].mean().rename("drift")
    d = d.join(drift, on=["coin", "h"])
    d["ex"] = d["ret"] - d["drift"]
    medvol = d[d.h == 1].groupby("coin")["vol30"].median().rename("mv")
    d = d.join(medvol, on="coin")
    d["agit"] = np.where(d["vol30"] > d["mv"], "agit", "calm")
    act = d[(d.fc != 0) & d.fc.notna()].copy()
    act["af"] = act["fc"].abs()

    def slope(g):
        g = g.dropna(subset=["ex", "af"])
        if len(g) < 15:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, mean_ex=np.nan))
        s = stats.linregress(g["af"], g["ex"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr,
                              mean_ex=g["ex"].mean(),
                              t_mean=g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g)))))

    out["by_horizon"] = act.groupby("h").apply(slope)
    a5 = act[act.h == 5]
    out["h5_by_coin"] = a5.groupby("coin").apply(slope)
    out["h5_by_window"] = a5.groupby("w").apply(slope)
    out["h5_by_agit"] = act.groupby(["h", "agit"]).apply(slope)
    act["q"] = act.groupby("h")["af"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["by_h_quintile_meanex"] = act.groupby(["h", "q"])["ex"].agg(["count", "mean"]).unstack(0)
    # depth in usual moves (raw) instead of standardised forecast
    a5r = a5.dropna(subset=["raw"]).copy()
    a5r["araw"] = a5r["raw"].abs()
    s = stats.linregress(a5r["araw"], a5r["ex"])
    out["h5_raw_depth_slope"] = pd.Series(dict(n=len(a5r), slope=s.slope, t=s.slope / s.stderr))
    out["h5_raw_quint"] = a5r.groupby(pd.qcut(a5r["araw"], 5, labels=False, duplicates="drop"))["ex"].agg(["count", "mean"])
    # comparison: regime-wide (in rising) vs out
    out["h5_rising_vs_not_meanex"] = d[d.h == 5].groupby(d["reg"] == "unknown")["ex"].agg(["count", "mean"])
    return out
