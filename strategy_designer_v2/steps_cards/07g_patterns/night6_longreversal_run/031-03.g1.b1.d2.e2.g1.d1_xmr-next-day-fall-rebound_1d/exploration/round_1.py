def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]["XMRUSD"]
    rows = []
    for w, b in bars.items():
        b = b.copy().reset_index(drop=True)
        c = b["close"]
        r = c.pct_change()
        vol = r.rolling(30, min_periods=20).std()
        z = r / vol
        d = pd.DataFrame({"w": w, "r": r, "z": z, "vol": vol,
                          "n1": c.shift(-1)/c-1, "n3": c.shift(-3)/c-1, "n5": c.shift(-5)/c-1,
                          "r5": c/c.shift(5)-1, "r20": c/c.shift(20)-1, "r60": c/c.shift(60)-1,
                          "rng": (b["high"]-b["low"])/c,
                          "clv": (c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                          "volu": b["volume"]/b["volume"].rolling(30,min_periods=10).mean(),
                          "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                          "yr": pd.to_datetime(b["timestamp"]).dt.year,
                          "alloc": b["postRebalance_current_allocation"],
                          "pos": np.arange(len(b))})
        d["gain"] = d["alloc"]*d["n1"]
        rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D["n1"].mean()
    D["ex1"] = D["n1"]-mu1
    D["vz"] = D["vol"]
    def summ(g, col="ex1"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    D["zb"] = pd.cut(D["z"], [-np.inf,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,np.inf])
    out["next1_by_z"] = D.groupby("zb").apply(summ)
    # multi-day horizons non-overlapping grid, after down days
    for h in [3,5]:
        G = D[(D["pos"]%h==0)]
        G = G.assign(ex=G[f"n{h}"]-G[f"n{h}"].mean())
        out[f"next{h}_by_z_grid"] = G.groupby(pd.cut(G["z"],[-np.inf,-1.5,-0.5,0.5,1.5,np.inf])).apply(lambda g: summ(g,"ex"))
    dn = D[D["z"]<0].copy()
    dn["volq"] = pd.qcut(dn["vol"], 4, labels=["v1low","v2","v3","v4high"])
    out["down_by_vol"] = dn.groupby("volq").apply(summ)
    dn["r60s"] = np.sign(dn["r60"])
    dn["r60q"] = pd.qcut(dn["r60"], 4, labels=["q1fell","q2","q3","q4rose"])
    out["down_by_r60"] = dn.groupby("r60q").apply(summ)
    dn["r5q"] = pd.qcut(dn["r5"], 4, labels=["q1fell","q2","q3","q4rose"])
    out["down_by_r5"] = dn.groupby("r5q").apply(summ)
    dn["clvq"] = pd.qcut(dn["clv"], 3, labels=["closeLow","mid","closeHigh"])
    out["down_by_closeloc"] = dn.groupby("clvq").apply(summ)
    dn["vq"] = pd.qcut(dn["volu"], 3, labels=["lowvol","mid","highvol"])
    out["down_by_volume"] = dn.groupby("vq").apply(summ)
    out["down_by_weekday"] = dn.groupby("wd").apply(summ)
    out["all_by_weekday"] = D.groupby("wd").apply(summ)
    out["down_by_year"] = dn.groupby("yr").apply(summ)
    up = D[D["z"]>0].copy()
    up["clvq"] = pd.qcut(up["clv"], 3, labels=["closeLow","mid","closeHigh"])
    out["up_by_closeloc"] = up.groupby("clvq").apply(summ)
    D["clvq"] = pd.qcut(D["clv"], 5, labels=False)
    out["all_by_closeloc"] = D.groupby("clvq").apply(summ)
    # book gains
    B = D.dropna(subset=["gain"])
    B["gq"] = pd.qcut(B["gain"].rank(method="first"), 20, labels=False)
    out["book_extremes_context"] = B[B["gq"].isin([0,19])].groupby("gq")[["z","r5","r60","vol","clv","volu"]].mean()
    out["book_gain_by_year"] = B.groupby("yr")["gain"].agg(["count","mean","sum"])
    return out
