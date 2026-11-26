def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    H=5
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol30=r1.rolling(30,min_periods=15).std()
            gap=c/c.rolling(20,min_periods=20).max()-1
            ret60=c/c.shift(60)-1
            for i in range(0,len(b)-H,H):
                rows.append(dict(coin=coin,w=w,year=pd.Timestamp(b.loc[i,"timestamp"]).year,
                    day=str(pd.Timestamp(b.loc[i,"timestamp"]).date()),
                    fc=b.loc[i,"forecast"],reg=b.loc[i,"regime"],gap=gap[i],
                    fwd=c[i+H]/c[i]-1,vol=vol30[i],ret5p=c[i]/c[i-5]-1 if i>=5 else np.nan,
                    big=r1[i]/vol30[i] if vol30[i]>0 else np.nan))
    df=pd.DataFrame(rows)
    df["drift"]=df.groupby("coin")["fwd"].transform("mean")
    df["xs"]=-(df["fwd"]-df["drift"])
    df["medvol"]=df.groupby("coin")["vol"].transform("median")
    df["agit"]=np.where(df["vol"]>df["medvol"],"agitated","calm")
    cs=df[(df["fc"]<0)].copy()
    out={}
    def summ(g):
        d=g.groupby("day")["xs"].sum()
        n=len(g); 
        t=g["xs"].mean()/(d.std(ddof=1)/np.sqrt(len(d))*len(d)/n) if len(d)>2 else np.nan
        return pd.Series(dict(n=n,days=len(d),mean_xs=g["xs"].mean(),t=t,mean_fwd=g["fwd"].mean()))
    out["all"]=summ(cs).to_frame().T
    out["regimes_of_cases"]=cs["reg"].value_counts()
    out["by_coin"]=cs.groupby("coin").apply(summ)
    out["by_window"]=cs.groupby("w").apply(summ)
    out["by_year"]=cs.groupby("year").apply(summ)
    out["by_agit"]=cs.groupby("agit").apply(summ)
    cs["gq"]=pd.qcut(cs["gap"].rank(method="first"),5,labels=False)
    out["by_gap_quint"]=cs.groupby("gq").apply(summ).join(cs.groupby("gq")["gap"].mean())
    cs["fq"]=pd.qcut(cs["fc"].rank(method="first"),5,labels=False)
    out["by_fc_quint"]=cs.groupby("fq").apply(summ).join(cs.groupby("fq")["fc"].mean())
    cs["r5s"]=np.sign(cs["ret5p"])
    out["by_last5_sign"]=cs.groupby("r5s").apply(summ)
    cs["bigq"]=pd.qcut(cs["big"].rank(method="first"),4,labels=False)
    out["by_lastday_swing_q"]=cs.groupby("bigq").apply(summ).join(cs.groupby("bigq")["big"].mean())
    out["agit_x_gapq"]=cs.groupby(["agit","gq"]).apply(summ)
    out["corr_gap_xs"]=stats.spearmanr(cs["gap"],cs["xs"],nan_policy="omit")[0]
    return out
