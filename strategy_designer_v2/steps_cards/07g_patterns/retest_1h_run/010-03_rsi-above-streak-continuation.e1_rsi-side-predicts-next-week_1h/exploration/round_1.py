def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    rows = []
    hb = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            f = b["forecast"].values
            ts = pd.to_datetime(b["timestamp"])
            # 168h grid
            for i in range(0, n - 168, 168):
                r168 = c[i+168]/c[i]-1
                r24 = c[i+24]/c[i]-1 if i+24 < n else np.nan
                past24 = c[i]/c[i-24]-1 if i >= 24 else np.nan
                past168 = c[i]/c[i-168]-1 if i >= 168 else np.nan
                lr = np.diff(np.log(c[max(0,i-168):i+1]))
                vol = lr.std() if len(lr) > 20 else np.nan
                rows.append(dict(coin=coin, w=w, f=f[i], r168=r168, r24=r24, p24=past24, p168=past168, vol=vol,
                                 year=ts[i].year))
            # hourly gross gain vs fee
            a = b["postRebalance_current_allocation"].values
            ret1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            g = a*ret1
            fee = (b["total_portfolio_value"].values - b["postRebalance_total_value"].values)/b["total_portfolio_value"].values
            hb.append(pd.DataFrame(dict(coin=coin, hour=ts.dt.hour, wd=ts.dt.dayofweek, gross=g, fee=fee, ret1=ret1,
                                        a=a, turn=np.abs(b["postRebalance_current_allocation"].values-b["previous_allocation"].values))))
    df = pd.DataFrame(rows)
    df["ex"] = df["r168"] - df.groupby("coin")["r168"].transform("mean")
    df["fq"] = df.groupby("coin")["f"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["fwd168_by_forecast_quintile"] = df.groupby("fq")["ex"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["fwd168_by_quintile_coin"] = df.groupby(["coin","fq"])["ex"].mean().unstack()
    df["p168q"] = df.groupby("coin")["p168"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["fwd168_by_past168_quintile"] = df.groupby("p168q")["ex"].agg(["mean","count"])
    df["volq"] = df.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["prod_by_volq"] = (df.assign(prod=df.f/10*df.ex)).groupby("volq")["prod"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["prod_by_year"] = (df.assign(prod=df.f/10*df.ex)).groupby("year")["prod"].agg(["mean","count"])
    # 24h grid within same samples for past24 reversal
    df["e24"] = df["r24"] - df.groupby("coin")["r24"].transform("mean")
    out["corr_p24_r24"] = df[["p24","e24"]].corr().iloc[0,1]
    H = pd.concat(hb)
    out["gross_fee_turn_by_coin"] = H.groupby("coin")[["gross","fee","turn"]].mean()*24
    out["gross_by_hour"] = H.groupby("hour")[["gross","fee","ret1"]].mean()
    out["ret_by_weekday"] = H.groupby("wd")["ret1"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # days
    D = pd.concat([d.assign(coin=c, w=w) for c in days for w, d in days[c].items()])
    out["book_daily_stats"] = D.groupby("coin")[["book_return","coin_return"]].mean()
    return out
