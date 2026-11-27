def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        allret=[]
        for w,b in wins.items():
            c=b["close"].astype(float).values
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            allret.append(r[1:])
        drift=np.nanmean(np.concatenate(allret))
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values
            o=b["open"].astype(float).values
            n=len(c)
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            nxt=np.r_[c[1:]/c[:-1]-1, np.nan]
            run=np.zeros(n); dn=0
            for i in range(1,n):
                if r[i]>0:
                    run[i]=dn; dn=0
                elif r[i]<0: dn+=1
                else: dn=0
            r60=pd.Series(c).pct_change(60).values*100
            vol30=pd.Series(r).rolling(30).std().values
            # depth of the run: return over the run days
            for i in range(1,n-1):
                if run[i]>=2:
                    k=int(run[i])
                    runret = c[i-1]/c[i-1-k]-1 if i-1-k>=0 else np.nan
                    rows.append(dict(coin=coin,win=w,ts=b["timestamp"].iloc[i],run=k,up=r[i],
                        runret=runret,r60=r60[i],regime=b["regime"].iloc[i],
                        upz=r[i]/vol30[i] if vol30[i]>0 else np.nan,
                        y=-(nxt[i]-drift), fc=b["forecast"].iloc[i]))
    d=pd.DataFrame(rows)
    d["day"]=pd.to_datetime(d["ts"]).dt.floor("D")
    d["year"]=pd.to_datetime(d["ts"]).dt.year
    def cl(g):
        s=g.groupby("day")["y"].apply(lambda v:(v-g["y"].mean()).sum())
        G=len(s); se=np.sqrt((s**2).sum()*G/(G-1))/len(g) if G>1 else np.nan
        return pd.Series(dict(n=len(g),days=G,mean=g["y"].mean(),t=g["y"].mean()/se if se else np.nan))
    d["prof"]=np.where(d["r60"]< -10,"falling",np.where(d["r60"]>10,"rising",np.where(d["r60"].isna(),"na","choppy")))
    f=d[d["regime"]=="mean_reversion"]
    out={}
    out["all_by_prof"]=d.groupby("prof").apply(cl)
    out["fall_by_run"]=f.assign(rb=f["run"].clip(upper=5)).groupby("rb").apply(cl)
    out["fall_by_coin"]=f.groupby("coin").apply(cl)
    out["fall_by_win"]=f.groupby("win").apply(cl)
    out["fall_by_year"]=f.groupby("year").apply(cl)
    f=f.copy()
    f["upq"]=pd.qcut(f["up"],4,labels=False)
    out["fall_by_upsize_q"]=f.groupby("upq").apply(cl)
    f["upzq"]=pd.qcut(f["upz"],4,labels=False)
    out["fall_by_upz_q"]=f.groupby("upzq").apply(cl)
    f["rrq"]=pd.qcut(f["runret"],4,labels=False)
    out["fall_by_runret_q (0=deepest)"]=f.groupby("rrq").apply(cl)
    f["r60q"]=pd.qcut(f["r60"],4,labels=False)
    out["fall_by_r60_q (0=deepest)"]=f.groupby("r60q").apply(cl)
    out["corr_y"]=pd.Series({k:stats.spearmanr(f[k],f["y"],nan_policy="omit")[0] for k in ["run","up","upz","runret","r60"]})
    out["n_regime"]=f.shape[0]
    return out
