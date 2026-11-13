def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            ma=r.abs().rolling(20,min_periods=20).mean().shift(1)
            z=r/ma
            ts=pd.to_datetime(b["timestamp"])
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            d=pd.DataFrame({"coin":coin,"w":w,"r":r,"z":z,"n1":r.shift(-1),
                "wd":ts.dt.weekday,"year":ts.dt.year,
                "clo":(c-b["low"])/rng,"rngz":(rng/c)/((rng/c).rolling(20,min_periods=20).mean().shift(1)),
                "f":b["forecast"].astype(float)})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["z","n1","clo"])
    def summ(g):
        return pd.Series({"n":len(g),"hit":(g.n1>0).mean(),"mean":g.n1.mean(),"t":g.n1.mean()/g.n1.std()*np.sqrt(len(g))})
    out={}
    D["sgn"]=np.where(D.r<0,"down","up")
    D["cb"]=pd.cut(D.clo,[-0.01,0.2,0.5,0.8,1.01])
    out["clo_by_sign"]=D.groupby(["sgn","cb"]).apply(summ)
    out["clo_alldays"]=D.groupby("cb").apply(summ)
    lowc=D[D.clo<=0.2]
    out["lowclose_by_year"]=lowc.groupby("year").apply(summ)
    out["lowclose_by_coin"]=lowc.groupby("coin").apply(summ)
    out["lowclose_by_rngz"]=lowc.groupby(pd.cut(lowc.rngz,[0,0.8,1.2,2,np.inf])).apply(summ)
    D["half"]=np.where(D.year<=2021,"2018-21","2022-25")
    out["wd_by_half"]=D.groupby(["half","wd"]).apply(summ)
    out["wd_by_coin_fri"]=D[D.wd==4].groupby("coin").apply(summ)
    out["wd2_by_coin"]=D[D.wd==2].groupby("coin").apply(summ)
    # book's daily returns by weekday and position
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy();t["coin"]=coin;dd.append(t)
    DD=pd.concat(dd).dropna(subset=["book_return"])
    DD["wd"]=pd.to_datetime(DD["day"]).dt.weekday
    out["book_by_wd"]=DD.groupby("wd").book_return.agg(["mean","std","size"])
    q=DD.book_return.quantile([0.01,0.99])
    out["book_tails_coinret"]=pd.Series({"worst1pct_n":(DD.book_return<=q.iloc[0]).sum(),
        "worst_mean_coinret":DD.coin_return[DD.book_return<=q.iloc[0]].mean(),
        "best1pct_mean_coinret":DD.coin_return[DD.book_return>=q.iloc[1]].mean()})
    return out
