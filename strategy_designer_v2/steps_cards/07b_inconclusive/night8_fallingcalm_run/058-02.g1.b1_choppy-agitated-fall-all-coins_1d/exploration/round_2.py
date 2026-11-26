import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    h=5
    rows=[]
    for coin in bars:
        rs=[]
        for w,df in bars[coin].items():
            c=df["close"].values
            for i in range(0,len(c)-h,h): rs.append(c[i+h]/c[i]-1)
        m=np.mean(rs); s=np.std(rs)
        for w,df in bars[coin].items():
            df=df.reset_index(drop=True)
            c=pd.Series(df["close"].values); v=pd.Series(df["volume"].values)
            f=df["forecast"].values
            ts=pd.to_datetime(df["timestamp"])
            r60=c.pct_change(60).values; r5=c.pct_change(5).values; r30=c.pct_change(30).values
            vr=(v.rolling(30).mean()/v.rolling(90,min_periods=45).mean()).values
            vr5=(v.rolling(5).mean()/v.rolling(30).mean()).values
            for i in range(0,len(c)-h,h):
                if f[i]<0:
                    rows.append(dict(coin=coin,w=w,year=ts[i].year,f=f[i],r60=r60[i],r5=r5[i],r30=r30[i],
                        vr=vr[i],vr5=vr5[i],ex=-(c[i+h]/c[i]-1-m),day=ts[i].normalize()))
    d=pd.DataFrame(rows)
    def summ(g):
        x=g["ex"]; n=len(x); wt=g["f"].abs()
        wm=(x*wt).sum()/wt.sum()
        dev=(wt*(x-wm)).groupby(g["day"]).sum(); D=len(dev)
        se=np.sqrt((dev**2).sum()*D/max(D-1,1))/wt.sum()
        return pd.Series(dict(n=n,days=D,mean_ex=x.mean(),wmean=wm,t_day=wm/se if se>0 else np.nan))
    out={}
    out["all"]=summ(d).to_frame().T
    out["corr_absf_ex"]=float(np.corrcoef(d.f.abs(),d.ex)[0,1])
    d["trend_half"]=np.where(d.r60<0,"r60<0",np.where(d.r60>=0,"r60>=0","na"))
    out["by_r60_side"]=d.groupby("trend_half").apply(summ)
    d["last5"]=np.where(d.r5<0,"still_falling_5d","bounced_5d")
    out["by_last5"]=d.groupby("last5").apply(summ)
    dv=d.dropna(subset=["vr"]).copy()
    dv["vq"]=pd.qcut(dv.vr.rank(method="first"),3,labels=["quiet","mid","heavy"])
    out["by_vol30"]=dv.groupby("vq").apply(summ)
    out["vol_x_depth_corr"]=dv.groupby("vq").apply(lambda g: pd.Series(dict(corr=np.corrcoef(g.f.abs(),g.ex)[0,1],n=len(g))))
    out["by_year"]=d.groupby("year").apply(summ)
    return out
