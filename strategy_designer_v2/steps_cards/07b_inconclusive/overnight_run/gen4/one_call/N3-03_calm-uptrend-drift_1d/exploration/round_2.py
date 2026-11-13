def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allf = []
        for w, b in wins.items():
            c = b["close"].astype(float).values; n=len(c)
            f5 = np.full(n, np.nan); f5[:-5] = c[5:]/c[:-5]-1; allf.append(f5)
        mu = np.nanmean(np.concatenate(allf))
        for w, b in wins.items():
            c = b["close"].astype(float).values; n=len(c)
            f5 = np.full(n, np.nan); f5[:-5] = c[5:]/c[:-5]-1
            r20 = np.full(n, np.nan); r20[20:] = c[20:]/c[:-20]-1
            r50 = np.full(n, np.nan); r50[50:] = c[50:]/c[:-50]-1
            sma50 = pd.Series(c).rolling(50).mean().values
            r5p = np.full(n, np.nan); r5p[5:] = c[5:]/c[:-5]-1
            lr = np.diff(np.log(c), prepend=np.nan)
            vol = pd.Series(lr).rolling(20).std()
            vrank = vol.rolling(100, min_periods=40).apply(lambda x: (x<=x[-1]).mean(), raw=True).values
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"win":w,"i":np.arange(n),"f5":f5,"ex":f5-mu,
                "fc":b["forecast"].astype(float).values,"reg":b["regime"].values,"r20":r20,"r50":r50,
                "abv50":c>sma50,"has50":~np.isnan(sma50),"r5p":r5p,"vrank":vrank,
                "ts":ts.dt.floor("D").values,"year":ts.dt.year.values}))
    d = pd.concat(rows); d = d[d["f5"].notna()]
    # cross-coin market mean of f5 same day
    d["mkt"] = d.groupby("ts")["f5"].transform("mean")
    d["rel"] = d["f5"] - d["mkt"]
    g = d[d["i"] % 5 == 0]
    def tt(x):
        x = x.dropna()
        if len(x) < 3: return pd.Series({"n":len(x),"mean":np.nan,"t":np.nan})
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std(ddof=1)*np.sqrt(len(x))})
    out = {}
    L = g[g["fc"]>0]; F = g[(g["reg"]=="trending")&(g["fc"]<=0)]
    out["long_rel_to_market"] = tt(L["rel"])
    out["flat_rel_to_market"] = tt(F["rel"])
    out["long_by_r50sign"] = L[L["r50"].notna()].groupby(L["r50"]>0)["ex"].apply(tt).unstack()
    out["long_by_abv50"] = L[L["has50"]].groupby("abv50")["ex"].apply(tt).unstack()
    out["long_by_prior5"] = L.groupby(L["r5p"]>0)["ex"].apply(tt).unstack()
    out["long_by_vrank"] = L.groupby(pd.cut(L["vrank"],[0,0.2,0.35,0.5,1.01]))["ex"].apply(tt).unstack()
    out["long_rel_by_year"] = L.groupby("year")["rel"].apply(tt).unstack()
    out["mkt_share_var"] = pd.Series({"var_ex":L["ex"].var(),"var_rel":L["rel"].var(),"corr_f5_mkt":L[["f5","mkt"]].corr().iloc[0,1]})
    # long minus flat within year
    out["spread_by_year"] = pd.DataFrame({"long":L.groupby("year")["ex"].mean(),"flat":F.groupby("year")["ex"].mean()})
    return out
