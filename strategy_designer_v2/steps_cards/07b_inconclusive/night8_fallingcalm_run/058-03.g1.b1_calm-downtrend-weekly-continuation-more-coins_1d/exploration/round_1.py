import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=5
    rows=[]
    coinmean={}
    for coin,ws in data["bars"].items():
        allr=[]
        for w,df in ws.items():
            c=df["close"].values
            for i in range(0,len(c)-H,H):
                allr.append(c[i+H]/c[i]-1)
        coinmean[coin]=np.mean(allr) if allr else np.nan
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"]; v=df["volume"]
            past=c/c.shift(5)-1
            fwd=c.shift(-H)/c-1
            vr=v.rolling(5).mean()/v.rolling(60,min_periods=20).mean()
            ts=pd.to_datetime(df["timestamp"])
            for i in range(0,len(df)-H,H):
                f=df["forecast"].iat[i]
                if df["regime"].iat[i]!="unknown" or pd.isna(f) or f==0: continue
                rows.append(dict(coin=coin,w=w,year=ts.iat[i].year,day=ts.iat[i].normalize(),
                    f=f/10,past=past.iat[i],fwd=fwd.iat[i]-coinmean[coin],fraw=fwd.iat[i],vr=vr.iat[i]))
    d=pd.DataFrame(rows).dropna(subset=["fwd"])
    def slope(g):
        g=g.dropna(subset=["f","fwd"])
        if len(g)<10: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan,mean_dir=np.nan))
        X=np.c_[np.ones(len(g)),g.f.values]; y=g.fwd.values
        b,_,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b
        XtXi=np.linalg.inv(X.T@X)
        sc=pd.DataFrame(X*e[:,None]).groupby(g.day.values).sum().values
        G=len(sc); V=XtXi@(sc.T@sc)@XtXi*G/max(G-1,1)
        md=(np.sign(g.f)*g.fwd)
        return pd.Series(dict(n=len(g),days=G,slope=b[1],t=b[1]/np.sqrt(V[1,1]),mean_dir=md.mean(),t_dir=md.mean()/md.std()*np.sqrt(len(md))))
    out={}
    out["all"]=slope(d).to_frame().T
    d["side"]=np.where(d.f>0,"long","short")
    out["by_side"]=d.groupby("side").apply(slope)
    out["by_coin"]=d.groupby("coin").apply(slope)
    out["by_year"]=d.groupby("year").apply(slope)
    d["fq"]=pd.qcut(d.f.abs(),4,labels=False)
    out["by_absf_quartile_side"]=d.groupby(["side","fq"]).apply(slope)
    d["vq"]=pd.qcut(d.vr,3,labels=False)
    out["by_volume_tercile_side"]=d.groupby(["side","vq"]).apply(slope)
    d["pq"]=pd.qcut(d.past,5,labels=False)
    out["fwd_by_past_quintile"]=d.groupby("pq").agg(n=("fwd","size"),past=("past","mean"),fwd_excess=("fwd","mean"),fraw=("fraw","mean"))
    return out
