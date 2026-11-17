def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    out={}
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            d=df.reset_index(drop=True)
            cl=d["close"].astype(float); v=d["volume"].astype(float)
            r1=cl.pct_change()
            n=len(d)
            for h in (7,14):
                for i in range(20,n-h,h):
                    past=cl.iloc[max(0,i-20):i+1]
                    rows.append(dict(coin=c,w=w,h=h,
                        fwd=cl.iloc[i+h]/cl.iloc[i]-1,
                        past7=cl.iloc[i]/cl.iloc[i-7]-1,
                        past20=cl.iloc[i]/cl.iloc[i-20]-1,
                        dist20=cl.iloc[i]/past.max()-1,
                        vr=v.iloc[i]/v.iloc[i-20:i].mean(),
                        vol20=r1.iloc[i-19:i+1].std(),
                        brk=int(d["regime"].iloc[i]=="trending"),
                        wd=pd.Timestamp(d["timestamp"].iloc[i]).weekday()))
    S=pd.DataFrame(rows)
    res=[]
    for h in (7,14):
        s=S[S.h==h].copy()
        s["ex"]=s.fwd-s.groupby("coin").fwd.transform("mean")
        for x in ["past7","past20","dist20","vr","vol20","brk"]:
            ss=s.dropna(subset=[x,"ex"])
            sl=stats.linregress(ss[x],ss.ex)
            rk=stats.spearmanr(ss[x],ss.ex)
            res.append(dict(h=h,x=x,n=len(ss),slope=sl.slope,t=sl.slope/sl.stderr,spear=rk.correlation))
        for x in ["past20","dist20","vr","vol20"]:
            s["q"]=s.groupby("coin")[x].transform(lambda z: pd.qcut(z.rank(method="first"),3,labels=False))
            g=s.groupby("q").ex.agg(["mean","count"])
            for q,r in g.iterrows(): res.append(dict(h=h,x=x+"_tercile"+str(q),n=r["count"],slope=r["mean"]))
    out["pooled_predictors"]=pd.DataFrame(res)
    # per coin slope for past20 and vr, h=7
    s=S[S.h==7].copy(); s["ex"]=s.fwd-s.groupby("coin").fwd.transform("mean")
    pc=[]
    for c,g in s.groupby("coin"):
        for x in ["past20","dist20","vr","vol20"]:
            sl=stats.linregress(g[x],g.ex); pc.append(dict(coin=c,x=x,n=len(g),t=sl.slope/sl.stderr))
    out["per_coin_h7_t"]=pd.DataFrame(pc).pivot(index="coin",columns="x",values="t")
    # daily data: weekday, book
    D=[]
    for c in days:
        for w,df in days[c].items():
            d=df.copy(); d["coin"]=c; d["w"]=w; D.append(d)
    D=pd.concat(D); D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    D["prev"]=D.groupby(["coin","w"]).coin_return.shift(1)
    out["weekday_coin_ret"]=D.groupby("wd").coin_return.agg(["mean","std","count"]).assign(t=lambda x:x["mean"]/(x["std"]/np.sqrt(x["count"])))
    dd=D.dropna(subset=["prev","coin_return"])
    sl=stats.linregress(dd.prev,dd.coin_return); out["daily_autocorr_t"]=float(sl.slope/sl.stderr)
    dd=dd.copy(); dd["pq"]=dd.groupby("coin").prev.transform(lambda z: pd.qcut(z.rank(method="first"),5,labels=False))
    out["next_day_by_prev_quintile"]=dd.groupby("pq").coin_return.agg(["mean","count"])
    # book: daily book mean by year, by in-position
    B=D.groupby(["w","day"]).agg(book=("book_return","mean"),coin=("coin_return","mean")).dropna().reset_index()
    B["yr"]=pd.to_datetime(B.day).dt.year
    out["book_by_year"]=B.groupby("yr").agg(book=("book","mean"),coin=("coin","mean"),n=("book","count"))
    out["book_by_window"]=B.groupby("w").agg(book=("book","sum"),coin=("coin","sum"))
    # breakout bars count by coin and regime share
    out["breakout_share"]=S[S.h==7].groupby("coin").brk.mean()
    return out
