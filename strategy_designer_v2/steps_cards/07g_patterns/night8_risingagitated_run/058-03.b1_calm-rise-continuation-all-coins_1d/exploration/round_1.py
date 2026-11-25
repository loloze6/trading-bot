import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sma=c.rolling(20).mean()
            dist=c/sma-1
            tr60=c/c.shift(60)-1
            vol30=r1.rolling(30).std()
            ret5p=c/c.shift(5)-1
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            inprof=(b["regime"]=="unknown")
            day=pd.to_datetime(b["timestamp"]).dt.floor("D")
            df=pd.DataFrame(dict(coin=coin,w=w,pos=np.arange(len(b)),dist=dist,tr60=tr60,vol30=vol30,
                ret5p=ret5p,f5=f5,f1=f1,r1=r1,inprof=inprof,day=day,wd=day.dt.weekday))
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["volrel"]=A["vol30"]/A.groupby("coin")["vol30"].transform("median")
    G=A[(A.pos%5==0)&A.f5.notna()].copy()
    G["ex5"]=G.f5-G.groupby("coin")["f5"].transform("mean")
    D=A[A.f1.notna()].copy()
    D["ex1"]=D.f1-D.groupby("coin")["f1"].transform("mean")
    def ct(df,col):
        m=df[col].mean()
        dev=(df[col]-m).groupby(df["day"]).sum()
        se=np.sqrt((dev**2).sum())/len(df)
        return pd.Series(dict(n=len(df),days=df.day.nunique(),mean=m,t=m/se if se>0 else np.nan))
    def slope(d):
        if len(d)<30: return pd.Series(dict(n=len(d),days=np.nan,slope=np.nan,t=np.nan,meanex=np.nan))
        x=d.dist; y=d.ex5
        bb=np.polyfit(x,y,1)[0]
        res=y-(y.mean()+bb*(x-x.mean()))
        sc=((x-x.mean())*res).groupby(d.day).sum()
        se=np.sqrt((sc**2).sum())/((x-x.mean())**2).sum()
        return pd.Series(dict(n=len(d),days=d.day.nunique(),slope=bb,t=bb/se,meanex=y.mean()))
    out={}
    Gd=G.dropna(subset=["dist"]).copy()
    Gd["dq"]=pd.qcut(Gd.dist,5,labels=False)
    out["ex5 by dist quintile x inprof"]=Gd.groupby(["inprof","dq"]).apply(lambda d:ct(d,"ex5"))
    G["trend"]=pd.cut(G.tr60,[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    G["agit"]=np.where(G.volrel>1,"agit","calm")
    G2=G.dropna(subset=["trend","dist","volrel"])
    out["slope ex5 on dist by trend x agit"]=G2.groupby(["trend","agit"]).apply(slope)
    out["slope ex5 on dist by inprof"]=G.dropna(subset=["dist"]).groupby("inprof").apply(slope)
    D["z"]=D.r1/D.vol30
    D["zq"]=pd.cut(D.z,[-99,-2,-1,0,1,2,99])
    out["ex1 after daily z"]=D.dropna(subset=["z"]).groupby("zq").apply(lambda d:ct(d,"ex1"))
    G["zq5"]=pd.cut(G.ret5p/(G.vol30*np.sqrt(5)),[-99,-1.5,-0.5,0.5,1.5,99])
    out["ex5 after 5d z"]=G.dropna(subset=["zq5"]).groupby("zq5").apply(lambda d:ct(d,"ex5"))
    out["ex1 by weekday"]=D.groupby("wd").apply(lambda d:ct(d,"ex1"))
    Gv=G.dropna(subset=["volrel"]).copy()
    Gv["vq"]=pd.qcut(Gv.volrel,4,labels=False)
    out["ex5 by volrel quartile"]=Gv.groupby("vq").apply(lambda d:ct(d,"ex5"))
    return out
