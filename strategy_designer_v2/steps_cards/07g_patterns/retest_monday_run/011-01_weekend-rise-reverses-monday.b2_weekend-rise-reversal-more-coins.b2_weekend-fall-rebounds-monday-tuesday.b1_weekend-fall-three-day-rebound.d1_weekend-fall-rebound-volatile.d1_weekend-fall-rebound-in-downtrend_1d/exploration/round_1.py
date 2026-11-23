def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        # drift: mean 3-bar return on non-overlapping grid across windows
        g3=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-3,3)
            g3+=list(c[idx+3]/c[idx]-1)
        drift=np.mean(g3); usual=np.std(g3,ddof=1)
        for w,b in ws.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"wd":ts.dt.weekday.values,"year":ts.dt.year.values})
            c=b["close"].reset_index(drop=True)
            d["r1"]=(c/c.shift(1)-1).values
            d["r2"]=(c/c.shift(2)-1).values
            d["r20"]=(c/c.shift(20)-1).values
            d["f3"]=(c.shift(-3)/c-1).values
            d["f1"]=(c.shift(-1)/c-1).values
            v=b["volume"].reset_index(drop=True)
            d["vr"]=(v/v.rolling(20).mean()).values
            d["vol20"]=d["r1"].rolling(20).std()
            d["u3"]=d["f3"]-drift
            d["s3"]=d["u3"]/usual
            d["coin"]=coin; d["w"]=w
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def tt(x):
        x=x.dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std(ddof=1)/np.sqrt(n)) if n>2 else np.nan})
    out={}
    D["cell"]=np.where(D.r1<0,"fall","rise")+"_"+np.where(D.r20<0,"dn20","up20")
    out["u3 by weekday x cell"]=D.groupby(["wd","cell"])["u3"].apply(tt).unstack()
    # graded: product within fall_dn20 by weekday
    fd=D[(D.cell=="fall_dn20")].dropna(subset=["u3"])
    fd=fd.assign(p=fd.r1*fd.r20)
    out["fall_dn20 corr(product,u3) by wd"]=fd.groupby("wd").apply(lambda g: pd.Series({"rho":stats.spearmanr(g.p,g.u3)[0],"n":len(g)}))
    # Sunday fall_dn20 by r1 quintile, by r20 quintile
    s=fd[fd.wd==6].copy()
    s["q_r1"]=pd.qcut(s.r1,5,labels=False)
    s["q_r20"]=pd.qcut(s.r20,5,labels=False)
    s["q_vr"]=pd.qcut(s.vr,3,labels=False)
    s["q_vol"]=pd.qcut(s.vol20,3,labels=False)
    out["sun fall_dn20 u3 by r1 quintile(0=deepest)"]=s.groupby("q_r1")["u3"].apply(tt).unstack()
    out["sun fall_dn20 u3 by r20 quintile"]=s.groupby("q_r20")["u3"].apply(tt).unstack()
    out["sun fall_dn20 u3 by volume ratio tercile"]=s.groupby("q_vr")["u3"].apply(tt).unstack()
    out["sun fall_dn20 s3 by vol20 tercile"]=s.groupby("q_vol")["s3"].apply(tt).unstack()
    out["sun fall_dn20 u3 by year"]=s.groupby("year")["u3"].apply(tt).unstack()
    # all weekdays: daily return by weekday (one-bar, non-overlapping)
    out["f1 by weekday of next bar start (wd+1)"]=D.groupby("wd")["f1"].apply(tt).unstack()
    # 2-day weekend (Sat+Sun) fall
    out["sun r2<0 & r20<0 vs r2>=0, u3"]=D[D.wd==6].assign(k=np.where(D.r2<0,"wkfall","wkrise")+np.where(D.r20<0,"_dn","_up")).groupby("k")["u3"].apply(tt).unstack()
    # book: by year
    bk=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd[["day","book_return","coin_return"]].copy(); x["w"]=w; x["coin"]=coin; bk.append(x)
    B=pd.concat(bk)
    B["day"]=pd.to_datetime(B["day"])
    dayb=B.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    dayb["year"]=dayb.day.dt.year
    out["book by year"]=dayb.groupby("year").apply(lambda g: pd.Series({"days":len(g),"mean":g.book_return.mean(),"sharpe":g.book_return.mean()/g.book_return.std()*np.sqrt(365),"coin_mean":g.coin_return.mean(),"worst":g.book_return.min()}))
    dayb["wd"]=dayb.day.dt.weekday
    out["book by weekday"]=dayb.groupby("wd")["book_return"].apply(tt).unstack()
    return out
