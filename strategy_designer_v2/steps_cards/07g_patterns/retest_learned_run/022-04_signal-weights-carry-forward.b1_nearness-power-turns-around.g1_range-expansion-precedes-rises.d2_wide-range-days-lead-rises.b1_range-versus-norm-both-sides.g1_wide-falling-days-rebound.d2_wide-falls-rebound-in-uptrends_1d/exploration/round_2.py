def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=3
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            r1=c.pct_change()
            rng=(h-l)/c.shift(1)
            df=pd.DataFrame({"coin":coin,"w":w,"r1":r1,"r30":c/c.shift(30)-1,
                "rngm":rng/rng.rolling(30).mean(),
                "volm":b["volume"]/b["volume"].rolling(30).mean(),
                "fc":b["forecast"],
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "fwd":c.shift(-H)/c-1,"fwd1":c.shift(-1)/c-1,"fwd7":c.shift(-7)/c-1})
            df["r1z"]=r1/r1.rolling(30).std()
            df=df.iloc[::H]
            rows.append(df)
    D=pd.concat(rows,ignore_index=True).dropna(subset=["fwd"])
    D["ex"]=D["fwd"]-D["coin"].map(D.groupby("coin")["fwd"].mean())
    out={}
    d=D.dropna(subset=["rngm","r1","r30","ex"]).copy()
    d["dn"]=d["r1"]<0
    d["q"]=d.groupby("coin")["rngm"].transform(lambda x:pd.qcut(x.rank(method="first"),5,labels=False))
    def tt(x): return pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/x.std()*np.sqrt(len(x))})
    out["down_q_by_r30sign"]=d[d.dn].groupby([d["r30"]>0,"q"])["ex"].apply(tt).unstack()
    top=d[d.dn&(d.q==4)]
    out["down_top_by_coin"]=top.groupby("coin")["ex"].apply(tt).unstack()
    out["down_top_by_year"]=top.groupby("yr")["ex"].apply(tt).unstack()
    # graded: signed range multiple: -sign(r1)*rngm ; slope among downdays
    dd=d[d.dn]
    s=stats.linregress(dd["rngm"],dd["ex"]); out["down_rngm_slope"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(dd)})
    s=stats.linregress(np.log(dd["rngm"]),dd["ex"]); out["down_logrngm_slope"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(dd)})
    # r1z reversal graded, by r30 sign
    e=D.dropna(subset=["r1z","r30","ex"])
    res=[]
    for k,g in e.groupby(e["r30"]>0):
        s=stats.linregress(g["r1z"],g["ex"]); res.append({"r30pos":k,"n":len(g),"slope":s.slope,"t":s.slope/s.stderr})
    out["r1z_slope_by_r30"]=pd.DataFrame(res)
    # r1z reversal by coin in downtrend
    e2=e[e.r30<=0]; res=[]
    for k,g in e2.groupby("coin"):
        s=stats.linregress(g["r1z"],g["ex"]); res.append({"coin":k,"n":len(g),"t":s.slope/s.stderr})
    out["r1z_down_by_coin"]=pd.DataFrame(res)
    # horizons for top down-range
    out["top_down_horizons"]=pd.Series({"fwd1":top["fwd1"].mean(),"fwd3":top["fwd"].mean(),"fwd7":top["fwd7"].mean(),"all_fwd1":D["fwd1"].mean(),"all_fwd3":D["fwd"].mean(),"all_fwd7":D["fwd7"].mean()})
    # volume multiple on down days
    v=D.dropna(subset=["volm","r1","ex"]); v=v[v.r1<0]
    s=stats.linregress(np.log(v["volm"]),v["ex"]); out["down_logvolm_slope"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(v)})
    # top down-range by forecast present (standardised forecast misses?)
    out["top_down_fc_bucket"]=top.groupby(pd.cut(top["fc"],[-0.1,0.001,10,21]))["ex"].apply(tt).unstack()
    return out
