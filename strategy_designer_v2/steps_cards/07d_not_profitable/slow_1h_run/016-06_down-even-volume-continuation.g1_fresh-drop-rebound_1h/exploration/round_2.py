def explore(data):
    import numpy as np, pandas as pd
    parts=[]; ev=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            a=b["postRebalance_current_allocation"].fillna(0); pa=b["previous_allocation"].fillna(0)
            turn=(a-pa).abs()
            reg=b["regime"]; rch=reg!=reg.shift(1)
            f=b["forecast"].fillna(0); fz=(f>0)!=(f.shift(1)>0)
            cause=np.where(rch,"regime_flip",np.where(fz,"forecast_on_off","resize"))
            parts.append(pd.DataFrame({"cause":cause,"turn":turn,"traded":turn>1e-6}))
            # slow version: forecast at grid bars held 72 bars
            r1=b["close"].shift(-1)/b["close"]-1
            c=b["close"].values; n=len(b)
            for i in range(0,n-72,72):
                ev.append(dict(coin=coin,f=f.iloc[i],a=a.iloc[i],ret=c[i+72]/c[i]-1,
                               r72=c[i]/c[i-72]-1 if i>=72 else np.nan))
            # regime run lengths
    P=pd.concat(parts)
    tc=P.groupby("cause").agg(bars=("turn","size"),traded=("traded","sum"),turn=("turn","sum"))
    E=pd.DataFrame(ev)
    E["exc"]=E["ret"]-E.groupby("coin")["ret"].transform("mean")
    act=E[E.f>0]
    slow=pd.Series(dict(n_active_grid=len(act),mean_ret=act.ret.mean(),mean_exc=act.exc.mean(),
        t_exc=act.exc.mean()/act.exc.std()*np.sqrt(len(act)),
        fw_exc=(act.exc*act.f).sum()/act.f.sum(),
        held72_gross_per_alloc=(act.ret*act.a).mean(),
        fee_per_roundtrip_est=0.002))
    # forecast persistence: share of hourly forecast>0 bars whose forecast is still >0 24 bars later
    pers=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            f=b["forecast"].fillna(0)>0
            pers.append(dict(on=f.mean(),stay1=(f&f.shift(-1,fill_value=False)).sum()/max(f.sum(),1),
                             stay24=(f&f.shift(-24,fill_value=False)).sum()/max(f.sum(),1)))
    pe=pd.DataFrame(pers).mean()
    return {"turnover_cause":tc,"slow_grid":slow,"persistence":pe}
