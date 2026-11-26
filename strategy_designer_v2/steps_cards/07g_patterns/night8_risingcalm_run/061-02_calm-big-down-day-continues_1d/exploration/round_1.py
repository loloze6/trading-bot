def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd=r1.rolling(30,min_periods=20).std()
            z=r1/sd
            calm=(b["regime"]!="chop")
            tr60=c/c.shift(60)-1
            rng=(b["high"]-b["low"])/c
            clv=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            wd=pd.to_datetime(b["timestamp"]).dt.weekday
            n=len(b)
            for h in (1,2,5):
                f=c.shift(-h)/c-1
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,i=i,z=z.iat[i],calm=bool(calm.iat[i]),
                        tr=tr60.iat[i],clv=clv.iat[i],rng=rng.iat[i]/sd.iat[i] if sd.iat[i]>0 else np.nan,
                        wd=wd.iat[i],f=f.iat[i],pos=b["postRebalance_current_allocation"].iat[i]))
    d=pd.DataFrame(rows).dropna(subset=["f"])
    out={}
    def tab(g):
        return pd.Series({"n":len(g),"mean%":g["f"].mean()*100,"t":g["f"].mean()/(g["f"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    for h in (1,2,5):
        x=d[d.h==h].dropna(subset=["z"]).copy()
        x["f"]=x["f"]-x.groupby("coin")["f"].transform("mean")
        x["zb"]=pd.cut(x["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
        out[f"h{h} excess by z x calm"]=x.groupby(["calm","zb"],observed=True).apply(tab).unstack(0)
    x=d[d.h==5].dropna(subset=["z"]).copy()
    x["f"]=x["f"]-x.groupby("coin")["f"].transform("mean")
    x["trb"]=pd.cut(x["tr"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    x["zs"]=np.sign(x["z"])
    out["h5 excess by trend x zsign x calm"]=x[abs(x.z)>1].groupby(["trb","calm","zs"],observed=True).apply(tab)
    x["cb"]=pd.cut(x["clv"],[-0.01,0.2,0.8,1.01],labels=["lowclose","mid","highclose"])
    out["h5 excess by close loc x calm"]=x.groupby(["calm","cb"],observed=True).apply(tab)
    x["rb"]=pd.qcut(x["rng"],4,labels=False)
    out["h5 excess by range/sd quartile x calm"]=x.groupby(["calm","rb"],observed=True).apply(tab)
    y=d[d.h==1].copy()
    y["f"]=y["f"]-y.groupby("coin")["f"].transform("mean")
    out["h1 excess by weekday"]=y.groupby("wd").apply(tab)
    out["h1 excess by calm"]=y.groupby("calm").apply(tab)
    # spearman z vs f by calm, h5
    out["h5 spearman z-f"]=x.groupby("calm").apply(lambda g: pd.Series(stats.spearmanr(g.z,g.f,nan_policy='omit')[:2],index=["rho","p"]))
    return out
