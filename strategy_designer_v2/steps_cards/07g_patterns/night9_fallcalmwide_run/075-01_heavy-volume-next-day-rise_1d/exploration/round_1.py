def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"].astype(float); v=b["volume"].astype(float)
            d=pd.DataFrame({"coin":c,"win":w,"pos":np.arange(len(b))})
            d["ts"]=pd.to_datetime(b["timestamp"])
            d["dret"]=cl/cl.shift(1)-1
            d["vr"]=v/v.shift(1).rolling(20,min_periods=10).mean()
            d["rng"]=(b["high"]-b["low"])/cl
            d["clpos"]=(cl-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            d["r1"]=cl.shift(-1)/cl-1
            d["r3"]=cl.shift(-3)/cl-1
            d["tr20"]=cl/cl.shift(20)-1
            d["fc"]=b["forecast"]; d["alloc"]=b["postRebalance_current_allocation"]
            d["g"]=d["alloc"]*d["r1"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r1"].mean(); D["x1"]=D["r1"]-D["coin"].map(mu)
    mu3=D[D.pos%3==0].groupby("coin")["r3"].mean(); D["x3"]=D["r3"]-D["coin"].map(mu3)
    D["lvr"]=np.log(D["vr"])
    D["vq"]=D.groupby("coin")["lvr"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    D["up"]=np.where(D["dret"]>0,"up","down")
    D["day"]=D["ts"].dt.floor("D")
    def tab(df,keys,col):
        g=df.dropna(subset=[col]).groupby(keys)[col]
        r=g.agg(["mean","count","std"]); r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"])); return r.drop(columns="std").round(5)
    out={}
    out["vq x dir next1"]=tab(D,["up","vq"],"x1")
    out["vq x dir next3 grid"]=tab(D[D.pos%3==0],["up","vq"],"x3")
    D["dq"]=D.groupby("coin")["dret"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["dret quint x vq(0/4) next1"]=tab(D[D.vq.isin([0,4])],["dq","vq"],"x1")
    D["tr"]=pd.cut(D["tr20"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    out["trend20 x vq next1"]=tab(D,["tr","vq"],"x1")
    D["cq"]=pd.cut(D["clpos"],[-0.01,0.33,0.67,1.01],labels=["lowcl","mid","highcl"])
    out["closepos x vq next1"]=tab(D,["cq","vq"],"x1")
    out["weekday next1"]=tab(D.assign(wd=D.ts.dt.weekday),["wd"],"x1")
    out["book gain by vq"]=tab(D,["vq"],"g")
    out["year"]=tab(D.assign(y=D.ts.dt.year),["y"],"x1")
    return out
