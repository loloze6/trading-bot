def explore(data):
    import numpy as np, pandas as pd
    H = 7
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values.astype(float))
            n = len(c)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            volyr = vol30.rolling(365, min_periods=60).median()
            r30 = c.pct_change(30)
            r60 = c.pct_change(60)
            for off in range(H):
                for i in range(off, n - H, H):
                    rows.append(dict(coin=coin, w=w, wn=int(w[1:]), off=off,
                                     day=str(b["timestamp"].iloc[i])[:10],
                                     fwd=c[i + H] / c[i] - 1,
                                     choppy=b["regime"].iloc[i] == "mean_reversion",
                                     r60=r60[i], r30=r30[i], fc=b["forecast"].iloc[i],
                                     agit=(vol30[i] > volyr[i]) if pd.notna(volyr[i]) else np.nan,
                                     vrel=vol30[i] / volyr[i] if pd.notna(volyr[i]) else np.nan))
    g = pd.DataFrame(rows)
    base = g[g.off == 0]
    drift = base.groupby("coin")["fwd"].mean()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    def summ(d, col="ex"):
        d = d.dropna(subset=[col])
        if len(d) < 5: return pd.Series(dict(n=len(d), days=d.day.nunique(), mean=np.nan, t=np.nan))
        m = d[col].mean()
        dev = (d[col] - m).groupby(d["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(d)
        return pd.Series(dict(n=len(d), days=D, mean=m, t=m / se))
    out = {}
    ch0 = g[(g.off == 0) & g.choppy].copy()
    ch0["fc_neg"] = ch0.fc < 0
    ch0["r30_neg"] = ch0.r30 < 0
    out["choppy_fcneg_x_r30neg"] = ch0.groupby(["fc_neg", "r30_neg"]).apply(summ)
    # falls in choppy, by agitation (profile def) and by fall depth tercile, offset 0
    f0 = ch0[ch0.r30 < 0].copy()
    f0["depth"] = pd.qcut(f0.r30, 3, labels=["deep", "mid", "shallow"])
    out["choppy_fall_depth_x_agit_off0"] = f0.groupby(["agit", "depth"]).apply(summ)
    # robustness over grid offsets: deep falls in choppy (r30 in lowest third of falls)
    chall = g[g.choppy & (g.r30 < 0)].copy()
    cut = f0.r30.quantile(1/3)
    chall["deep"] = chall.r30 <= cut
    out["choppy_fall_by_offset"] = chall.groupby(["off", "deep"]).apply(summ)["mean"].unstack()
    # by window, choppy falls, all offsets pooled (counted per offset averaged)
    out["choppy_fall_agit_by_window"] = chall[chall.agit == True].groupby("wn").apply(summ)
    out["choppy_fall_calm_by_window"] = chall[chall.agit == False].groupby("wn").apply(summ)
    # graded: correlation of r30 with ex inside choppy falls, agitated
    a = f0[f0.agit == True].dropna(subset=["ex"])
    out["agit_fall_corr_r30_ex"] = float(a.r30.corr(a.ex))
    out["agit_fall_n_coins"] = a.groupby("coin").apply(summ)
    # non-choppy (trend) agitated falls for contrast
    nf = g[(g.off == 0) & ~g.choppy & (g.r30 < 0)]
    out["nonchoppy_fall_by_agit"] = nf.groupby("agit").apply(summ)
    return out
