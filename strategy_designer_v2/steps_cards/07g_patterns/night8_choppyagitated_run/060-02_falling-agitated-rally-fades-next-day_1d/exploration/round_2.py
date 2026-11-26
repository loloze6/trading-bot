import numpy as np, pandas as pd

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std(); z=r/sd
            ts=pd.to_datetime(b["timestamp"])
            rng=(b["high"]-b["low"])/c
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"r":r,"z":z,
                "inprof":(b["regime"]=="unknown").values,"day":ts.dt.floor("D"),"year":ts.dt.year,
                "rng_z":rng/rng.rolling(30,min_periods=20).mean(),"sd":sd})
            for h in (1,2,3,5):
                df[f"f{h}"]=c.shift(-h)/c-1
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    for h in (1,2,3,5):
        d[f"x{h}"]=d[f"f{h}"]-d.groupby("coin")[f"f{h}"].transform(lambda s: s[d.loc[s.index,"pos"]%h==0].mean())
    def clus_t(y,x,day):
        m=pd.DataFrame({"y":y,"x":x,"day":day}).dropna()
        if len(m)<10: return (np.nan,np.nan,len(m),0)
        X=np.column_stack([np.ones(len(m)),m.x.values]); Y=m.y.values
        XtX=np.linalg.inv(X.T@X); bta=XtX@X.T@Y; e=Y-X@bta
        S=np.zeros((2,2))
        for _,idx in m.groupby("day").indices.items():
            g=X[idx].T@e[idx]; S+=np.outer(g,g)
        V=XtX@S@XtX; return (bta[1],bta[1]/np.sqrt(V[1,1]),len(m),m.day.nunique())
    def mean_t(y,day):
        m=pd.DataFrame({"y":y,"day":day}).dropna()
        s=m.groupby("day")["y"].apply(lambda v:(v-m.y.mean()).sum())
        se=np.sqrt((s**2).sum())/len(m)
        return m.y.mean()*100, m.y.mean()/se
    out={}
    res=[]
    for side,cond in (("up",lambda q:q.z>0),("down",lambda q:q.z<0)):
        for h in (1,2,3,5):
            q=d[(d.inprof)&(d.pos%h==0)&cond(d)]
            sl,t,n,nd=clus_t(-q[f"x{h}"] if side=="up" else q[f"x{h}"], q.z.abs(), q.day)
            mm,mt=mean_t(-q[f"x{h}"] if side=="up" else q[f"x{h}"], q.day)
            res.append({"side":side,"h":h,"slope%":sl*100,"slope_t":t,"mean%":mm,"mean_t":mt,"n":n,"days":nd})
    out["in profile: signal-dir excess vs |z| (short after up, long after down)"]=pd.DataFrame(res)
    res=[]
    for side,cond in (("up",lambda q:q.z>0),("down",lambda q:q.z<0)):
        for h in (1,3):
            q=d[(d.inprof)&(d.pos%h==0)&cond(d)]
            sl,t,n,nd=clus_t(-q[f"x{h}"] if side=="up" else q[f"x{h}"], q.rng_z, q.day)
            res.append({"side":side,"h":h,"slope_on_range%":sl*100,"t":t,"n":n})
    out["in profile: signal-dir excess vs range/30d range"]=pd.DataFrame(res)
    res=[]
    for y,g in d[d.inprof&(d.z>0)&(d.pos%3==0)].groupby("year"):
        mm,mt=mean_t(-g["x3"],g.day); res.append({"year":y,"n":len(g),"mean3%":mm,"t":mt})
    out["in profile up days, short 3d excess by year"]=pd.DataFrame(res)
    res=[]
    for y,g in d[d.inprof&(d.z<0)].groupby("year"):
        mm,mt=mean_t(g["x1"],g.day); res.append({"year":y,"n":len(g),"mean1%":mm,"t":mt})
    out["in profile down days, long 1d excess by year"]=pd.DataFrame(res)
    q=d[(~d.inprof)&(d.z<0)]
    sl,t,n,nd=clus_t(q["x1"],q.z.abs(),q.day)
    out["out profile down days slope on |z| next1"]=pd.Series({"slope%":sl*100,"t":t,"n":n,"days":nd})
    return out
