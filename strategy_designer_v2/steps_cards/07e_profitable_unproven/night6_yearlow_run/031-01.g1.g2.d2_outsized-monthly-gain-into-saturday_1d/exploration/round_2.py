def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            b["wd"]=ts.dt.weekday.values; b["yr"]=ts.dt.year.values
            b["nxt"]=b["close"].shift(-1)/b["close"]-1
            b["nxt2"]=b["close"].shift(-2)/b["close"]-1
            b["nxt_wd"]=b["wd"].shift(-1)
            b["r20"]=b["close"]/b["close"].shift(20)-1
            b["r5"]=b["close"]/b["close"].shift(5)-1
            lr=np.log(b["close"]).diff()
            b["vol20"]=lr.rolling(20).std()
            b["vol365"]=lr.rolling(365,min_periods=120).std()
            b["coin"]=coin; b["win"]=w
            b["pnl"]=b["postRebalance_current_allocation"]*b["nxt"]
            rows.append(b[["coin","win","wd","yr","nxt","nxt2","nxt_wd","r20","r5","vol20","vol365","pnl"]])
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin")["nxt"].mean()
    d["ex"]=d["nxt"]-d["coin"].map(mu)
    d["ex2"]=d["nxt2"]-2*d["coin"].map(mu)
    def summ(x):
        x=x.dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"median":x.median(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out={}
    fr=d[d["nxt_wd"]==5].dropna(subset=["ex","r20"]).copy()
    pos=fr[fr["r20"]>0].copy()
    out["Sat excess, r20>0, by year"]=pos.groupby("yr")["ex"].apply(summ).unstack()
    lo,hi=pos["ex"].quantile([0.01,0.99])
    out["Sat excess r20>0, winsorised 1%"]=summ(pos["ex"].clip(lo,hi))
    pos["volq"]=pos.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["Sat excess r20>0 by vol20 tercile"]=pos.groupby("volq")["ex"].apply(summ).unstack()
    fr["z"]=fr["r20"]/(fr["vol365"]*np.sqrt(20))
    fr["zq"]=fr.groupby("coin")["z"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["Sat excess by vol-scaled r20 quintile"]=fr.groupby("zq")["ex"].apply(summ).unstack()
    fr["r5q"]=fr.groupby("coin")["r5"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["Sat excess by r5 quintile"]=fr.groupby("r5q")["ex"].apply(summ).unstack()
    out["Fri->Sun 2-day excess by r20 quintile"]=fr.assign(q=fr.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))).groupby("q")["ex2"].apply(summ).unstack()
    for k,name in [(4,"Fri"),(6,"Sun"),(0,"Mon")]:
        o=d[d["nxt_wd"]==k].dropna(subset=["ex","r20"]).copy()
        o["q"]=o.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
        out[f"{name} excess by r20 quintile"]=o.groupby("q")["ex"].apply(summ).unstack()[["n","mean","t"]]
    # book daily, equal-weight
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items(): dd.append(x.assign(coin=coin,win=w))
    D=pd.concat(dd); D["key"]=D["win"]+"_"+D["day"].astype(str)
    bk=D.groupby("key")["book_return"].mean().dropna()
    s=bk.sort_values(ascending=False)
    out["book daily"]=pd.Series({"days":len(bk),"sum":bk.sum(),"top10 days":s.head(10).sum(),"top30":s.head(30).sum(),"mean":bk.mean(),"mean ex top10":s.iloc[10:].mean(),"t ex top10":s.iloc[10:].mean()/(s.iloc[10:].std()/np.sqrt(len(s)-10))})
    return out
