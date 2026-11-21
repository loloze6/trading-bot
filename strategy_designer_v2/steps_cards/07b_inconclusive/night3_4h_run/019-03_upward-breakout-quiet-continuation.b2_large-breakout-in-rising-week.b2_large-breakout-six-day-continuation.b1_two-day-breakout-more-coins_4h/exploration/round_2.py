def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=36
    rows=[]; drift={}; usual={}
    for coin,wins in data["bars"].items():
        rs=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            rs+=list(c[idx+H]/c[idx]-1)
        drift[coin]=np.mean(rs); usual[coin]=np.std(rs,ddof=1)
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            hh=b["high"].rolling(12).max().shift(1)
            rng=(b["high"]-b["low"]).rolling(180,min_periods=45).mean()
            raw=((b["close"]-hh)/rng).values
            r7=(b["close"]/b["close"].shift(42)-1).values
            r7n=((b["close"]/b["close"].shift(42)-1)/(rng/b["close"])).values
            base=0.0; cells=set(); n=len(c)
            for t in range(n):
                if f[t]<=0: base=0.0; continue
                if f[t]<base: base=f[t]
                if f[t]-base>=2:
                    base=f[t]; cell=t//H
                    if cell in cells: continue
                    cells.add(cell)
                    if t+H>=n: continue
                    u=c[t+H]/c[t]-1-drift[coin]
                    rows.append({"coin":coin,"year":pd.Timestamp(b["timestamp"].iloc[t]).year,"raw":raw[t],"r7":r7[t],"r7n":r7n[t],"u":u,"s":u/usual[coin],"tot":c[t+H]/c[t]-1})
    df=pd.DataFrame(rows).dropna()
    out={}
    med=df.raw.median()
    hi=df[df.raw>med]; lo=df[df.raw<=med]
    out["raw_median"]=float(med)
    out["raw_split"]=pd.DataFrame({"n":[len(hi),len(lo)],"mean_u":[hi.u.mean(),lo.u.mean()],"mean_s":[hi.s.mean(),lo.s.mean()],"mean_tot":[hi.tot.mean(),lo.tot.mean()]},index=["larger","smaller"])
    out["raw_split_welch_t"]=float(stats.ttest_ind(hi.u,lo.u,equal_var=False).statistic)
    out["raw_split_diff"]=float(hi.u.mean()-lo.u.mean())
    def g(x):
        h=x[x.raw>med]; l=x[x.raw<=med]
        return pd.Series({"n_hi":len(h),"hi":h.u.mean(),"n_lo":len(l),"lo":l.u.mean(),"diff":h.u.mean()-l.u.mean()})
    out["raw_split_by_year"]=df.groupby("year").apply(g)
    out["raw_split_by_coin"]=df.groupby("coin").apply(g)
    out["share_coins_diff_pos"]=float((df.groupby("coin").apply(g)["diff"]>0).mean())
    df["rq"]=pd.qcut(df.raw.rank(method="first"),3,labels=False)
    df["wq"]=pd.qcut(df.r7.rank(method="first"),3,labels=False)
    out["raw_x_r7_mean"]=df.pivot_table(index="rq",columns="wq",values="u",aggfunc="mean")
    out["raw_x_r7_n"]=df.pivot_table(index="rq",columns="wq",values="u",aggfunc="count")
    out["spearman_raw_s"]=float(stats.spearmanr(df.raw,df.s).correlation)
    out["spearman_r7n_s"]=float(stats.spearmanr(df.r7n,df.s).correlation)
    df["sq"]=pd.qcut(df.r7n.rank(method="first"),5,labels=False)
    out["by_r7_in_ranges_q"]=df.groupby("sq").agg(n=("u","size"),mean=("u","mean"),r7n=("r7n","mean"))
    return out
