import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            b["z"]=r/sd
            for h in (1,2,3,5):
                b[f"f{h}"]=c.shift(-h)/c-1
            b["inprof"]=(b["regime"]=="unknown")
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            b["cloc"]=(b["close"]-b["low"])/rng
            b["coin"]=coin; b["win"]=w; b["pos"]=np.arange(len(b))
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b[["coin","win","pos","year","day","z","cloc","f1","f2","f3","f5","inprof"]])
    d=pd.concat(rows)
    m1=d.groupby("coin")["f1"].mean()
    for h in (1,2,3,5):
        d[f"x{h}"]=d[f"f{h}"]-d["coin"].map(m1*h)
    p=d[d.inprof & d.z.notna()].copy()
    out={}
    def reg(g,y,xcol):
        g=g.dropna(subset=[y,xcol])
        if len(g)<10: return {"n":len(g)}
        sl=stats.linregress(g[xcol],g[y])
        return {"n":len(g),"slope":sl.slope,"t":sl.slope/sl.stderr,"mean":g[y].mean(),
                "t_mean":g[y].mean()/(g[y].std()/np.sqrt(len(g)))}
    res={}
    for name,sub in [("all",p),("down",p[p.z<0]),("up",p[p.z>0])]:
        for h in (1,2,3,5):
            g=sub[sub.pos%h==0]
            res[f"{name} h{h} on z"]=reg(g,f"x{h}","z")
            res[f"{name} h{h} on cloc"]=reg(g,f"x{h}","cloc")
    out["regressions in profile"]=pd.DataFrame(res).T
    dn=p[p.z<0]
    out["down days in profile by coin"]=dn.groupby("coin").apply(lambda g: pd.Series({"n":g.x1.notna().sum(),"mean_x1":g.x1.mean(),"corr_z_x1":g[["z","x1"]].corr().iloc[0,1]}))
    out["down days in profile by year"]=dn.groupby("year").apply(lambda g: pd.Series({"n":g.x1.notna().sum(),"mean_x1":g.x1.mean(),"corr_z_x1":g[["z","x1"]].corr().iloc[0,1]}))
    p["zq"]=pd.qcut(p.z,5)
    out["x1,x3 by z quintile in profile"]=p.groupby("zq").agg(n=("x1","count"),x1=("x1","mean"),x3=("x3","mean"))
    p["cq"]=pd.qcut(p.cloc,4)
    out["x1 by close location quartile in profile"]=p.groupby("cq").agg(n=("x1","count"),x1=("x1","mean"),sd=("x1","std"))
    return out
