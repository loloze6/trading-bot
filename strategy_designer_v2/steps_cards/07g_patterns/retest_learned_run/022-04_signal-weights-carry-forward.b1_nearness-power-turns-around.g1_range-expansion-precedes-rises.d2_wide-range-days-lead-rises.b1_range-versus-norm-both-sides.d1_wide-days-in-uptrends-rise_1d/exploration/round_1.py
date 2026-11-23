def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        grid_rets=[]
        tmp=[]
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; rng=(b["high"]-b["low"])
            ratio=rng/rng.rolling(30).mean()
            ret30=c/c.shift(30)-1
            r1=c/c.shift(1)-1
            vol30=r1.rolling(30).std()
            clv=(c-b["low"])/rng.replace(0,np.nan)
            fwd=c.shift(-3)/c-1
            idx=np.arange(0,len(b),3)
            d=pd.DataFrame({"ratio":ratio,"ret30":ret30,"r1":r1,"vol30":vol30,"clv":clv,"fwd":fwd,
                            "fc":b["forecast"],"wd":pd.to_datetime(b["timestamp"]).dt.weekday,"win":w}).iloc[idx]
            d=d[d["fwd"].notna()]
            tmp.append(d)
        d=pd.concat(tmp); d["coin"]=coin
        d["ex"]=d["fwd"]-d["fwd"].mean()
        # usual move
        d["z"]=d["ex"]/d["fwd"].std()
        rows.append(d)
    D=pd.concat(rows)
    def summ(g):
        x=g["ex"].dropna()
        return pd.Series({"n":len(x),"mean_ex_%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    D["up30"]=np.where(D["ret30"]>0,"up30","down30")
    E=D.dropna(subset=["ratio","ret30"])
    E["rq"]=pd.qcut(E["ratio"],5,labels=["q1","q2","q3","q4","q5"])
    out["ratio_quintile_x_regime"]=E.groupby(["up30","rq"]).apply(summ)
    sp={}
    for reg,g in E.groupby("up30"):
        r,p=stats.spearmanr(g["ratio"],g["ex"]); sp[reg+"_rho"]=r; sp[reg+"_p"]=p; sp[reg+"_n"]=len(g)
    out["spearman_ratio_ex"]=pd.Series(sp)
    W=E[E["ratio"]>1].copy()
    W["clvq"]=pd.qcut(W["clv"],3,labels=["low_close","mid_close","high_close"])
    out["wide_days_by_close_loc_x_regime"]=W.groupby(["up30","clvq"]).apply(summ)
    F=D.dropna(subset=["r1"]).copy()
    F["r1q"]=pd.qcut(F["r1"],5,labels=["q1","q2","q3","q4","q5"])
    out["day_return_quintile_x_regime"]=F.groupby(["up30","r1q"]).apply(summ)
    V=D.dropna(subset=["vol30"]).copy()
    V["vq"]=V.groupby("coin")["vol30"].transform(lambda s:pd.qcut(s,3,labels=False))
    out["vol_tercile_x_regime"]=V.groupby(["up30","vq"]).apply(summ)
    R=D.dropna(subset=["ret30"]).copy()
    R["r30q"]=pd.qcut(R["ret30"],5,labels=["q1","q2","q3","q4","q5"])
    out["ret30_quintile"]=R.groupby("r30q").apply(summ)
    out["weekday"]=D.groupby("wd").apply(summ)
    return out
