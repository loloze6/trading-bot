def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        allret=[]
        for w,b in wins.items():
            c=b["close"].astype(float).values
            allret.append(c[1:]/c[:-1]-1)
        drift=np.nanmean(np.concatenate(allret))
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values
            n=len(c)
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            nxt=np.r_[c[1:]/c[:-1]-1, np.nan]
            run=np.zeros(n); dn=0
            for i in range(1,n):
                if r[i]>0: run[i]=dn; dn=0
                elif r[i]<0: dn+=1
                else: dn=0
            vol30=pd.Series(r).rolling(30).std().values
            for i in range(1,n-1):
                if run[i]>=2 and b["regime"].iloc[i]=="mean_reversion":
                    k=int(run[i])
                    if i-1-k<0: continue
                    rr=c[i-1]/c[i-1-k]-1
                    rows.append(dict(coin=coin,win=w,ts=b["timestamp"].iloc[i],run=k,up=r[i],
                        runret=rr,runz=rr/(vol30[i]*np.sqrt(k)) if vol30[i]>0 else np.nan,
                        depthv=rr/vol30[i] if vol30[i]>0 else np.nan,
                        retr=r[i]/(-rr) if rr<0 else np.nan,
                        y=-(nxt[i]-drift)))
    d=pd.DataFrame(rows)
    d["day"]=pd.to_datetime(d["ts"]).dt.floor("D")
    d["year"]=pd.to_datetime(d["ts"]).dt.year
    def cl(g):
        s=g.groupby("day")["y"].apply(lambda v:(v-g["y"].mean()).sum())
        G=len(s); se=np.sqrt((s**2).sum()*G/(G-1))/len(g) if G>1 else np.nan
        return pd.Series(dict(n=len(g),days=G,mean=g["y"].mean(),t=g["y"].mean()/se if se else np.nan))
    out={}
    d["rrq"]=pd.qcut(d["runret"],4,labels=False)
    d["dvq"]=pd.qcut(d["depthv"],4,labels=False)
    out["by_depth_q(0=deepest)"]=d.groupby("rrq").apply(cl)
    out["by_depth_in_vol_q(0=deepest)"]=d.groupby("dvq").apply(cl)
    out["deep_half_by_year"]=d[d["rrq"]<=1].groupby("year").apply(cl)
    out["shallow_half_by_year"]=d[d["rrq"]>=2].groupby("year").apply(cl)
    out["depth_q_by_run2_vs_3plus"]=d.assign(r3=(d["run"]>=3).astype(int)).groupby(["r3","rrq"]).apply(cl)
    out["spearman"]=pd.Series({k:stats.spearmanr(d[k],d["y"],nan_policy="omit")[0] for k in ["run","runret","depthv","runz","retr"]})
    out["spearman_by_year_depthv"]=d.groupby("year").apply(lambda g: stats.spearmanr(g["depthv"],g["y"],nan_policy="omit")[0])
    out["n"]=len(d)
    return out
