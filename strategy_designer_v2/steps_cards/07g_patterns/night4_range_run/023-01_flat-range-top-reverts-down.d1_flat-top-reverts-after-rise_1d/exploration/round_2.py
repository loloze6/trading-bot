def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            hi=c.rolling(30).max(); lo=c.rolling(30).min()
            mid=(hi+lo)/2; rng=(hi-lo)
            pos=(c-mid)/(rng/2)
            flat=1-(c-c.shift(29)).abs()/rng
            fwd=c.shift(-5)/c-1
            fwd10=c.shift(-10)/c-1
            ts=pd.to_datetime(df["timestamp"])
            for i in range(0,len(df),5):
                rows.append(dict(coin=coin,w=w,wi=int(w[1:]),fwd=fwd[i],fwd10=fwd10[i] if i%10==0 else np.nan,
                    pos=pos[i],flat=flat[i],reg=df["regime"].iloc[i],yr=ts.iloc[i].year))
    d=pd.DataFrame(rows).dropna(subset=["fwd","pos"])
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    out={}
    def slope(g,col="ex"):
        g=g.dropna(subset=[col])
        if len(g)<10: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        r=stats.linregress(g["pos"],g[col])
        return pd.Series({"n":len(g),"slope":r.slope,"t":r.slope/r.stderr})
    mr=d[d.reg=="mean_reversion"].copy(); un=d[d.reg=="unknown"].copy()
    out["slope_by_regime"]=d.groupby("reg").apply(slope)
    out["slope_mr_by_coin"]=mr.groupby("coin").apply(slope)
    out["slope_mr_by_year"]=mr.groupby("yr").apply(slope)
    mr["half"]=np.where(mr.wi<=12,"w1-w12","w13-w24")
    out["slope_mr_by_half"]=mr.groupby("half").apply(slope)
    mr["fq"]=pd.qcut(mr["flat"],3,labels=False)
    out["slope_mr_by_flat"]=mr.groupby("fq").apply(slope)
    e=d.dropna(subset=["fwd10"]).copy()
    e["ex10"]=e["fwd10"]-e.groupby("coin")["fwd10"].transform("mean")
    out["slope10_by_regime"]=e.groupby("reg").apply(lambda g: slope(g,"ex10"))
    q=mr.copy(); q["pq"]=pd.qcut(q["pos"],5,labels=False)
    a=q[q.pq==4].ex; b=q[q.pq==0].ex
    t=stats.ttest_ind(a,b,equal_var=False)
    out["mr_top_minus_bottom"]=pd.Series({"diff":a.mean()-b.mean(),"t":t.statistic,"n_top":len(a),"n_bot":len(b)})
    # book days around largest gains/losses
    br=[]
    for coin,ws in data["days"].items():
        for w,df in ws.items():
            br.append(df[["book_return","coin_return"]].dropna())
    br=pd.concat(br)
    out["book_vs_coin_corr"]=pd.Series({"corr":br.book_return.corr(br.coin_return),"n":len(br),
        "book_mean":br.book_return.mean()})
    return out
