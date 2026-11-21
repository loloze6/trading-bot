import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r1=c.pct_change()
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"win":w,"year":ts.dt.year,
                "fwd":c.shift(-H)/c-1,"fwd10":c.shift(-10)/c-1,
                "fc":b["forecast"].astype(float),"alloc":b["postRebalance_current_allocation"].astype(float),
                "reg":b["regime"],"mom28":c/c.shift(28)-1,"rev1":-r1,
                "near90":c/c.rolling(90,min_periods=60).max()-1,"nvol30":-r1.rolling(30).std(),
                "g1":b["postRebalance_current_allocation"].astype(float)*(c.shift(-1)/c-1),
                "pos":np.arange(len(b))}))
    A=pd.concat(rows,ignore_index=True)
    out={}
    def summ(x,col="ex"):
        v=x[col].dropna()
        return pd.Series({"n":len(v),"mean_%":v.mean()*100,"t":v.mean()/(v.std()/np.sqrt(len(v))) if len(v)>2 else np.nan})
    g=A[A.pos%H==0].dropna(subset=["fwd"]).copy()
    g["ex"]=g.fwd-g.groupby("coin")["fwd"].transform("mean")
    tr=g[g.reg=="trending"].dropna(subset=["mom28"]).copy()
    tr["mq"]=tr.groupby("coin")["mom28"].transform(lambda x:pd.qcut(x.rank(method="first"),4,labels=False))
    out["trend_mom28_quartile_5d_ex"]=tr.groupby("mq").apply(summ)
    tr["tot"]=tr.fwd
    out["trend_mom28_quartile_5d_total"]=tr.groupby("mq").apply(lambda x:summ(x,"tot"))
    g10=A[A.pos%10==0].dropna(subset=["fwd10","mom28"]).copy()
    g10["ex"]=g10.fwd10-g10.groupby("coin")["fwd10"].transform("mean")
    t10=g10[g10.reg=="trending"].copy()
    t10["mq"]=t10.groupby("coin")["mom28"].transform(lambda x:pd.qcut(x.rank(method="first"),4,labels=False))
    out["trend_mom28_quartile_10d_ex"]=t10.groupby("mq").apply(summ)
    # what the score loads on, trending bars
    T=A[(A.reg=="trending")&(A.fc!=0)]
    out["fc_corr_with_features_trend"]=T[["fc","mom28","rev1","near90","nvol30"]].corr(method="spearman")["fc"]
    out["share_short_in_trend"]=float((T.fc<0).mean())
    # bar gain by regime and side
    A["side"]=np.sign(A.alloc)
    out["bar_gain_bps_by_reg_side"]=A.groupby(["reg","side"])["g1"].agg(["count","mean"]).assign(bps=lambda x:x["mean"]*1e4)
    out["long_short_gain_bps_by_year"]=A[A.side!=0].groupby(["year","side"])["g1"].mean().unstack()*1e4
    # forecast sign flips: how often does forecast change sign within trending
    return out
