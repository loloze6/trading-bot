def explore(data):
    import numpy as np, pandas as pd
    H=10
    rows=[]; drows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            df=pd.DataFrame(index=b.index)
            df["coin"]=coin; df["w"]=w
            df["ret28"]=c/c.shift(28)-1
            df["prox"]=c/c.rolling(28).max()
            df["ret5"]=c/c.shift(5)-1
            df["r1"]=r1
            df["vol20"]=r1.rolling(20).std()
            df["volratio"]=r1.rolling(10).std()/r1.rolling(60,min_periods=30).std()
            rng=(hi-lo)/c
            df["rngratio"]=rng.rolling(5).mean()/rng.rolling(60,min_periods=30).mean()
            df["vratio"]=v.rolling(5).mean()/v.rolling(60,min_periods=30).mean()
            df["fwd"]=c.shift(-H)/c-1
            df["fwd1"]=c.shift(-1)/c-1
            df["regime"]=b["regime"].values
            df["alloc"]=b["postRebalance_current_allocation"].astype(float)
            df["grid"]=(np.arange(len(b))%H==0)
            ts=pd.to_datetime(b["timestamp"])
            df["wd"]=ts.dt.weekday.values; df["yr"]=ts.dt.year.values; df["day"]=ts.dt.floor("D").values
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
        x=g[col].dropna(); n=len(x); m=x.mean() if n else np.nan
        t=m/(x.std()/np.sqrt(n)) if n>2 else np.nan
        return pd.Series({"n":n,"mean":m,"t":t})
    def daysumm(g):
        s=g.groupby("day")["ex"].sum(); n=len(g); nd=len(s)
        m=g["ex"].mean()
        se=np.sqrt((( s - g.groupby("day")["ex"].count()*m)**2).sum())/n if n>2 else np.nan
        return pd.Series({"n":n,"days":nd,"mean":m,"t_day":m/se if se else np.nan})
    def q(s,k): 
        r=s.rank(method="first")
        return pd.qcut(r,k,labels=False) if r.notna().sum()>=k else r*np.nan
    out={}
    def tr(name,f):
        try: out[name]=f()
        except Exception as e: out[name]="err "+str(e)[:80]
    G["in"]=G.ret28>0
    tr("regime_on_off",lambda: G.groupby("in").apply(daysumm))
    G["r28q"]=G.groupby("coin")["ret28"].transform(lambda s:q(s,5))
    tr("by_ret28_quintile",lambda: G.groupby("r28q").apply(daysumm))
    G["vq"]=G.groupby("coin")["volratio"].transform(lambda s:q(s,3))
    neg=G[G.ret28<0]
    tr("neg28_by_volratio_tercile",lambda: neg.groupby("vq").apply(daysumm))
    tr("corr_ret28_ex_neg_calm",lambda: float(neg[neg.vq==0][["ret28","ex"]].corr().iloc[0,1]))
    tr("corr_ret28_ex_neg_hot",lambda: float(neg[neg.vq==2][["ret28","ex"]].corr().iloc[0,1]))
    G["pq"]=G.groupby("coin")["prox"].transform(lambda s:q(s,5))
    tr("by_prox_quintile_all",lambda: G.groupby("pq").apply(daysumm))
    tr("in_by_volratio_tercile",lambda: G[G["in"]].groupby("vq").apply(daysumm))
    tr("newhigh_in_by_volratio",lambda: G[G["in"]&(G.prox>=1-1e-9)].groupby("vq").apply(daysumm))
    G["rq"]=G.groupby("coin")["rngratio"].transform(lambda s:q(s,3))
    tr("by_rngratio_tercile",lambda: G.groupby("rq").apply(daysumm))
    G["vvq"]=G.groupby("coin")["vratio"].transform(lambda s:q(s,3))
    tr("by_volumeratio_tercile",lambda: G.groupby("vvq").apply(daysumm))
    tr("in_by_volumeratio_tercile",lambda: G[G["in"]].groupby("vvq").apply(daysumm))
    G["q5"]=G.groupby("coin")["ret5"].transform(lambda s:q(s,5))
    tr("by_ret5_quintile",lambda: G.groupby("q5").apply(daysumm))
    tr("by_coin_in",lambda: G[G["in"]].groupby("coin").apply(summ))
    tr("by_year_all",lambda: G.groupby("yr").apply(summ))
    A["z"]=A.r1/A.vol20.shift(1)
    A["zb"]=pd.cut(A.z,[-99,-2,-1,1,2,99])
    tr("next_day_after_z",lambda: A.groupby("zb").apply(lambda g: summ(g,"fwd1")))
    A["mu10"]=A.coin.map(mu)
    A["ex10"]=A.fwd-A.mu10
    tr("next10_after_z_grid",lambda: A[A.grid].groupby("zb").apply(lambda g: summ(g,"ex10")))
    D=pd.concat(drows,ignore_index=True)
    tr("coin_ret_by_weekday",lambda: D.groupby("wd").apply(lambda g: summ(g,"coin_return")))
    bk=D.groupby(["w","day"])["book_return"].mean().reset_index()
    bk["wd"]=pd.to_datetime(bk["day"]).dt.weekday
    tr("book_ret_by_weekday",lambda: bk.groupby("wd").apply(lambda g: summ(g,"book_return")))
    bk["yr"]=pd.to_datetime(bk["day"]).dt.year
    tr("book_by_year",lambda: bk.groupby("yr").apply(lambda g: summ(g,"book_return")))
    bk2=bk.dropna(subset=["book_return"]).copy()
    lo_,hi_=bk2.book_return.quantile([0.05,0.95])
    tr("book_extreme_share_of_total",lambda: pd.Series({"top5pct_sum":bk2[bk2.book_return>=hi_].book_return.sum(),"bot5pct_sum":bk2[bk2.book_return<=lo_].book_return.sum(),"all_sum":bk2.book_return.sum()}))
    return out
