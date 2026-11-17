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
            lr = np.log(c)
            r30 = np.r_[[np.nan]*30, c[30:]/c[:-30]-1] if n > 30 else np.full(n, np.nan)
            vol = pd.Series(r1).rolling(30).std().values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in [1, 2, 3, 5, 7, 10]:
                for i in range(0, n-h, h):
                    rows.append((coin, w, h, i, f[i], c[i+h]/c[i]-1, r1[i], r30[i], vol[i], year[i]))
    d = pd.DataFrame(rows, columns=["coin","w","h","i","f","fr","r1","r30","vol","year"])
    d["ex"] = d["fr"] - d.groupby(["coin","h"])["fr"].transform("mean")
    def slope(g):
        g = g.dropna(subset=["f","ex"])
        if len(g) < 10 or g["f"].std() == 0: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        res = stats.linregress(g["f"], g["ex"])
        return pd.Series({"n":len(g),"npos":(g["f"]>0).sum(),"slope":res.slope,"t":res.slope/res.stderr,
                          "mean_ex_pos":g.loc[g.f>0,"ex"].mean()})
    out = {}
    out["by_h"] = d.groupby("h").apply(slope)
    d3 = d[d.h==3].copy()
    out["h3_by_coin"] = d3.groupby("coin").apply(slope)
    out["h3_by_year"] = d3.groupby("year").apply(slope)
    d3["trend"] = np.where(d3["r30"]>0,"up30","down30")
    out["h3_by_trend"] = d3.dropna(subset=["r30"]).groupby("trend").apply(slope)
    d3["volq"] = d3.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["h3_by_volq"] = d3.groupby("volq").apply(slope)
    pos = d3[d3.f>0].copy()
    pos["fq"] = pd.qcut(pos["f"], 5, labels=False, duplicates="drop")
    out["h3_pos_fq"] = pos.groupby("fq").agg(n=("ex","size"), fmean=("f","mean"), ex=("ex","mean"),
                                           t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    out["h3_zero_vs_pos"] = d3.assign(p=d3.f>0).groupby("p")["ex"].agg(["size","mean","std"])
    for h in [1,5,10]:
        dh = d[d.h==h].copy(); dh["trend"]=np.where(dh["r30"]>0,"up30","down30")
        out[f"h{h}_by_trend"] = dh.dropna(subset=["r30"]).groupby("trend").apply(slope)
    return out
