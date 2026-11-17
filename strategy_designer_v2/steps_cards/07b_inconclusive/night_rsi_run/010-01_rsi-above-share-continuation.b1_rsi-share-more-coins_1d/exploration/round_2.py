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
            raw = df[fc].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r60 = pd.Series(c).pct_change(60).values
            r30 = pd.Series(c).pct_change(30).values
            for h in [7, 14, 30]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], raw=raw[i], yr=yr[i],
                                     r60=r60[i], r30=r30[i], ret=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows).dropna(subset=["f", "ret"])
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")
    def st(g, x="f"):
        g = g.dropna(subset=[x])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g[x], g["ex"])
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})
    out = {}
    d["trend"] = np.where(d["r60"] > 0, "up60", "down60")
    dd = d.dropna(subset=["r60"])
    out["trend_by_h"] = dd.groupby(["h", "trend"]).apply(st)
    out["trend_by_h_raw"] = dd.groupby(["h", "trend"]).apply(lambda g: st(g, "raw"))
    out["noXRP_by_h"] = d[d.coin != "XRPUSD"].groupby("h").apply(st)
    d14 = d[d.h == 14].copy()
    d14["absraw"] = d14["raw"].abs()
    d14["ext"] = pd.qcut(d14["absraw"].rank(method="first"), 3, labels=["mild", "mid", "extreme"])
    out["by_extremity_14"] = d14.groupby("ext").apply(lambda g: st(g, "raw"))
    out["r30_14"] = st(d14.dropna(subset=["r30"]), "r30")
    out["r30_by_trend_14"] = d14.dropna(subset=["r30", "r60"]).groupby("trend").apply(lambda g: st(g, "r30"))
    out["coin_year_sign_14"] = d14.groupby("yr").apply(lambda g: pd.Series({"share_coins_pos": np.mean([st(x)["slope"] > 0 for _, x in g.groupby("coin")])}))
    return out
