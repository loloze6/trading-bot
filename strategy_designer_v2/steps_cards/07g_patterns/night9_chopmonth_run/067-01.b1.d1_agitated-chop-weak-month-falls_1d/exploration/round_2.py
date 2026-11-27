def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for H in [1,3,7]:
            allr=[]
            for w,b in ws.items():
                c=b["close"].values
                for i in range(0,len(c)-H,H): allr.append(c[i+H]/c[i]-1)
            drift=np.mean(allr); sd=np.std(allr,ddof=1)
            for w,b in ws.items():
                b=b.reset_index(drop=True)
                c=b["close"].values;hi=b["high"].values;lo=b["low"].values;n=len(c)
                ts=pd.to_datetime(b["timestamp"])
                for i in range(0,n-H,H):
                    fwd=c[i+H]/c[i]-1
                    r60=c[i]/c[i-60]-1 if i>=60 else np.nan
                    rng=(hi[i]-lo[i])/c[i]
                    rows.append(dict(H=H,coin=coin,w=w,day=ts[i].date(),yr=ts[i].year,wd=ts[i].weekday(),
                      reg=b["regime"].iloc[i],z=(fwd-drift)/sd,ex=fwd-drift,
                      clpos=(c[i]-lo[i])/(hi[i]-lo[i])-0.5 if hi[i]>lo[i] else np.nan,
                      r1=c[i]/c[i-1]-1 if i>=1 else np.nan,rng=rng,
                      tr=("rise" if r60>0.1 else "fall" if r60<-0.1 else "chop") if r60==r60 else "na"))
    d=pd.DataFrame(rows)
    def cl(df,x):
        df=df.dropna(subset=[x,"z"])
        if len(df)<30: return pd.Series(dict(n=len(df)))
        xm=df[x]-df[x].mean()
        b=(xm*df["z"]).sum()/(xm**2).sum()
        e=df["z"]-df["z"].mean()-b*xm
        g=(xm*e).groupby(df["day"]).sum()
        se=np.sqrt((g**2).sum())/(xm**2).sum()
        return pd.Series(dict(n=len(df),days=df["day"].nunique(),slope=b,t_day=b/se))
    out={}
    res={}
    for H in [1,3,7]:
        s=d[d.H==H]
        for x in ["clpos","r1"]:
            res[(H,x,"all")]=cl(s,x)
            for tr in ["rise","chop","fall"]: res[(H,x,tr)]=cl(s[s.tr==tr],x)
            for y in sorted(s.yr.unique()): res[(H,x,y)]=cl(s[s.yr==y],x)
            res[(H,x,"wideday")]=cl(s[s.rng>s.groupby("coin")["rng"].transform("median")],x)
            res[(H,x,"narrowday")]=cl(s[s.rng<=s.groupby("coin")["rng"].transform("median")],x)
    out["clustered slopes"]=pd.DataFrame(res).T
    s=d[d.H==1]
    g=s.groupby(["wd","day"])["ex"].mean().groupby("wd")
    out["next-day excess by weekday of signal day (day means)"]=pd.DataFrame(dict(mean=g.mean(),n=g.size(),t=g.mean()/g.std()*np.sqrt(g.size())))
    s7=d[d.H==7]
    out["7d weekday x window count"]=s7.groupby("wd")["w"].nunique()
    out["coins: clpos 7d slope"]=pd.DataFrame({c:cl(s7[s7.coin==c],"clpos") for c in s7.coin.unique()}).T
    return out
