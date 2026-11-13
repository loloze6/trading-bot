def explore(data):
    import pandas as pd, numpy as np
    H=10
    rows=[]
    bars=data["bars"]
    for coin in bars:
        for w,df in bars[coin].items():
            df=df.reset_index(drop=True)
            c=df["close"].values; n=len(c)
            fc=df["forecast"].values
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(0,n-H,H):
                r=c[i+H]/c[i]-1
                p10=c[i]/c[i-10]-1 if i>=10 else np.nan
                p20=c[i]/c[i-20]-1 if i>=20 else np.nan
                rv=np.std(np.diff(np.log(c[max(0,i-20):i+1]))) if i>=10 else np.nan
                rows.append(dict(coin=coin,w=w,yr=yr[i],f=fc[i],r=r,p10=p10,p20=p20,rv=rv,ts=str(df["timestamp"].iloc[i])))
    d=pd.DataFrame(rows)
    d["hold"]=d.groupby("coin")["r"].transform("mean")
    d["ex"]=d["r"]-d["hold"]
    def summ(g):
        x=g["ex"].dropna()
        if len(x)<3: return pd.Series(dict(n=len(x),mean=x.mean() if len(x) else np.nan,hit=np.nan,t=np.nan,t_dateclust=np.nan,ndates=g.ts.nunique()))
        cm=g.groupby("ts")["ex"].mean()
        tc=cm.mean()/cm.std()*np.sqrt(len(cm)) if len(cm)>2 else np.nan
        return pd.Series(dict(n=len(x),mean=x.mean(),hit=(x>0).mean(),t=x.mean()/x.std()*np.sqrt(len(x)),t_dateclust=tc,ndates=len(cm)))
    out={}
    act=d[d.f>0].copy()
    act["p10b"]=pd.cut(act["p10"],[-1,-0.25,-0.15,-0.08,0,10])
    out["active_by_p10"]=act.groupby("p10b").apply(summ)
    allb=d.copy()
    allb["p10b"]=pd.cut(allb["p10"],[-1,-0.25,-0.15,-0.08,0,10])
    out["inactive_by_p10"]=allb[allb.f==0].groupby("p10b").apply(summ)
    s=d[d.f>=5].copy()
    s["crash"]=np.where(s.p10<=-0.15,"fell>=15%","other")
    out["deep_crash"]=s.groupby("crash").apply(summ)
    cr=s[s.p10<=-0.15]
    out["deep_crash_by_coin"]=cr.groupby("coin").apply(summ)
    out["deep_crash_by_year"]=cr.groupby("yr").apply(summ)
    act2=d[d.f>0]
    a2=act2[act2.p10<=-0.15]
    out["active_crash_by_year"]=a2.groupby("yr").apply(summ)
    out["active_crash_by_coin"]=a2.groupby("coin").apply(summ)
    out["deep_all_dateclust"]=summ(s)
    s["rvb"]=pd.qcut(s["rv"],3,labels=["calm","mid","wild"])
    out["deep_wild_x_crash"]=s.groupby(["rvb","crash"]).apply(summ)
    return out
