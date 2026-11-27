import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w, b in wins.items():
            c=b["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        drift=np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values
            n=len(c)
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            nxt=np.r_[c[1:]/c[:-1]-1, np.nan]
            nxt2=np.r_[c[2:]/c[:-2]-1, np.nan, np.nan]
            run=np.zeros(n); depth=np.zeros(n)
            k=0; cum=0.0
            for i in range(1,n):
                if r[i]<0: k+=1; cum+=np.log1p(r[i])
                else:
                    if r[i]>0: run[i]=k; depth[i]=cum
                    k=0; cum=0.0
            vol=pd.Series(r).rolling(20,min_periods=10).std().values
            tr60=np.r_[[np.nan]*60, c[60:]/c[:-60]-1] if n>60 else np.full(n,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            reg=b["regime"].astype(str).values
            inprof=np.isin(reg,["mean_reversion","unknown"])
            for i in range(1,n):
                rows.append(dict(coin=coin,w=w,t=ts.iloc[i],r=r[i],nx=nxt[i],nx2=nxt2[i],run=run[i],
                    depth=depth[i],vol=vol[i],tr60=tr60[i],inprof=inprof[i],yr=ts.iloc[i].year,drift=drift))
    d=pd.DataFrame(rows)
    d["ex"]=d["nx"]-d["drift"]; d["ex2"]=d["nx2"]-2*d["drift"]
    d["z"]=d["r"]/d["vol"]; d["dz"]=-d["depth"]/(d["vol"]*np.sqrt(d["run"].clip(lower=1)))
    d["dsc"]=-d["depth"]/d["vol"]
    def dt(sub,col="ex"):
        s=sub.dropna(subset=[col])
        if len(s)<5: return pd.Series(dict(n=len(s),days=0,mean=np.nan,t=np.nan))
        g=s.groupby("t")[col].sum(); m=s[col].mean()
        t=g.mean()/(g.std(ddof=1)/np.sqrt(len(g))) if len(g)>2 else np.nan
        return pd.Series(dict(n=len(s),days=len(g),mean=m,t=t))
    out={}
    brk=d[d.run>=1].dropna(subset=["z"]).copy()
    brk["runb"]=brk.run.clip(upper=5)
    # all profiles: by run
    out["breaks_all_by_run"]=brk.groupby("runb").apply(dt)
    out["breaks_all_by_run_h2"]=brk.groupby("runb").apply(lambda s:dt(s,"ex2"))
    # depth of run in vol units, quartiles, all & in profile
    brk["dq"]=pd.qcut(brk["dsc"],4,labels=False,duplicates="drop")
    out["breaks_all_by_depth_q"]=brk.groupby("dq").apply(dt)
    out["breaks_inprof_by_depth_q"]=brk[brk.inprof].groupby("dq").apply(dt)
    out["breaks_outprof_by_depth_q"]=brk[~brk.inprof].groupby("dq").apply(dt)
    # out of profile breaks by trend
    o=brk[~brk.inprof].copy()
    o["trend"]=np.where(o.tr60>0.10,"rising",np.where(o.tr60<-0.10,"falling","choppy"))
    o.loc[o.tr60.isna(),"trend"]="na"
    out["breaks_outprof_by_trend"]=o.groupby("trend").apply(dt)
    # small vs large up day x run (all)
    brk["weak"]=brk.z<brk.z.median()
    brk["long"]=brk.run>=3
    out["breaks_weak_x_long"]=brk.groupby(["weak","long"]).apply(dt)
    # long runs in profile by year and coin
    L=brk[brk.inprof&(brk.run>=4)]
    out["inprof_run4plus_by_year"]=L.groupby("yr").apply(dt)
    out["inprof_run4plus_by_coin"]=L.groupby("coin").apply(dt)
    La=brk[brk.run>=4]
    out["all_run4plus_by_year"]=La.groupby("yr").apply(dt)
    # breaks by year all
    out["breaks_all_by_year"]=brk.groupby("yr").apply(dt)
    # regression slopes
    res={}
    for nm,s in [("all",brk),("in",brk[brk.inprof]),("out",brk[~brk.inprof])]:
        s=s.dropna(subset=["ex","dsc"])
        lr=stats.linregress(s["run"].clip(upper=8),s["ex"]); lr2=stats.linregress(s["dsc"].clip(upper=8),s["ex"])
        res[nm]=dict(slope_run=lr.slope,t_run=lr.slope/lr.stderr,slope_depth=lr2.slope,t_depth=lr2.slope/lr2.stderr,n=len(s))
    out["slopes"]=pd.DataFrame(res).T
    return out
