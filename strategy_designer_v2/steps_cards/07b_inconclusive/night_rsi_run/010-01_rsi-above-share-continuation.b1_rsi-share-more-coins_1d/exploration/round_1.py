def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    fc = "debug_info.components.rsi_share.last_history_value"
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            raw = df[fc].values if fc in df.columns else np.full(len(df), np.nan)
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r60 = pd.Series(c).pct_change(60).values
            for h in [3, 7, 14, 30]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], raw=raw[i], yr=yr[i],
                                     r60=r60[i], ret=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows).dropna(subset=["f", "ret"])
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")
    def slope_t(g, x="f"):
        g = g.dropna(subset=[x])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g[x], g["ex"])
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})
    out = {}
    out["by_horizon"] = d.groupby("h").apply(slope_t)
    out["by_horizon_raw"] = d.groupby("h").apply(lambda g: slope_t(g, "raw"))
    d14 = d[d.h == 14].copy()
    out["by_coin_14"] = d14.groupby("coin").apply(slope_t)
    out["by_year_14"] = d14.groupby("yr").apply(slope_t)
    d14["side"] = np.where(d14["f"] > 0, "long", np.where(d14["f"] < 0, "short", "flat"))
    out["side_14"] = d14.groupby("side")["ex"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    d14["q"] = pd.qcut(d14["raw"].rank(method="first"), 5, labels=False)
    out["raw_quintile_14"] = d14.groupby("q").agg(n=("ex", "count"), raw=("raw", "mean"), ex=("ex", "mean"), ret=("ret", "mean"))
    d14["trend"] = np.where(d14["r60"] > 0, "up60", "down60")
    out["by_trend_14"] = d14.dropna(subset=["r60"]).groupby("trend").apply(slope_t)
    d30 = d[d.h == 30].copy()
    d30["q"] = pd.qcut(d30["raw"].rank(method="first"), 5, labels=False)
    out["raw_quintile_30"] = d30.groupby("q").agg(n=("ex", "count"), raw=("raw", "mean"), ex=("ex", "mean"))
    return out
