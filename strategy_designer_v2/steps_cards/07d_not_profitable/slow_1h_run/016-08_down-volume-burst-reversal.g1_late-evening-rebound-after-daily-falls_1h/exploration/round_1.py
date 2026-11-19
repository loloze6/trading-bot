def explore(data):
    import pandas as pd, numpy as np
    rows=[]; trs=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"])
            b["hour"]=ts.dt.hour
            cl=b["close"].values
            b["r1"]=pd.Series(cl).shift(-1).values/cl-1
            b["r2"]=pd.Series(cl).shift(-2).values/cl-1
            b["r4"]=pd.Series(cl).shift(-4).values/cl-1
            b["r24"]=pd.Series(cl).shift(-24).values/cl-1
            b["p24"]=cl/pd.Series(cl).shift(24).values-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["gain"]=b["pos"]*b["r1"]
            b["fee"]=b["postRebalance_total_value"]/b["total_portfolio_value"]-1
            b["coin"]=c; b["win"]=w
            rows.append(b[["coin","win","hour","forecast","pos","gain","fee","r1","r2","r4","r24","p24"]])
            t=data["trades"][c][w]
            if len(t): t=t.copy(); t["coin"]=c; trs.append(t)
    B=pd.concat(rows); T=pd.concat(trs)
    held=B[B.pos.abs()>1e-9]
    out={}
    out["held_by_hour"]=held.groupby("hour").agg(n=("gain","size"),pos=("pos","mean"),gain=("gain","mean"),r1=("r1","mean"))
    out["gross_vs_fee_total"]=pd.Series({"sum_gain":B.gain.sum(),"sum_fee":B.fee.sum(),"n_held_bars":len(held)})
    out["trades"]=pd.Series({"n":len(T),"dur_med_min":T.duration_minutes.median(),"pl_mean":T.profit_loss_percent.mean(),"net_mean":T.net_profit_loss_percent.mean(),"comm_mean":T.total_commission.mean()})
    act=B[(B.forecast>0)]
    out["active_hour"]=act.groupby("hour").size()
    act=act.copy(); act["q"]=pd.qcut(act.forecast.rank(method="first"),3,labels=["lo","mid","hi"])
    mean_all={k:B[k].mean() for k in ["r1","r2","r4","r24"]}
    out["active_by_tercile_excess"]=act.groupby("q").agg(n=("r1","size"),r1=("r1","mean"),r2=("r2","mean"),r4=("r4","mean"),r24=("r24","mean"),p24=("p24","mean"))
    out["coin_mean_r"]=pd.Series(mean_all)
    out["by_coin"]=B.groupby("coin").agg(gain=("gain","sum"),fee=("fee","sum"))
    # all 20:00-close bars incl rises
    h=B[B.hour==19].copy()
    h["q"]=pd.qcut(h.p24.rank(method="first"),5,labels=False)
    out["h19_by_p24_quint"]=h.groupby("q").agg(n=("r1","size"),p24=("p24","mean"),r1=("r1","mean"),r2=("r2","mean"),r4=("r4","mean"),r24=("r24","mean"))
    return out
