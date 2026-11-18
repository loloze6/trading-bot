def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(df)
            fc = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            hi20 = df["high"].shift(1).rolling(20).max().values
            lo20 = df["low"].shift(1).rolling(20).min().values
            r20 = (df["close"]/df["close"].shift(20)-1).values
            for h in [1, 3, 5, 10]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, wn=int(w[1:]), h=h, yr=yr[i], fc=fc[i],
                                     r=c[i+h]/c[i]-1,
                                     bd=(c[i]/hi20[i]-1) if not np.isnan(hi20[i]) else np.nan,
                                     bw=(hi20[i]/lo20[i]-1) if not np.isnan(hi20[i]) else np.nan,
                                     r20=r20[i]))
    d = pd.DataFrame(rows)
    d["base"] = d.groupby(["coin", "h"])["r"].transform("mean")
    d["ex"] = d["r"] - d["base"]
    def slope(g, x):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 8 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, spear=np.nan))
        r = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope/r.stderr,
                              spear=stats.spearmanr(g[x], g["ex"]).correlation))
    out = {}
    b = d[(d.fc > 0) & d.bd.notna() & (d.bd > 0)].copy()
    out["bd_by_h"] = b.groupby("h").apply(lambda g: slope(g, "bd"))
    b3 = b[b.h == 3].copy()
    out["bd_h3_by_coin"] = b3.groupby("coin").apply(lambda g: slope(g, "bd"))
    out["bd_h3_by_year"] = b3.groupby("yr").apply(lambda g: slope(g, "bd"))
    b3["q"] = pd.qcut(b3["bd"], 4, labels=False, duplicates="drop")
    out["bd_h3_quart"] = b3.groupby("q").agg(n=("ex","size"), bd=("bd","mean"), mean_ex=("ex","mean"),
                                             med_ex=("ex","median"), sd=("ex","std"))
    # trimmed: drop top 2% bd
    cut = b3["bd"].quantile(0.98)
    out["bd_h3_trim98"] = slope(b3[b3.bd <= cut], "bd")
    # break distance scaled by band width
    b3["bd_rel"] = b3["bd"] / b3["bw"]
    out["bd_rel_h3"] = slope(b3, "bd_rel")
    out["bw_h3"] = slope(b3, "bw")
    # control: same 'close vs prior high' on all bars (momentum generally)
    a3 = d[(d.h == 3) & d.bd.notna()]
    out["bd_allbars_h3"] = slope(a3, "bd")
    out["bd_nonbreak_h3"] = slope(a3[a3.bd <= 0], "bd")
    out["r20_break_h3"] = slope(b3, "r20")
    return out
