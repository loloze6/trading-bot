def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "loc":(c-b["low"])/(b["high"]-b["low"]),"fc":b["forecast"],"reg":b["regime"]})
            for h in [1,2,3,5]:
                d[f"r{h}"]=c.shift(-h)/c-1
            d["r1prev"]=c/c.shift(1)-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["r1"].mean()
    D["dr"]=D["coin"].map(drift)
    for h in [1,2,3,5]:
        D[f"u{h}"]=h*D["dr"]-D[f"r{h}"]   # short unusual move
    D["locbin"]=pd.cut(D["loc"],[0,0.25,0.5,0.75,0.9,1.0001],include_lowest=True)
    out={}
    def agg(g,col="u1"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["regime_counts"]=D["reg"].value_counts()
    out["by_reg_locbin_u1"]=D.groupby(["reg","locbin"],observed=True).apply(agg)
    C=D[D["fc"]<0]
    out["cases_by_coin"]=C.groupby("coin").apply(agg)
    out["cases_by_window"]=C.groupby(["coin","w"]).apply(agg)
    out["cases_by_year"]=C.groupby("year").apply(agg)
    C=C.copy(); C["fq"]=pd.qcut(C["fc"].abs(),4,labels=False)
    out["cases_by_fq"]=C.groupby("fq").apply(agg)
    out["cases_horizons"]=pd.DataFrame({h:agg(C,f"u{h}") for h in [1,2,3,5]})
    C["prevup"]=C["r1prev"]>0
    out["cases_by_prevday_up"]=C.groupby("prevup").apply(agg)
    out["cases_by_loc"]=C.groupby("locbin",observed=True).apply(agg)
    return out
