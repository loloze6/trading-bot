def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    dayrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            raw = b.get("debug_info.components.vol_scaled_mom.last_history_value")
            pp = b.get("debug_info.components.vol_scaled_mom.post_pipeline_value")
            ret30 = c / c.shift(30) - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60, min_periods=20).std()
            # signed streak
            s = np.sign(r1.fillna(0)).values
            st = np.zeros(len(s))
            for i in range(1, len(s)):
                st[i] = st[i-1] + s[i] if (s[i] != 0 and np.sign(st[i-1]) == s[i]) else s[i]
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n - 10, 10):
                rows.append(dict(coin=coin, w=w, day=ts[i].normalize(), wd=ts[i].dayofweek, yr=ts[i].year,
                                 fwd=c[i+10]/c[i]-1, fwd3=c[min(i+3,n-1)]/c[i]-1,
                                 raw=raw[i] if raw is not None else np.nan,
                                 pp=pp[i] if pp is not None else np.nan,
                                 r1=r1[i], ret30=ret30[i], vol20=vol20[i], vol60=vol60[i],
                                 volratio=vol20[i]/vol60[i] if vol60[i] else np.nan,
                                 streak=st[i], alloc=b["postRebalance_current_allocation"][i]))
            # daily rows: next-day return after big moves, weekday
            z = r1 / vol60.shift(1)
            for i in range(1, n-1):
                dayrows.append(dict(coin=coin, wd=ts[i].dayofweek, z=z[i], nxt=r1[i+1]))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["fwd"].mean()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    sd = g.groupby("coin")["fwd"].std()
    g["str"] = g["ex"] / g["coin"].map(sd)

    def summ(df, key):
        out = []
        for k, d in df.groupby(key, observed=True):
            dd = d.dropna(subset=["ex"])
            dev = (dd["ex"] - dd["ex"].mean())
            per = dev.groupby(dd["day"]).sum()
            se = np.sqrt((per**2).sum()) / len(dd) if len(dd) > 1 else np.nan
            out.append(dict(key=str(k), n=len(dd), days=dd["day"].nunique(),
                            ex_mean=dd["ex"].mean(), strength=dd["str"].mean(),
                            t_day=dd["ex"].mean()/se if se else np.nan))
        return pd.DataFrame(out)

    res = {}
    g["raw_q"] = pd.qcut(g["raw"], 10, duplicates="drop")
    res["raw ratio deciles -> 10d excess"] = summ(g.dropna(subset=["raw"]), "raw_q")
    g["streak_b"] = pd.cut(g["streak"], [-99,-5,-3,-1.5,0,1.5,3,5,99])
    res["streak at grid bar -> 10d excess"] = summ(g, "streak_b")
    g["vol_t"] = g.groupby("coin")["vol60"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    g["pos"] = np.where(g["raw"] > 0, "up30", "down30")
    g["vt_pos"] = g["vol_t"].astype(str) + "_" + g["pos"]
    res["vol tercile x 30d sign -> excess"] = summ(g.dropna(subset=["vol_t"]), "vt_pos")
    g["vr_q"] = pd.qcut(g["volratio"], 4, duplicates="drop")
    res["vol20/vol60 quartile -> excess"] = summ(g.dropna(subset=["volratio"]), "vr_q")
    g["vr_pos"] = pd.qcut(g["volratio"], 3, labels=["vrLo","vrMid","vrHi"]).astype(str) + "_" + g["pos"]
    res["volratio tercile x 30d sign"] = summ(g.dropna(subset=["volratio"]), "vr_pos")
    g["r1z"] = g["r1"] / g["vol60"]
    g["r1z_b"] = pd.cut(g["r1z"], [-99,-2,-1,0,1,2,99])
    res["last day z -> 10d excess"] = summ(g.dropna(subset=["r1z"]), "r1z_b")
    res["year -> excess when up30"] = summ(g[g.pos=="up30"], "yr")
    d = pd.DataFrame(dayrows).dropna()
    d["zb"] = pd.cut(d["z"], [-99,-3,-2,-1,0,1,2,3,99])
    res["daily z -> next day ret"] = d.groupby("zb", observed=True)["nxt"].agg(["count","mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    res["weekday -> next day ret"] = d.groupby("wd")["nxt"].agg(["count","mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    if tr:
        T = pd.concat(tr)
        T["fb"] = pd.qcut(T["entry_forecast"], 5, duplicates="drop")
        res["trades by entry forecast"] = T.groupby("fb", observed=True)["net_profit_loss_percent"].agg(["count","mean","median"])
        T["db"] = pd.qcut(T["duration_minutes"], 4, duplicates="drop")
        res["trades by duration"] = T.groupby("db", observed=True)["net_profit_loss_percent"].agg(["count","mean"])
    return res
