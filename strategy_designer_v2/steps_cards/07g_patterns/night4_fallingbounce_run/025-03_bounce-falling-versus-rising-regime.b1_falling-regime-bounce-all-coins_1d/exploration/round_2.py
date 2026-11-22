def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std().shift(1)
            z=r/sd
            r90=c/c.shift(90)-1
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"z":z,"r90":r90,"f5":f5,"f1":f1,
                             "reg":b["regime"],"wd":ts.dt.weekday,"yr":ts.dt.year,"day":ts.dt.normalize(),
                             "pos":b["postRebalance_current_allocation"]})
            df["grid"]=(np.arange(len(df))%5==0)
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    out={}
    # weekday: average across coins per day first (removes cross-coin correlation)
    A["u1"]=A["f1"]-A.groupby("coin")["f1"].transform("mean")
    dd=A.groupby(["w","day"]).agg(u1=("u1","mean"),wd=("wd","first"),yr=("yr","first")).dropna()
    def tt(x):
        x=x.dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out["weekday_daymean"]=dd.groupby("wd")["u1"].apply(tt).unstack()
    dd["tf"]=dd["wd"].isin([1,3,4]).map({True:"TueThuFri",False:"other"})
    piv=dd.groupby(["yr","tf"])["u1"].mean().unstack()
    piv["diff"]=piv["TueThuFri"]-piv["other"]
    out["weekday_split_by_year"]=piv
    g=A[A.grid].copy()
    g["u5"]=g["f5"]-g["coin"].map(g.groupby("coin")["f5"].mean())
    # rise continuation in trending, by year, z>1
    tr=g[(g.reg=="trending")&(g.z>1)]
    out["trend_rise_by_year"]=tr.groupby("yr")["u5"].apply(tt).unstack()
    out["trend_rise_vs_z_spearman"]=pd.Series(dict(zip(["rho","p"],stats.spearmanr(tr["z"],tr["u5"],nan_policy="omit"))))
    # falling regime, down/flat days continuation by year
    mr=g[(g.reg=="mean_reversion")&(g.z<=0)&(g.z>-1)]
    out["fall_smalldown_by_year"]=mr.groupby("yr")["u5"].apply(tt).unstack()
    # graded by 90-day return across all grid bars (trend on 90 days)
    g["r90q"]=g.groupby("coin")["r90"].transform(lambda v: pd.qcut(v.rank(method="first"),5,labels=False))
    out["r90_quintile_u5"]=g.groupby("r90q")["u5"].apply(tt).unstack()
    out["r90_quintile_by_year_mean"]=g.groupby(["yr","r90q"])["u5"].mean().unstack()
    # book's largest days: side of the position
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            D.append(d.assign(coin=coin,w=w))
    D=pd.concat(D,ignore_index=True)
    bd=D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    A["side"]=np.sign(A["pos"].fillna(0))
    ps=A.groupby(["w","day"])["side"].agg(lambda s:(s>0).mean()-(s<0).mean())
    bd=bd.join(ps.rename("netlong"),how="left")
    q=bd["book_return"].rank(pct=True)
    bd["grp"]=pd.cut(q,[0,0.02,0.98,1],labels=["worst2%","mid","best2%"])
    out["book_extremes"]=bd.groupby("grp",observed=True).agg(n=("book_return","size"),book=("book_return","mean"),hold=("coin_return","mean"),netlong=("netlong","mean"))
    return out
