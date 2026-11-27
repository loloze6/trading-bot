def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"].astype(float); v=b["volume"].astype(float)
            d=pd.DataFrame({"coin":c,"win":w,"pos":np.arange(len(b))})
            d["ts"]=pd.to_datetime(b["timestamp"])
            d["dret"]=cl/cl.shift(1)-1
            d["vr"]=v/v.shift(1).rolling(20,min_periods=10).mean()
            d["r1"]=cl.shift(-1)/cl-1
            d["r2"]=cl.shift(-2)/cl-1
            d["tr60"]=cl/cl.shift(60)-1
            sd=d["dret"].rolling(30,min_periods=20).std()
            d["sdq"]=sd.rolling(365,min_periods=60).apply(lambda a:(a<=a[-1]).mean(),raw=True)
            d["alloc"]=b["postRebalance_current_allocation"]
            d["g"]=d["alloc"]*d["r1"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r1"].mean(); D["x1"]=D["r1"]-D["coin"].map(mu)
    D["lvr"]=np.log(D["vr"])
    D["vq"]=D.groupby("coin")["lvr"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    D["day"]=D["ts"].dt.floor("D")
    D["prof_tr"]=pd.cut(D["tr60"],[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    D["prof_ag"]=np.where(D["sdq"].isna(),np.nan,np.where(D["sdq"]>0.5,"agit","calm"))
    def ctab(df,keys,col):
        out=[]
        for k,g in df.dropna(subset=[col]).groupby(keys):
            s=g.groupby("day")[col].apply(lambda a:(a-0).sum())
            n=len(g); m=g[col].mean()
            dev=g.groupby("day")[col].apply(lambda a:(a-m).sum())
            se=np.sqrt((dev**2).sum())/n
            out.append(pd.Series({"mean":m,"n":n,"days":len(dev),"t_day":m/se},name=k))
        return pd.DataFrame(out).round(5)
    up=D[D.dret>0].copy(); dn=D[D.dret<0].copy()
    out={}
    out["up days vq, clustered"]=ctab(up,["vq"],"x1")
    out["down days vq, clustered"]=ctab(dn,["vq"],"x1")
    upl=up[up.vq<=2]
    out["up light by window"]=ctab(upl,["win"],"x1")
    out["up light by profile"]=ctab(upl.dropna(subset=["prof_tr"]),["prof_tr","prof_ag"],"x1")
    # graded within up days: size of up move x light volume
    up["dq"]=up.groupby("coin")["dret"].transform(lambda s: pd.qcut(s,3,labels=False))
    out["up: move tercile x vq"]=ctab(up,["dq","vq"],"x1")
    # rank-correlation within up days of vr vs next
    up["lr"]=-up["lvr"]
    out["up: corr(-logvr, x1) by year"]=up.dropna(subset=["x1","lvr"]).assign(y=lambda d:d.ts.dt.year).groupby("y").apply(lambda g: g["lr"].corr(g["x1"],method="spearman")).round(4)
    # 2-day on grid
    up2=up[(up.pos%2==0)&(up.vq<=2)].copy()
    mu2=D[D.pos%2==0].groupby("coin")["r2"].mean(); up2["x2"]=up2["r2"]-up2["coin"].map(mu2)
    out["up light next2 grid"]=ctab(up2,["vq"],"x2")
    out["dn heavy by profile"]=ctab(dn[dn.vq==4].dropna(subset=["prof_tr"]),["prof_tr","prof_ag"],"x1")
    out["book gain by dir x vq"]=ctab(D.assign(dd=np.where(D.dret>0,"up","dn")),["dd","vq"],"g")
    return out
