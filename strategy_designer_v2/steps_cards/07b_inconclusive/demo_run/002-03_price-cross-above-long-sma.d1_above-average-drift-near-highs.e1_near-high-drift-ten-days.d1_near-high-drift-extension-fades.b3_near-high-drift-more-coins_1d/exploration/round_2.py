def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values; n=len(df); h=10
            r20=df.get("debug_info.components.range20.post_pipeline_value",pd.Series([np.nan]*n))
            raw=df.get("debug_info.components.ext30.last_history_value",pd.Series([np.nan]*n))
            for i in range(0,n-h,h):
                rows.append(dict(coin=coin,w=w,year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                    reg=df["regime"].iloc[i],r20=r20.iloc[i],raw=raw.iloc[i],ret=c[i+h]/c[i]-1))
    g=pd.DataFrame(rows)
    g["ex"]=g["ret"]-g.groupby("coin")["ret"].transform("mean")
    t=g[g.reg=="trending"].dropna(subset=["r20","raw"]).copy()
    out={}
    t["q"]=pd.qcut(t["r20"],5,labels=False)
    top=t[t.q==4]; rest=t[t.q<4]
    out["top_vs_rest"]=pd.DataFrame([dict(n_top=len(top),ex_top=top.ex.mean(),med_top=top.ex.median(),
        n_rest=len(rest),ex_rest=rest.ex.mean(),med_rest=rest.ex.median(),
        welch_t=stats.ttest_ind(top.ex,rest.ex,equal_var=False).statistic)])
    out["top_by_year"]=t.groupby("year").apply(lambda d: pd.Series(dict(n=len(d),top_minus_rest=d[d.q==4].ex.mean()-d[d.q<4].ex.mean(),
        r20t=stats.linregress(d.r20,d.ex).slope/stats.linregress(d.r20,d.ex).stderr)))
    out["share_coins_top_pos"]=float(np.mean([v[v.q==4].ex.mean()>v[v.q<4].ex.mean() for k,v in t.groupby("coin")]))
    X=np.column_stack([np.ones(len(t)),t.r20,t.raw])
    b,res,_,_=np.linalg.lstsq(X,t.ex,rcond=None)
    e=t.ex-X@b; s2=(e@e)/(len(t)-3); cov=s2*np.linalg.inv(X.T@X)
    out["joint_reg"]=pd.DataFrame(dict(coef=b,t=b/np.sqrt(np.diag(cov))),index=["c","r20","raw30"])
    w=t.copy(); w["ex_w"]=w.ex.clip(w.ex.quantile(.01),w.ex.quantile(.99))
    r=stats.linregress(w.r20,w.ex_w); out["r20_winsor_t"]=r.slope/r.stderr
    rk=stats.spearmanr(t.r20,t.ex); out["r20_spearman"]=pd.Series(dict(rho=rk.correlation,p=rk.pvalue))
    return out
