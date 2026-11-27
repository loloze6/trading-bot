def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    drift={}
    rows=[]
    H=[1,2,3,5,7,10]
    for coin,ws in data["bars"].items():
        for h in H:
            rs=[]
            for w,df in ws.items():
                c=df["close"].values
                for i in range(0,len(c)-h,h):
                    rs.append(c[i+h]/c[i]-1)
            drift[(coin,h)]=np.mean(rs)
        for w,df in ws.items():
            d=df.reset_index(drop=True).copy()
            r=d["close"].pct_change()
            s=r.rolling(30).std()
            d["rng"]=(d["high"]-d["low"])/d["close"]/s
            d["clv"]=(d["close"]-d["low"])/(d["high"]-d["low"])
            d["r1"]=r/s
            d["inprof"]=d["regime"].isin(["mean_reversion","unknown"])
            d["mr"]=d["regime"].eq("mean_reversion")
            col="debug_info.components"
            d["pos"]=np.arange(len(d))
            for h in H:
                d[f"f{h}"]=d["close"].shift(-h)/d["close"]-1-drift[(coin,h)]
            d["coin"]=coin; d["day"]=pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["yr"]=pd.to_datetime(d["timestamp"]).dt.year
            rows.append(d)
    A=pd.concat(rows)
    F=A[A.inprof].dropna(subset=["rng","clv","f1"]).copy()
    F["wh"]=F["rng"]*F["clv"]  # width x nearness to high
    def tab(g):
        res={}
        for h in H:
            sub=g.dropna(subset=[f"f{h}"])
            if h>1: sub=sub[sub.pos%h==0]
            x=sub.groupby("day")[f"f{h}"].sum()
            res[f"m{h}"]=sub[f"f{h}"].mean()
            res[f"t{h}"]=x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan
            res[f"n{h}"]=len(sub)
        return pd.Series(res)
    out={}
    out["mr_vs_unknown"]=F.groupby("mr").apply(tab)
    F["whq"]=pd.qcut(F["wh"],4,labels=False)
    out["by_widthxhigh_q"]=F.groupby("whq").apply(tab)
    out["corr_wh"]=pd.Series({h:stats.spearmanr(F["wh"],F[f"f{h}"],nan_policy="omit")[0] for h in H})
    F["r1q"]=pd.qcut(F["r1"],4,labels=False)
    out["by_r1_q"]=F.groupby("r1q").apply(tab)
    out["corr_r1"]=pd.Series({h:stats.spearmanr(F["r1"],F[f"f{h}"],nan_policy="omit")[0] for h in H})
    top=F[F.whq==3]
    out["top_wh_by_coin"]=top.groupby("coin").apply(tab)[["m1","t1","n1","m5","t5","n5","m10","t10","n10"]]
    out["top_wh_by_year"]=top.groupby("yr").apply(tab)[["m1","t1","n1","m5","t5","n5","m10","t10","n10"]]
    topr=F[F.r1q==3]
    out["top_r1_by_coin"]=topr.groupby("coin").apply(tab)[["m1","n1","m5","t5","n5","m10","t10","n10"]]
    out["top_r1_by_year"]=topr.groupby("yr").apply(tab)[["m1","n1","m5","t5","n5","m10","t10","n10"]]
    return out
