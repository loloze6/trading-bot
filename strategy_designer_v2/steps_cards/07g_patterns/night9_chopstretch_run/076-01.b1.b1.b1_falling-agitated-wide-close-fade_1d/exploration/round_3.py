def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            rng=b.high-b.low
            mr=rng.rolling(20).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b.timestamp)})
            d["day"]=d.ts.dt.floor("D")
            d["prod"]=(b.close-(b.high+b.low)/2)/mr
            d["wid"]=rng/mr
            d["loc"]=(b.close-b.low)/rng.replace(0,np.nan)
            d["tr60"]=b.close/b.close.shift(60)-1
            r=b.close.pct_change()
            v30=r.rolling(30).std()
            d["agit"]=v30>v30.expanding(30).median()
            d["nxt"]=b.close.shift(-1)/b.close-1
            d["inprof"]=(b.regime!="chop")
            rows.append(d)
    D=pd.concat(rows)
    dr=D.groupby("coin").nxt.mean()
    D["ab"]=D.nxt-D.coin.map(dr)
    D=D.dropna(subset=["prod","ab"])
    def ct(df):
        if len(df)<5: return pd.Series({"mean%":np.nan,"n":len(df),"days":0,"t_day":np.nan})
        s=df.groupby("day").ab.apply(lambda x:(x-df.ab.mean()).sum())
        se=np.sqrt((s**2).sum())/len(df)
        return pd.Series({"mean%":df.ab.mean()*100,"n":len(df),"days":df.day.nunique(),"t_day":df.ab.mean()/se})
    D["trend"]=np.where(D.tr60.isna(),"na",np.where(D.tr60>0.10,"rising",np.where(D.tr60<-0.10,"falling","choppy")))
    D["yr"]=D.ts.dt.year
    out={}
    up=D[D["prod"]>0].copy()
    up["pq"]=up.groupby("trend")["prod"].transform(lambda x: pd.qcut(x,4,labels=False,duplicates="drop"))
    out["prod>0 by trend x quartile"]=up.groupby(["trend","pq"]).apply(ct).round(3)
    out["spearman prod>0 vs ab by trend"]=up.groupby("trend").apply(lambda g: pd.Series(stats.spearmanr(g["prod"],g.ab)[:2],index=["rho","p"])).round(4)
    ch=up[(up.trend=="choppy")]
    ch_top=ch[ch.pq==3]
    out["choppy top quartile by agit proxy"]=ch_top.groupby("agit").apply(ct).round(3)
    out["choppy top quartile by year"]=ch_top.groupby("yr").apply(ct).round(3)
    out["choppy top quartile by coin"]=ch_top.groupby("coin").apply(ct).round(3)
    lo=D[D["prod"]<0].copy()
    lo["pq"]=lo.groupby("trend")["prod"].transform(lambda x: pd.qcut(x,4,labels=False,duplicates="drop"))
    out["prod<0 by trend x quartile"]=lo.groupby(["trend","pq"]).apply(ct).round(3)
    return out
