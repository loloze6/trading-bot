def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for H in [5, 10, 20]:
        for coin, wins in bars.items():
            allr = []; cells = []
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                vs = pd.Series(df["volume"].values)
                rec = np.log(vs.rolling(30).mean() / vs.shift(30).rolling(30).mean()).values
                rawc = df.get("debug_info.components.vol_dryup.last_history_value")
                rawv = rawc.values if rawc is not None else np.full(len(df), np.nan)
                lr = np.log(pd.Series(c)).diff()
                sd30 = lr.rolling(30).std()
                med = sd30.rolling(365, min_periods=120).median()
                agit = (sd30 > med).values
                fc = df["forecast"].values
                n = len(df)
                for t in range(0, n - H, H):
                    r = c[t + H] / c[t] - 1
                    allr.append(r)
                    cells.append(dict(H=H, coin=coin, w=w, r=r, regime=df["regime"].iloc[t],
                                      raw=rawv[t] if not np.isnan(rawv[t]) else rec[t], fc=fc[t],
                                      yr=pd.Timestamp(df["timestamp"].iloc[t]).year,
                                      agit=("agitated" if agit[t] else "calm") if not np.isnan(med.values[t]) else "na"))
            m = np.mean(allr)
            for cc in cells:
                cc["ex_short"] = -(cc["r"] - m); rows.append(cc)
    d = pd.DataFrame(rows)
    f = d[d.regime == "unknown"].dropna(subset=["raw"])
    def sl(g, x):
        if len(g) < 8: return pd.Series({"n": len(g), "slope_t": np.nan})
        s = stats.linregress(x(g), g.ex_short)
        return pd.Series({"n": len(g), "slope": s.slope, "slope_t": s.slope / s.stderr})
    res = {}
    for H in [5, 10, 20]:
        g = f[f.H == H]
        out[f"H{H}_rawslope_by_year"] = g.groupby("yr").apply(lambda q: sl(q, lambda z: -z.raw))
        out[f"H{H}_rawslope_by_agit"] = g.groupby("agit").apply(lambda q: sl(q, lambda z: -z.raw))
        gs = g[g.fc < 0]
        out[f"H{H}_fcslope_by_year"] = gs.groupby("yr").apply(lambda q: sl(q, lambda z: -z.fc))
        out[f"H{H}_rawslope_by_coin"] = g.groupby("coin").apply(lambda q: sl(q, lambda z: -z.raw))
    g10 = f[f.H == 10].copy()
    g10["q"] = pd.qcut(g10.raw, 5, labels=False)
    out["H10_raw_quintile"] = g10.groupby("q").agg(n=("ex_short", "size"), mean_ex=("ex_short", "mean"),
                                                   sd=("ex_short", "std"), raw=("raw", "mean"))
    return out
