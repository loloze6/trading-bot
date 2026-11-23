def explore(data):
    import numpy as np, pandas as pd
    def tt(s):
        s = s.dropna(); return pd.Series({"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))),"n":len(s)})
    H = []; G = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp","close"]].copy().reset_index(drop=True)
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            b["r1"] = b["close"].pct_change()
            b["hour"] = b["ts"].dt.hour; b["year"] = b["ts"].dt.year
            b["sd720"] = b["r1"].rolling(720, min_periods=500).std()
            b["r24p"] = b["close"]/b["close"].shift(24)-1
            b["z24"] = b["r24p"]/(b["sd720"]*np.sqrt(24))
            b["f2"] = b["close"].shift(-2)/b["close"]-1
            b["f24"] = b["close"].shift(-24)/b["close"]-1
            b["coin"] = coin
            # 21:00 bar start -> return of 21 and 22 bars: from close of 20:00 bar
            h = b[b["hour"]==20][["coin","year","sd720","z24","f2"]]
            H.append(h)
            gidx = b.index[b.index % 24 == 0]
            G.append(b.loc[gidx, ["coin","year","sd720","z24","f24"]])
    h = pd.concat(H).dropna()
    h["e"] = h["f2"] - h.groupby("coin")["f2"].transform("mean")
    h["vq"] = h.groupby("coin")["sd720"].transform(lambda s: pd.qcut(s,3,labels=False))
    h["zq"] = h.groupby("coin")["z24"].transform(lambda s: pd.qcut(s,5,labels=False))
    out = {}
    out["h21_22_raw_2h_ret_by_vol_tercile"] = h.groupby("vq")["f2"].apply(tt).unstack()
    out["h21_22_raw_in_vol_units_by_vol"] = h.assign(s=h["f2"]/h["sd720"]).groupby("vq")["s"].apply(tt).unstack()
    out["h21_22_excess_by_prior24_z_quintile"] = h.groupby("zq")["e"].apply(tt).unstack()
    g = pd.concat(G).dropna()
    g["e"] = g["f24"] - g.groupby("coin")["f24"].transform("mean")
    g["zd"] = g.groupby("coin")["z24"].transform(lambda s: pd.qcut(s,10,labels=False))
    g["vq"] = g.groupby("coin")["sd720"].transform(lambda s: pd.qcut(s,3,labels=False))
    out["any_hour_grid_next24_excess_by_prior24z_decile"] = g.groupby("zd")["e"].apply(tt).unstack()
    dn = g[g["z24"]<0]
    out["down_grid_excess_by_vol_and_ztercile"] = dn.groupby(["vq", dn.groupby("coin")["z24"].transform(lambda s: pd.qcut(s,3,labels=False))])["e"].mean().unstack()
    out["down_grid_graded_by_vol"] = dn.assign(x=-dn["z24"]*dn["e"]).groupby("vq")["x"].apply(tt).unstack()
    out["down_grid_lowest_tercile_high_vol_by_year"] = dn[(dn["vq"]==2)].assign(zt=dn.groupby("coin")["z24"].transform(lambda s: pd.qcut(s,3,labels=False))).query("zt==0").groupby("year")["e"].apply(tt).unstack()
    return out
