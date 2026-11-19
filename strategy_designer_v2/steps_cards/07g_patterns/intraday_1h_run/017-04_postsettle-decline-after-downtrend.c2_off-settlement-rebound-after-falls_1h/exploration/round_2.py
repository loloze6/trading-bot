def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            d=pd.DataFrame()
            ts=pd.to_datetime(df["timestamp"],utc=True)
            d["ch"]=((ts.dt.hour+1)%24).values
            d["yr"]=ts.dt.year.values
            cl=df["close"].values.astype(float)
            s=pd.Series(cl)
            r1=s.pct_change(1)
            vol=r1.rolling(24).std()
            d["r1s"]=(r1/vol).values
            d["r3s"]=(s.pct_change(3)/(vol*np.sqrt(3))).values
            d["r6s"]=(s.pct_change(6)/(vol*np.sqrt(6))).values
            d["vol"]=vol.values
            d["f2"]=(s.shift(-2)/s-1).values
            d["coin"]=c; d["win"]=w
            rows.append(d.iloc[::2])
    G=pd.concat(rows)
    G["f2x"]=G["f2"]-G.groupby("coin")["f2"].transform("mean")
    G=G.dropna(subset=["f2x","r1s","r3s","r6s"])
    def tt(s): return pd.Series({"mean_bp":s.mean()*1e4,"t":s.mean()/s.std()*np.sqrt(len(s)),"n":len(s)})
    out={}
    G["r1q"]=G.groupby("coin")["r1s"].transform(lambda x:pd.qcut(x,5,labels=False))
    G["vq"]=G.groupby("coin")["vol"].transform(lambda x:pd.qcut(x,3,labels=False))
    sp=lambda g: g.loc[g.r1q==0,"f2x"].mean()-g.loc[g.r1q==4,"f2x"].mean()
    out["r1_Q1minusQ5_bp_by_coin"]=(G.groupby("coin").apply(sp)*1e4)
    wv=G.groupby(["coin","win"]).apply(sp)
    out["r1_spread_share_windows_pos"]=float((wv>0).mean())
    out["r1_spread_by_year_bp"]=G.groupby("yr").apply(sp)*1e4
    out["r1_spread_by_vol_t"]=G.groupby("vq").apply(lambda g: pd.Series({"spread_bp":sp(g)*1e4,
        "corr_t":np.corrcoef(g.r1s,g.f2x)[0,1]*np.sqrt(len(g))})).T
    # graded: slope of f2x on r1s in high vol per coin
    hv=G[G.vq==2]
    out["highvol_corr_by_coin"]=hv.groupby("coin").apply(lambda g: pd.Series({"corr":np.corrcoef(g.r1s,g.f2x)[0,1],"n":len(g)}))
    # longer lookbacks
    out["corr_lookback"]=pd.Series({k:np.corrcoef(G[k],G.f2x)[0,1] for k in ["r1s","r3s","r6s"]})
    # hour 21 by coin and year
    h=G[G.ch==21]
    out["h21_by_coin"]=h.groupby("coin")["f2x"].apply(tt).unstack()
    out["h21_by_year"]=h.groupby("yr")["f2x"].apply(tt).unstack()
    out["h21_share_windows_pos"]=float((h.groupby(["coin","win"])["f2x"].mean()>0).mean())
    return out
