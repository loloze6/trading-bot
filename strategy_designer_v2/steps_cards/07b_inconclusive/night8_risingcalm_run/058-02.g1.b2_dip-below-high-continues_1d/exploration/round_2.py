def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    def build(H):
        rows=[]
        for coin,ws in data["bars"].items():
            for w,b in ws.items():
                b=b.reset_index(drop=True)
                c=b["close"].astype(float)
                r=c.pct_change()
                hi=c.rolling(5,min_periods=5).max()
                sd=r.rolling(30,min_periods=20).std()
                depth=(c-hi)/hi/sd
                fwd=c.shift(-H)/c-1
                ret5=c/c.shift(5)-1
                for i in range(0,len(b),H):
                    if pd.isna(fwd.iloc[i]): continue
                    rows.append(dict(coin=coin,w=w,day=str(b["timestamp"].iloc[i])[:10],
                        fc=b["forecast"].iloc[i],depth=depth.iloc[i],fwd=fwd.iloc[i],ret5s=ret5.iloc[i]/sd.iloc[i] if sd.iloc[i]>0 else np.nan))
        d=pd.DataFrame(rows)
        d["ex"]=d["fwd"]-d["coin"].map(d.groupby("coin")["fwd"].mean())
        return d
    def cl(g,x="fc"):
        g=g.dropna(subset=[x,"ex"])
        if len(g)<30: return pd.Series(dict(n=len(g)))
        X=g[x].values; y=g["ex"].values
        Xm=X-X.mean(); s=(Xm*(y-y.mean())).sum()/(Xm**2).sum()
        e=y-y.mean()-s*Xm
        sc=pd.Series(Xm*e).groupby(g["day"].values).sum()
        G=len(sc); n=len(g)
        v=(sc**2).sum()/(Xm**2).sum()**2*G/(G-1)*(n-1)/(n-2)
        return pd.Series(dict(n=n,days=G,slope=s,t_cl=s/np.sqrt(v)))
    out={}
    for H in [1,3,5,10]:
        d=build(H)
        out[f"H{H} fc clustered"]=cl(d)
        out[f"H{H} ret5s clustered"]=cl(d,"ret5s")
    d=build(5)
    out["H5 fc<0 only"]=cl(d[d.fc<0])
    out["H5 by coin clustered"]=d.groupby("coin").apply(cl)
    d["q"]=pd.qcut(d["fc"].rank(method="first"),5,labels=False)
    def mt(x):
        return x.mean()/x.std()*np.sqrt(len(x))
    out["fc quintile"]=d.groupby("q").agg(n=("ex","size"),fc=("fc","mean"),ex=("ex","mean"),t=("ex",mt))
    # day-clustered mean of extremes
    def daymean(s,days):
        ds=s.groupby(days).sum(); return s.mean(), s.mean()/(np.sqrt((( s.groupby(days).sum()-s.groupby(days).size()*s.mean())**2).sum())/len(s))
    for q in [0,4]:
        g=d[d.q==q]; m,t=daymean(g["ex"],g["day"]); out[f"q{q} mean ex day-cl t"]=pd.Series(dict(mean=m,t=t,days=g.day.nunique()))
    return out
