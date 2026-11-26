def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=10
    rows=[]
    drows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            df=pd.DataFrame({"coin":coin,"w":w})
            df=pd.DataFrame(index=b.index)
            df["coin"]=coin; df["w"]=w
            df["ret28"]=c/c.shift(28)-1
            df["prox"]=c/c.rolling(28).max()
            df["proxlow"]=c/c.rolling(28).min()
            df["ret5"]=c/c.shift(5)-1
            df["r1"]=r1
            df["vol20"]=r1.rolling(20).std()
            df["volratio"]=r1.rolling(10).std()/r1.rolling(60,min_periods=30).std()
            rng=(hi-lo)/c
            df["rngratio"]=rng.rolling(5).mean()/rng.rolling(60,min_periods=30).mean()
            df["vratio"]=v.rolling(5).mean()/v.rolling(60,min_periods=30).mean()
            df["fwd"]=c.shift(-H)/c-1
            df["fwd1"]=c.shift(-1)/c-1
            df["regime"]=b["regime"]
            df["fc"]=b["forecast"]
            df["alloc"]=b["postRebalance_current_allocation"]
            df["grid"]=(np.arange(len(b))%H==0)
            df["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            rows.append(df)
        for w,d in data["days"][coin].items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w
            dd["wd"]=pd.to_datetime(dd["day"]).dt.weekday
            drows.append(dd)
    A=pd.concat(rows,ignore_index=True)
    G=A[A.grid & A.fwd.notna()].copy()
    mu=G.groupby("coin")["fwd"].mean()
    G["ex"]=G["fwd"]-G["coin"].map(mu)
    def summ(g,col="ex"):
        x=g[col].dropna()
        n=len(x); m=x.mean()
        t=m/(x.std()/np.sqrt(n)) if n>2 else np.nan
        return pd.Series({"n":n,"mean":m,"t":t})
    out={}
    G["in"]=G.ret28>0
    out["regime_on_off"]=G.groupby("in").apply(summ)
    # ret28 quintiles
    G["r28q"]=G.groupby("coin")["ret28"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["by_ret28_quintile"]=G.groupby("r28q").apply(summ)
    G["vq"]=G.groupby("coin")["volratio"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    # calm decline per brief: ret28<0, by vol tercile
    neg=G[G.ret28<0]
    out["neg28_by_volratio_tercile"]=neg.groupby("vq").apply(summ)
    out["corr_ret28_ex_neg_calm"]=float(neg[neg.vq==0][["ret28","ex"]].corr().iloc[0,1])
    G["pq"]=G.groupby("coin")["prox"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["by_prox_quintile_all"]=G.groupby("pq").apply(summ)
    out["in_by_volratio_tercile"]=G[G["in"]].groupby("vq").apply(summ)
    G["rq"]=G.groupby("coin")["rngratio"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["by_rngratio_tercile"]=G.groupby("rq").apply(summ)
    G["vvq"]=G.groupby("coin")["vratio"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["by_volumeratio_tercile"]=G.groupby("vvq").apply(summ)
    G["q5"]=G.groupby("coin")["ret5"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["by_ret5_quintile"]=G.groupby("q5").apply(summ)
    out["by_coin_in"]=G[G["in"]].groupby("coin").apply(summ)
    out["by_window_all"]=G.groupby("w").apply(summ)
    # daily: after large daily moves (z of r1/vol20) next day return
    A["z"]=A.r1/A.vol20.shift(1)
    A["zb"]=pd.cut(A.z,[-99,-2,-1,1,2,99])
    out["next_day_after_z"]=A.groupby("zb").apply(lambda g: summ(g,"fwd1"))
    D=pd.concat(drows,ignore_index=True)
    out["coin_ret_by_weekday"]=D.groupby("wd").apply(lambda g: summ(g,"coin_return"))
    bk=D.groupby(["w","day"])["book_return"].mean().reset_index()
    bk["wd"]=pd.to_datetime(bk["day"]).dt.weekday
    out["book_ret_by_weekday"]=bk.groupby("wd").apply(lambda g: summ(g,"book_return"))
    return out
