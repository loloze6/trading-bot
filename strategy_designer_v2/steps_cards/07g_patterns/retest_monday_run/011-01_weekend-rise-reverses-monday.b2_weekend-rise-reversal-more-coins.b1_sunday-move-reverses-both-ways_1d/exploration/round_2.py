def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            r1=c/c.shift(1)-1
            scale=r1.abs().shift(1).rolling(60,min_periods=20).mean()
            vr=v/v.shift(1).rolling(60,min_periods=20).mean()
            vol=r1.rolling(20,min_periods=10).std()
            volrank=vol/r1.rolling(60,min_periods=20).std().shift(20)
            f1=c.shift(-1)/c-1; f2=c.shift(-2)/c-1; f3=c.shift(-3)/c-1
            r5=c/c.shift(5)-1
            df=pd.DataFrame(dict(coin=coin,w=w,wd=ts.dt.weekday,year=ts.dt.year,r1=r1,z=r1/scale,
                vr=vr,volrank=volrank,f1=f1,f2=f2,f3=f3,r5=r5,z5=r5/(scale*np.sqrt(5))))
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    dm=d.groupby("coin")["r1"].mean(); d["drift1"]=d["coin"].map(dm)
    d["a1"]=d.f1-d.drift1; d["a2"]=d.f2-2*d.drift1; d["a3"]=d.f3-3*d.drift1
    d["zc"]=d.z.clip(-2,2)
    out={}
    def sig(g,col,x="zc"):
        g=g.dropna(subset=[col,x]); return -np.sign(g[x])*g[col]
    def summ(g,col,x="zc"):
        s=sig(g,col,x); y=-(g.dropna(subset=[col,x])[x])*g.dropna(subset=[col,x])[col]
        return pd.Series(dict(n=len(s),mean_signed=s.mean(),t_signed=s.mean()/(s.std()/np.sqrt(len(s))),
                              mean_prod=y.mean(),t_prod=y.mean()/(y.std()/np.sqrt(len(y)))))
    # volatility regime x weekday (non-overlap: one case per week per weekday)
    dd=d.dropna(subset=["volrank","a2","zc"]).copy()
    dd["vq"]=pd.qcut(dd.volrank,3,labels=["calm","mid","wild"])
    t=dd.groupby(["wd","vq"]).apply(lambda g:summ(g,"a2"))
    out["wd_x_volregime_2d"]=t[["n","mean_signed","t_signed","t_prod"]]
    s=dd[dd.wd==6]
    a=sig(s[s.vq=="wild"],"a2"); b=sig(s[s.vq=="calm"],"a2")
    a2=sig(dd[(dd.wd!=6)&(dd.vq=="wild")],"a2")
    out["sun_wild_minus_calm"]=pd.Series(dict(diff=a.mean()-b.mean(),t=stats.ttest_ind(a,b,equal_var=False).statistic,
        sun_wild_minus_otherdays_wild=a.mean()-a2.mean(),t2=stats.ttest_ind(a,a2,equal_var=False).statistic))
    # sunday volume: own-day volume ratio
    s=d[d.wd==6].dropna(subset=["vr","a2","zc"]).copy()
    s["vq"]=pd.qcut(s.vr,3,labels=["low","mid","high"])
    out["sun_by_sunvolume"]=s.groupby("vq").apply(lambda g:summ(g,"a2"))
    hi=sig(s[s.vq=="high"],"a2"); lo=sig(s[s.vq=="low"],"a2")
    out["sun_highvol_minus_lowvol"]=pd.Series(dict(diff=hi.mean()-lo.mean(),t=stats.ttest_ind(hi,lo,equal_var=False).statistic))
    # Friday continuation: friday move -> sat+sun
    f=d[d.wd==4]
    out["fri_into_weekend"]=pd.DataFrame({"1d":summ(f,"a1"),"2d":summ(f,"a2"),"3d":summ(f,"a3")}).T
    ff=f.dropna(subset=["volrank","a2","zc"]).copy(); ff["vq"]=pd.qcut(ff.volrank,3,labels=["calm","mid","wild"])
    out["fri_by_volregime_2d"]=ff.groupby("vq").apply(lambda g:summ(g,"a2"))
    out["fri_by_year_2d"]=f.groupby("year").apply(lambda g:summ(g,"a2"))[["n","mean_signed","t_signed"]]
    # Sunday reversal: does prior 5-day trend matter? sunday move with vs against 5-day move
    s=d[d.wd==6].dropna(subset=["r5","a2","zc"]).copy()
    s["agree"]=np.where(np.sign(s.r5-s.r1)==np.sign(s.r1),"with_trend","against_trend")
    out["sun_by_prior_trend"]=s.groupby("agree").apply(lambda g:summ(g,"a2"))
    # book: daily returns by weekday and by year, drawdown
    br=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["w"]=w; x["coin"]=coin; br.append(x)
    B=pd.concat(br); B["day"]=pd.to_datetime(B["day"],utc=True)
    bk=B.groupby("day")["book_return"].mean().dropna()
    out["book_by_year"]=bk.groupby(bk.index.year).agg(["count","mean","std"]).assign(sharpe=lambda q:q["mean"]/q["std"]*np.sqrt(365))
    out["book_by_weekday"]=bk.groupby(bk.index.weekday).agg(["count","mean","std"])
    return out
