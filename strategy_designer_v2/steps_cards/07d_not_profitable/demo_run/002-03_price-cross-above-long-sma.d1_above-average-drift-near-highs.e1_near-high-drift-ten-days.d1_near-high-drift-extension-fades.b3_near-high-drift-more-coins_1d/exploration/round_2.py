def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    rows=[]; grid=[]
    for c in bars:
        for w, b in bars[c].items():
            r1 = b["close"].shift(-1)/b["close"]-1
            pos = b["postRebalance_current_allocation"]
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            df = pd.DataFrame({"coin":c,"w":w,"pos":pos,"r1":r1,"gain":pos*r1-fee,"fee":fee,"regime":b["regime"],
                "rng":b.get("debug_info.components.range20.post_pipeline_value"),
                "ext":b.get("debug_info.components.ext30.post_pipeline_value"),
                "ret30":b.get("debug_info.components.ext30.last_history_value")})
            rows.append(df)
            idx=np.arange(0,len(b),10)
            gg=df.iloc[idx].copy(); gg["f10"]=(b["close"].shift(-10)/b["close"]-1).iloc[idx].values
            grid.append(gg)
    A=pd.concat(rows); G=pd.concat(grid)
    G["ex10"]=G["f10"]-G.groupby("coin")["f10"].transform("mean")
    T=A[A["regime"]=="trending"].copy()
    def cause(r):
        if r["pos"]>0: return "long"
        if r["pos"]==0: return "flat"
        if r["ext"]<=-1: return "short_ext"
        if r["rng"]<0: return "short_lowrange"
        return "short_other"
    T["cause"]=T.apply(cause,axis=1)
    out["trending bars by cause"]=T.groupby("cause").agg(n=("gain","size"),gain_net=("gain","mean"),r1=("r1","mean"),pos=("pos","mean"),fee=("fee","mean"))
    # daily-style counterfactuals per bar (1d bars) : long only, and long only no ext
    A["g_long"]=A["pos"].clip(lower=0)*A["r1"]
    A["g_hold"]=A["r1"]
    def sh(x):
        x=x.dropna(); return pd.Series({"mean":x.mean(),"sharpe":x.mean()/x.std()*np.sqrt(365),"n":len(x)})
    out["per-bar sharpe: book, long-only clip, hold"]=pd.DataFrame({"book":sh(A["gain"]),"long_only(no fee)":sh(A["g_long"]),"hold":sh(A["g_hold"])})
    GT=G[G["regime"]=="trending"].dropna(subset=["ex10"]).copy()
    ext=GT[GT["ext"]<=-5]
    out["extended grid ex10"]=pd.Series({"mean":ext["ex10"].mean(),"t":stats.ttest_1samp(ext["ex10"],0).statistic,"n":len(ext),
        "slope ex10 on ret30":stats.linregress(ext["ret30"],ext["ex10"]).slope,"slope t":stats.linregress(ext["ret30"],ext["ex10"]).rvalue*np.sqrt((len(ext)-2)/(1-stats.linregress(ext["ret30"],ext["ex10"]).rvalue**2))})
    lr=stats.linregress(GT["rng"],GT["ex10"])
    out["range-only slope trending grid"]=pd.Series({"slope":lr.slope,"t":lr.slope/lr.stderr,"n":len(GT)})
    GT["ret30q"]=pd.qcut(GT["ret30"].rank(method="first"),3,labels=False)
    GT["rhalf"]=np.where(GT["rng"]>0,"upper","lower")
    out["ex10 by range half x ret30 tercile"]=GT.groupby(["rhalf","ret30q"]).agg(ex10=("ex10","mean"),ret30=("ret30","mean"),n=("ex10","size"))
    GN=G[G["regime"]!="trending"].dropna(subset=["ex10"])
    out["nontrend grid ex10 vs range sign"]=GN.assign(h=np.where(GN["rng"].fillna(0)>0,"up","low")).groupby("h")["ex10"].agg(["mean","size"])
    out["window book mean (bar net gain)"]=A.groupby("w")["gain"].mean().describe()
    return out
