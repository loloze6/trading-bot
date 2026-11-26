def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            hi=c.rolling(5,min_periods=5).max()
            sd=r.rolling(30,min_periods=20).std()
            depth=(c-hi)/hi/sd
            tr60=c/c.shift(60)-1
            ret5=c.pct_change(5)
            sd30_rel=sd/ r.rolling(90,min_periods=60).std()
            fwd=c.shift(-H)/c-1
            for i in range(0,len(b),H):
                if pd.isna(fwd.iloc[i]): continue
                rows.append(dict(coin=coin,w=w,i=i,day=str(b["timestamp"].iloc[i])[:10],
                    year=pd.Timestamp(b["timestamp"].iloc[i]).year,fc=b["forecast"].iloc[i],
                    depth=depth.iloc[i],fwd=fwd.iloc[i],tr60=tr60.iloc[i],ret5=ret5.iloc[i],agr=sd30_rel.iloc[i],sd=sd.iloc[i]))
    d=pd.DataFrame(rows)
    drift=d.groupby("coin")["fwd"].mean()
    d["ex"]=d["fwd"]-d["coin"].map(drift)
    def slope(g,x="fc"):
        g=g.dropna(subset=[x,"ex"])
        if len(g)<30: return pd.Series(dict(n=len(g)))
        s,ic,rv,p,se=stats.linregress(g[x],g["ex"])
        return pd.Series(dict(n=len(g),slope=s,t=s/se,mean_ex=g["ex"].mean()))
    out={}
    out["all fc"]=slope(d)
    out["all depth"]=slope(d,"depth")
    out["by coin"]=d.groupby("coin").apply(slope)
    out["by year"]=d.groupby("year").apply(slope)
    out["by window"]=d.groupby("w").apply(slope)
    d["q"]=pd.qcut(d["depth"].rank(method="first"),5,labels=False)
    out["depth quintile"]=d.groupby("q").agg(n=("ex","size"),depth=("depth","mean"),ex=("ex","mean"),
        t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x))),fwd=("fwd","mean"))
    d["trend"]=np.where(d.tr60>0.1,"rising",np.where(d.tr60<-0.1,"falling","choppy"))
    d.loc[d.tr60.isna(),"trend"]="na"
    d["agit"]=np.where(d.agr>1,"agit",np.where(d.agr.notna(),"calm","na"))
    out["by trend"]=d.groupby("trend").apply(slope)
    out["by trend agit"]=d.groupby(["trend","agit"]).apply(slope)
    d["tq"]=pd.qcut(d["tr60"],4,labels=False)
    out["by trend quartile"]=d.groupby("tq").apply(slope)
    out["fc=0 share"]=float((d.fc==0).mean())
    return out
