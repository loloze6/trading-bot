def explore(data):
    import numpy as np, pandas as pd
    out = {}
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
            vol20 = pd.Series(r1).rolling(20).std().values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(n-1):
                daily.append(dict(coin=coin, w=w, f=f[i], r1=r1[i], fwd1=fwd1[i], vol=vol20[i], wd=ts.iloc[i].dayofweek, yr=ts.iloc[i].year, d=ts.iloc[i].normalize()))
    Y = pd.DataFrame(daily).dropna(subset=["r1","fwd1","vol"])
    Y["z"] = Y["r1"]/Y["vol"]
    Y["dip"] = (Y.z<-0.5)&(Y.z>-99)
    Y["act"] = Y.f>0
    Y["grp"] = np.where(Y.act,"act","flat") + np.where(Y.z<-0.5,"_dn",np.where(Y.z>0.5,"_up","_mid"))
    # cluster by day: average across coins per day per group, then t over days
    def clust(df, key):
        g = df.groupby([key,"d"])["fwd1"].mean().reset_index()
        return g.groupby(key)["fwd1"].agg(n="count", mean="mean", t=lambda x: x.mean()/x.std()*np.sqrt(len(x)))
    out["clustered_by_trend_and_move"] = clust(Y, "grp")
    out["clustered_weekday"] = clust(Y, "wd")
    # dip effect by year and coin (dip minus non-dip)
    Y["dipflag"] = Y.z<-0.5
    out["dip_by_year"] = Y.groupby(["yr","dipflag"])["fwd1"].mean().unstack()
    out["dip_by_coin"] = Y.groupby(["coin","dipflag"])["fwd1"].agg(["count","mean"]).unstack()
    # weekday Thu/Fri vs rest by year
    Y["thfr"] = Y.wd.isin([3,4])
    out["thfr_by_year"] = Y.groupby(["yr","thfr"])["fwd1"].mean().unstack()
    out["thfr_by_coin"] = Y.groupby(["coin","thfr"])["fwd1"].mean().unstack()
    # dip in active: next 5-day return non-overlapping-ish: use fwd1 only; also 2-day after dip
    # trades: long-lasting vs quick, and trade exits caused by forecast going to 0
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    T["days"] = T["duration_minutes"]/1440
    out["trades_by_exitfc"] = T.groupby(pd.cut(T.exit_forecast,[-1,0,2,5,21]),observed=True)["net_profit_loss_percent"].agg(["count","mean","median"])
    out["share_trades_le3d"] = (T.days<=3).mean()
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
