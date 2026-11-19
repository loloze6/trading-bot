def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values.astype(float)
            ts=pd.to_datetime(df["timestamp"])
            hrs=ts.dt.hour.values
            n=len(c)
            for t in np.where(hrs==20)[0]:
                if t<24 or t+2>=n: continue
                if (ts.iloc[t+2]-ts.iloc[t]).total_seconds()!=7200: continue
                rows.append(dict(coin=coin,year=ts.iloc[t].year,wd=ts.iloc[t].weekday(),
                                 p24=c[t]/c[t-24]-1,p72=(c[t]/c[t-72]-1) if t>=72 else np.nan,
                                 f2=c[t+2]/c[t]-1,f6=(c[t+6]/c[t]-1) if t+6<n else np.nan,
                                 f24=(c[t+24]/c[t]-1) if t+24<n else np.nan))
    g=pd.DataFrame(rows)
    out={}
    def q(d,col,val,k=5):
        d=d.dropna(subset=[col,val]).copy()
        d["q"]=d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),k,labels=False))
        a=d.groupby("q")[val].agg(["mean","std","count"]);a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a
    def wel(d,col,val):
        d=d.dropna(subset=[col,val])
        r=d.groupby("coin")[col].transform(lambda x:x.rank(pct=True))
        a=d.loc[r<=0.5,val];b=d.loc[r>0.5,val]
        return pd.Series({"low_minus_high":a.mean()-b.mean(),"t":stats.ttest_ind(a,b,equal_var=False).statistic,"n":len(d)})
    out["2h from 21UTC overall"]=g[["f2","f6","f24"]].agg(["mean","std","count"])
    out["f2 by p24 quintile"]=q(g,"p24","f2")
    out["f2 by p72 quintile"]=q(g,"p72","f2")
    out["f2 low-high p24 by coin"]=g.groupby("coin").apply(lambda d: wel(d,"p24","f2"))
    out["f2 low-high p24 by year"]=g.groupby("year").apply(lambda d: wel(d,"p24","f2"))
    out["f2 low-high p24 pooled"]=wel(g,"p24","f2").to_frame()
    out["f6 low-high p24 pooled"]=wel(g,"p24","f6").to_frame()
    out["f24 low-high p24 pooled"]=wel(g,"p24","f24").to_frame()
    out["f2 by year"]=g.groupby("year")["f2"].agg(["mean","count"])
    sp=g.dropna(subset=["p24","f2"])
    out["spearman p24 f2 by coin"]=sp.groupby("coin").apply(lambda d: pd.Series(stats.spearmanr(d.p24,d.f2),index=["rho","p"]))
    return out
