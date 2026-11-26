def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; lo=b["low"].values; hi=b["high"].values
            n=len(b)
            pl=pd.Series(lo).shift(1).rolling(30,min_periods=30).min().values
            ph=pd.Series(hi).shift(1).rolling(30,min_periods=30).max().values
            r60=np.r_[[np.nan]*60, c[60:]/c[:-60]-1] if n>60 else np.full(n,np.nan)
            r1=np.r_[np.nan, c[1:]/c[:-1]-1]
            v30=pd.Series(r1).rolling(30,min_periods=25).std().values
            ts=pd.to_datetime(b["timestamp"])
            for t in range(n):
                ok=not np.isnan(pl[t]); okh=not np.isnan(ph[t]); rng=hi[t]-lo[t]
                r=dict(coin=coin,w=w,t=t,day=ts.iloc[t].floor("D"),reg=b["regime"].iloc[t],
                       reclaim=ok and lo[t]<pl[t]<c[t], hpierce=okh and hi[t]>ph[t]>c[t],
                       cl=(hi[t]-c[t])/rng if rng>0 else np.nan, r60=r60[t],
                       rngz=(rng/c[t])/v30[t] if v30[t]>0 else np.nan)
                for H in (1,3,5,10):
                    r["f%d"%H]=c[t+H]/c[t]-1 if t+H<n else np.nan
                rows.append(r)
    d=pd.DataFrame(rows)
    d["out"]=d.reg=="chop"
    d["nonfall"]=d.out&(d.r60>=-0.10)
    out={}
    def clt(e,col):
        m=e[col].mean(); dev=(e[col]-m).groupby(e.day).sum()
        se=np.sqrt((dev**2).sum())/len(e); return m,m/se,len(e),e.day.nunique()
    res=[]
    for H in (1,3,5,10):
        g=d[(d.t%H==0)&d["f%d"%H].notna()]
        drift=g.groupby("coin")["f%d"%H].mean()
        d["ex%d"%H]=d["f%d"%H]-d.coin.map(drift)
        d["cell%d"%H]=d.t//H
        for nm,mk in [("reclaim nonfalling out",d.reclaim&d.nonfall),("reclaim out",d.reclaim&d.out),
                      ("hpierce all",d.hpierce),("hpierce rising",d.hpierce&(d.r60>0.10))]:
            e=d[mk&d["ex%d"%H].notna()].groupby(["coin","w","cell%d"%H]).head(1)
            m,tt,nn,dd=clt(e,"ex%d"%H)
            res.append(dict(set=nm,H=H,mean=m,t_cl=tt,n=nn,days=dd))
    out["horizons"]=pd.DataFrame(res)
    e=d[d.reclaim&d.nonfall&d.ex5.notna()].groupby(["coin","w","cell5"]).head(1)
    res=[]
    for gv in ["r60","cl","rngz"]:
        x=e.dropna(subset=[gv]); rho=stats.spearmanr(x[gv],x.ex5)
        res.append(dict(grade=gv,n=len(x),spear=rho.correlation,p=rho.pvalue))
    out["reclaim_nonfall_grading"]=pd.DataFrame(res)
    out["reclaim_nonfall_by_coin"]=e.groupby("coin").ex5.agg(["mean","count"])
    out["reclaim_nonfall_by_yr"]=e.groupby(e.day.dt.year).ex5.agg(["mean","count"])
    e2=d[d.reclaim&d.out&d.ex5.notna()&d.r60.notna()].groupby(["coin","w","cell5"]).head(1)
    out["reclaim_out_by_r60_tercile"]=e2.groupby(pd.qcut(e2.r60,3,labels=False)).agg(mean=("ex5","mean"),n=("ex5","size"),r60=("r60","mean"))
    return out
