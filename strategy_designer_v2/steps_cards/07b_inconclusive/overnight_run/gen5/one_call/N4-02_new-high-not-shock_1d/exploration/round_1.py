def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        allnon=[]
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            n=len(c)
            f10=np.full(n,np.nan); f10[:n-10]=c[10:]/c[:n-10]-1
            allnon+=list(f10[::10][~np.isnan(f10[::10])])
            fc=b["forecast"].fillna(0).values
            r1=np.r_[np.nan,c[1:]/c[:-1]-1]
            tr60=np.r_[[np.nan]*60,c[60:]/c[:-60]-1] if n>60 else np.full(n,np.nan)
            vol=pd.Series(r1).abs().rolling(60,min_periods=20).mean().shift(1).values
            last=-999; clus=-1; prevpos=False
            for i in range(n):
                if fc[i]>0:
                    if i-last>10: clus+=1; first=True
                    else: first=False
                    rows.append(dict(coin=coin,w=w,i=i,clus=f"{coin}{w}{clus}",first=first,
                        newrun=not prevpos,fc=fc[i],f10=f10[i],r1=r1[i],tr60=tr60[i],vol=vol[i],
                        year=pd.Timestamp(b["timestamp"].iloc[i]).year))
                    last=i
                prevpos=fc[i]>0
        m=np.mean(allnon)
        for r in rows:
            if r["coin"]==coin and "ex" not in r: r["ex"]=r["f10"]-m
    d=pd.DataFrame(rows).dropna(subset=["ex"])
    d["ex"]*=100
    med=d.fc.median(); d["top"]=d.fc>med
    out={}
    fst=d[d["first"]]
    def summ(g):
        return pd.Series(dict(n=len(g),mean=g.ex.mean(),sd=g.ex.std(),t=g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    out["first-of-cluster by fc quintile"]=fst.groupby(pd.qcut(fst.fc,5,labels=False)).apply(summ)
    out["first-of-cluster by top"]=fst.groupby("top").apply(summ)
    out["first by coin x top"]=fst.groupby(["coin","top"]).apply(summ)
    out["first by year x top"]=fst.groupby(["year","top"]).apply(summ)
    fst=fst.assign(trend=np.where(fst.tr60>0.3,"up>30%",np.where(fst.tr60>0,"up0-30","down60")))
    out["first by 60d trend x top"]=fst.groupby(["trend","top"]).apply(summ)
    vq=pd.qcut(fst.vol,3,labels=["lowvol","midvol","highvol"])
    out["first by vol tercile x top"]=fst.groupby([vq,"top"]).apply(summ)
    rq=pd.qcut(fst.r1,4,labels=False)
    out["first by raw return quartile"]=fst.groupby(rq).apply(summ)
    out["all bars: newrun vs continuing"]=d.groupby("newrun").apply(summ)
    out["all positive bars every 10th by top"]=d.iloc[::10].groupby("top").apply(summ)
    return out
