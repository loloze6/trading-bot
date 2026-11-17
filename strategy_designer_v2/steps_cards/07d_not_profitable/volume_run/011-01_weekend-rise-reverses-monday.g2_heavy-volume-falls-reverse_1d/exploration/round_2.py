def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    coin_mean={}
    for c in bars:
        coin_mean[c]=pd.concat([b["close"].pct_change().dropna() for b in bars[c].values()]).mean()
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True).copy()
            cl=b["close"]; v=b["volume"]; r=cl.pct_change()
            b["vr"]=v/v.rolling(60,min_periods=20).mean()
            b["vs"]=r/r.rolling(20,min_periods=10).std()
            for h in [1,2,3,5,7]:
                b[f"f{h}"]=cl.shift(-h)/cl-1-h*coin_mean[c]
            # daily-step excess for days 2..5 after
            for k in [2,3,4,5]:
                b[f"d{k}"]=cl.shift(-k)/cl.shift(-k+1)-1-coin_mean[c]
            b["coin"]=c; b["w"]=w
            b["alloc"]=b["postRebalance_current_allocation"]
            b["ret20"]=cl/cl.shift(20)-1
            rows.append(b)
    B=pd.concat(rows)
    act=B[B.forecast>0].copy()
    out={}
    def tt(x):
        x=x.dropna(); return pd.Series({"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)),"n":len(x)})
    out["active: excess on each later day"]=pd.DataFrame({k:tt(act[k]) for k in ["f1","d2","d3","d4","d5"]})
    # vr quintiles among active
    act["vrq"]=pd.qcut(act.vr,4,labels=["q1","q2","q3","q4"])
    out["active by vr quartile"]=act.groupby("vrq")[["vr","f1","f3","f5"]].mean().join(act.groupby("vrq").size().rename("n"))
    act["fq"]=pd.qcut(act.forecast.rank(method="first"),4,labels=["q1","q2","q3","q4"])
    out["active by forecast quartile"]=act.groupby("fq")[["forecast","alloc","vr","f1","f3"]].mean()
    out["corr f1"]=pd.Series({"forecast":stats.spearmanr(act.forecast,act.f1,nan_policy="omit")[0],
        "vr":stats.spearmanr(act.vr,act.f1,nan_policy="omit")[0],
        "vs":stats.spearmanr(act.vs,act.f1,nan_policy="omit")[0],
        "corr f3 vr":stats.spearmanr(act.vr,act.f3,nan_policy="omit")[0]})
    # heavy volume up days: what follows
    up=B[(B.vs>0)&(B.vr>=1.5)]
    out["heavy-vol up days"]=up[["f1","f3","f5"]].agg(["mean","count"])
    # trend context
    act["tr"]=np.where(act.ret20>0,"20d up","20d down")
    out["active by 20d trend"]=act.groupby("tr")[["f1","f3","f5"]].mean().join(act.groupby("tr").size().rename("n"))
    # non-overlapping 3-day grid for active bars
    g=B[B.groupby(["coin","w"]).cumcount()%3==0]
    ga=g[(g.vr>=1.5)&(g.vs<0)]
    out["grid3 heavy-down f3"]=tt(ga.f3)
    return out
