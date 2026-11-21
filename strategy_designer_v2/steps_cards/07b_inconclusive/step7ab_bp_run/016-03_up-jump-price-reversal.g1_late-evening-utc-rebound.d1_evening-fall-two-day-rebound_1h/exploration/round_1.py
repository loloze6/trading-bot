def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [24, 48, 96, 168]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.concatenate(rs).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            n = len(c)
            r24 = pd.Series(c).pct_change(24).values
            r720 = pd.Series(c).pct_change(720).values
            lr = np.log(pd.Series(c)).diff()
            vol = lr.rolling(720).std().values
            ev = np.where(ts.dt.hour.values == 19)[0]
            for k, i in enumerate(ev):
                rec = dict(coin=coin, window=w, k=k, fc=df["forecast"].iloc[i],
                           r24=r24[i], r720=r720[i], vol=vol[i], year=ts.iloc[i].year)
                for h in H:
                    rec[f"x{h}"] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    cases = d[(d.fc > 0) & (d.k % 2 == 0)].dropna(subset=["x48"])

    def reg(g, col="x48", xcol="fc"):
        g = g.dropna(subset=[col, xcol])
        if len(g) < 10:
            return pd.Series(dict(n=len(g), slope_t=np.nan, mean=np.nan))
        s = stats.linregress(g[xcol], g[col])
        return pd.Series(dict(n=len(g), slope_t=s.slope / s.stderr, mean=g[col].mean(),
                              t_mean=g[col].mean() / (g[col].std() / np.sqrt(len(g)))))

    out["by_coin"] = cases.groupby("coin").apply(reg)
    out["by_year"] = cases.groupby("year").apply(reg)
    cases = cases.copy()
    cases["tq"] = pd.qcut(cases.fc, 5, labels=False, duplicates="drop")
    out["by_fc_quintile"] = cases.groupby("tq").agg(n=("x48", "size"), fc=("fc", "mean"),
                                                     x48=("x48", "mean"), x24=("x24", "mean"), x96=("x96", "mean"))
    hz = {}
    for h in H:
        step = max(1, int(np.ceil(h / 24)))
        g = d[(d.fc > 0) & (d.k % step == 0)]
        hz[h] = reg(g, f"x{h}")
    out["by_horizon"] = pd.DataFrame(hz).T
    cases["trend"] = np.where(cases.r720 > 0, "up30d", "down30d")
    out["by_trend"] = cases.groupby("trend").apply(reg)
    cases["volq"] = pd.qcut(cases.vol, 3, labels=["lowvol", "midvol", "highvol"])
    out["by_vol"] = cases.groupby("volq").apply(reg)
    # all evenings, raw 24h return, both sides
    a = d[d.k % 2 == 0].dropna(subset=["x48", "r24"]).copy()
    out["all_eve_raw_r24"] = reg(a, "x48", "r24").to_frame("v")
    a["rq"] = pd.qcut(a.r24, 5, labels=False)
    out["all_eve_r24_quintile"] = a.groupby("rq").agg(n=("x48", "size"), r24=("r24", "mean"),
                                                      x48=("x48", "mean"), x96=("x96", "mean"))
    return out
