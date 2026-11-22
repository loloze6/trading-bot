def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drift={}
    for coin,wins in data["bars"].items():
        for h in (5,20):
            nr=[]
            for w,b in wins.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                nr+=list(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=np.mean(nr)
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            n=len(c)
            r1=pd.Series(c).pct_change()
            z=(r1/r1.rolling(20).std().shift(1)).values
            r90=(pd.Series(c)/pd.Series(c).shift(90)-1).values
            for H in (5,20):
                for start in range(0,n,H):
                    for t in range(start,min(start+H,n)):
                        if abs(f[t])>=2:
                            rows.append({"H":H,"coin":coin,"year":yr[t],"f":f[t],"side":"up" if f[t]>0 else "down","z":z[t],"r90":r90[t],
                                         "u":(c[t+H]/c[t]-1-drift[(coin,H)]) if t+H<n else np.nan}); break
    d=pd.DataFrame(rows)
    def welch(g):
        a=g.loc[g.side=="up","u"].dropna(); bb=g.loc[g.side=="down","u"].dropna()
        if len(a)<3 or len(bb)<3: return pd.Series({"n_up":len(a),"n_dn":len(bb)})
        return pd.Series({"n_up":len(a),"n_dn":len(bb),"mean_up":a.mean(),"t_up":a.mean()/(a.std()/np.sqrt(len(a))),"mean_dn":bb.mean(),"t_dn":bb.mean()/(bb.std()/np.sqrt(len(bb))),"diff":a.mean()-bb.mean(),"t":stats.ttest_ind(a,bb,equal_var=False)[0]})
    res={}
    for H in (5,20):
        g=d[d.H==H].copy()
        res["H%d_overall"%H]=welch(g).to_frame().T
        g["fq"]=g.groupby("side")["f"].transform(lambda s:pd.qcut(s.abs().rank(method="first"),4,labels=False))
        res["H%d_by_fq"%H]=g.groupby("fq").apply(welch)
        res["H%d_by_coin"%H]=g.groupby("coin").apply(welch)
        res["H%d_by_year"%H]=g.groupby("year").apply(welch)
        g["r90q"]=pd.qcut(g["r90"],6,labels=False)
        res["H%d_by_r90_sextile"%H]=g.groupby("r90q").agg(n=("u","count"),r90_mean=("r90","mean"),u_mean=("u","mean"),u_t=("u",lambda x:x.mean()/(x.std()/np.sqrt(x.count()))))
    return res
