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
            n=len(c)
            for t in range(1,n-1):
                if not c[t]>c[t-1]: continue
                k=0; j=t-1
                while j>=1 and c[j]<c[j-1] and k<30:
                    k+=1; j-=1
                if k<2: continue
                loss=c[t-1]/c[j]-1
                r=c[t+1]/c[t]-1
                up=c[t]/c[t-1]-1
                tr=c[t]/c[t-60]-1 if t>=60 else np.nan
                rows.append(dict(coin=coin,w=w,year=ts.iloc[t].year,day=ts.iloc[t].normalize(),
                    k=k,loss=loss,up=up,r=r,ex=-(r-mu),tot=-r,f=f[t],tr=tr))
    d=pd.DataFrame(rows)
    def summ(g):
        s=g.groupby("day")["ex"].sum()
        return pd.Series(dict(n=len(g),mean_ex=g.ex.mean(),mean_tot=g.tot.mean(),
            t_day=s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s)>2 else np.nan))
    out={}
    out["all"]=summ(d)
    d["dq"]=d.groupby("coin")["loss"].transform(lambda x: pd.qcut(-x,5,labels=False,duplicates="drop"))
    out["by_depth_quintile(4=deepest)"]=d.groupby("dq").apply(summ)
    d["kk"]=d.k.clip(upper=5)
    out["by_runlen"]=d.groupby("kk").apply(summ)
    out["by_coin"]=d.groupby("coin").apply(summ)
    out["by_window"]=d.groupby("w").apply(summ)
    d["trend"]=pd.cut(d.tr,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    out["by_trend60"]=d.groupby("trend").apply(summ)
    d["uq"]=d.groupby("coin")["up"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["by_upday_tercile"]=d.groupby("uq").apply(summ)
    out["forecast_zero_share"]=float((d.f==0).mean())
    ev=d[d.f<0]
    med=ev.f.abs().median()
    a=ev[ev.f.abs()>med].ex; b_=ev[ev.f.abs()<=med].ex
    out["fc_split"]=pd.Series(dict(n_ev=len(ev),deep=a.mean(),shallow=b_.mean(),welch=stats.ttest_ind(a,b_,equal_var=False).statistic))
    out["spearman_depth_ex"]=pd.Series(stats.spearmanr(-d.loss,d.ex))
    out["spearman_up_ex"]=pd.Series(stats.spearmanr(d.up,d.ex))
    return out
