def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            nxt=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            nxt2=c.shift(-3)/c-1
            d=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.dayofweek,"nxt":nxt,"nxt3":nxt2,
                "a":b["postRebalance_current_allocation"].astype(float),"f":b["forecast"].astype(float),
                "r20":c/c.shift(20)-1,"r5":c/c.shift(5)-1,"rfri":c/c.shift(1)-1,
                "vol":c.pct_change().rolling(20).std(),"pv":b["postRebalance_total_value"].astype(float)})
            rows.append(d)
    D=pd.concat(rows)
    def st(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x))})
    out={}
    F=D[D.wd==4].dropna(subset=["nxt","r20"]).copy()
    F["trend"]=np.where(F.r20>0,"up20","down20")
    F["active"]=F.a>1e-9
    out["fri_nxt_by_trend_active"]=F.groupby(["trend","active"]).nxt.apply(st).unstack()
    F["r5s"]=np.where(F.r5>0,"up5","down5")
    out["fri_nxt_by_r5"]=F.groupby("r5s").nxt.apply(st).unstack()
    F["fri_day"]=np.where(F.rfri>0,"fri_up","fri_down")
    out["fri_nxt_by_fri_day"]=F.groupby("fri_day").nxt.apply(st).unstack()
    out["fri_nxt3_weekend_by_trend"]=F.groupby("trend").nxt3.apply(st).unstack()
    A=D.dropna(subset=["nxt","r20"]).copy(); A["trend"]=np.where(A.r20>0,"up20","down20")
    out["all_days_nxt_by_wd_trend_mean"]=A.groupby(["wd","trend"]).nxt.mean().unstack()
    out["all_days_nxt_by_wd_trend_t"]=A.groupby(["wd","trend"]).nxt.apply(lambda x: x.mean()/x.std()*np.sqrt(len(x))).unstack()
    F["fz"]=pd.cut(F.f,[-0.1,0.1,5,10,20.1])
    out["fri_by_forecast_trend"]=F[F.active].groupby(["fz","trend"]).nxt.apply(lambda x: x.mean()).unstack()
    # calmar: book drawdown by year
    dd=[]
    for (coin,w),g in D.groupby(["coin","w"]):
        pv=g.pv.dropna(); dd.append({"coin":coin,"w":w,"ret":pv.iloc[-1]/pv.iloc[0]-1,"mdd":(pv/pv.cummax()-1).min()})
    dd=pd.DataFrame(dd)
    out["window_ret_mdd_summary"]=dd[["ret","mdd"]].describe()
    return out
