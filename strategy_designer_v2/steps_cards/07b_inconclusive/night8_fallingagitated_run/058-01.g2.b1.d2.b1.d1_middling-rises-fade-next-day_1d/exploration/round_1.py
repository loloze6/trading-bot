def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna().values)
        drift=np.concatenate(allr).mean() if allr else 0
        for w,b in ws.items():
            c=pd.Series(b["close"].astype(float).values)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z1=r/sd
            r3=c/c.shift(3)-1
            z3=r3/(sd*np.sqrt(3))
            nxt=c.shift(-1)/c-1
            nxt3=c.shift(-3)/c-1
            reg=b["regime"].values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            df=pd.DataFrame({"coin":coin,"w":w,"yr":yr,"reg":reg,"z1":z1,"z3":z3,
                             "u1":-(nxt-drift),"u3":-(nxt3-3*drift),"ts":pd.to_datetime(b["timestamp"]).dt.floor("D").values,
                             "fc":b["forecast"].values})
            rows.append(df)
    d=pd.concat(rows)
    out={}
    out["regime counts"]=d["reg"].value_counts()
    ip=d[d.reg=="unknown"].dropna(subset=["z1","u1"])
    def summ(g,col="u1"):
        x=g[col].dropna()
        pd_=g.groupby("ts")[col].sum()
        n=len(x); G=len(pd_)
        m=x.mean()
        dev=g.groupby("ts")[col].apply(lambda s:(s-m).sum())
        se=np.sqrt((dev**2).sum()*G/(G-1))/n if G>1 else np.nan
        return pd.Series({"n":n,"days":G,"mean":m,"t_day":m/se if se else np.nan})
    bins=[-np.inf,-1,0,0.5,1,1.5,2,3,np.inf]
    ip["zb"]=pd.cut(ip.z1,bins)
    out["in-profile by 1d z, next-day short unusual"]=ip.groupby("zb").apply(summ)
    ip3=ip.dropna(subset=["z3","u3"]).copy()
    # non-overlap grid on 3-day horizon approximation: take every 3rd row
    ip3["zb3"]=pd.cut(ip3.z3,bins)
    out["in-profile by 3d z, next-3day short unusual"]=ip3.groupby("zb3").apply(lambda g:summ(g,"u3"))
    out["in-profile by 3d z, next-day short unusual"]=ip3.groupby("zb3").apply(lambda g:summ(g,"u1"))
    up=ip[ip.z1>0]
    out["up days in-profile by year"]=up.groupby("yr").apply(summ)
    out["up days in-profile by coin"]=up.groupby("coin").apply(summ)
    out["corr z1 vs u1 on up days"]=float(np.corrcoef(up.z1,up.u1)[0,1])
    out["spearman z1 u1 up"]=float(up[["z1","u1"]].corr("spearman").iloc[0,1])
    op=d[(d.reg!="unknown")].dropna(subset=["z1","u1"]).copy()
    op["zb"]=pd.cut(op.z1,bins)
    out["out-of-profile by 1d z"]=op.groupby("zb").apply(summ)
    return out
