def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 20
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < 30: continue
            f = b["forecast"].astype(float).values
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            fwd1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            r20 = pd.Series(c).pct_change(20).values
            r60 = pd.Series(c).pct_change(60).values
            vol20 = pd.Series(r1).rolling(20).std().values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n-H, H):
                rows.append(dict(coin=coin, w=w, f=f[i], fwd=c[i+H]/c[i]-1, r20=r20[i], r60=r60[i], vol=vol20[i], yr=ts.iloc[i].year))
            for i in range(n-1):
                daily.append(dict(coin=coin, w=w, f=f[i], r1=r1[i], fwd1=fwd1[i], vol=vol20[i], wd=ts.iloc[i].dayofweek, r20=r20[i], r60=r60[i]))
    D = pd.DataFrame(rows)
    D["ex"] = D["fwd"] - D.groupby("coin")["fwd"].transform("mean")
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan, hit=(g["fwd"]>0).mean()))
    D["fb"] = pd.cut(D["f"], [-0.01, 0, 0.5, 1, 1.5, 2, 21])
    out["fwd20_by_forecast_bucket"] = D.groupby("fb", observed=True).apply(summ)
    # quadrant of r20/r60 signs
    D["quad"] = np.where(D.r60>0,"r60+","r60-") + np.where(D.r20>0,"r20+","r20-")
    out["fwd20_by_quadrant"] = D.dropna(subset=["r60"]).groupby("quad").apply(summ)
    D["volq"] = D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["fwd20_by_volterc"] = D.groupby("volq").apply(summ)
    out["fwd20_active_by_year"] = D[D.f>0].groupby("yr").apply(summ)
    out["fwd20_by_coin_active"] = D[D.f>0].groupby("coin").apply(summ)
    # daily
    Y = pd.DataFrame(daily).dropna(subset=["r1","fwd1"])
    Y["z"] = Y["r1"]/Y["vol"]
    Y["zb"] = pd.cut(Y["z"], [-99,-2.5,-1.5,-0.5,0.5,1.5,2.5,99])
    def s1(g):
        x=g["fwd1"]; return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/x.std()*np.sqrt(len(x))))
    out["next_day_by_move_z"] = Y.groupby("zb", observed=True).apply(s1)
    out["next_day_by_weekday"] = Y.groupby("wd").apply(s1)
    out["next_day_by_active"] = Y.groupby(Y.f>0).apply(s1)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    T["days"] = T["duration_minutes"]/1440
    T["db"] = pd.cut(T["days"], [0,1,3,10,30,1000])
    out["trades_by_duration"] = T.groupby("db", observed=True)["net_profit_loss_percent"].agg(["count","mean","median","sum"])
    out["trades_by_entryfc"] = T.groupby(pd.cut(T.entry_forecast,[-1,0.25,0.5,1,2,21]), observed=True)["net_profit_loss_percent"].agg(["count","mean","median","sum"])
    out["trades_n"] = len(T)
    return out
