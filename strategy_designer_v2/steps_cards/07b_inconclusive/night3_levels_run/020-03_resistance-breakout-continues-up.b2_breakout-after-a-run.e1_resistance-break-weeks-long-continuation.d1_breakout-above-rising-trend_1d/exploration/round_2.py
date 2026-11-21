def explore(data):
    import numpy as np, pandas as pd
    H=20
    bars=data["bars"]
    drift={}
    for c in bars:
        rs=[]
        for w,df in bars[c].items():
            cl=df["close"].values
            for i in range(0,len(cl)-H,H):
                rs.append(cl[i+H]/cl[i]-1)
        drift[c]=np.mean(rs)
    rows=[]; base=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            cl=df["close"].values; f=df["forecast"].fillna(0).values; n=len(df)
            s=pd.Series(cl)
            sma=s.rolling(50).mean().values
            smaslope=(s.rolling(50).mean()/s.rolling(50).mean().shift(20)-1).values
            r90=(s/s.shift(90)-1).values
            r20p=(s/s.shift(20)-1).values
            yrs=pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(0,n-H,H):
                if not np.isnan(sma[i]) and cl[i]>sma[i]:
                    base.append(dict(coin=c,yr=yrs[i],ma=(cl[i]/sma[i]-1)*100,slope=smaslope[i],r20p=r20p[i],u=cl[i+H]/cl[i]-1-drift[c]))
            low=0.0; taken=set()
            for i in range(n):
                if f[i]<=0:
                    low=0.0; continue
                low=min(low,f[i])
                if f[i]-low>=2:
                    cell=i//H
                    if cell not in taken and i+H<n:
                        taken.add(cell)
                        rows.append(dict(coin=c,yr=yrs[i],f=f[i],ma=(cl[i]/sma[i]-1)*100 if not np.isnan(sma[i]) else np.nan,
                          slope=smaslope[i],r90=r90[i],r20p=r20p[i],u=cl[i+H]/cl[i]-1-drift[c]))
                    low=f[i]
    d=pd.DataFrame(rows); b=pd.DataFrame(base)
    def summ(x):
        x=x.dropna(); return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,med=x.median()))
    out={}
    out["cases_ex2018"]=summ(d[d.yr!=2018].u)
    out["base_above_all"]=summ(b.u)
    out["base_ex2018"]=summ(b[b.yr!=2018].u)
    bins=[-1,2,5,10,20,1000]
    d["mab"]=pd.cut(d.ma,bins); b["mab"]=pd.cut(b.ma,bins)
    out["cases_by_ma"]=d.groupby("mab").u.apply(summ).unstack()
    out["base_by_ma"]=b.groupby("mab").u.apply(summ).unstack()
    d["sl"]=pd.qcut(d.slope.rank(method="first"),3,labels=False)
    out["cases_by_smaslope_tercile"]=d.groupby("sl").agg(med_slope=("slope","median")).join(d.groupby("sl").u.apply(summ).unstack())
    d["r9"]=pd.qcut(d.r90.rank(method="first"),3,labels=False)
    out["cases_by_r90_tercile"]=d.groupby("r9").agg(med=("r90","median")).join(d.groupby("r9").u.apply(summ).unstack())
    d["rp"]=pd.qcut(d.r20p.rank(method="first"),3,labels=False)
    out["cases_by_prior20_tercile"]=d.groupby("rp").agg(med=("r20p","median")).join(d.groupby("rp").u.apply(summ).unstack())
    out["year_counts_base"]=b.groupby("yr").u.apply(summ).unstack()
    return out
