def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        for h in [1,2,3,5]:
            rs=[]
            for w,df in ws.items():
                c=df["close"].values
                for i in range(0,len(c)-h,h):
                    rs.append(c[i+h]/c[i]-1)
            drift[(coin,h)]=(np.mean(rs),np.std(rs,ddof=1))
        for w,df in ws.items():
            d=df.reset_index(drop=True).copy()
            r=d["close"].pct_change()
            s=r.rolling(30).std()
            d["lift"]=(d["close"]-d["low"])/d["close"]/s
            d["rng"]=(d["high"]-d["low"])/d["close"]/s
            d["clv"]=(d["close"]-d["low"])/(d["high"]-d["low"])
            d["r1"]=r/s
            d["fc"]=d["regime"].isin(["mean_reversion","unknown"])
            d["yr"]=pd.to_datetime(d["timestamp"]).dt.year
            d["pos"]=np.arange(len(d))
            for h in [1,2,3,5]:
                d[f"f{h}"]=d["close"].shift(-h)/d["close"]-1-drift[(coin,h)][0]
            d["coin"]=coin; d["w"]=w; d["day"]=pd.to_datetime(d["timestamp"]).dt.floor("D")
            rows.append(d)
    A=pd.concat(rows)
    F=A[A.fc].dropna(subset=["lift","f1"])
    out={}
    out["n_fc_days"]=len(F); out["share_fc"]=float(A.fc.mean())
    F["lq"]=pd.qcut(F["lift"],5,labels=False)
    def tab(g):
        res={}
        for h in [1,2,3,5]:
            sub=g.dropna(subset=[f"f{h}"])
            if h>1: sub=sub[sub.pos%h==0]
            x=sub.groupby("day")[f"f{h}"].sum()
            res[f"m{h}"]=sub[f"f{h}"].mean(); res[f"t{h}"]=x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan; res[f"n{h}"]=len(sub)
        return pd.Series(res)
    out["by_lift_q"]=F.groupby("lq").apply(tab)
    out["by_lift_q_lift_mean"]=F.groupby("lq")["lift"].mean()
    out["by_coin"]=F.groupby("coin").apply(tab)
    out["by_year"]=F.groupby("yr").apply(tab)
    F["cq"]=pd.qcut(F["clv"],3,labels=False,duplicates="drop")
    F["rq"]=pd.qcut(F["rng"],3,labels=False)
    out["by_range_x_clv_m1"]=F.groupby(["rq","cq"])["f1"].agg(["mean","count"])
    F["r1q"]=pd.qcut(F["r1"],5,labels=False)
    out["by_dayreturn_q"]=F.groupby("r1q").apply(tab)
    out["corr_lift"]=pd.Series({h:stats.spearmanr(F["lift"],F[f"f{h}"],nan_policy="omit")[0] for h in [1,2,3,5]})
    out["corr_r1"]=pd.Series({h:stats.spearmanr(F["r1"],F[f"f{h}"],nan_policy="omit")[0] for h in [1,2,3,5]})
    out["all_fc"]=tab(F)
    out["lift_ge2"]=tab(F[F.lift>=2])
    return out
