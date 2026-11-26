import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        tmp=[];allf=[]
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vol=r.rolling(20,min_periods=20).std()
            z=r/vol
            fwd=c.shift(-1)/c-1
            fwd2=c.shift(-2)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"win":w,"year":ts.dt.year,"day":ts.dt.floor("D"),
                            "r":r,"z":z,"fwd":fwd,"fwd2":fwd2,"pos":np.arange(len(b)),
                            "inprof":b["regime"].astype(str)=="unknown"})
            tmp.append(d); allf.append(fwd.dropna())
        mu=pd.concat(allf).mean()
        for d in tmp:
            d["ex"]=d["fwd"]-mu
            d["ex2"]=d["fwd2"]-2*mu
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["fwd","z"])
    def clslope(g,y="ex",x="z"):
        g=g.dropna(subset=[y,x])
        X=np.column_stack([np.ones(len(g)),g[x].values]); Y=g[y].values
        XtX=np.linalg.inv(X.T@X); b=XtX@X.T@Y; e=Y-X@b
        S=np.zeros((2,2))
        for _,idx in g.groupby("day").indices.items():
            s=X[idx].T@e[idx]; S+=np.outer(s,s)
        G=g["day"].nunique(); n=len(g)
        V=XtX@S@XtX*(G/(G-1))*((n-1)/(n-2))
        return pd.Series({"n":n,"days":G,"slope_pct_per_z":100*b[1],"t":b[1]/np.sqrt(V[1,1])})
    P=D[D.inprof]
    out={}
    out["inprof_all_slope"]=clslope(P)
    out["inprof_all_slope_by_year"]=P.groupby("year").apply(clslope)
    out["inprof_up_slope"]=clslope(P[P.r>0])
    out["inprof_down_slope"]=clslope(P[P.r<=0])
    out["inprof_down_slope_negz"]=clslope(P[P.r<=0].assign(nz=-P.z),x="nz")
    out["outprof_all_slope"]=clslope(D[~D.inprof])
    out["inprof_all_slope_by_coin"]=P.groupby("coin").apply(clslope)
    # 2-day horizon, non-overlapping grid
    P2=P[P.pos%2==0]
    out["inprof_all_slope_2d_grid"]=clslope(P2,y="ex2")
    # binned z across all in-profile days
    Q=P.copy(); Q["zb"]=pd.cut(Q.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    out["inprof_next_ex_by_zbin"]=Q.groupby("zb").agg(n=("ex","size"),mean_next_pct=("ex",lambda s:100*s.mean()),
        t=("ex",lambda s:s.mean()/(s.std()/np.sqrt(len(s)))))
    return out
