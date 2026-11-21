def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    recs=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r1=c.pct_change()
            ts=pd.to_datetime(df["timestamp"])
            f=pd.DataFrame({
                "fwd":c.shift(-H)/c-1,
                "fwd1":c.shift(-1)/c-1,
                "raw":df.get("debug_info.components.support_break.last_history_value"),
                "fc":df["forecast"],
                "pos":df["postRebalance_current_allocation"],
                "hi20":c/c.rolling(20).max()-1,
                "lo20":c/c.rolling(20).min()-1,
                "hi90":c/c.rolling(90,min_periods=60).max()-1,
                "dd90":c/c.rolling(90,min_periods=60).min()-1,
                "p20":c/c.shift(20)-1,
                "vol20":r1.rolling(20).std(),
                "wd":ts.dt.weekday,"yr":ts.dt.year,
            })
            f["coin"]=coin; f["win"]=w; f["idx"]=np.arange(len(f))
            recs.append(f)
    A=pd.concat(recs)
    out={}
    # 5-day grid
    G=A[A["idx"]%H==0].dropna(subset=["fwd"]).copy()
    G["u"]=G["fwd"]-G.groupby("coin")["fwd"].transform("mean")
    G["s"]=G["u"]/G.groupby("coin")["fwd"].transform("std")
    # weekday by coin and by half of years
    G["half"]=np.where(G["yr"]<=2021,"early","late")
    out["wd_by_half"]=G.pivot_table(index="wd",columns="half",values="s",aggfunc="mean")
    out["wd_monTue_by_coin"]=G.assign(mt=G.wd.isin([0,1])).groupby(["coin","mt"])["s"].mean().unstack()
    # 1-day returns by weekday, all bars (each bar's next-day return counted once)
    A1=A.dropna(subset=["fwd1"]).copy()
    A1["u1"]=A1["fwd1"]-A1.groupby("coin")["fwd1"].transform("mean")
    t=A1.groupby("wd")["u1"].agg(["mean","std","count"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["next_day_by_weekday_of_signal_close"]=t
    # deep break rebound: within broken, continuous raw vs s per coin
    B=G[G["raw"].fillna(0)>0].copy()
    B["lraw"]=np.log(B["raw"])
    out["broken_rho_by_coin"]=B.groupby("coin").apply(lambda g: pd.Series({"rho":stats.spearmanr(g["lraw"],g["s"])[0],"n":len(g)}))
    B["q"]=B.groupby("coin")["lraw"].transform(lambda s: pd.qcut(s.rank(method="first"),4,labels=False))
    t=B.groupby("q")["s"].agg(["mean","std","count"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"])); t["u"]=B.groupby("q")["u"].mean()
    out["broken_q"]=t
    out["broken_q_half"]=B.pivot_table(index="q",columns="half",values="s",aggfunc="mean")
    # dd90: distance above 90-day low (all grid)
    for col in ["dd90","hi90","hi20","lo20"]:
        x=G.dropna(subset=[col]).copy()
        x["q"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
        t=x.groupby("q")["s"].agg(["mean","std","count"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        t["early"]=x[x.half=="early"].groupby("q")["s"].mean(); t["late"]=x[x.half=="late"].groupby("q")["s"].mean()
        out["q_"+col]=t.drop(columns="std")
        out["rho_coin_"+col]=x.groupby("coin").apply(lambda g: stats.spearmanr(g[col],g["s"])[0])
    # book decomposition
    rows=[]
    for coin,wins in data["bars"].items():
        allc=pd.concat([d["close"].pct_change() for d in wins.values()])
    out["pos_mean"]=A.groupby("coin")["pos"].mean()
    return out
