def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            sma=c.rolling(20).mean(); sd=r.rolling(20).std()
            z=(c/sma-1)/sd
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"r":r,
                "r1z":r/r.rolling(20).std().shift(1),
                "r10":c/c.shift(10)-1,
                "fwd5":c.shift(-5)/c-1,"fwd1":c.shift(-1)/c-1,"fwd3":c.shift(-3)/c-1,
                "reg":b["regime"].astype(str),"wd":ts.dt.weekday,"day":ts.dt.floor("D"),
                "pos":b["postRebalance_current_allocation"].fillna(0)})
            d["i"]=np.arange(len(d)); rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    out["regime_counts"]=A.reg.value_counts()
    for H,col in [(5,"fwd5"),(1,"fwd1"),(3,"fwd3")]:
        g=A[A.i%H==0]; dr=g.groupby("coin")[col].mean()
        A["ex%d"%H]=A[col]-A.coin.map(dr)
    def clus(g,x,y):
        g=g.dropna(subset=[x,y])
        if len(g)<40: return [len(g),np.nan,np.nan,np.nan]
        X=np.c_[np.ones(len(g)),g[x].values]; Y=g[y].values
        bta=np.linalg.lstsq(X,Y,rcond=None)[0]; e=Y-X@bta
        XtXi=np.linalg.inv(X.T@X); M=np.zeros((2,2))
        for _,idx in g.groupby("day").indices.items():
            s=(X[idx]*e[idx,None]).sum(0); M+=np.outer(s,s)
        V=XtXi@M@XtXi; return [len(g),g.day.nunique(),bta[1],bta[1]/np.sqrt(V[1,1])]
    G5=A[A.i%5==0]
    res=[]
    for reg,g in G5.groupby("reg"):
        res.append(["z",reg]+clus(g,"z","ex5"))
        res.append(["r10",reg]+clus(g,"r10","ex5"))
    out["slope_5d_by_regime"]=pd.DataFrame(res,columns=["x","reg","n","days","slope","t"]).round(4)
    # quintiles of z out of profile, day-cluster-free simple t
    for reg,g in G5.groupby("reg"):
        g=g.dropna(subset=["z","ex5"]).copy()
        if len(g)<100: continue
        g["b"]=pd.qcut(g.z,5,labels=False)
        q=g.groupby("b").agg(n=("ex5","size"),zlo=("z","min"),m=("ex5","mean"),s=("ex5","std"))
        q["t"]=q.m/(q.s/np.sqrt(q.n)); out["zq_"+reg]=q.drop(columns="s").round(4)
    # out of profile, split by sign of 10d return (proxy rising/falling)
    g=G5[G5.reg=="chop"].copy(); g["side"]=np.sign(g.r10)
    res=[]
    for s,gg in g.groupby("side"): res.append([s]+clus(gg,"z","ex5"))
    out["chop_split_by_r10sign"]=pd.DataFrame(res,columns=["sign","n","days","slope","t"]).round(4)
    # next day after big daily move, by regime
    res=[]
    for reg,g in A.groupby("reg"):
        res.append(["r1z->1d",reg]+clus(g,"r1z","ex1"))
        res.append(["r1z->3d",reg]+clus(g[g.i%3==0],"r1z","ex3"))
    out["daymove_slopes"]=pd.DataFrame(res,columns=["x","reg","n","days","slope","t"]).round(5)
    # weekday daily returns
    wd=A.dropna(subset=["ex1"]).groupby("wd")["ex1"].agg(["size","mean","std"])
    wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["size"])); out["weekday_1d"]=wd.drop(columns="std").round(5)
    # book pnl by regime and by side
    A["pnl"]=A.pos*A.fwd1
    out["pnl_by_reg_side"]=A.assign(s=np.sign(A.pos)).groupby(["reg","s"])["pnl"].agg(["size","mean"]).round(5)
    return out
