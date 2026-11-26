import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std().shift(1)
            ts=pd.to_datetime(b["timestamp"])
            v=b["volume"].astype(float)
            df=pd.DataFrame({"coin":coin,"w":w,"z":r/sd,"day":ts.dt.floor("D"),
                "fa":(b["regime"]=="unknown"),
                "n1":c.shift(-1)/c-1,"n2":c.shift(-2)/c-1,"n3":c.shift(-3)/c-1,
                "p5":c.shift(1)/c.shift(6)-1,
                "vr":v/v.rolling(30,min_periods=20).mean().shift(1),
                "pos":np.arange(len(b))})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    out={}
    def clus(x,col):
        x=x.dropna(subset=[col])
        n=len(x)
        if n<5: return pd.Series({"n":n,"mean%":np.nan,"t_day":np.nan,"days":np.nan})
        m=x[col].mean(); dev=(x[col]-m).groupby(x["day"]).sum(); G=len(dev)
        se=np.sqrt(G/(G-1)*(dev**2).sum())/n
        return pd.Series({"n":n,"mean%":m*100,"t_day":m/se,"days":G})
    zb=[-99,-2,-1,-0.3,0.3,1,2,99]
    for h in [1,2,3]:
        col=f"n{h}"
        mu=d[d.pos%h==0].groupby("coin")[col].mean()
        d[f"u{h}"]=d[col]-d["coin"].map(mu)
        res=[]
        for off in range(h):
            g=d[(d.pos%h==off)&d.fa]
            res.append(g.groupby(pd.cut(g.z,zb))[f"u{h}"].mean()*100)
        out[f"FA h{h} unusual% by z bin, each grid offset"]=pd.concat(res,axis=1)
        g=d[(d.pos%h==0)&d.fa]
        out[f"FA h{h} clustered by z bin (grid 0)"]=g.groupby(pd.cut(g.z,zb)).apply(lambda x:clus(x,f"u{h}"))
        up=g[g.z>0].dropna(subset=[f"u{h}"])
        sl=np.polyfit(up.z,up[f"u{h}"],1)[0]
        dn=g[g.z<0].dropna(subset=[f"u{h}"])
        sl2=np.polyfit(dn.z,dn[f"u{h}"],1)[0]
        out[f"FA h{h} slopes"]=pd.Series({"slope up days (u on z)%":sl*100,"slope down days%":sl2*100})
    g=d[d.fa&(d.z>0.3)]
    out["FA up days next1 by prior 5d return tercile"]=g.groupby(pd.qcut(g.p5,3,labels=["low","mid","high"])).apply(lambda x:clus(x,"u1"))
    out["FA up days next1 by volume ratio tercile"]=g.groupby(pd.qcut(g.vr,3,labels=["low","mid","high"])).apply(lambda x:clus(x,"u1"))
    g=d[d.fa&(d.z<-0.3)]
    out["FA down days next1 by volume ratio tercile"]=g.groupby(pd.qcut(g.vr,3,labels=["low","mid","high"])).apply(lambda x:clus(x,"u1"))
    out["FA down days next1 by prior 5d tercile"]=g.groupby(pd.qcut(g.p5,3,labels=["low","mid","high"])).apply(lambda x:clus(x,"u1"))
    return out
