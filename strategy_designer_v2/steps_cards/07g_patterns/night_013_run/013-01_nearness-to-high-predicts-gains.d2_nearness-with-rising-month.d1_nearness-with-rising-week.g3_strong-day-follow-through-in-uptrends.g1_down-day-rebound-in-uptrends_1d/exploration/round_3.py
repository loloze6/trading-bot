def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            d=pd.DataFrame(index=b.index)
            d["coin"]=c; d["win"]=w
            d["z"]=r/r.rolling(30).std()
            d["vol"]=r.rolling(30).std()
            d["ret30"]=cl/cl.shift(30)-1
            d["fwd1"]=cl.shift(-1)/cl-1
            d["vz"]=np.log(b["volume"].replace(0,np.nan)/b["volume"].rolling(30).mean())
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year.values
            d["alloc"]=b["postRebalance_current_allocation"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["ex1"]=D["fwd1"]-D.groupby("coin")["fwd1"].transform("mean")
    D=D.dropna(subset=["z","ret30","ex1","vz"]).copy()
    D["wn"]=D["win"].str[1:].astype(int)
    D["half"]=np.where(D["wn"]<=12,"w1-12","w13-24")
    out={}
    dn=D[D.z<0].copy()
    def reg(g,x):
        s=stats.linregress(g[x],g["ex1"]); return pd.Series({"n":len(g),"slope":s.slope,"t":s.slope/s.stderr})
    out["down days: ex1 on vz, per coin"]=dn.groupby("coin").apply(lambda g:reg(g,"vz")).round(4)
    out["down days: ex1 on vz, by half"]=dn.groupby("half").apply(lambda g:reg(g,"vz")).round(4)
    out["down days: ex1 on vz, by year"]=dn.groupby("yr").apply(lambda g:reg(g,"vz")).round(4)
    dn["fall"]=-dn["z"]
    X=np.column_stack([np.ones(len(dn)),dn["fall"],dn["vz"],dn["fall"]*dn["vz"]])
    beta,res,_,_=np.linalg.lstsq(X,dn["ex1"].values,rcond=None)
    e=dn["ex1"].values-X@beta; s2=e@e/(len(e)-4); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["down days multi: const,fall,vz,fall*vz"]=pd.DataFrame({"b":beta,"t":beta/se}).round(4)
    up=D[D.z>0]
    out["up days: ex1 on vz, per coin"]=up.groupby("coin").apply(lambda g:reg(g,"vz")).round(4)
    D["volq"]=D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=False))
    hv=D[(D.volq==2)]
    out["high-vol tercile: ex1 on z per coin"]=hv.groupby("coin").apply(lambda g:reg(g,"z")).round(4)
    out["high-vol tercile: ex1 on z by half"]=hv.groupby("half").apply(lambda g:reg(g,"z")).round(4)
    out["all: ex1 on z by vol tercile"]=D.groupby("volq").apply(lambda g:reg(g,"z")).round(4)
    return out
