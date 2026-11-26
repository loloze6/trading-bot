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
            for i in range(0,len(b)-H,H):
                rows.append(dict(coin=coin,w=w,year=pd.Timestamp(b.loc[i,"timestamp"]).year,
                    day=str(pd.Timestamp(b.loc[i,"timestamp"]).date()),
                    fc=b.loc[i,"forecast"],gap=gap[i],fwd=c[i+H]/c[i]-1,vol=vol30[i]))
    df=pd.DataFrame(rows)
    df["drift"]=df.groupby("coin")["fwd"].transform("mean")
    df["xs"]=-(df["fwd"]-df["drift"])
    df["medvol"]=df.groupby("coin")["vol"].transform("median")
    df["agit"]=np.where(df["vol"]>df["medvol"],"agitated","calm")
    cs=df[(df["fc"]<0)].dropna(subset=["gap","vol"]).copy()
    cs["gapvol"]=cs["gap"]/cs["vol"]
    out={}
    def summ(g):
        d=g.groupby("day")["xs"].sum(); n=len(g)
        t=g["xs"].mean()/(d.std(ddof=1)/np.sqrt(len(d))*len(d)/n) if len(d)>2 else np.nan
        return pd.Series(dict(n=n,days=len(d),mean_xs=g["xs"].mean(),t=t))
    res=[]
    for a,g in [("all",cs)]+list(cs.groupby("agit")):
        for col in ["gap","fc","gapvol"]:
            med=g[col].median()
            big=g[g[col]<med]["xs"]; small=g[g[col]>=med]["xs"]
            res.append(dict(set=a,var=col,spearman=stats.spearmanr(g[col],g["xs"])[0],
                big_half=big.mean(),small_half=small.mean(),diff=big.mean()-small.mean(),
                welch_t=stats.ttest_ind(big,small,equal_var=False)[0]))
    out["halves"]=pd.DataFrame(res)
    cal=cs[cs["agit"]=="calm"].copy()
    cal["w_"]=cal["gap"].abs()/cal["gap"].abs().mean()*cal["xs"]
    d=cal.groupby("day")["w_"].sum()
    out["calm_gapweighted"]=pd.Series(dict(n=len(cal),days=len(d),mean=cal["w_"].mean(),
        t=cal["w_"].mean()/(d.std(ddof=1)/np.sqrt(len(d))*len(d)/len(cal))))
    out["calm_by_year"]=cal.groupby("year").apply(summ)
    out["calm_by_coin"]=cal.groupby("coin").apply(summ)
    cal["gq"]=pd.qcut(cal["gap"].rank(method="first"),3,labels=False)
    out["calm_gap_terc_by_year"]=cal.groupby(["gq","year"]).apply(summ)
    out["corr_fc_gap"]=stats.spearmanr(cs["fc"],cs["gap"])[0]
    return out
