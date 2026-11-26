def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float).reset_index(drop=True)
            r=c.pct_change()
            er=(c-c.shift(30)).abs()/(c.diff().abs().rolling(30).sum())
            r7=c/c.shift(7)-1; r30=c/c.shift(30)-1; r1=r
            vol=r.rolling(30).std()
            s7=r7/(vol*np.sqrt(7))
            fwd=c.shift(-7)/c-1
            r3=c/c.shift(3)-1
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            df=pd.DataFrame({"coin":coin,"w":w,"er":er,"r7":r7,"r30":r30,"vol":vol,"s7":s7,"fwd":fwd,"r1":r1,"r3":r3,
                             "fc":b["forecast"].values,"regime":b["regime"].values,"wd":ts.dt.weekday,"year":ts.dt.year})
            df=df.iloc[::7]
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["er","s7","fwd","vol"])
    drift=d.groupby("coin")["fwd"].transform("mean")
    d["ex"]=d["fwd"]-drift
    d["agree"]=np.sign(d.r7)==np.sign(d.r30)
    d["chop"]=d.er<=0.3
    def summ(g):
        x=np.sign(g.s7)*g.ex
        sl=stats.linregress(g.s7,g.ex) if len(g)>10 else None
        return pd.Series({"n":len(g),"mean_sign_ex":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(g))),
                          "slope_t":(sl.slope/sl.stderr) if sl else np.nan})
    out={}
    out["by_chop_agree"]=d.groupby(["chop","agree"]).apply(summ)
    d["erq"]=pd.qcut(d.er,5,labels=False)
    out["by_er_quintile"]=d.groupby("erq").apply(summ)
    d["volq"]=d.groupby("coin")["vol"].transform(lambda v: pd.qcut(v,3,labels=False))
    out["by_vol_tercile"]=d.groupby("volq").apply(summ)
    out["by_coin"]=d.groupby("coin").apply(summ)
    out["by_year"]=d.groupby("year").apply(summ)
    # 30-day momentum alone
    d["s30"]=d.r30/(d.vol*np.sqrt(30))
    def summ30(g):
        x=np.sign(g.s30)*g.ex; sl=stats.linregress(g.s30,g.ex)
        return pd.Series({"n":len(g),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(g))),"slope_t":sl.slope/sl.stderr})
    out["mom30_by_chop"]=d.groupby("chop").apply(summ30)
    # forecast buckets in regime
    rg=d[d.regime=="mean_reversion"].copy()
    rg["fq"]=pd.qcut(rg.fc.abs(),4,labels=False,duplicates="drop")
    out["regime_fc_abs_quartile"]=rg.groupby("fq").apply(lambda g: pd.Series({"n":len(g),"mean_sign_ex":(np.sign(g.fc)*g.ex).mean(),"long_share":(g.fc>0).mean()}))
    out["regime_long_vs_short"]=rg.groupby(np.sign(rg.fc)).apply(lambda g: pd.Series({"n":len(g),"mean_sign_ex":(np.sign(g.fc)*g.ex).mean(),"t":(np.sign(g.fc)*g.ex).mean()/((np.sign(g.fc)*g.ex).std()/np.sqrt(len(g)))}))
    # book daily
    dd=pd.concat([x.assign(coin=c) for c,ws in data["days"].items() for x in ws.values()])
    dd["wd"]=pd.to_datetime(dd["day"]).dt.weekday
    out["book_by_weekday"]=dd.groupby("wd")["book_return"].agg(["mean","count"])
    return out
