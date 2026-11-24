def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            o,h,l,c=b.open,b.high,b.low,b.close
            rng=(h-l)
            rr=rng/rng.rolling(20,min_periods=20).mean()
            loc=(c-l)/rng.replace(0,np.nan)
            body=(c-o)/rng.replace(0,np.nan)
            r1=c.pct_change()
            vol=r1.rolling(20).std()
            vr=vol/vol.rolling(60,min_periods=30).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b.timestamp).dt.floor("D"),
                "rr":rr,"loc":loc,"body":body,"r1":r1,"ret5":c/c.shift(5)-1,"vr":vr,
                "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,"fc":b.forecast,
                "alloc":b.postRebalance_current_allocation})
            d["wd"]=d.day.dt.dayofweek
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu1=D.groupby("coin").f1.mean(); mu3=D.groupby("coin").f3.mean()
    D["x1"]=D.f1-D.coin.map(mu1); D["x3"]=D.f3-D.coin.map(mu3)
    def st(g,col="x1"):
        g=g.dropna(subset=[col]); n=len(g)
        if n<5: return pd.Series({"n":n,"mean":np.nan,"t":np.nan})
        m=g[col].mean(); ds=(g[col]-m).groupby(g.day).sum()
        se=np.sqrt((ds**2).sum())/n
        return pd.Series({"n":n,"mean":m,"t":m/se if se>0 else np.nan})
    out={}
    W=D[D.rr>=1.5].copy()
    W["locb"]=pd.cut(W["loc"],[-0.01,0.1,0.25,0.5,0.75,0.9,1.01])
    out["wide_by_loc_x1"]=W.groupby("locb").apply(st)
    out["wide_by_loc_x3"]=W.groupby("locb").apply(lambda g:st(g,"x3"))
    L=D[D["loc"]<=0.25].copy()
    L["rrb"]=pd.cut(L.rr,[0,0.75,1,1.25,1.5,2,2.5,10])
    out["lowclose_by_range"]=L.groupby("rrb").apply(st)
    H=D[D["loc"]>=0.75].copy()
    H["rrb"]=pd.cut(H.rr,[0,0.75,1,1.25,1.5,2,2.5,10])
    out["highclose_by_range"]=H.groupby("rrb").apply(st)
    S=D[(D.rr>=1.5)&(D["loc"]<=0.25)].copy()
    S["r5b"]=pd.qcut(S.ret5,4)
    out["sig_by_prior5"]=S.groupby("r5b").apply(st)
    S["bodyb"]=pd.qcut(S.body,3)
    out["sig_by_body"]=S.groupby("bodyb").apply(st)
    S["vrb"]=pd.qcut(S.vr,4)
    out["sig_by_vr"]=S.groupby("vrb").apply(st)
    out["sig_by_coin"]=S.groupby("coin").apply(st)
    out["sig_x3"]=st(S,"x3")
    A=D.copy(); A["r1b"]=pd.qcut(A.r1,10)
    out["all_by_r1_decile"]=A.groupby("r1b").apply(st)
    out["all_by_weekday"]=D.groupby("wd").apply(st)
    out["sig_by_weekday"]=S.groupby("wd").apply(st)
    return out
