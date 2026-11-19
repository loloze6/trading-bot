def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    rows=[];hourly=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values.astype(float)
            n=len(c)
            r1=np.r_[np.nan, c[1:]/c[:-1]-1]
            ts=pd.to_datetime(df["timestamp"])
            # past 20h return before hour 21 bar
            r20=pd.Series(c).pct_change(20).values
            hourly.append(pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year.values,"hour":ts.dt.hour.values,
                                        "wd":ts.dt.weekday.values,"r":r1,"r20prev":np.r_[np.nan,r20[:-1]]}))
            for t in range(0,n-H,H):
                if t<H: continue
                past=c[t]/c[t-H]-1
                seg=r1[t-H+1:t+1]
                eff=abs(np.log(c[t]/c[t-H]))/np.nansum(np.abs(np.log1p(seg)))
                fwd=c[t+H]/c[t]-1
                rows.append(dict(coin=coin,w=w,year=ts.iloc[t].year,past=past,eff=eff,fwd=fwd))
    g=pd.DataFrame(rows)
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    out={}
    def wel(d,col):
        q=d.groupby("coin")[col].transform(lambda x: x.rank(pct=True))
        a=d.loc[q>0.5,"ex"];b=d.loc[q<=0.5,"ex"]
        t=stats.ttest_ind(a,b,equal_var=False).statistic
        return pd.Series({"diff":a.mean()-b.mean(),"t":t,"n_top":len(a),"n_bot":len(b)})
    R=g[g.past>0]; F=g[g.past<0]
    out["rises: eff top-bottom by coin"]=R.groupby("coin").apply(lambda d: wel(d,"eff"))
    out["rises: eff top-bottom by year"]=R.groupby("year").apply(lambda d: wel(d,"eff"))
    out["rises: eff top-bottom pooled"]=wel(R,"eff").to_frame()
    out["falls: eff top-bottom by coin"]=F.groupby("coin").apply(lambda d: wel(d,"eff"))
    out["falls: eff top-bottom pooled"]=wel(F,"eff").to_frame()
    # signed: eff * sign(past) as predictor over all
    g["seff"]=np.sign(g.past)*g.eff
    out["all: signed eff top-bottom pooled"]=wel(g,"seff").to_frame()
    out["all: signed eff by year"]=g.groupby("year").apply(lambda d: wel(d,"seff"))
    hr=pd.concat(hourly)
    h=hr[hr.hour.isin([21,22])]
    a=h.groupby("coin")["r"].agg(["mean","std","count"]);a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["h21-22 by coin"]=a
    a=h.groupby("year")["r"].agg(["mean","std","count"]);a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["h21-22 by year"]=a
    h=h.copy();h["q"]=h.groupby("coin")["r20prev"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    a=h.groupby("q")["r"].agg(["mean","std","count"]);a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["h21-22 by prior 20h ret quintile"]=a
    o=hr[~hr.hour.isin([21,22])].copy();o["q"]=o.groupby("coin")["r20prev"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    a=o.groupby("q")["r"].agg(["mean","std","count"]);a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["other hours by prior 20h quintile"]=a
    a=h.groupby("wd")["r"].agg(["mean","count"]);out["h21-22 by weekday"]=a
    return out
