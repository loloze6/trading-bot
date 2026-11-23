def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close","regime"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.set_index("timestamp")
            c = d["close"]
            r1 = c.pct_change()
            vol = r1.rolling(720, min_periods=300).std()
            # day starts at 00:00
            midn = d.index[d.index.hour == 0]
            for t in midn:
                i = d.index.get_loc(t)
                if i - 48 < 0 or i + 48 >= len(d) or i - 168 < 0: continue
                # past day: close[i]/close[i-24]-1 (bar at i opens at 00:00; close[i-1] is end of previous day)
                p = c.iloc[i-1]
                prev_day = p / c.iloc[i-25] - 1
                day2 = c.iloc[i-25] / c.iloc[i-49] - 1
                wk = p / c.iloc[i-169] - 1
                fwd = c.iloc[i+47] / p - 1
                fwd24 = c.iloc[i+23] / p - 1
                v = vol.iloc[i-1]
                rows.append(dict(coin=coin, w=w, wd=t.weekday(), year=t.year,
                                 prev=prev_day, prev2=day2, wk=wk, fwd=fwd, fwd24=fwd24,
                                 vol=v, reg=d["regime"].iloc[i-1]))
    X = pd.DataFrame(rows).dropna()
    X["prevs"] = X.prev / (X.vol*np.sqrt(24))
    X["prev2s"] = X.prev2 / (X.vol*np.sqrt(24))
    X["fwds"] = X.fwd / (X.vol*np.sqrt(48))
    X["fwd24s"] = X.fwd24 / (X.vol*np.sqrt(24))
    X["vt"] = X.groupby("coin").vol.transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=["lo","mid","hi"]))
    def slope(g, xcol, ycol):
        g = g[[xcol,ycol]].dropna()
        if len(g) < 30: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, corr=np.nan))
        r = stats.linregress(g[xcol], g[ycol])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope/r.stderr, corr=r.rvalue))
    out = {}
    # prev day (scaled) -> next 48h, by weekday of day start (wd=0 Monday means prev day = Sunday)
    out["prevday_to_48h_by_startwd"] = X.groupby("wd").apply(lambda g: slope(g,"prevs","fwds"))
    out["day2back_to_48h_by_startwd"] = X.groupby("wd").apply(lambda g: slope(g,"prev2s","fwds"))
    M = X[X.wd==0].copy()
    M["agree"] = np.sign(M.prev2) == np.sign(M.wk)
    out["mon_sat_by_vol_agree"] = M.groupby(["vt","agree"]).apply(lambda g: slope(g,"prev2s","fwds"))
    out["mon_sat_by_coin"] = M.groupby("coin").apply(lambda g: slope(g,"prev2s","fwds"))
    out["mon_sun_to_24h_and_48h"] = pd.DataFrame({"48h": slope(M,"prevs","fwds"), "24h": slope(M,"prevs","fwd24s")})
    # weekly return alone -> next 48h by start weekday
    X["wks"] = X.wk/(X.vol*np.sqrt(168))
    out["week_to_48h_by_startwd"] = X.groupby("wd").apply(lambda g: slope(g,"wks","fwds"))
    # mean fwd 24h scaled return by weekday
    out["mean_day_ret_by_wd"] = X.groupby("wd").fwd24s.agg(["mean","count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # trades
    T = []
    for coin, wins in trades.items():
        for w, tdf in wins.items():
            if tdf is None or len(tdf)==0: continue
            t = tdf.copy(); t["coin"]=coin; T.append(t)
    T = pd.concat(T)
    T["year"] = pd.to_datetime(T.entry_time, utc=True).dt.year
    out["trades_by_side"] = T.groupby("side").net_profit_loss_percent.agg(["count","mean","median",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["trades_by_year"] = T.groupby("year").net_profit_loss_percent.agg(["count","mean",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["trades_by_coin"] = T.groupby("coin").net_profit_loss_percent.agg(["count","mean",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    T["q"] = pd.qcut(T.entry_forecast.abs().rank(method="first"), 4, labels=False)
    out["trades_by_absforecast_q"] = T.groupby("q").net_profit_loss_percent.agg(["count","mean",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    return out
