def explore(data):
    import numpy as np, pandas as pd
    out = {}
    B=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.copy(); b["coin"]=c; b["w"]=w
            b["r1"]=b["close"].pct_change()
            b["fwd1"]=b["close"].shift(-1)/b["close"]-1
            b["fwd5"]=b["close"].shift(-5)/b["close"]-1
            b["z"]=b["r1"]/b["r1"].rolling(20).std()
            b["vr"]=b["volume"]/b["volume"].shift(1).rolling(30).mean()
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            b["ret60"]=b["close"]/b["close"].shift(60)-1
            b["pos"]=np.arange(len(b))
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["gain"]=b["postRebalance_current_allocation"]*b["fwd1"]
            B.append(b)
    B=pd.concat(B)
    B["cm1"]=B.groupby("coin")["fwd1"].transform("mean")
    B["drift"]=B["postRebalance_current_allocation"]*B["cm1"]
    B["timing"]=B["gain"]-B["drift"]
    B["held"]=B["postRebalance_current_allocation"]<-0.01
    H=B[B["held"]].copy()
    H["tr20"]=np.where(H["ret20"]>0,"up20","down20")
    H["tr60"]=np.where(H["ret60"]>0,"up60","down60")
    def agg(g): return pd.Series({"n":len(g),"gain":g["gain"].mean(),"drift":g["drift"].mean(),"timing":g["timing"].mean(),"fee":g["fee"].mean(),"t_gain":g["gain"].mean()/(g["gain"].std()/np.sqrt(len(g)))})
    out["held_by_tr20"]=H.groupby("tr20").apply(agg)
    out["held_by_tr60"]=H.groupby("tr60").apply(agg)
    out["fee_vs_timing_all"]=pd.Series({"fee_sum_share":B["fee"].sum(),"timing_sum":B["timing"].sum(),"drift_sum":B["drift"].sum()})
    G=B[B["pos"]%5==0].dropna(subset=["fwd5","z","vr","ret20"]).copy()
    G["cm5"]=G.groupby("coin")["fwd5"].transform("mean"); G["ex5"]=G["fwd5"]-G["cm5"]
    def tt(x): x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    up=G[(G["z"]>0)&(G["vr"]<1)].copy()
    up["tr"]=np.where(up["ret20"]>0,"up20","down20")
    up["zq"]=pd.qcut(up["z"],3,labels=["small","mid","big"])
    out["thin_up_ex5_by_trend_size"]=up.groupby(["tr","zq"])["ex5"].apply(tt).unstack()
    hv=G[(G["z"]>0)&(G["vr"]>=1)].copy()
    hv["vq"]=pd.qcut(hv["vr"],3,labels=["lo","mid","hi"])
    out["heavy_up_ex5_by_volq"]=hv.groupby("vq")["ex5"].apply(tt).unstack()
    hv["zq"]=pd.qcut(hv["z"],3,labels=["small","mid","big"])
    out["heavy_up_ex5_by_size"]=hv.groupby("zq")["ex5"].apply(tt).unstack()
    out["corr_heavy_up"]=pd.Series({"corr_z_ex5":hv["z"].corr(hv["ex5"]),"corr_logvr_ex5":np.log(hv["vr"]).corr(hv["ex5"]),"n":len(hv)})
    return out
