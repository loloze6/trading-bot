def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        g5 = []; g10 = []
        for w, b in wins.items():
            c = b["close"].values; n = len(c)
            for i in range(0, n-5, 5): g5.append(c[i+5]/c[i]-1)
            for i in range(0, n-10, 10): g10.append(c[i+10]/c[i]-1)
        d5 = np.mean(g5); d10 = np.mean(g10)
        for w, b in wins.items():
            b = b.reset_index(drop=True); c = b["close"]
            r1 = c.pct_change(); sd = r1.rolling(30, min_periods=20).std()
            z = r1/sd
            zstd = (z - z.rolling(60, min_periods=20).mean())/z.rolling(60, min_periods=20).std()
            f5 = c.shift(-5)/c-1; f10 = c.shift(-10)/c-1
            hi20 = c/c.rolling(20, min_periods=10).max()-1
            n = len(b)
            for i in range(0, n-5, 5):
                rows.append(dict(coin=coin, w=w, z=z.iloc[i], zs=zstd.iloc[i], ex5=f5.iloc[i]-d5,
                                 ex10=f10.iloc[i]-d10 if i+10 < n else np.nan,
                                 inside=b["regime"].iloc[i]=="unknown", hi20=hi20.iloc[i],
                                 g10=(i % 10 == 0)))
    d = pd.DataFrame(rows).dropna(subset=["z","ex5"])
    def summ(x, col="ex5"):
        x = x.dropna(subset=[col]); m = x[col].mean()
        return pd.Series(dict(n=len(x), mean=m, t=m/(x[col].std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out = {}
    di = d[d.inside].copy()
    di["hib"] = pd.cut(di["hi20"], [-1, -0.10, -0.04, 0.001], labels=["far","mid","near"])
    out["inside_all_by_hi20_cond_alone"] = di.groupby("hib").apply(summ)
    out["inside_up_by_hi20"] = di[di.z > 0].groupby("hib").apply(summ)
    out["inside_notup_by_hi20"] = di[di.z <= 0].groupby("hib").apply(summ)
    out["inside_zgt1"] = summ(di[di.z > 1]).to_frame().T
    out["inside_zgt1_10d"] = summ(di[(di.z > 1) & di.g10], "ex10").to_frame().T
    out["inside_zle1_up"] = summ(di[(di.z > 0) & (di.z <= 1)]).to_frame().T
    out["inside_fcpos_raw_zle0"] = summ(di[(di.zs > 0) & (di.z <= 0)]).to_frame().T
    out["inside_fcpos_by_zs"] = di[di.zs > 0].assign(b=lambda x: pd.cut(x.zs, [0, 0.5, 1, 1.5, 9])).groupby("b").apply(summ)
    di["near_and_up"] = (di.z > 0) & (di.hi20 > -0.04)
    out["inside_up_10d_by_near"] = di[(di.z > 0) & di.g10].groupby(di.hi20 > -0.04).apply(lambda x: summ(x, "ex10"))
    # all profiles: z>1 with near high vs far
    da = d[(d.z > 1)].copy()
    out["all_zgt1_by_inside_near"] = da.groupby([da.inside, da.hi20 > -0.04]).apply(summ)
    # book's deepest falls by window
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bk.append(dd.assign(coin=coin, w=w)[["w","day","book_return"]])
    bk = pd.concat(bk).dropna()
    daily = bk.groupby(["w","day"])["book_return"].mean().reset_index()
    res = []
    for w, g in daily.groupby("w"):
        v = (1+g.book_return).cumprod(); dd_ = (v/v.cummax()-1).min()
        res.append(dict(w=w, maxdd=dd_, total=v.iloc[-1]-1))
    out["book_dd_by_window"] = pd.DataFrame(res).set_index("w")
    return out
