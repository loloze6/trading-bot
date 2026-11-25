def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["fwd"]=c.shift(-1)/c-1
            s20=r.rolling(20).std()
            s30=r.rolling(30).std()
            d["s30"]=s30
            d["agit_rank"]=s30.expanding(min_periods=30).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            d["vol_rel"]=s20/r.rolling(60,min_periods=40).std()
            d["s20"]=s20
            hl=(b["high"]-b["low"]).replace(0,np.nan)
            d["prod"]=(b["high"]-c)/c/s20
            d["fc"]=b["forecast"]
            d["pos"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["ex"]=D["fwd"]-D.groupby("coin")["fwd"].transform("mean")
    D["day"]=D["ts"].dt.floor("D"); D["yr"]=D["ts"].dt.year
    # coin-level s20 rank vs coin's own whole-sample median (approx of year median)
    D["s20_coinrank"]=D.groupby("coin")["s20"].rank(pct=True)
    def tday(sub,col="ex"):
        sub=sub.dropna(subset=[col])
        g=sub.groupby("day")[col].sum(); n=len(g)
        return pd.Series({"mean_bp":sub[col].mean()*1e4,"n":len(sub),"days":n,"t":g.mean()/(g.std()/np.sqrt(n)) if n>2 else np.nan})
    def slope(sub,x="fc"):
        sub=sub.dropna(subset=[x,"ex"])
        X=np.column_stack([np.ones(len(sub)),sub[x].values]); y=sub["ex"].values
        beta=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@beta
        XtXi=np.linalg.inv(X.T@X); S=np.zeros((2,2))
        for _,idx in pd.Series(np.arange(len(sub))).groupby(sub["day"].values):
            u=X[idx.values].T@e[idx.values]; S+=np.outer(u,u)
        se=np.sqrt(np.diag(XtXi@S@XtXi))
        return pd.Series({"slope_bp_per_fc":beta[1]*1e4,"t":beta[1]/se[1],"n":len(sub)})
    out={}
    D["fq"]=D.groupby("coin")["fc"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    for name,col,cut in [("agit_s20_vs_coin_median","s20_coinrank",0.5),("agit_s20_vs_s60","vol_rel",1.0),("agit_s30_expanding","agit_rank",0.5)]:
        D["_a"]=np.where(D[col]>cut,"agitated",np.where(D[col].notna(),"calm",None))
        S=D.dropna(subset=["_a"])
        out[name+"_slope"]=S.groupby("_a").apply(slope)
        out[name+"_top_fifth"]=S[S["fq"]==4].groupby("_a").apply(tday)
        out[name+"_bottom_fifth"]=S[S["fq"]==0].groupby("_a").apply(tday)
    # agitation tercile by coin rank, graded within
    D["aq"]=pd.qcut(D["s20_coinrank"],3,labels=False)
    out["slope_by_s20_tercile"]=D.dropna(subset=["aq"]).groupby("aq").apply(slope)
    # by year within agitated (coin median)
    A=D[D["s20_coinrank"]>0.5]
    out["agit_slope_by_year"]=A.groupby("yr").apply(slope)
    out["agit_slope_by_coin"]=A.groupby("coin").apply(slope)
    # total move per case: top fifth, in agitated vs calm, raw fwd mean
    D["_a"]=np.where(D["s20_coinrank"]>0.5,"agitated","calm")
    out["top_fifth_total_move_bp"]=D[D["fq"]==4].groupby("_a")["fwd"].agg(lambda x:x.mean()*1e4)
    out["usual_move_bp"]=D.groupby("_a")["fwd"].agg(lambda x:x.std()*1e4)
    # day after: is rebound gone by day 2?
    return out
