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
            raw = df[fc].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r60 = pd.Series(c).pct_change(60).values
            r30 = pd.Series(c).pct_change(30).values
            h = 14
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, raw=raw[i], yr=yr[i], r60=r60[i], r30=r30[i], ret=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows).dropna(subset=["raw", "ret"])
    d["ex"] = d["ret"] - d.groupby("coin")["ret"].transform("mean")
    def st(g, x="raw"):
        g = g.dropna(subset=[x])
        if len(g) < 8 or g[x].std() == 0:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g[x], g["ex"])
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})
    out = {}
    dn = d.dropna(subset=["r60"])
    down = dn[dn.r60 <= 0].copy()
    up = dn[dn.r60 > 0].copy()
    out["down_by_coin"] = down.groupby("coin").apply(st)
    out["down_by_year"] = down.groupby("yr").apply(st)
    down["q"] = pd.qcut(down["raw"].rank(method="first"), 4, labels=False)
    out["down_quartile"] = down.groupby("q").agg(n=("ex", "count"), raw=("raw", "mean"), r30=("r30", "mean"), ex=("ex", "mean"), ret=("ret", "mean"))
    up["q"] = pd.qcut(up["raw"].rank(method="first"), 4, labels=False)
    out["up_quartile"] = up.groupby("q").agg(n=("ex", "count"), raw=("raw", "mean"), ex=("ex", "mean"))
    out["down_noXRP"] = st(down[down.coin != "XRPUSD"])
    out["all_14_raw_n"] = st(d)
    out["nan_r60_share"] = float(d["r60"].isna().mean())
    return out
