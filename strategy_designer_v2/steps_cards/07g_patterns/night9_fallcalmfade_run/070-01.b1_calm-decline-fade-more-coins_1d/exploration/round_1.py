import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w, b in wins.items():
            c=b["close"].astype(float).values
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            allr.append(r[1:])
        drift=np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values; o=b["open"].astype(float).values
            h=b["high"].astype(float).values; l=b["low"].astype(float).values
            n=len(c)
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            nxt=np.r_[c[1:]/c[:-1]-1, np.nan]
            nxt2=np.r_[c[2:]/c[:-2]-1, np.nan, np.nan]
            nxt3=np.r_[c[3:]/c[:-3]-1, [np.nan]*3]
            run=np.zeros(n); dr=np.zeros(n)
            k=0
            for i in range(1,n):
                if r[i]<0: k+=1; dr[i]=k
                else:
                    run[i]=k if r[i]>0 else 0; k=0
            vol=pd.Series(r).rolling(20,min_periods=10).std().values
            ts=pd.to_datetime(b["timestamp"])
            reg=b["regime"].astype(str).values
            inprof=np.isin(reg,["mean_reversion","unknown"])
            for i in range(1,n):
                rows.append(dict(coin=coin,w=w,t=ts.iloc[i],r=r[i],nx=nxt[i],nx2=nxt2[i],nx3=nxt3[i],
                    run=run[i],dr=dr[i],vol=vol[i],inprof=inprof[i],reg=reg[i],
                    rng=(h[i]-l[i])/c[i-1],clpos=(c[i]-l[i])/(h[i]-l[i]) if h[i]>l[i] else np.nan,
                    wd=ts.iloc[i].dayofweek,yr=ts.iloc[i].year,drift=drift,
                    alloc=float(b["postRebalance_current_allocation"].iloc[i])))
    d=pd.DataFrame(rows)
    d["ex"]=d["nx"]-d["drift"]; d["ex2"]=d["nx2"]-2*d["drift"]; d["ex3"]=d["nx3"]-3*d["drift"]
    d["z"]=d["r"]/d["vol"]
    def dt(sub,col="ex"):
        s=sub.dropna(subset=[col])
        if len(s)<5: return pd.Series(dict(n=len(s),days=0,mean=np.nan,t=np.nan))
        g=s.groupby("t")[col].sum(); m=s[col].mean()
        t=g.mean()/(g.std(ddof=1)/np.sqrt(len(g))) if len(g)>2 else np.nan
        return pd.Series(dict(n=len(s),days=len(g),mean=m,t=t))
    out={}
    d["runb"]=d["run"].clip(upper=5)
    brk=d[d.run>=1]
    out["breaks_by_run_inprof"]=brk[brk.inprof].groupby("runb").apply(dt)
    out["breaks_by_run_outprof"]=brk[~brk.inprof].groupby("runb").apply(dt)
    out["breaks_inprof_h2"]=brk[brk.inprof].groupby("runb").apply(lambda s: dt(s,"ex2"))
    # break day size z
    bb=brk.copy(); bb["zq"]=pd.qcut(bb["z"],4,labels=False,duplicates="drop")
    out["breaks_by_upday_z_q_all"]=bb.groupby("zq").apply(dt)
    out["breaks_by_upday_z_q_inprof"]=bb[bb.inprof].groupby("zq").apply(dt)
    # all days: next-day by today's z quintile, in vs out profile
    a=d.dropna(subset=["z"]).copy(); a["zq"]=pd.qcut(a["z"],5,labels=False)
    out["all_by_z_q_inprof"]=a[a.inprof].groupby("zq").apply(dt)
    out["all_by_z_q_outprof"]=a[~a.inprof].groupby("zq").apply(dt)
    # close position in range, in profile
    a["cq"]=pd.qcut(a["clpos"],5,labels=False,duplicates="drop")
    out["all_by_closepos_inprof"]=a[a.inprof].groupby("cq").apply(dt)
    out["all_by_closepos_outprof"]=a[~a.inprof].groupby("cq").apply(dt)
    # down runs ongoing, in profile
    out["downrun_ongoing_inprof"]=d[(d.dr>=1)&d.inprof].assign(drb=lambda x:x.dr.clip(upper=5)).groupby("drb").apply(dt)
    out["weekday_inprof"]=d[d.inprof].groupby("wd").apply(dt)
    out["weekday_all"]=d.groupby("wd").apply(dt)
    out["profile_share"]=pd.Series(dict(inprof=d.inprof.mean(),breaks_inprof=brk.inprof.sum(),breaks_out=(~brk.inprof).sum()))
    # book daily returns: largest gains/losses
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            dd.append(x.assign(coin=coin,w=w))
    D=pd.concat(dd)
    bk=D.groupby(["w","day"])["book_return"].mean().dropna()
    out["book_by_window"]=bk.groupby(level=0).agg(["mean","count",lambda s:(s!=0).mean()])
    out["breaks_inprof_by_year"]=brk[brk.inprof].groupby("yr").apply(dt)
    return out
