def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    D["year"]=pd.to_datetime(D["day"]).dt.year
    out["book_by_coin"] = D.groupby("coin").agg(book_mean=("book_return","mean"), book_sd=("book_return","std"), coin_mean=("coin_return","mean"))
    out["book_by_year"] = D.groupby("year").agg(book_mean=("book_return","mean"), coin_mean=("coin_return","mean"), n=("book_return","count"))
    # bar-level
    B=[]
    for c, ws in data["bars"].items():
        cm_all=[]
        for w, b in ws.items():
            b=b.copy()
            b["coin"]=c; b["w"]=w
            b["r1"]=b["close"].pct_change()
            b["fwd1"]=b["close"].shift(-1)/b["close"]-1
            b["fwd5"]=b["close"].shift(-5)/b["close"]-1
            b["z"]=b["r1"]/b["r1"].rolling(20).std()
            b["vr"]=b["volume"]/b["volume"].shift(1).rolling(30).mean()
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            b["pos"]=np.arange(len(b))
            b["fee"]=b["total_portfolio_value"]-b["postRebalance_total_value"]
            b["gain"]=b["postRebalance_current_allocation"]*b["fwd1"]
            B.append(b)
    B=pd.concat(B)
    B["coin_mean1"]=B.groupby("coin")["fwd1"].transform("mean")
    B["drift"]=B["postRebalance_current_allocation"]*B["coin_mean1"]
    B["timing"]=B["gain"]-B["drift"]
    B["feefrac"]=B["fee"]/B["total_portfolio_value"]
    out["decomp_per_bar"]=pd.Series({"gain":B["gain"].mean(),"drift":B["drift"].mean(),"timing":B["timing"].mean(),"fee":B["feefrac"].mean(),
        "mean_alloc":B["postRebalance_current_allocation"].mean(),"share_short":(B["postRebalance_current_allocation"]<-0.01).mean()})
    # grid
    G=B[B["pos"]%5==0].dropna(subset=["fwd5"]).copy()
    G["cm5"]=G.groupby("coin")["fwd5"].transform("mean")
    G["ex5"]=G["fwd5"]-G["cm5"]
    act=G[G["forecast"]<0].copy()
    def tt(x): x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    act["zq"]=pd.qcut(act["z"],4,labels=False)
    act["vq"]=pd.qcut(act["vr"],4,labels=False)
    out["active_ex5_by_rise_q"]=act.groupby("zq")["ex5"].apply(tt).unstack()
    out["active_ex5_by_vol_q"]=act.groupby("vq")["ex5"].apply(tt).unstack()
    act["trend_up"]=(act["ret20"]>0)
    out["active_ex5_by_trend20"]=act.groupby("trend_up")["ex5"].apply(tt).unstack()
    out["active_ex5_by_coin"]=act.groupby("coin")["ex5"].apply(tt).unstack()
    # all up days by volume ratio group, sharp rises
    up=G[G["z"]>0].copy()
    up["thin"]=up["vr"]<1
    up["zq"]=pd.qcut(up["z"],3,labels=["small","mid","big"])
    out["up_ex5_by_thin_and_size"]=up.groupby(["zq","thin"])["ex5"].apply(tt).unstack()
    dn=G[G["z"]<0].copy()
    dn["thin"]=dn["vr"]<1
    dn["zq"]=pd.qcut(dn["z"],3,labels=["big","mid","small"])
    out["down_ex5_by_thin_and_size"]=dn.groupby(["zq","thin"])["ex5"].apply(tt).unstack()
    tr=[]
    for c, ws in data["trades"].items():
        for w,t in ws.items(): tr.append(t)
    T=pd.concat(tr)
    out["trades"]=pd.Series({"n":len(T),"mean_pl":T["profit_loss_percent"].mean(),"mean_net":T["net_profit_loss_percent"].mean(),"mean_dur_days":T["duration_minutes"].mean()/1440,"share_short":(T["side"]=="SHORT").mean()})
    return out
