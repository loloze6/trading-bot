import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sma=c.rolling(20).mean()
            day=pd.to_datetime(b["timestamp"]).dt.floor("D")
            df=pd.DataFrame(dict(coin=coin,w=w,pos=np.arange(len(b)),dist=c/sma-1,tr60=c/c.shift(60)-1,
                vol30=r1.rolling(30).std(),f5=c.shift(-5)/c-1,f3=c.shift(-3)/c-1,f10=c.shift(-10)/c-1,
                day=day,yr=day.dt.year))
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["volrel"]=A["vol30"]/A.groupby("coin")["vol30"].transform("median")
    A["trend"]=pd.cut(A.tr60,[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    A["agit"]=np.where(A.volrel>1,"agit","calm")
    A["dz"]=A.dist/(A.vol30*np.sqrt(20))
    def slope(d,x="dist",y="ex"):
        d=d.dropna(subset=[x,y])
        if len(d)<25: return pd.Series(dict(n=len(d),days=np.nan,slope=np.nan,t=np.nan,meanex=np.nan))
        X=d[x];Y=d[y]
        bb=np.polyfit(X,Y,1)[0]
        res=Y-(Y.mean()+bb*(X-X.mean()))
        sc=((X-X.mean())*res).groupby(d.day).sum()
        se=np.sqrt((sc**2).sum())/((X-X.mean())**2).sum()
        return pd.Series(dict(n=len(d),days=d.day.nunique(),slope=bb,t=bb/se,meanex=Y.mean()))
    def ct(d,col="ex"):
        m=d[col].mean(); dev=(d[col]-m).groupby(d.day).sum(); se=np.sqrt((dev**2).sum())/len(d)
        return pd.Series(dict(n=len(d),days=d.day.nunique(),mean=m,t=m/se))
    out={}
    for h,col in [(3,"f3"),(5,"f5"),(10,"f10")]:
        G=A[(A.pos%h==0)&A[col].notna()].copy()
        G["ex"]=G[col]-G.groupby("coin")[col].transform("mean")
        G=G.dropna(subset=["trend","dist","volrel"])
        G["side"]=np.where(G.dist>0,"above","below")
        out[f"h{h} slope dz by trend x agit"]=G.groupby(["trend","agit"]).apply(lambda d:slope(d,"dz"))
        if h==5:
            G5=G
    cc=G5[(G5.trend!="rise")&(G5.agit=="calm")].copy()
    out["nonrise calm h5 slope by side"]=cc.groupby("side").apply(lambda d:slope(d,"dz"))
    cc["q"]=pd.qcut(cc.dz,4,labels=False)
    out["nonrise calm h5 ex by dz quartile"]=cc.groupby("q").apply(ct)
    out["nonrise calm h5 slope by year"]=cc.groupby("yr").apply(lambda d:slope(d,"dz"))
    out["nonrise calm h5 slope by coin"]=cc.groupby("coin").apply(lambda d:slope(d,"dz"))
    ra=G5[(G5.trend=="rise")&(G5.agit=="agit")].copy()
    ra["q"]=pd.qcut(ra.dz,4,labels=False)
    out["rise agit h5 ex by dz quartile"]=ra.groupby("q").apply(ct)
    return out
