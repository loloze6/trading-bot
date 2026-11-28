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
            b["ret1"]=b["close"]/b["close"].shift(1)-1
            b["up"]=(b["ret1"]>0).astype(float)
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            b["cl"]=(b["close"]-b["low"])/rng
            for h in [2,5,10]:
                b[f"f{h}"]=b["close"].shift(-h)/b["close"]-1
            b["coin"]=coin; b["win"]=w; b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["dkey"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    out={}
    def tt(s):
        s=s.dropna()
        return pd.Series({"n":len(s),"mean%":100*s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    res=[]
    for h in [2,5,10]:
        g=B[(B["pos"]%h==0)&B[f"f{h}"].notna()].copy()
        drift=g.groupby("coin")[f"f{h}"].mean()
        g["u"]=g[f"f{h}"]-g["coin"].map(drift)
        g["tot"]=g[f"f{h}"]
        fc=g[g["fc"]&g["volr"].notna()].copy()
        fc["lvq"]=pd.qcut(fc["volr"],4,labels=["v1light","v2","v3","v4heavy"])
        for side,sub in [("up",fc[fc.up==1]),("down",fc[fc.up==0])]:
            for q,s2 in sub.groupby("lvq"):
                r=tt(s2["u"]); r["h"]=h; r["grp"]=f"{side} {q}"; r["tot%"]=100*s2["tot"].mean(); res.append(r)
            r=pd.Series({"n":len(sub),"rho volr,u":stats.spearmanr(sub["volr"],sub["u"]).correlation,
                         "rho ret1,u":stats.spearmanr(sub["ret1"],sub["u"]).correlation,
                         "rho cl,u":stats.spearmanr(sub["cl"],sub["u"],nan_policy="omit").correlation})
            out[f"h{h} {side} rank corrs"]=r.round(3)
        if h==5:
            lu=fc[(fc.up==1)&(fc.volr<1)]
            out["h5 light up by coin"]=lu.groupby("coin")["u"].agg(["count",lambda s:100*s.mean()])
            out["h5 light up by year"]=lu.groupby("year")["u"].agg(["count",lambda s:100*s.mean()])
            ld=fc[(fc.up==0)&(fc.volr<1)]
            out["h5 light down by coin"]=ld.groupby("coin")["u"].agg(["count",lambda s:100*s.mean()])
            out["h5 light down by year"]=ld.groupby("year")["u"].agg(["count",lambda s:100*s.mean()])
            # inverse volume ratio grading among up days
            up=fc[fc.up==1].copy()
            up["inv"]=1/up["volr"]
            out["h5 up: u% by inverse volr tercile"]=up.groupby(pd.qcut(up["inv"],3,labels=["heavy","mid","light"]))["u"].agg(["count",lambda s:100*s.mean()])
            out["h5 all fc: u% by volr tercile"]=fc.groupby(pd.qcut(fc["volr"],3,labels=["light","mid","heavy"]))["u"].agg(["count",lambda s:100*s.mean()])
            out["h5 all fc: u% by close-loc tercile"]=fc.groupby(pd.qcut(fc["cl"],3,labels=["low","mid","high"]))["u"].agg(["count",lambda s:100*s.mean()])
    out["groups"]=pd.DataFrame(res).set_index(["grp","h"]).round(3)
    return out
