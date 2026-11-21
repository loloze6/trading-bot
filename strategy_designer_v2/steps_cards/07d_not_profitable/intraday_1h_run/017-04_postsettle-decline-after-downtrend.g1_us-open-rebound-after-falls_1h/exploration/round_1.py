def explore(data):
    import pandas as pd, numpy as np
    rows=[]; hrs=[]; trd=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            b["ts"]=pd.to_datetime(b["timestamp"])
            b["nr"]=b["close"].shift(-1)/b["close"]-1
            a=b["postRebalance_current_allocation"].fillna(0)
            b["g"]=a*b["nr"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["hr"]=b["ts"].dt.hour
            b["a"]=a
            b["c"]=c
            hrs.append(b[["hr","a","g","fee","forecast","c","nr"]])
        for w,t in data["trades"][c].items():
            t=t.copy(); t["c"]=c; trd.append(t)
    H=pd.concat(hrs); T=pd.concat(trd)
    byhr=H.groupby("hr").agg(mean_alloc=("a","mean"),gross_sum=("g","sum"),fee_sum=("fee","sum"),fc_mean=("forecast","mean"))
    bycoin=H.groupby("c").agg(gross_sum=("g","sum"),fee_sum=("fee","sum"),mean_alloc_active=("a",lambda x:x[x!=0].mean()))
    tr=T.groupby("c").agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),comm=("total_commission","mean"),dur=("duration_minutes","mean"))
    trd_side=T.groupby("side").size()
    act=H[H["a"]!=0].copy()
    act["q"]=pd.qcut(act["a"],5,labels=False,duplicates="drop")
    byq=act.groupby("q").agg(n=("g","size"),a=("a","mean"),g=("g","mean"),fee=("fee","mean"))
    # fee on bars of entry/exit
    feehr=H[H["fee"].abs()>1e-9].groupby("hr").agg(n=("fee","size"),fee=("fee","mean"))
    return {"byhr":byhr,"bycoin":bycoin,"trades":tr,"sides":trd_side,"byallocq":byq,"feehr":feehr,
            "dur_dist":T["duration_minutes"].describe()}
