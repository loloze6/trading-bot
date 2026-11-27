import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b))})
            d["inprof"]=(b["regime"]=="unknown").values
            d["r1"]=c.pct_change().values
            d["r7"]=(c/c.shift(7)-1).values
            d["r30"]=(c/c.shift(30)-1).values
            lr=np.log(c).diff()
            d["vol20"]=lr.rolling(20).std().values
            d["rng"]=((b["high"]-b["low"])/c).values
            d["clpos"]=((c-b["low"])/(b["high"]-b["low"])).values
            for h in [1,3,7,21]:
                d[f"f{h}"]=(c.shift(-h)/c-1).values
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday.values
            d["alloc"]=b["postRebalance_current_allocation"].values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    # drift per coin per horizon from grids
    for h in [1,3,7,21]:
        g=D[(D.pos%h==0)&D[f"f{h}"].notna()]
        D[f"x{h}"]=D[f"f{h}"]-D.coin.map(g.groupby("coin")[f"f{h}"].mean())
    D["vz"]=D["vol20"]/D.groupby("coin")["vol20"].transform("median")
    def grid(h): return D[(D.pos%h==0)&D[f"x{h}"].notna()]
    # r30 quintiles vs fwd excess, in and out of profile
    res=[]
    for h in [7,21]:
        g=grid(h).dropna(subset=["r30"])
        g["q"]=pd.qcut(g.r30,5,labels=False)
        for ip in [True,False]:
            s=g[g.inprof==ip]
            for q,t in s.groupby("q")[f"x{h}"]:
                res.append(dict(h=h,inprof=ip,q=q,n=len(t),mean=t.mean(),t=t.mean()/(t.std()/np.sqrt(len(t))) if len(t)>2 else np.nan))
    out["r30 quintile -> fwd excess"]=pd.DataFrame(res)
    # r7 and r1 quintiles vs fwd 3/7
    res=[]
    for var in ["r1","r7","vz","rng","clpos"]:
        for h in [1,3,7]:
            g=grid(h).dropna(subset=[var]).copy()
            g["q"]=pd.qcut(g[var],5,labels=False,duplicates="drop")
            for q,t in g.groupby("q")[f"x{h}"]:
                res.append(dict(var=var,h=h,q=q,n=len(t),mean=t.mean(),t=t.mean()/(t.std()/np.sqrt(len(t)))))
    R=pd.DataFrame(res)
    out["feature quintiles all bars"]=R[R.h.isin([1,7])]
    out["feature quintiles h3"]=R[R.h==3]
    # weekday
    g=grid(1)
    out["weekday x1"]=g.groupby("wd")["x1"].agg(["count","mean",lambda s:s.mean()/(s.std()/np.sqrt(len(s)))])
    # book daily: biggest days
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy();t["coin"]=coin;t["w"]=w;dd.append(t)
    DD=pd.concat(dd)
    bk=DD.groupby(["w","day"])["book_return"].mean().dropna()
    out["book by window"]=DD.groupby("w")["book_return"].agg(["count","mean","std"])
    out["share in prof"]=D.inprof.mean()
    return out
