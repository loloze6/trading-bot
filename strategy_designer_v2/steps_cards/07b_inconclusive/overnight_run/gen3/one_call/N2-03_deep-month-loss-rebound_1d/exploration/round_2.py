def explore(data):
    import pandas as pd, numpy as np
    H=20
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"];h=b["high"];l=b["low"]
            lr=np.log(c).diff()
            d=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),
                "ts":pd.to_datetime(b["timestamp"]),"f":b["forecast"].values,
                "fr":(c.shift(-H)/c-1).values,"r20":(c/c.shift(20)-1).values,
                "r5":(c/c.shift(5)-1).values,"r60":(c/c.shift(60)-1).values,
                "vol20":lr.rolling(20).std().values,
                "pos20":((c-l.rolling(20).min())/(h.rolling(20).max()-l.rolling(20).min())).values,
                "dd_low":(c/l.rolling(5).min()-1).values,
                "vratio":(b["volume"]/b["volume"].rolling(20).mean()).values})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["mu"]=D.groupby("coin")["fr"].transform("mean")
    D["ex"]=D["fr"]-D["mu"]
    N=D[(D.i%H==0)&D.fr.notna()].copy()
    def st(x):
        x=x.dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"med":x.median(),"hit":(x>0).mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out={}
    out["share_capped_among_pos"]=float((D.f[D.f>0]>=20).mean())
    P=N[N.f>0].copy()
    T=N[N.f>=20].copy()
    out["top_r5"]=T.groupby(np.where(T.r5>0,"r5_up","r5_dn")).ex.apply(st).unstack()
    out["pos_r5"]=P.groupby(np.where(P.r5>0,"r5_up","r5_dn")).ex.apply(st).unstack()
    out["top_pos20"]=T.groupby(pd.cut(T.pos20,[-0.01,0.1,0.25,1.01])).ex.apply(st).unstack()
    out["top_vol"]=T.groupby(pd.qcut(T.vol20,3,labels=["lowvol","mid","highvol"])).ex.apply(st).unstack()
    out["top_r60"]=T.groupby(np.where(T.r60.isna(),"na",np.where(T.r60>0,"r60_up","r60_dn"))).ex.apply(st).unstack()
    out["top_vratio"]=T.groupby(pd.qcut(T.vratio,3,labels=["lowv","midv","highv"])).ex.apply(st).unstack()
    out["top_bounce"]=T.groupby(pd.qcut(T.dd_low,3,labels=["atlow","small","bounced"])).ex.apply(st).unstack()
    N["absf"]=pd.cut(N.r20,[-1,-0.3,-0.2,-0.1,0,10])
    out["all_by_raw_r20"]=N.groupby("absf").ex.apply(st).unstack()
    Nm=N[(N.r20<-0.1)]
    out["r20lt10_r5"]=Nm.groupby(np.where(Nm.r5>0,"r5_up","r5_dn")).ex.apply(st).unstack()
    return out
