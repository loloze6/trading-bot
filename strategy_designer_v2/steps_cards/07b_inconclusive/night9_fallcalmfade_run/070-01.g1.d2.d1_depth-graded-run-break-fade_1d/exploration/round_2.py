def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            c=b["close"].values.astype(float)
            allr.append(c[1:]/c[:-1]-1)
        mu=np.nanmean(np.concatenate(allr))
        for w,b in wins.items():
            c=b["close"].values.astype(float)
            f=b["forecast"].values.astype(float)
            ts=pd.to_datetime(b["timestamp"])
            dr=pd.Series(c).pct_change()
            s30=dr.rolling(30).std()
            n=len(c)
            for t in range(1,n-1):
                if not c[t]>c[t-1]: continue
                k=0; j=t-1
                while j>=1 and c[j]<c[j-1] and k<30:
                    k+=1; j-=1
                if k<2: continue
                loss=c[t-1]/c[j]-1
                r=c[t+1]/c[t]-1
                tr=c[t]/c[t-60]-1 if t>=60 else np.nan
                # agitation within window (approx: current 30d vol vs window's median of past 30d vols up to t)
                past=s30.iloc[:t+1].dropna()
                ag=(s30.iloc[t]>past.median()) if len(past)>=60 else np.nan
                rows.append(dict(coin=coin,w=w,year=ts.iloc[t].year,day=ts.iloc[t].normalize(),
                    k=k,loss=loss,r=r,ex=-(r-mu),f=f[t],tr=tr,ag=ag,
                    lossz=loss/s30.iloc[t] if s30.iloc[t]>0 else np.nan))
    d=pd.DataFrame(rows)
    def summ(g):
        s=g.groupby("day")["ex"].sum()
        return pd.Series(dict(n=len(g),mean_ex=g.ex.mean(),
            t_day=s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s)>2 else np.nan))
    out={}
    out["forecast_desc"]=d.f.describe()
    out["share_f_eq_-20"]=float((d.f<=-19.99).mean())
    out["share_f_eq_median"]=float((d.f==d.f.median()).mean())
    d["dq"]=d.groupby("coin")["loss"].transform(lambda x: pd.qcut(-x,2,labels=False))
    out["depth_half_split"]=d.groupby("dq").apply(summ)
    a=d[d.dq==1].ex;b=d[d.dq==0].ex
    out["deep_minus_shallow_welch"]=pd.Series(dict(diff=a.mean()-b.mean(),t=stats.ttest_ind(a,b,equal_var=False).statistic))
    d["trend"]=pd.cut(d.tr,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    out["trend_x_depthhalf"]=d.groupby(["trend","dq"]).apply(summ)
    out["trend_x_ag"]=d.groupby(["trend","ag"]).apply(summ)
    d["zq"]=d.groupby("coin")["lossz"].transform(lambda x: pd.qcut(-x,5,labels=False,duplicates="drop"))
    out["by_vol_scaled_depth_q"]=d.groupby("zq").apply(summ)
    out["by_year"]=d.groupby("year").apply(summ)
    out["deep_q_by_year"]=d[d.groupby("coin")["loss"].transform(lambda x: x<=x.quantile(0.4))].groupby("year").apply(summ)
    return out
