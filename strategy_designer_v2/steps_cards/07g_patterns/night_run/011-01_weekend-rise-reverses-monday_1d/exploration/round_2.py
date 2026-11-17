def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=pd.Series(b["close"].astype(float).values); v=pd.Series(b["volume"].astype(float).values)
            r=c.pct_change()
            scale=r.abs().rolling(60,min_periods=20).mean()
            vr=v/v.rolling(60,min_periods=20).mean()
            df=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.weekday.values,"year":ts.dt.year.values,
                             "r":r,"z":r/scale,"scale":scale,"vr":vr,"f1":c.shift(-1)/c-1})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["e1"]=d["f1"]-d.groupby("coin")["f1"].transform("mean")
    d["zc"]=d.z.clip(-5,5)
    d["volq"]=d.groupby("coin").scale.transform(lambda x: pd.qcut(x,4,labels=False,duplicates="drop"))
    def slope(x,y):
        ok=x.notna()&y.notna(); x=x[ok]; y=y[ok]
        if len(x)<30: return (np.nan,np.nan,len(x))
        res=stats.linregress(x,y); return (res.slope*1e3,res.slope/res.stderr,len(x))
    out={}
    hv=d[d.volq>=2]
    out["high-vol half: slope next1 on z by year"]=pd.DataFrame([[k,*slope(g.zc,g.e1)] for k,g in hv.groupby("year")],columns=["year","sl","t","n"])
    out["high-vol half: slope by coin"]=pd.DataFrame([[k,*slope(g.zc,g.e1)] for k,g in hv.groupby("coin")],columns=["coin","sl","t","n"])
    out["top vol quartile: slope down-moves vs up-moves"]=pd.DataFrame([[k,*slope(g.zc,g.e1)] for k,g in d[d.volq==3].groupby(d.z>0)],columns=["up","sl","t","n"])
    # vol x volume ratio interaction
    d["hivr"]=d.vr>d.groupby("coin").vr.transform("median")
    out["all days slope by volq x high volume"]=pd.DataFrame([[a,b_,*slope(g.zc,g.e1)] for (a,b_),g in d.groupby(["volq","hivr"])],columns=["volq","hivr","sl","t","n"])
    # weekday seasonality by year
    for wd,name in [(4,"fri->sat"),(2,"wed->thu"),(0,"mon->tue"),(3,"thu->fri")]:
        s=d[d.wd==wd]
        out[name+" next-day excess by year (x1e3)"]=s.groupby("year").e1.agg(lambda x: x.mean()*1e3).to_frame("mean").join(s.groupby("year").e1.agg(lambda x: stats.ttest_1samp(x.dropna(),0).statistic).to_frame("t")).join(s.groupby("year").e1.count().to_frame("n"))
    # graded: thursday->friday & friday->saturday by vol level
    s=d[d.wd==4]
    out["fri->sat excess by vol quartile (x1e3)"]=s.groupby("volq").e1.agg(["mean","count"]).assign(mean=lambda x:x["mean"]*1e3)
    # book: daily returns around largest gains/losses
    bk=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            dd=dd.copy(); dd["wd"]=pd.to_datetime(dd["day"]).dt.weekday; bk.append(dd)
    B=pd.concat(bk)
    out["book daily return by weekday (x1e4)"]=B.groupby("wd").book_return.agg(["mean","std","count"]).assign(mean=lambda x:x["mean"]*1e4,std=lambda x:x["std"]*1e4)
    return out
