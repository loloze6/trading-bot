def explore(data):
    import numpy as np, pandas as pd
    rows=[]; hz=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            a=b["postRebalance_current_allocation"].fillna(0).values
            r1=np.r_[c[1:]/c[:-1]-1,np.nan]
            gross=np.nansum(a*r1)
            fee=np.nansum(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"].mean()
            turn=np.nansum(np.abs(np.diff(np.r_[b["previous_allocation"].fillna(0).values[0],a])))
            ndays=len(b)/24
            # forecast autocorr / horizon
            f=b["forecast"].values
            rows.append(dict(coin=coin,w=w,gross_per_day=gross/ndays,fee_per_day=fee/ndays,turn_per_day=turn/ndays,
                             meanabsalloc=np.mean(np.abs(a))))
            for h in [1,4,12,24,48]:
                idx=np.arange(0,len(c)-h,h)
                fr=c[idx+h]/c[idx]-1
                hz.append(dict(h=h,coin=coin,prod=np.mean(-np.sign(-f[idx])*0+(f[idx]/10)*fr)))
    d=pd.DataFrame(rows)
    H=pd.DataFrame(hz)
    bycoin=d.groupby("coin")[["gross_per_day","fee_per_day","turn_per_day","meanabsalloc"]].mean()
    tot=d[["gross_per_day","fee_per_day","turn_per_day","meanabsalloc"]].mean()
    hzs=H.groupby("h")["prod"].agg(["mean","std","count"])
    hzs["per_hour"]=hzs["mean"]/hzs.index
    # trades
    tr=pd.concat([t for coin in data["trades"] for t in data["trades"][coin].values()])
    ts=pd.Series(dict(n=len(tr),med_dur_h=tr["duration_minutes"].median()/60,mean_pl=tr["profit_loss_percent"].mean(),
                      mean_net=tr["net_profit_loss_percent"].mean(),mean_comm=tr["total_commission"].mean()))
    return {"by coin":bycoin,"total":tot,"horizon gain per forecast":hzs,"trades":ts}
