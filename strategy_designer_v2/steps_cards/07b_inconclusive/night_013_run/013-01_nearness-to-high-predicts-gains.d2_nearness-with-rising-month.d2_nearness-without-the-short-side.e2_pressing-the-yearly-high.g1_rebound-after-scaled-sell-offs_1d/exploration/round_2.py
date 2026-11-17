def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            f = df["forecast"].fillna(0).values.astype(float)
            n = len(c)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            vol = pd.Series(r1).rolling(30).std().values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in [1, 2]:
                for i in range(0, n-h, h):
                    rows.append((coin, w, h, i, f[i], c[i+h]/c[i]-1, c[i+1]/c[i]-1, vol[i], year[i]))
    d = pd.DataFrame(rows, columns=["coin","w","h","i","f","fr","fr1","vol","year"])
    d["ex"] = d["fr"] - d.groupby(["coin","h"])["fr"].transform("mean")
    def slope(g):
        g = g.dropna(subset=["f","ex"])
        if len(g) < 10 or g["f"].std() == 0: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        res = stats.linregress(g["f"], g["ex"])
        return pd.Series({"n":len(g),"npos":(g["f"]>0).sum(),"slope":res.slope,"t":res.slope/res.stderr,
                          "mean_ex_pos":g.loc[g.f>0,"ex"].mean()})
    out = {}
    d1 = d[d.h==1].copy()
    out["h1_by_coin"] = d1.groupby("coin").apply(slope)
    out["h1_by_year"] = d1.groupby("year").apply(slope)
    d1["volq"] = d1.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["h1_by_volq"] = d1.groupby("volq").apply(slope)
    pos = d1[d1.f>0].copy()
    pos["fq"] = pd.qcut(pos["f"], 5, labels=False, duplicates="drop")
    out["h1_pos_fq"] = pos.groupby("fq").agg(n=("ex","size"), fmean=("f","mean"), ex=("ex","mean"),
                                           t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    out["h1_window_half"] = d1.assign(half=np.where(d1.w.str[1:].astype(int)<=12,"w1-12","w13-24")).groupby("half").apply(slope)
    d2 = d[d.h==2].copy()
    out["h2_by_coin"] = d2.groupby("coin").apply(slope)
    return out
