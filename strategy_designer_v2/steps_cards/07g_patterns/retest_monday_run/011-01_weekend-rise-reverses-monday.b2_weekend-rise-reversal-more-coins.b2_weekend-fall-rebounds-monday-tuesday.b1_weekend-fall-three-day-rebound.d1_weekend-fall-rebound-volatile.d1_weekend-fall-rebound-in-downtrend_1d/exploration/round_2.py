def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        g3=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-3,3)
            g3+=list(c[idx+3]/c[idx]-1)
        drift=np.mean(g3); usual=np.std(g3,ddof=1)
        for w,b in ws.items():
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            c=b["close"].reset_index(drop=True).astype(float)
            v=b["volume"].reset_index(drop=True).astype(float)
            d=pd.DataFrame({"wd":ts.dt.weekday,"year":ts.dt.year})
            d["r1"]=c/c.shift(1)-1
            d["r2"]=c/c.shift(2)-1
            d["r20"]=c/c.shift(20)-1
            d["r60"]=c/c.shift(60)-1
            for h in (1,2,3,5,7):
                d[f"f{h}"]=c.shift(-h)/c-1
            d["vr"]=v/v.rolling(20).mean()
            d["vol20"]=d["r1"].rolling(20).std()
            d["u3"]=d["f3"]-drift
            d["s3"]=d["u3"]/usual
            d["alloc"]=b["postRebalance_current_allocation"].reset_index(drop=True).astype(float)
            d["coin"]=coin; d["w"]=w
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def tt(x):
        x=x.dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std(ddof=1)/np.sqrt(n)) if n>2 else np.nan})
    out={}
    D["cell"]=np.where(D.r1<0,"fall","rise")+"_"+np.where(D.r20<0,"dn20","up20")
    out["u3 by weekday x cell (mean)"]=D.groupby(["wd","cell"])["u3"].mean().unstack()
    out["u3 by weekday x cell (t)"]=D.groupby(["wd","cell"])["u3"].apply(lambda x: tt(x)["t"]).unstack()
    fd=D[(D.cell=="fall_dn20")].dropna(subset=["u3"])
    fd=fd.assign(p=fd.r1*fd.r20)
    out["fall_dn20 spearman(product,u3) by wd"]=fd.groupby("wd").apply(lambda g: pd.Series({"rho":stats.spearmanr(g.p,g.u3)[0],"n":len(g)}))
    s=fd[fd.wd==6].copy()
    s["q_r1"]=pd.qcut(s.r1,5,labels=False)
    s["q_r20"]=pd.qcut(s.r20,5,labels=False)
    s["q_vr"]=pd.qcut(s.vr,3,labels=False)
    s["q_vol"]=pd.qcut(s.vol20,3,labels=False)
    out["sun fall_dn20 u3 by r1 quintile (0 deepest)"]=s.groupby("q_r1")["u3"].apply(tt).unstack()
    out["sun fall_dn20 u3 by r20 quintile (0 deepest)"]=s.groupby("q_r20")["u3"].apply(tt).unstack()
    out["sun fall_dn20 u3 by vol ratio tercile"]=s.groupby("q_vr")["u3"].apply(tt).unstack()
    out["sun fall_dn20 s3 by vol20 tercile"]=s.groupby("q_vol")["s3"].apply(tt).unstack()
    out["sun fall_dn20 u3 by r60 sign"]=s.groupby(np.where(s.r60<0,"r60dn","r60up"))["u3"].apply(tt).unstack()
    out["sun fall_dn20 u3 by year"]=s.groupby("year")["u3"].apply(tt).unstack()
    out["sun fall_dn20 raw fwd by horizon"]=pd.DataFrame({h:tt(s[f"f{h}"]) for h in (1,2,3,5,7)}).T
    out["wed fall_dn20 raw fwd by horizon"]=pd.DataFrame({h:tt(fd[fd.wd==2][f"f{h}"]) for h in (1,2,3,5,7)}).T
    sub=D[D.wd==6].copy()
    sub["k"]=np.where(sub.r2<0,"wkfall","wkrise")+np.where(sub.r20<0,"_dn","_up")
    out["sun 2day weekend x r20, u3"]=sub.groupby("k")["u3"].apply(tt).unstack()
    out["f1 by weekday of bar"]=D.groupby("wd")["f1"].apply(tt).unstack()
    bk=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd[["day","book_return","coin_return"]].copy(); x["w"]=w; bk.append(x)
    B=pd.concat(bk); B["day"]=pd.to_datetime(B["day"])
    dayb=B.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    dayb["year"]=dayb.day.dt.year
    out["book by year"]=dayb.groupby("year").apply(lambda g: pd.Series({"days":len(g),"mean":g.book_return.mean(),"sharpe":g.book_return.mean()/g.book_return.std()*np.sqrt(365),"coin_mean":g.coin_return.mean(),"worst":g.book_return.min()}))
    dayb["wd"]=dayb.day.dt.weekday
    out["book by weekday"]=dayb.groupby("wd")["book_return"].apply(tt).unstack()
    q=dayb.book_return.quantile([0.01,0.99])
    worst=dayb[dayb.book_return<=q.iloc[0]]; best=dayb[dayb.book_return>=q.iloc[1]]
    out["book extremes: coin_return mean, wd share"]=pd.DataFrame({"worst":[len(worst),worst.book_return.mean(),worst.coin_return.mean()],"best":[len(best),best.book_return.mean(),best.coin_return.mean()]},index=["n","book","coin"])
    out["sun fall_dn20 u3 by vol20 tercile x r1 quintile hi/lo"]=s.assign(deep=np.where(s.q_r1<=1,"deep","shallow")).groupby(["q_vol","deep"])["u3"].mean().unstack()
    return out
