def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; lo=b["low"].values; hi=b["high"].values
            n=len(b)
            pl=pd.Series(lo).shift(1).rolling(30,min_periods=30).min().values
            ph=pd.Series(hi).shift(1).rolling(30,min_periods=30).max().values
            r60=np.r_[[np.nan]*60, c[60:]/c[:-60]-1] if n>60 else np.full(n,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            for t in range(n):
                fwd=c[t+H]/c[t]-1 if t+H<n else np.nan
                rng=hi[t]-lo[t]
                ok=not np.isnan(pl[t]); okh=not np.isnan(ph[t])
                rows.append(dict(coin=coin,w=w,t=t,cell=t//H,fwd=fwd,day=ts.iloc[t].floor("D"),
                    yr=ts.iloc[t].year,reg=b["regime"].iloc[t],
                    reclaim=ok and lo[t]<pl[t]<c[t],
                    breakdown=ok and c[t]<pl[t],
                    hpierce=okh and hi[t]>ph[t]>c[t],
                    hbreak=okh and c[t]>ph[t],
                    cl=(hi[t]-c[t])/rng if rng>0 else np.nan,
                    depth=(pl[t]-lo[t])/c[t] if ok else np.nan,
                    hdepth=(hi[t]-ph[t])/c[t] if okh else np.nan,
                    r60=r60[t]))
    d=pd.DataFrame(rows)
    d["infp"]=d.reg!="chop"
    g=d[(d.t%H==0)&d.fwd.notna()]
    drift=g.groupby("coin").fwd.mean()
    d["ex"]=d.fwd-d.coin.map(drift)
    d["trend"]=np.where(d.r60.isna(),"na",np.where(d.r60>0.10,"rising",np.where(d.r60<-0.10,"falling","choppy")))
    def cases(mask):
        return d[mask&d.ex.notna()].groupby(["coin","w","cell"]).head(1)
    def ev(e,name):
        if len(e)<3: return dict(name=name,n=len(e))
        day=e.groupby("day").ex.sum()
        tc=day.sum()/len(e)/ (np.sqrt(((day-day.mean()*0)**2).sum())/len(e)) if len(day)>1 else np.nan
        # clustered t: mean / se with se = sqrt(sum (sum_dev_day)^2)/n
        m=e.ex.mean(); dev=(e.ex-m).groupby(e.day).sum()
        se=np.sqrt((dev**2).sum())/len(e)
        return dict(name=name,n=len(e),days=e.day.nunique(),mean=m,t_cl=m/se,hit=(e.ex>0).mean())
    out={}
    res=[]
    for nm,mk in [("reclaim",d.reclaim),("breakdown",d.breakdown),("hpierce",d.hpierce),("hbreak",d.hbreak)]:
        res.append(ev(cases(mk),nm+" all"))
        res.append(ev(cases(mk&~d.infp),nm+" outFA"))
        for tr in ["rising","choppy","falling","na"]:
            res.append(ev(cases(mk&~d.infp&(d.trend==tr)),nm+" outFA "+tr))
    out["events_by_trend"]=pd.DataFrame(res)
    # grading inside outFA reclaim and hpierce
    res=[]
    for nm,mk,gv in [("reclaim outFA",d.reclaim&~d.infp,"cl"),("reclaim outFA",d.reclaim&~d.infp,"depth"),
                     ("hpierce all",d.hpierce,"cl"),("hpierce all",d.hpierce,"hdepth"),
                     ("breakdown outFA",d.breakdown&~d.infp,"depth")]:
        e=cases(mk).dropna(subset=[gv])
        med=e[gv].median()
        a=e[e[gv]>med].ex; bb=e[e[gv]<med].ex
        rho=stats.spearmanr(e[gv],e.ex)
        res.append(dict(set=nm,grade=gv,n=len(e),hi_mean=a.mean(),lo_mean=bb.mean(),
                        welch_t=stats.ttest_ind(a,bb,equal_var=False).statistic,spear=rho.correlation,sp_p=rho.pvalue))
    out["grading"]=pd.DataFrame(res)
    # stability by year and coin
    for nm,mk in [("reclaim_outFA",d.reclaim&~d.infp),("hpierce",d.hpierce)]:
        e=cases(mk)
        out[nm+"_by_yr"]=e.groupby("yr").ex.agg(["mean","count"])
        out[nm+"_by_coin"]=e.groupby("coin").ex.agg(["mean","count"])
        out[nm+"_by_w"]=e.groupby("w").ex.agg(["mean","count"])
    # reclaim high close vs low close in outFA
    e=cases(d.reclaim&~d.infp)
    out["reclaim_outFA_clq"]=e.groupby(pd.qcut(e.cl,3,labels=False)).ex.agg(["mean","count"])
    return out
