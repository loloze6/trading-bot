def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            b["fwd"]=c.shift(-H)/c-1
            b["r30"]=c/c.shift(30)-1
            b["r60"]=c/c.shift(60)-1
            b["vol30"]=r1.rolling(30).std()
            b["v30_90"]=np.log(v.rolling(30).mean()/v.rolling(90).mean())
            b["v30_60"]=np.log(v.rolling(30).mean()/v.rolling(60).mean())
            b["v10_60"]=np.log(v.rolling(10).mean()/v.rolling(60).mean())
            b["v365"]=b.get("debug_info.components.quiet_vol.last_history_value")
            b["fc"]=b["forecast"]
            b["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["coin"]=coin; b["win"]=w
            rows.append(b.iloc[::H].copy())
    G=pd.concat(rows).dropna(subset=["fwd"])
    G["ex"]=G["fwd"]-G.groupby("coin")["fwd"].transform("mean")
    G["vq"]=G.groupby("coin")["vol30"].transform(lambda s:s.rank(pct=True))
    def clt(x):
        # day-clustered t of mean
        d=x.groupby("day")["y"].sum(); n=len(x); m=x["y"].mean()
        dev=x.assign(e=x["y"]-m).groupby("day")["e"].sum()
        nd=len(dev); se=np.sqrt((dev**2).sum()*nd/(nd-1))/n
        return pd.Series({"n":n,"days":nd,"mean":m,"t":m/se})
    def graded(df,k):
        z=(df[k]-df[k].mean())/df[k].std()
        x=df.assign(y=-z*df["ex"]).dropna(subset=["y"])  # positive if quieter -> lower ex
        return clt(x)
    out={}
    T=G[G.regime=="trending"].copy()
    res={}
    for k in ["v30_90","v30_60","v10_60","v365","r30"]:
        res[k]=graded(T,k)
    out["trend_graded_quiet_predicts_fall"]=pd.DataFrame(res).T.round(4)
    # per-year and per-coin sign for v30_90 inside trending
    T["vqq"]=pd.qcut(T["v30_90"],2,labels=["quiet","heavy"])
    out["trend_v30_90_half_by_year"]=T.groupby(["yr","vqq"])["ex"].agg(["count","mean"]).round(4).unstack()
    out["trend_v30_90_half_by_coin"]=T.groupby(["coin","vqq"])["ex"].agg(["count","mean"]).round(4).unstack()
    # same graded measure in other situations (r30<0, by r60 trend, by calm/agitated proxy)
    G["tr"]=np.where(G.r60>0.10,"rising",np.where(G.r60<-0.10,"falling","choppy")); G.loc[G.r60.isna(),"tr"]="na"
    G["ag"]=np.where(G.vq>0.5,"agit","calm")
    res={}
    for (tr,ag),df in G[G.r30<0].groupby(["tr","ag"]):
        if len(df)>30: res[f"{tr}_{ag}"]=graded(df,"v30_90")
    res["all_r30neg"]=graded(G[G.r30<0],"v30_90")
    res["all_r30pos"]=graded(G[G.r30>=0],"v30_90")
    res["nontrend_r30neg"]=graded(G[(G.r30<0)&(G.regime!="trending")],"v30_90")
    out["v30_90_graded_by_situation"]=pd.DataFrame(res).T.round(4)
    # quintiles of v30_90 over all r30<0
    A=G[G.r30<0].copy()
    A["q"]=pd.qcut(A["v30_90"],5,labels=False)
    o=A.groupby("q")["ex"].agg(["count","mean","std"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["r30neg_v30_90_quint"]=o.round(4)
    # forecast vs v30_90 correlation in trending
    out["corr_v365_v30_90_trend"]=float(T[["v365","v30_90"]].corr().iloc[0,1])
    return out
