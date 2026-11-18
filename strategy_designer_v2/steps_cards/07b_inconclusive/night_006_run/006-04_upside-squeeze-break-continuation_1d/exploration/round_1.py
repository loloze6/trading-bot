def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            fc = df["forecast"].values
            raw = df.get("debug_info.components.compression.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            hi20 = df["high"].shift(1).rolling(20).max().values
            for h in [1, 3, 5, 10]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, wn=int(w[1:]), h=h, i=i, yr=yr[i],
                                     fc=fc[i], raw=raw[i], r=c[i+h]/c[i]-1,
                                     brkdist=(c[i]/hi20[i]-1) if not np.isnan(hi20[i]) else np.nan))
    d = pd.DataFrame(rows)
    d["base"] = d.groupby(["coin", "h"])["r"].transform("mean")
    d["ex"] = d["r"] - d["base"]
    out = {}
    def slope(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 8 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, mean_ex=np.nan))
        r = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope/r.stderr, mean_ex=g["ex"].mean(),
                              t_mean=g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g)))))
    b = d[d.fc > 0]
    out["by_h"] = b.groupby("h").apply(slope)
    out["by_h_raw"] = b.groupby("h").apply(lambda g: slope(g, "raw"))
    b3 = b[b.h == 3].copy()
    out["h3_by_coin"] = b3.groupby("coin").apply(slope)
    out["h3_by_year"] = b3.groupby("yr").apply(slope)
    b3["q"] = pd.qcut(b3["fc"], 4, labels=False, duplicates="drop")
    out["h3_by_fc_quart"] = b3.groupby("q").agg(n=("ex", "size"), fc=("fc", "mean"), raw=("raw", "mean"),
                                                 mean_ex=("ex", "mean"), sd=("ex", "std"))
    # break vs non-break by h
    d["brk"] = d.fc > 0
    tt = []
    for h, g in d.groupby("h"):
        a = g[g.brk]["ex"]; z = g[~g.brk]["ex"]
        t = stats.ttest_ind(a, z, equal_var=False)
        tt.append(dict(h=h, n_brk=len(a), mean_brk=a.mean(), n_non=len(z), mean_non=z.mean(), t=t.statistic,
                       absret_brk=g[g.brk]["r"].abs().mean(), absret_non=g[~g.brk]["r"].abs().mean()))
    out["brk_vs_non"] = pd.DataFrame(tt)
    # market drift: corr fc with base? coin mean 3d
    out["h3_breakdist_slope"] = slope(b3, "brkdist")
    return out
