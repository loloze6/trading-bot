def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); v=b["volume"].astype(float)
            b["fwd"]=c.shift(-H)/c-1
            b["r1"]=c.pct_change()
            b["r5"]=c/c.shift(5)-1
            b["r20"]=c/c.shift(20)-1
            b["volr"]=v/v.shift(1).rolling(20,min_periods=20).mean()
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            b["cl"]=(c-b["low"])/rng
            b["rngr"]=rng/c/ (rng/c).shift(1).rolling(20,min_periods=20).mean()
            b["dd20"]=c/c.rolling(20,min_periods=20).max()-1
            b["vol20"]=b["r1"].rolling(20,min_periods=20).std()
            b["inprof"]=b["regime"].isin(["trending","unknown"])
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["pos"]=np.arange(len(b))
            b["coin"]=coin; b["win"]=w
            rows.append(b)
    a=pd.concat(rows,ignore_index=True)
    # normal drift per coin over all windows, grid
    grid=a[(a["pos"]%H==0)&a["fwd"].notna()]
    drift=grid.groupby("coin")["fwd"].mean()
    usual=grid.groupby("coin")["fwd"].std()
    a["unus"]=a["fwd"]-a["coin"].map(drift)
    a["str"]=a["unus"]/a["coin"].map(usual)
    g=a[(a["pos"]%H==0)&a["fwd"].notna()]
    gp=g[g["inprof"]]
    out={}
    out["drift_usual"]=pd.DataFrame({"drift":drift,"usual":usual})
    out["profile_share"]=a.groupby("coin")["inprof"].mean()
    def summ(df,key):
        r=df.groupby(key)["unus"].agg(["count","mean","std"])
        r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        r["tot"]=df.groupby(key)["fwd"].mean()
        return r
    out["inprof_vs_out"]=summ(g,"inprof")
    for k in ["r1","r5","r20","volr","cl","rngr","dd20","vol20"]:
        d=gp.dropna(subset=[k]).copy()
        d["q"]=pd.qcut(d[k],5,labels=False,duplicates="drop")
        out["q_"+k]=summ(d,"q")
    out["wd"]=summ(gp,"wd")
    out["year"]=summ(gp,"year")
    out["coin"]=summ(gp,"coin")
    # spearman across in-profile grid
    sp={}
    for k in ["r1","r5","r20","volr","cl","rngr","dd20","vol20"]:
        d=gp.dropna(subset=[k,"unus"])
        sp[k]=stats.spearmanr(d[k],d["unus"])[0]
    out["spearman"]=pd.Series(sp)
    out["n_inprof_grid"]=len(gp)
    return out
