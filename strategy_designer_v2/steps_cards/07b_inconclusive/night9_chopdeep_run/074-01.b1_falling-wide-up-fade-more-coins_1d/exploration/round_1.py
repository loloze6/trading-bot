def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            allr.append(b["close"].pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; rng=(b["high"]-b["low"])
            ratio=rng/rng.rolling(20,min_periods=20).mean()
            clv=(c-b["low"])/rng.replace(0,np.nan)
            body=(c-b["open"])/rng.replace(0,np.nan)
            upret=c.pct_change()
            r1=c.shift(-1)/c-1; r2=c.shift(-2)/c-1; r3=c.shift(-3)/c-1
            vol10=c.pct_change().rolling(10).std()
            for i in np.where(b["regime"]=="mean_reversion")[0]:
                rows.append(dict(coin=coin,w=w,year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                    day=pd.Timestamp(b["timestamp"].iloc[i]).normalize(),
                    ratio=ratio.iloc[i],fc=b["forecast"].iloc[i],clv=clv.iloc[i],body=body.iloc[i],
                    up=upret.iloc[i],e1=-(r1.iloc[i]-mu),e2=-(r2.iloc[i]-2*mu),e3=-(r3.iloc[i]-3*mu),
                    vol=vol10.iloc[i]))
    d=pd.DataFrame(rows)
    def st(g,col="e1"):
        x=g[col].dropna()
        if len(x)<5: return pd.Series(dict(n=len(x),mean=x.mean(),t=np.nan))
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x)))))
    out={}
    out["all"]=pd.DataFrame({k:st(d,k) for k in ["e1","e2","e3"]}).T
    d["rq"]=pd.qcut(d["ratio"],5,labels=False)
    out["by_ratio_q"]=d.groupby("rq").apply(st)
    out["ratio_q_bounds"]=d.groupby("rq")["ratio"].agg(["min","max"])
    d["fq"]=pd.qcut(d["fc"].abs(),5,labels=False,duplicates="drop")
    out["by_absforecast_q"]=d.groupby("fq").apply(st)
    d["cq"]=pd.qcut(d["clv"],3,labels=["low","mid","high"])
    out["by_close_loc"]=d.groupby("cq").apply(st)
    d["uq"]=pd.qcut(d["up"],3,labels=["small","mid","big"])
    out["by_up_size"]=d.groupby("uq").apply(st)
    out["by_close_x_ratio"]=d.groupby(["cq",pd.qcut(d["ratio"],2,labels=["lo","hi"])]).apply(st)
    d["vq"]=pd.qcut(d["vol"],2,labels=["calm","agit"])
    out["by_vol"]=d.groupby("vq").apply(st)
    out["by_year"]=d.groupby("year").apply(st)
    out["by_coin"]=d.groupby("coin").apply(st)
    out["corr_ratio_e1"]=stats.spearmanr(d["ratio"],d["e1"],nan_policy="omit")[0]
    out["corr_up_e1"]=stats.spearmanr(d["up"],d["e1"],nan_policy="omit")[0]
    out["corr_clv_e1"]=stats.spearmanr(d["clv"],d["e1"],nan_policy="omit")[0]
    return out
