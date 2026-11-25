def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            sdy=sd.rolling(365,min_periods=120).median()
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b))})
            df["z1"]=r/sd
            df["z3"]=(c/c.shift(3)-1)/(sd*np.sqrt(3))
            df["z5"]=(c/c.shift(5)-1)/(sd*np.sqrt(5))
            df["ret60"]=c/c.shift(60)-1
            df["agit"]=(sd>sdy).astype(float).where(sdy.notna())
            df["f3"]=c.shift(-3)/c-1
            df["f5"]=c.shift(-5)/c-1
            df["usd3"]=np.nan
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            df["rangez"]=(rng/c.shift(1))/sd
            df["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            df["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            df["f1"]=c.shift(-1)/c-1
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["trend"]=np.where(A.ret60>0.1,"rising",np.where(A.ret60<-0.1,"falling","choppy"))
    A.loc[A.ret60.isna(),"trend"]=np.nan
    out={}
    def clslope(D,x,y):
        d=D.dropna(subset=[x,y]).copy()
        drift=d[y].mean()
        X=d[x]-d[x].mean(); Y=d[y]-drift
        b=(X*Y).sum()/(X*X).sum()
        e=Y-b*X
        s=(X*e).groupby(d["day"]).sum()
        D_=len(s)
        se=np.sqrt((s**2).sum()*D_/(D_-1))/(X*X).sum()
        return pd.Series({"slope%":b*100,"t_cl":b/se,"n":len(d),"days":D_})
    res={}
    for h,g in [("f3",3),("f5",5)]:
        G=A[A.pos%g==0]
        for k in ["z1","z3","z5","rangez"]:
            for tr in ["rising","choppy","falling"]:
                res[f"{h}_{k}_{tr}"]=clslope(G[G.trend==tr],k,h)
            res[f"{h}_{k}_all"]=clslope(G,k,h)
    out["clustered slopes"]=pd.DataFrame(res).T.round(3)
    # z3 momentum by window (non-falling), f3
    G=A[(A.pos%3==0)&(A.trend!="falling")&A.trend.notna()]
    out["z3->f3 notfalling by window"]=G.groupby("w").apply(lambda d:clslope(d,"z3","f3")).round(3)
    G=A[(A.pos%3==0)&A.trend.notna()]
    out["z3->f3 by agitation"]=G.groupby("agit").apply(lambda d:clslope(d,"z3","f3")).round(3)
    out["z3->f3 by coin"]=G.groupby("coin").apply(lambda d:clslope(d,"z3","f3")).round(3)
    # f5 by z1 all clustered big up days
    G5=A[A.pos%5==0].dropna(subset=["z1","f5"])
    dr=G5.f5.mean()
    def clmean(d):
        s=(d.f5-dr).groupby(d.day).sum(); D_=len(s)
        se=np.sqrt(((s-s.mean()*0)**2).sum()*D_/(D_-1))/len(d) if D_>1 else np.nan
        return pd.Series({"ex%":(d.f5-dr).mean()*100,"t_cl":(d.f5-dr).mean()/se,"n":len(d),"days":D_})
    out["f5 by z1 clustered"]=G5.groupby(pd.cut(G5.z1,[-99,-2,-1,0,1,2,99]),observed=True).apply(clmean).round(3)
    # weekday by day-level mean of coins
    dm=A.groupby(["w","day"]).agg(f1=("f1","mean"),wd=("wd","first")).dropna()
    m=dm.f1.mean()
    out["weekday day-avg f1"]=dm.groupby("wd").f1.agg(lambda x:pd.Series({"ex%":(x-m).mean()*100,"t":(x-m).mean()/(x.std()/np.sqrt(len(x)))}).values.tolist()).apply(pd.Series).rename(columns={0:"ex%",1:"t"}).round(3)
    return out
