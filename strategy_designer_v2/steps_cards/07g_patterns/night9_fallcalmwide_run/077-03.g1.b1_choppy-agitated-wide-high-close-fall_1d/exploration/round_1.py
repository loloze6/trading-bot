import numpy as np, pandas as pd

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            width=((b["high"]-b["low"])/c)/sd
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            cl=(c-b["low"])/rng
            nxt=c.shift(-1)/c-1
            r5=c/c.shift(5)-1
            df=pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"]),
                "regime":b["regime"],"cl":cl,"width":width,"nxt":nxt,"r1":r,"r5":r5,
                "pos":b["postRebalance_current_allocation"]})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    D=D.dropna(subset=["nxt"])
    drift=D.groupby("coin")["nxt"].mean()
    D["dev"]=D["nxt"]-D["coin"].map(drift)
    D["day"]=D["ts"].dt.floor("D")
    D["prof"]=np.where(D["regime"]=="chop","out","in")
    def ct(g,sign=1):
        g=g.dropna(subset=["dev"])
        x=g["dev"]*sign; n=len(x)
        if n<5: return pd.Series({"n":n,"mean%":np.nan,"t":np.nan,"days":0})
        m=x.mean()
        S=(x-m).groupby(g["day"]).sum(); G=len(S)
        se=np.sqrt(G/(G-1)*(S**2).sum())/n if G>1 else np.nan
        return pd.Series({"n":n,"mean%":100*m,"t":m/se,"days":G})
    D["clbin"]=pd.cut(D["cl"],[-0.01,0.1,0.25,0.5,0.75,0.9,1.01],labels=["0-.1",".1-.25",".25-.5",".5-.75",".75-.9",".9-1"])
    out={}
    out["regime counts"]=D["regime"].value_counts()
    out["next-day dev (raw, long sign) by profile x close loc"]=D.groupby(["prof","clbin"]).apply(ct)
    D["wq"]=D.groupby("prof")["width"].transform(lambda s: pd.qcut(s,3,labels=["narrow","mid","wide"]))
    hi=D[D["cl"]>=0.75]; lo=D[D["cl"]<=0.25]
    out["high closes: dev (raw) by profile x width tercile"]=hi.groupby(["prof","wq"]).apply(ct)
    out["low closes: dev (raw) by profile x width tercile"]=lo.groupby(["prof","wq"]).apply(ct)
    D["r1q"]=D.groupby("prof")["r1"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["dev by profile x day return quintile"]=D.groupby(["prof","r1q"]).apply(ct)
    D["r5q"]=D.groupby("prof")["r5"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["dev by profile x 5d return quintile"]=D.groupby(["prof","r5q"]).apply(ct)
    out["dev by weekday (all)"]=D.groupby(D["ts"].dt.dayofweek).apply(ct)
    out["dev by year (all)"]=D.groupby(D["ts"].dt.year).apply(ct)
    # high close in profile by year
    out["in-profile high close short by year"]=hi[hi.prof=="in"].groupby(hi["ts"].dt.year).apply(lambda g: ct(g,-1))
    return out
