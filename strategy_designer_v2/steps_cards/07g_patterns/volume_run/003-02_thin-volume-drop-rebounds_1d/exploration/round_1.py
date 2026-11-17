def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(20).std()
            z=r1/vol.shift(1)
            vr=v/v.rolling(30).mean()
            r5p=c/c.shift(5)-1
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"vr":vr,"vol":vol,"r5p":r5p,"f5":f5,"f1":f1,"r1":r1,"wd":ts.dt.weekday,"yr":ts.dt.year})
            rows.append(d)
    D=pd.concat(rows)
    m5=D[D.pos%5==0].groupby("coin")["f5"].mean()
    D["x5"]=D["f5"]-D["coin"].map(m5)
    G=D[(D.pos%5==0)].dropna(subset=["z","vr","x5"]).copy()
    def summ(g):
        x=g["x5"]; n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    G["zb"]=pd.cut(G.z,[-99,-2,-1,1,2,99])
    G["vb"]=pd.cut(G.vr,[0,0.7,1.0,1.5,99])
    out={}
    out["z_x_vr"]=G.groupby(["zb","vb"]).apply(summ)
    out["z_only"]=G.groupby("zb").apply(summ)
    G["r5b"]=pd.qcut(G.r5p,5,labels=False)
    out["past5_quint"]=G.groupby("r5b").apply(summ)
    G["volb"]=G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["vol_quint"]=G.groupby("volb").apply(summ)
    # interaction regression: x5 on z, log vr, z*logvr
    lv=np.log(G.vr); X=np.column_stack([np.ones(len(G)),G.z,lv,G.z*lv])
    beta,res,_,_=np.linalg.lstsq(X,G.x5.values,rcond=None)
    e=G.x5.values-X@beta; s2=e@e/(len(e)-4); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["reg_z_lvr_inter"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","z","logvr","z*logvr"])
    out["by_coin_z"]=G.groupby("coin").apply(lambda g: pd.Series({"n":len(g),"corr_z_x5":g.z.corr(g.x5),"corr_lvr_x5":np.log(g.vr).corr(g.x5)}))
    # weekday daily returns (all bars, daily, non-overlapping)
    W=D.dropna(subset=["f1"])
    out["weekday_f1"]=W.groupby("wd")["f1"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))])
    out["year_x5"]=G.groupby("yr").apply(summ)
    # book
    act=sum((b["forecast"]>0).sum() for ws in data["bars"].values() for b in ws.values())
    out["active_bars"]=int(act)
    return out
