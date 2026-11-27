def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; rng=(b["high"]-b["low"])/c
            df=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            df["r1"]=c.pct_change(); df["r5"]=c/c.shift(5)-1
            df["tr60"]=c/c.shift(60)-1
            df["width"]=rng/rng.rolling(20).mean()
            df["n1"]=c.shift(-1)/c-1
            df["n2"]=c.shift(-2)/c.shift(-1)-1
            df["n3"]=c.shift(-3)/c-1
            df["vol30"]=df["r1"].rolling(30).std()
            df["alloc"]=b["postRebalance_current_allocation"]
            df["yr"]=df.ts.dt.year
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    for col in ["n1","n2"]:
        D["a"+col]=D[col]-D["coin"].map(D.groupby("coin")[col].mean())
    # n3 drift on non-overlapping grid would be ideal; use n3 every 3rd bar
    D["vrank"]=D.groupby("coin")["vol30"].rank(pct=True)
    D["trend"]=np.where(D.tr60<-0.10,"falling",np.where(D.tr60>0.10,"rising",np.where(D.tr60.notna(),"choppy","na")))
    D["agit"]=np.where(D.vrank>0.5,"agit","calm")
    D["wq5"]=D.groupby("coin")["width"].transform(lambda x: pd.qcut(x,5,labels=False))
    D["r5q"]=D.groupby("coin")["r5"].transform(lambda x: pd.qcut(x,5,labels=False))
    def stat(g,col="an1"):
        g=g.dropna(subset=[col]); n=len(g)
        if n<20: return pd.Series({"n":n,"mean%":np.nan,"t":np.nan,"days":g.ts.nunique()})
        m=g[col].mean(); s=g.groupby("ts")[col].apply(lambda x:(x-m).sum())
        se=np.sqrt((s**2).sum())/n
        return pd.Series({"n":n,"mean%":100*m,"t":m/se,"days":g.ts.nunique()})
    E=D[D.trend!="na"]; up=E[E.r1>0]
    out={}
    out["choppy_up_agit_width3"]=up[up.trend=="choppy"].assign(wq=lambda x:np.where(x.wq5>=3,"wide",np.where(x.wq5<=1,"narrow","mid"))).groupby(["agit","wq"]).apply(stat)
    out["choppy_up_r5neg_wq5"]=up[(up.trend=="choppy")&(up.r5<0)].groupby("wq5").apply(stat)
    out["choppy_up_r5pos_wq5"]=up[(up.trend=="choppy")&(up.r5>=0)].groupby("wq5").apply(stat)
    fr=up[(up.trend=="falling")&(up.r5<0)]
    out["fall_r5neg_wq5"]=fr.groupby("wq5").apply(stat)
    out["fall_r5neg_agit"]=fr.groupby("agit").apply(stat)
    out["fall_r5neg_day2"]=fr.groupby("wq5").apply(lambda g:stat(g,"an2"))
    out["fall_r5neg_by_year"]=fr.groupby("yr").apply(stat)
    out["choppy_up_wide_by_year"]=up[(up.trend=="choppy")&(up.wq5>=3)].groupby("yr").apply(stat)
    # all up days: r5 quintile in choppy
    out["choppy_up_r5q"]=up[up.trend=="choppy"].groupby("r5q").apply(stat)
    out["rising_down_r5q"]=E[(E.trend=="rising")&(E.r1<0)].groupby("r5q").apply(stat)
    # book extremes
    bk=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items(): bk.append(d.assign(coin=coin,w=w))
    B=pd.concat(bk); bd=B.groupby("day")["book_return"].mean().dropna()
    q=bd.quantile([0.01,0.05,0.5,0.95,0.99])
    out["book_quantiles"]=q
    top=bd.sort_values()
    out["book_share_top20_days"]=float(top.tail(20).sum()/bd.sum())
    out["book_share_worst20_days"]=float(top.head(20).sum()/bd.sum())
    return out
