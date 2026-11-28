def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            n=len(b)
            b["pos"]=np.arange(n)
            b["fc"]=b["regime"].isin(["trending","unknown"])
            b["volr"]=b["volume"]/b["volume"].shift(1).rolling(20,min_periods=20).mean()
            b["up"]=(b["close"]>b["close"].shift(1)).astype(float)
            b["ret1"]=b["close"]/b["close"].shift(1)-1
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            b["cl"]=(b["close"]-b["low"])/rng
            b["ret5past"]=b["close"]/b["close"].shift(5)-1
            for h in [1,3,5,10]:
                b[f"f{h}"]=b["close"].shift(-h)/b["close"]-1
            b["coin"]=coin; b["win"]=w; b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["dkey"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    out={}
    out["regime share"]=B["regime"].value_counts(normalize=True)
    res=[]; grp=[]
    for h in [1,3,5,10]:
        g=B[(B["pos"]%h==0)&B[f"f{h}"].notna()].copy()
        drift=g.groupby("coin")[f"f{h}"].mean()
        g["u"]=g[f"f{h}"]-g["coin"].map(drift)
        fc=g[g["fc"]&g["volr"].notna()].copy()
        fc["vq"]=pd.qcut(fc["volr"],3,labels=["light","mid","heavy"])
        def tt(s):
            s=s.dropna(); 
            return pd.Series({"n":len(s),"mean%":100*s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
        for name,sub in [("all fc",fc),("fc up",fc[fc.up==1]),("fc down",fc[fc.up==0]),
                         ("fc heavy(>=1.5)",fc[fc.volr>=1.5]),("fc heavy up",fc[(fc.volr>=1.5)&(fc.up==1)]),
                         ("fc heavy down",fc[(fc.volr>=1.5)&(fc.up==0)]),("fc light up(<1)",fc[(fc.volr<1)&(fc.up==1)]),
                         ("fc light down(<1)",fc[(fc.volr<1)&(fc.up==0)]),
                         ("fc heavy cl>0.5",fc[(fc.volr>=1.5)&(fc.cl>0.5)]),("fc heavy cl<=0.5",fc[(fc.volr>=1.5)&(fc.cl<=0.5)])]:
            r=tt(sub["u"]); r["h"]=h; r["grp"]=name; res.append(r)
        if h==5:
            fc["rq"]=pd.qcut(fc["ret1"],4,labels=["r1","r2","r3","r4"])
            out["h5 by volr tercile x up: mean u%"]=fc.pivot_table(index="vq",columns="up",values="u",aggfunc=lambda s:100*s.mean())
            out["h5 by volr tercile x up: n"]=fc.pivot_table(index="vq",columns="up",values="u",aggfunc="count")
            out["h5 by day return quartile: u%"]=fc.groupby("rq")["u"].agg(["count",lambda s:100*s.mean()])
            hv=fc[fc.volr>=1.5]
            out["h5 heavy by coin"]=hv.groupby("coin")["u"].agg(["count",lambda s:100*s.mean()])
            out["h5 heavy by year"]=hv.groupby("year")["u"].agg(["count",lambda s:100*s.mean()])
            out["h5 heavy by day ret quartile"]=hv.groupby(pd.qcut(hv["ret1"],3))["u"].agg(["count",lambda s:100*s.mean()])
            out["h5 fc by past5 tercile"]=fc.groupby(pd.qcut(fc["ret5past"],3,labels=["low","mid","high"]))["u"].agg(["count",lambda s:100*s.mean()])
            out["h5 fc corr volr,u (spearman)"]=float(stats.spearmanr(fc["volr"],fc["u"]).correlation)
            up=fc[fc.up==1]
            out["h5 fc up corr volr,u"]=float(stats.spearmanr(up["volr"],up["u"]).correlation)
    out["groups by horizon"]=pd.DataFrame(res).set_index(["grp","h"]).round(3)
    return out
