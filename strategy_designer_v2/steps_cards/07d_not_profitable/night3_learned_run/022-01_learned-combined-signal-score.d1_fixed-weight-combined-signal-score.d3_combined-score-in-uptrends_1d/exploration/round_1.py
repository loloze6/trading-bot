import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            df=pd.DataFrame({
                "coin":coin,"win":w,
                "fwd":c.shift(-H)/c-1,
                "fwd20":c.shift(-20)/c-1,
                "fc":b["forecast"].astype(float),
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "reg":b["regime"],
                "mom28":c/c.shift(28)-1,
                "rev1":-r1,
                "near90":c/c.rolling(90,min_periods=60).max()-1,
                "nvol30":-r1.rolling(30).std(),
                "pos":np.arange(len(b))})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    g=A[A.pos%H==0].dropna(subset=["fwd"]).copy()
    g["drift"]=g.groupby("coin")["fwd"].transform("mean")
    g["ex"]=g["fwd"]-g["drift"]
    out={}
    tr=g[(g.reg=="trending")&(g.fc!=0)].copy()
    tr["side"]=np.sign(tr.fc)
    def summ(x,col="ex"):
        v=x[col].dropna()
        return pd.Series({"n":len(v),"mean_%":v.mean()*100,"t":v.mean()/(v.std()/np.sqrt(len(v))) if len(v)>2 else np.nan})
    out["trend_by_side_excess"]=tr.groupby("side").apply(summ)
    tr["q"]=pd.qcut(tr.fc.rank(method="first"),5,labels=False)
    out["trend_fc_quintile"]=tr.groupby("q").apply(summ)
    # features on all grid and trending grid: t of correlation with ex, per-coin z
    res=[]
    for f in ["mom28","rev1","near90","nvol30"]:
        for lab,s in [("all",g),("trend",g[g.reg=="trending"]),("down",g[g.reg!="trending"])]:
            s=s.dropna(subset=[f,"ex"]).copy()
            z=s.groupby("coin")[f].transform(lambda x:(x-x.mean())/x.std())
            rr,p=stats.pearsonr(z,s.ex)
            n=len(s); t=rr*np.sqrt((n-2)/(1-rr**2))
            res.append({"feat":f,"set":lab,"n":n,"corr":rr,"t":t})
    out["feature_vs_fwd5"]=pd.DataFrame(res)
    # mom28 quintiles all grid, 5d and 20d
    s=g.dropna(subset=["mom28"]).copy()
    s["mq"]=s.groupby("coin")["mom28"].transform(lambda x:pd.qcut(x.rank(method="first"),5,labels=False))
    s["ex20"]=s["fwd20"]-s.groupby("coin")["fwd20"].transform("mean")
    out["mom28_quintile_5d"]=s.groupby("mq").apply(summ)
    s2=A[A.pos%20==0].dropna(subset=["fwd20","mom28","near90"]).copy()
    s2["ex20"]=s2.fwd20-s2.groupby("coin")["fwd20"].transform("mean")
    s2["mq"]=s2.groupby("coin")["mom28"].transform(lambda x:pd.qcut(x.rank(method="first"),5,labels=False))
    s2["nq"]=s2.groupby("coin")["near90"].transform(lambda x:pd.qcut(x.rank(method="first"),5,labels=False))
    out["mom28_quintile_20d"]=s2.groupby("mq").apply(lambda x:summ(x,"ex20"))
    out["near90_quintile_20d"]=s2.groupby("nq").apply(lambda x:summ(x,"ex20"))
    # book by side
    D=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float).values; a=b["postRebalance_current_allocation"].astype(float).values
            gain=a[:-1]*(c[1:]/c[:-1]-1)
            D.append(pd.DataFrame({"side":np.sign(a[:-1]),"gain":gain,"coin":coin}))
    D=pd.concat(D)
    out["bar_gain_by_side_bps"]=D.groupby("side")["gain"].agg(["count","mean","sum"]).assign(mean_bps=lambda x:x["mean"]*1e4)
    out["bar_gain_by_coin_bps"]=D.groupby("coin")["gain"].mean()*1e4
    out["mean_abs_alloc"]=float(A.alloc.abs().mean())
    out["share_trending"]=float((A.reg=="trending").mean())
    return out
