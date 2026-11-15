def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"].astype(float)
            d=c.diff()
            up=d.clip(lower=0).ewm(alpha=1/14,adjust=False,min_periods=14).mean()
            dn=(-d.clip(upper=0)).ewm(alpha=1/14,adjust=False,min_periods=14).mean()
            rsi=100-100/(1+up/dn)
            r14=c/c.shift(14)-1
            r60=c/c.shift(60)-1
            yr=pd.to_datetime(df["timestamp"]).dt.year
            for h in [5,10]:
                fr=(c.shift(-h)/c-1).values
                for i in np.arange(0,len(df),h):
                    if np.isnan(fr[i]): continue
                    rows.append(dict(coin=coin,w=w,h=h,rsi=rsi.iloc[i],fc=df["forecast"].iloc[i],r14=r14.iloc[i],r60=r60.iloc[i],yr=yr.iloc[i],fr=fr[i]))
    R=pd.DataFrame(rows)
    R["ex"]=R["fr"]-R.groupby(["coin","h"])["fr"].transform("mean")
    R=R.dropna(subset=["rsi"])
    def agg(g):
        n=len(g); m=g["ex"].mean()
        return pd.Series(dict(n=n,mean=m,t=m/(g["ex"].std()/np.sqrt(n)) if n>2 else np.nan))
    out={}
    F=R[R.fc<0].copy()
    F["fq"]=pd.qcut(F.fc.rank(method="first"),4,labels=["most_extreme","q2","q3","mildest"])
    out["fc_quartile_by_h"]=F.groupby(["h","fq"]).apply(agg).unstack(0)
    out["fc_quartile_fc_mean"]=F.groupby("fq")["fc"].mean()
    R10=R[R.h==10]
    out["h10_coin_rsi>70"]=R10[R10.rsi>70].groupby("coin").apply(agg)
    out["h10_coin_fc<=-5"]=R10[R10.fc<=-5].groupby("coin").apply(agg)
    # r14 graded continuation
    for h in [5,10]:
        X=R[R.h==h].dropna(subset=["r14"]).copy()
        X["q"]=pd.qcut(X.r14,5,labels=["q1low","q2","q3","q4","q5high"])
        out[f"h{h}_r14_quintile"]=X.groupby("q").apply(agg)
        out[f"h{h}_spearman_r14"]=pd.Series(stats.spearmanr(X.r14,X.ex)[:2],index=["rho","p"])
    # rsi>60 split by r60 regime
    X=R[(R.h==10)].dropna(subset=["r60"]).copy()
    X["reg"]=np.where(X.r60>0,"up60","down60")
    X["rb"]=pd.cut(X.rsi,[0,40,50,60,70,100])
    out["h10_reg60_rb"]=X.groupby(["reg","rb"]).apply(agg).unstack(0)
    # book decomposition
    D=[]
    for coin,wins in data["days"].items():
        for w,df in wins.items():
            D.append(df.assign(coin=coin,w=w))
    D=pd.concat(D)
    # position at day end from bars
    P=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            P.append(pd.DataFrame(dict(coin=coin,w=w,pos=df["postRebalance_current_allocation"].astype(float).values,
                                       nxt=(df["close"].shift(-1)/df["close"]-1).values)))
    P=pd.concat(P).dropna()
    mu=P.groupby("coin")["nxt"].transform("mean")
    P["mkt"]=P.pos*mu; P["gain"]=P.pos*P.nxt
    out["book_decomp_by_coin"]=P.groupby("coin")[["pos","gain","mkt"]].mean().assign(timing=lambda x:x.gain-x.mkt)
    out["book_decomp_all"]=P[["pos","gain","mkt"]].mean()
    out["share_bars_short"]=(P.pos<0).mean()
    return out
