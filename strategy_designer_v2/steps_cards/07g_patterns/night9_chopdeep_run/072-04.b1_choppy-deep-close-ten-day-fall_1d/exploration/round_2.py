def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std()
            hi=c.rolling(20).max()
            depth=(c/hi-1)/sd
            sd30=r.rolling(30).std()
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"depth":depth,
                            "choppy":(b["regime"]=="unknown"),
                            "fc":b["forecast"].astype(float),
                            "ts":pd.to_datetime(b["timestamp"]),
                            "sd30":sd30,"alloc":b["postRebalance_current_allocation"].astype(float)})
            for h in (5,10):
                d[f"f{h}"]=c.shift(-h)/c-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["yr"]=D.ts.dt.year
    D["day"]=D.ts.dt.normalize()
    D["sdrank"]=D.groupby("coin").sd30.rank(pct=True)
    D["agit"]=D.sdrank>0.5
    out={}
    for h in (5,10):
        g=D[D.pos%h==0]
        drift=g.groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"]=D[f"f{h}"]-D.coin.map(drift)
    def reg(s,xcol,ycol):
        s=s.dropna(subset=[xcol,ycol])
        x=s[xcol].values;y=s[ycol].values
        X=np.column_stack([np.ones(len(x)),x])
        beta=np.linalg.lstsq(X,y,rcond=None)[0]
        e=y-X@beta
        XtXi=np.linalg.inv(X.T@X)
        meat=np.zeros((2,2))
        for _,idx in s.reset_index(drop=True).groupby("day").groups.items():
            sc=(X[idx]*e[idx][:,None]).sum(0);meat+=np.outer(sc,sc)
        V=XtXi@meat@XtXi
        return pd.Series({"slope":beta[1],"t":beta[1]/np.sqrt(V[1,1]),"n":len(x),"days":s.day.nunique()})
    res={}
    for h in (5,10):
        for ch in (True,False):
            s=D[(D.pos%h==0)&(D.choppy==ch)]
            res[f"raw depth h{h} choppy={ch}"]=reg(s,"depth",f"x{h}")
        s=D[(D.pos%h==0)&D.choppy&(D.fc<0)]
        res[f"forecast h{h} choppy fc<0"]=reg(s,"fc",f"x{h}")
        s=D[(D.pos%h==0)]
        res[f"raw depth h{h} all"]=reg(s,"depth",f"x{h}")
    out["regressions"]=pd.DataFrame(res).T.round(4)
    g=D[(D.pos%10==0)].dropna(subset=["x10","depth"]).copy()
    g["dq"]=pd.qcut(g.depth,3,labels=["deep","mid","near"])
    o=g.groupby(["choppy","agit","dq"]).x10.agg(["mean","count","std"])
    o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["10d by choppy x agit x depth tercile"]=o.drop(columns="std").round(4)
    o=g.groupby(["yr","dq"]).x10.agg(["mean","count"]).unstack()
    out["10d by year x depth tercile (all)"]=o.round(4)
    o=g.groupby(["coin","dq"]).x10.mean().unstack()
    out["10d by coin x depth tercile (all)"]=o.round(4)
    gc=g[g.choppy]
    out["10d choppy by coin x tercile"]=gc.groupby(["coin","dq"]).x10.mean().unstack().round(4)
    out["corr depth vs forecast (choppy, fc<0)"]=float(D[D.choppy&(D.fc<0)][["depth","fc"]].corr().iloc[0,1])
    return out
