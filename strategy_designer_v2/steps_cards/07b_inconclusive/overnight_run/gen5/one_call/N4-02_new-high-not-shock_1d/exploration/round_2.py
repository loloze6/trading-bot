def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        allnon=[]; crow=[]
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values.astype(float); n=len(c)
            f10=np.full(n,np.nan)
            if n>10: f10[:n-10]=c[10:]/c[:n-10]-1
            s=f10[::10]; allnon+=list(s[~np.isnan(s)])
            fc=b["forecast"].fillna(0).values
            r1=np.r_[np.nan,c[1:]/c[:-1]-1]
            tr60=np.full(n,np.nan)
            if n>60: tr60[60:]=c[60:]/c[:-60]-1
            vol=pd.Series(r1).abs().rolling(60,min_periods=20).mean().shift(1).values
            ts=pd.to_datetime(b["timestamp"])
            last=-999; clus=-1; prev=False
            for i in range(n):
                if fc[i]>0:
                    first = (i-last>10)
                    if first: clus+=1
                    crow.append(dict(coin=coin,w=w,clus=f"{coin}{w}{clus}",first=first,newrun=not prev,
                        fc=fc[i],f10=f10[i],r1=r1[i],tr60=tr60[i],vol=vol[i],year=ts.iloc[i].year))
                    last=i
                prev=fc[i]>0
        m=np.mean(allnon)
        for r in crow: r["ex"]=(r["f10"]-m)*100; r["raw"]=r["f10"]*100
        rows+=crow
    d=pd.DataFrame(rows).dropna(subset=["ex"])
    med=d.fc.median(); d["top"]=d.fc>med
    def q(x,k): return pd.qcut(x.rank(method="first"),k,labels=False)
    def summ(g):
        n=len(g); sd=g.ex.std()
        return pd.Series(dict(n=n,mean=g.ex.mean(),med=g.ex.median(),sd=sd,
            t=g.ex.mean()/(sd/np.sqrt(n)) if n>2 else np.nan,hit=(g.raw>0).mean()))
    out={}
    fst=d[d["first"]].copy()
    out["median fc; share fc==20"]=pd.Series(dict(med=med,cap=(d.fc>=19.99).mean(),nfirst=len(fst),nall=len(d)))
    out["first by fc quintile"]=fst.groupby(q(fst.fc,5)).apply(summ)
    out["first by top"]=fst.groupby("top").apply(summ)
    out["first by coin x top"]=fst.groupby(["coin","top"]).apply(summ)
    out["first by year x top"]=fst.groupby(["year","top"]).apply(summ)
    fst["trend"]=np.where(fst.tr60>0.3,"a_up>30",np.where(fst.tr60>0,"b_up0-30","c_down60"))
    out["first by 60d trend x top"]=fst.groupby(["trend","top"]).apply(summ)
    fst["vq"]=q(fst.vol.fillna(fst.vol.median()),3)
    out["first by vol tercile x top"]=fst.groupby(["vq","top"]).apply(summ)
    out["first by raw r1 quartile"]=fst.groupby(q(fst.r1,4)).apply(summ)
    out["all: newrun vs cont"]=d.groupby("newrun").apply(summ)
    out["every 10th pos bar by top"]=d.iloc[::10].groupby("top").apply(summ)
    return out
