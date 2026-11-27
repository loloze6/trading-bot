def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].values; allr.append(pd.Series(c).pct_change().dropna())
        drift=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            rng=(b["high"]-b["low"])
            mult=rng/rng.shift(1).rolling(20).mean()
            loc=(b["close"]-b["low"])/rng.replace(0,np.nan)
            c=b["close"]
            df=pd.DataFrame({"coin":coin,"win":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "mult":mult,"loc":loc,"fc":b["forecast"],"agit":(b["regime"]!="chop"),
                "r1":c.shift(-1)/c-1,"r2":c.shift(-2)/c-1,"r3":c.shift(-3)/c-1,
                "tr60":c/c.shift(60)-1,"ret1":c/c.shift(1)-1,"drift":drift})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    D["year"]=D["day"].dt.year
    for h in (1,2,3):
        D[f"u{h}"]=-(D[f"r{h}"]-h*D["drift"])
    def st(g,col="u1"):
        g=g.dropna(subset=[col]); n=len(g)
        if n<5: return pd.Series({"n":n,"days":g["day"].nunique(),"mean%":np.nan,"t":np.nan})
        m=g[col].mean(); S=(g[col]-m).groupby(g["day"]).sum()
        se=np.sqrt((S**2).sum())/n
        return pd.Series({"n":n,"days":g["day"].nunique(),"mean%":100*m,"t":m/se})
    cases=D[D["fc"]<=-2]
    out={}
    out["cases_all_h"]=pd.DataFrame({f"h{h}":st(cases,f"u{h}") for h in (1,2,3)}).T
    out["cases_by_coin"]=cases.groupby("coin").apply(st)
    out["cases_by_year"]=cases.groupby("year").apply(st)
    cases=cases.copy()
    cases["fq"]=pd.qcut(cases["fc"].abs().rank(method="first"),4,labels=False)
    out["cases_by_fc_quart"]=cases.groupby("fq").apply(st)
    wide=D[(D["mult"]>=1)]
    W=wide.copy()
    W["mb"]=pd.cut(W["mult"],[1,1.3,1.7,2.5,100],right=False)
    W["lb"]=pd.cut(W["loc"],[0,0.25,0.5,0.75,0.9,1.01],right=False)
    out["agit_wide_by_loc"]=W[W.agit].groupby("lb").apply(st)
    out["calm_wide_by_loc"]=W[~W.agit].groupby("lb").apply(st)
    out["agit_upper_by_mult"]=W[W.agit&(W["loc"]>=0.5)].groupby("mb").apply(st)
    W["trend"]=np.where(W["tr60"]>0.1,"rising",np.where(W["tr60"]<-0.1,"falling",np.where(W["tr60"].notna(),"choppy","na")))
    out["agit_upper_by_trend"]=W[W.agit&(W["loc"]>=0.5)].groupby("trend").apply(st)
    W["up"]=W["ret1"]>0
    out["agit_upper_by_dayup"]=W[W.agit&(W["loc"]>=0.5)].groupby("up").apply(st)
    return out
