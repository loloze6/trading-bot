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
            b["coin"]=coin; b["win"]=w; b["pos"]=np.arange(len(b))
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","win","pos","year","z","f1","f2","f3","f5","inprof","forecast","postRebalance_current_allocation"]])
    d=pd.concat(rows)
    drift={h:d.groupby("coin")[f"f{h}"].apply(lambda s: s.iloc[::1].mean()) for h in (1,2,3,5)}
    for h in (1,2,3,5):
        d[f"x{h}"]=d[f"f{h}"]-d["coin"].map(d.groupby("coin")["f1"].mean()*h)
    p=d[d.inprof & d.z.notna()].copy()
    out={}
    out["share in profile"]=float(d.inprof.mean())
    p["zbin"]=pd.cut(p.z,[-10,-2,-1,-0.5,0,0.5,1,2,10])
    def agg(g):
        s=g["x1"].dropna()
        return pd.Series({"n":len(s),"mean_x1":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out["x1 by z bin, in profile"]=p.groupby("zbin").apply(agg)
    q=d[(~d.inprof)&d.z.notna()].copy()
    q["zbin"]=pd.cut(q.z,[-10,-2,-1,-0.5,0,0.5,1,2,10])
    out["x1 by z bin, out of profile"]=q.groupby("zbin").apply(agg)
    up=p[p.z>0]
    out["up days in profile by coin"]=up.groupby("coin").apply(lambda g: pd.Series({"n":g.x1.notna().sum(),"mean_x1":g.x1.mean(),"corr_z_x1":g[["z","x1"]].corr().iloc[0,1]}))
    out["up days in profile by year"]=up.groupby("year").apply(lambda g: pd.Series({"n":g.x1.notna().sum(),"mean_x1":g.x1.mean(),"corr_z_x1":g[["z","x1"]].corr().iloc[0,1]}))
    res={}
    for h in (1,2,3,5):
        g=up[up.pos%h==0].dropna(subset=[f"x{h}"])
        sl=stats.linregress(g.z,g[f"x{h}"])
        top=g[g.z>g.z.quantile(0.75)][f"x{h}"]
        res[h]={"n":len(g),"slope":sl.slope,"t":sl.slope/sl.stderr,"mean_x":g[f"x{h}"].mean(),"top_quartile_mean":top.mean(),"top_n":len(top)}
    out["up days horizons"]=pd.DataFrame(res).T
    return out
