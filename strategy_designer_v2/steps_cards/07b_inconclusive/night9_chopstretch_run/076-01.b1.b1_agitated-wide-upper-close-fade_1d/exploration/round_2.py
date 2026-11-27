def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            allr.append(pd.Series(b["close"].values).pct_change().dropna())
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
                "tr60":c/c.shift(60)-1,"tr30":c/c.shift(30)-1,"drift":drift})
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
    D["trend"]=np.where(D["tr60"]>0.1,"rising",np.where(D["tr60"]<-0.1,"falling",np.where(D["tr60"].notna(),"choppy","na")))
    D["trend30"]=np.where(D["tr30"]>0.1,"rising",np.where(D["tr30"]<-0.1,"falling",np.where(D["tr30"].notna(),"choppy","na")))
    U=D[D.agit&(D["mult"]>=1)&(D["loc"]>=0.5)].copy()
    out={}
    out["upper_trend_h"]=pd.DataFrame({(t,h):st(U[U.trend==t],f"u{h}") for t in ["falling","choppy","rising","na"] for h in (1,2,3)}).T
    out["upper_na_by_trend30"]=U[U.trend=="na"].groupby("trend30").apply(st)
    F=U[U.trend=="falling"].copy()
    out["falling_by_year"]=F.groupby("year").apply(st)
    out["falling_by_coin"]=F.groupby("coin").apply(st)
    F["prod"]=F["mult"]*F["loc"]
    F["pq"]=pd.qcut(F["prod"].rank(method="first"),2,labels=["low","high"])
    out["falling_by_prod_half"]=F.groupby("pq").apply(st)
    out["falling_by_loc"]=F.groupby(pd.cut(F["loc"],[0.5,0.75,0.9,1.01],right=False)).apply(st)
    NF=U[U.trend.isin(["choppy","falling"])].copy()
    NF["prod"]=NF["mult"]*NF["loc"]
    NF["pq"]=pd.qcut(NF["prod"].rank(method="first"),2,labels=["low","high"])
    out["notrising_by_prod_half"]=NF.groupby("pq").apply(st)
    out["notrising_all"]=st(NF).to_frame().T
    return out
