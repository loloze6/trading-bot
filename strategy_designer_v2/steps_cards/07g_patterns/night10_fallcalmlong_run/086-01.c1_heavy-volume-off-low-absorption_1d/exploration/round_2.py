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
            b["r3"]=c/c.shift(3)-1
            b["r5"]=c/c.shift(5)-1
            b["r10"]=c/c.shift(10)-1
            b["volr"]=v/v.shift(1).rolling(20,min_periods=20).mean()
            b["dd10"]=c/c.rolling(10,min_periods=10).max()-1
            b["dd20"]=c/c.rolling(20,min_periods=20).max()-1
            b["up20"]=c/c.rolling(20,min_periods=20).min()-1
            sd=b["r1"].rolling(30,min_periods=20).std()
            b["r5s"]=b["r5"]/(sd*np.sqrt(5))
            b["dd20s"]=b["dd20"]/(sd*np.sqrt(20))
            b["vr5"]=v.rolling(5).mean()/v.shift(5).rolling(20,min_periods=20).mean()
            b["inprof"]=b["regime"].isin(["trending","unknown"])
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["pos"]=np.arange(len(b))
            b["coin"]=coin; b["win"]=w
            rows.append(b)
    a=pd.concat(rows,ignore_index=True)
    grid0=a[(a["pos"]%H==0)&a["fwd"].notna()]
    drift=grid0.groupby("coin")["fwd"].mean(); usual=grid0.groupby("coin")["fwd"].std()
    a["unus"]=a["fwd"]-a["coin"].map(drift)
    keys=["r3","r5","r10","dd10","dd20","up20","r5s","dd20s","vr5"]
    out={}
    # spearman per grid offset
    tab={}
    for off in range(H):
        gp=a[(a["pos"]%H==off)&a["fwd"].notna()&a["inprof"]]
        tab[off]={k:stats.spearmanr(*gp.dropna(subset=[k])[[k,"unus"]].T.values)[0] for k in keys}
        tab[off]["n"]=len(gp)
    out["spearman_by_offset"]=pd.DataFrame(tab)
    gp=a[(a["pos"]%H==0)&a["fwd"].notna()&a["inprof"]].copy()
    # day-clustered regression slope t for r5s and dd20s (standardized x)
    def cl_t(d,k):
        d=d.dropna(subset=[k]).copy()
        x=(d[k]-d[k].mean())/d[k].std()
        d["prod"]=x*d["unus"]
        s=d.groupby("day")["prod"].sum()
        D=len(s); m=s.mean()*D/len(d)
        se=np.sqrt(((s-s.mean())**2).sum()*D/(D-1))/len(d)
        return pd.Series({"slope_per_sd":m,"t_clustered":m/se,"days":D,"n":len(d)})
    out["clustered"]=pd.DataFrame({k:cl_t(gp,k) for k in keys})
    # terciles of r5s by coin and by year
    gp["t3"]=pd.qcut(gp["r5s"],3,labels=["low","mid","high"])
    out["r5s_tercile_coin"]=gp.pivot_table(index="coin",columns="t3",values="unus",aggfunc="mean")
    out["r5s_tercile_year"]=gp.pivot_table(index="year",columns="t3",values="unus",aggfunc="mean")
    out["r5s_tercile_stats"]=gp.groupby("t3")["unus"].agg(["count","mean","std"]).assign(tot=gp.groupby("t3")["fwd"].mean())
    gp["d3"]=pd.qcut(gp["dd20s"],3,labels=["deep","mid","near_high"])
    out["dd20s_tercile_coin"]=gp.pivot_table(index="coin",columns="d3",values="unus",aggfunc="mean")
    out["dd20s_tercile_year"]=gp.pivot_table(index="year",columns="d3",values="unus",aggfunc="mean")
    out["dd20s_tercile_stats"]=gp.groupby("d3")["unus"].agg(["count","mean","std"]).assign(tot=gp.groupby("d3")["fwd"].mean())
    # out of profile, same relation (is it profile-specific?)
    go=a[(a["pos"]%H==0)&a["fwd"].notna()&~a["inprof"]]
    out["spearman_outprof"]=pd.Series({k:stats.spearmanr(*go.dropna(subset=[k])[[k,"unus"]].T.values)[0] for k in keys})
    # trades: pnl vs entry
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            tr.append(t)
    T=pd.concat(tr,ignore_index=True) if tr else pd.DataFrame()
    out["trades"]=pd.Series({"n":len(T),"mean_pnl":T["profit_loss_percent"].mean(),"mean_net":T["net_profit_loss_percent"].mean(),"win":(T["profit_loss_percent"]>0).mean()})
    return out
