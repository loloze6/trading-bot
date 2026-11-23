def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        g=[]
        for w,b in wins.items():
            c=b["close"].values
            if len(c)>3:
                a=c[0::3]; g+=list(a[1:]/a[:-1]-1)
        drift=np.nanmean(g) if g else 0.0
        for w,b in wins.items():
            ts=pd.to_datetime(b["timestamp"],utc=True)
            r=b["close"].pct_change()
            mabs=r.abs().rolling(60,min_periods=20).mean()
            r20=b["close"]/b["close"].shift(20)-1
            r7=b["close"]/b["close"].shift(7)-1
            f3=b["close"].shift(-3)/b["close"]-1
            vol20=r.rolling(20).std(); vol120=r.rolling(120,min_periods=60).std()
            df=pd.DataFrame({"coin":coin,"win":w,"wd":ts.dt.weekday.values,"year":ts.dt.year.values,
              "z":(r/mabs).values,"r20z":(r20/(mabs*np.sqrt(20))).values,"r7z":(r7/(mabs*np.sqrt(7))).values,
              "vr":(vol20/vol120).values,"ex3":(f3-drift).values,
              "alloc":b["postRebalance_current_allocation"].values})
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["z","ex3","r20z"])
    def summ(s):
        s=s.dropna(); n=len(s)
        return pd.Series({"n":n,"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    sf=d[(d.wd==6)&(d.z<-0.3)].copy()
    sf["r20q"]=pd.qcut(sf["r20z"],5)
    out["sun falls by 20d return (vol units) quintile"]=sf.groupby("r20q",observed=True)["ex3"].apply(summ).unstack().round(4)
    res=stats.linregress(sf["r20z"],sf["ex3"]); out["sun falls slope ex3 on r20z"]=pd.Series({"slope":res.slope,"t":res.slope/res.stderr,"n":len(sf)})
    # all sundays regression multi
    s=d[d.wd==6].dropna(subset=["r20z"])
    X=np.column_stack([np.ones(len(s)),s.z,s.r20z,s.z*s.r20z]); y=s.ex3.values
    beta,_,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@beta
    cov=np.linalg.inv(X.T@X)*(e@e/(len(y)-4)); out["sun ols ex3~z+r20z+z*r20z"]=pd.DataFrame({"beta":beta,"t":beta/np.sqrt(np.diag(cov))},index=["c","z","r20z","zxr20z"]).round(5)
    # same on other weekdays
    o=[]
    for wd,gg in d.groupby("wd"):
        X=np.column_stack([np.ones(len(gg)),gg.z,gg.r20z]); y=gg.ex3.values
        b_,_,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b_; cv=np.linalg.inv(X.T@X)*(e@e/(len(y)-3))
        o.append({"wd":wd,"b_z":b_[1],"t_z":b_[1]/np.sqrt(cv[1,1]),"b_r20z":b_[2],"t_r20z":b_[2]/np.sqrt(cv[2,2]),"n":len(gg)})
    out["ols ex3~z+r20z by weekday"]=pd.DataFrame(o).round(5)
    dn=sf[sf.r20z<sf.r20z.quantile(1/3)]
    out["sun falls in decline: by year"]=dn.groupby("year")["ex3"].apply(summ).unstack().round(4)
    out["sun falls in decline: by coin"]=dn.groupby("coin")["ex3"].apply(summ).unstack().round(4)
    # sunday rises
    sr=d[(d.wd==6)&(d.z>1)]
    out["sun rises>1u by year"]=sr.groupby("year")["ex3"].apply(summ).unstack().round(4)
    sr2=d[(d.wd==6)&(d.z>0.3)].copy(); sr2["r20q"]=pd.qcut(sr2["r20z"],3,labels=["down","mid","up"])
    out["sun rises by trend"]=sr2.groupby("r20q",observed=True)["ex3"].apply(summ).unstack().round(4)
    # friday falls continuation
    ff=d[(d.wd==4)&(d.z<-1)]
    out["fri falls>1u by year"]=ff.groupby("year")["ex3"].apply(summ).unstack().round(4)
    # vol regime for sunday falls
    sf2=sf.dropna(subset=["vr"]).copy(); sf2["vq"]=pd.qcut(sf2["vr"],3,labels=["calm","mid","hot"])
    out["sun falls by vol20/vol120"]=sf2.groupby("vq",observed=True)["ex3"].apply(summ).unstack().round(4)
    # book largest days
    br=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items(): br.append(dd.assign(coin=coin,win=w))
    br=pd.concat(br).dropna(subset=["book_return"])
    br["wd"]=pd.to_datetime(br["day"]).dt.weekday
    bd=br.groupby(["win","day"]).agg(b=("book_return","mean"),c=("coin_return","mean"),wd=("wd","first")).reset_index()
    q=bd.b.quantile([0.02,0.98])
    big=bd[bd.b>=q.iloc[1]]; small=bd[bd.b<=q.iloc[0]]
    out["book top2% days"]=pd.Series({"n":len(big),"mean_b":big.b.mean(),"mean_coin":big.c.mean(),"share_mon_wed":big.wd.isin([0,1,2]).mean()})
    out["book bottom2% days"]=pd.Series({"n":len(small),"mean_b":small.b.mean(),"mean_coin":small.c.mean(),"share_mon_wed":small.wd.isin([0,1,2]).mean()})
    out["book share of total gain from top 2% days"]=bd.b[bd.b>=q.iloc[1]].sum()/bd.b.sum()
    return out
