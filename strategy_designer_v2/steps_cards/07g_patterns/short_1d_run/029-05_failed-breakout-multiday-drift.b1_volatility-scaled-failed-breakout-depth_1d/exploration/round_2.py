def explore(data):
    import numpy as np, pandas as pd
    H = 8
    rows = []; daily = []; fb = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < 40:
                continue
            s = pd.Series(c)
            r1 = s.pct_change()
            vol = r1.rolling(20).std()
            hi20 = s.shift(1).rolling(20).max()
            z = r1 / vol
            r3 = s / s.shift(3) - 1
            z3 = r3 / (vol * np.sqrt(3))
            ts = pd.to_datetime(b["timestamp"])
            yr = ts.dt.year.values; dow = ts.dt.dayofweek.values
            half = "early" if int(w[1:]) <= 12 else "late"
            brk_up = (s > hi20).values
            for t in range(0, n - H, H):
                rows.append(dict(coin=coin, half=half, fwd=c[t+H]/c[t]-1, z=z.iloc[t], z3=z3.iloc[t],
                                 fwd2=c[t+2]/c[t]-1 if t+2<n else np.nan))
            for t in range(1, n):
                daily.append(dict(coin=coin, half=half, yr=yr[t], r=c[t]/c[t-1]-1, dow=dow[t],
                                  zp=z.iloc[t-1], z3p=z3.iloc[t-1]))
            # failed breakout events at t (not gridded), forward pieces 0-2 and 2-10
            last = -100
            for t in range(24, n - 10):
                hit = False
                for k in range(1, 4):
                    j = t - k
                    if brk_up[j] and c[t] < hi20.iloc[j] and not brk_up[t]:
                        hit = True; break
                if hit and t - last >= 10:
                    last = t
                    fb.append(dict(coin=coin, half=half, f02=c[t+2]/c[t]-1, f210=c[t+10]/c[t+2]-1, f010=c[t+10]/c[t]-1,
                                   z=z.iloc[t]))
    df = pd.DataFrame(rows); dd = pd.DataFrame(daily); fe = pd.DataFrame(fb)
    df["ex"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    dd["ex"] = dd["r"] - dd.groupby("coin")["r"].transform("mean")
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    out = {}
    # next-day reversal after prior-day z, deciles, and by coin / half
    dd["zq"] = pd.qcut(dd["zp"], 10, labels=False)
    out["next_day_ex_by_prevday_z_decile"] = dd.groupby("zq")["ex"].apply(tt).unstack()
    low = dd[dd["zq"] <= 1]
    out["next_day_ex_prevz_bottom20_by_coin"] = low.groupby("coin")["ex"].apply(tt).unstack()
    out["next_day_ex_prevz_bottom20_by_half"] = low.groupby("half")["ex"].apply(tt).unstack()
    out["next_day_ex_prevz_bottom20_by_year"] = low.groupby("yr")["ex"].apply(tt).unstack()
    # slope: regression of next day ex on prev z within negative z only
    neg = dd[dd["zp"] < 0].dropna(subset=["zp", "ex"])
    sl = np.polyfit(neg["zp"], neg["ex"], 1)
    out["slope_nextday_on_negz"] = float(sl[0])
    out["corr_nextday_negz"] = float(np.corrcoef(neg["zp"], neg["ex"])[0, 1]); out["n_negz"] = len(neg)
    # 3-day z, next day
    dd["z3q"] = pd.qcut(dd["z3p"], 5, labels=False)
    out["next_day_ex_by_prev3d_z_quintile"] = dd.groupby("z3q")["ex"].apply(tt).unstack()
    # 8-day grid by 1-day z deciles and by half
    df["zq"] = pd.qcut(df["z"], 5, labels=False)
    out["fwd8_ex_by_z_quintile_half"] = df.groupby(["half", "zq"])["ex"].apply(tt).unstack()
    # saturday
    sat = dd[dd["dow"] == 5]
    out["sat_ex_by_coin"] = sat.groupby("coin")["ex"].apply(tt).unstack()
    out["sat_ex_by_year"] = sat.groupby("yr")["ex"].apply(tt).unstack()
    out["sat_ex_by_half"] = sat.groupby("half")["ex"].apply(tt).unstack()
    # failed breakout events
    out["failed_breakout_pieces"] = pd.DataFrame({k: tt(fe[k]) for k in ["f02", "f210", "f010"]})
    out["failed_breakout_by_half_f02"] = fe.groupby("half")["f02"].apply(tt).unstack()
    return out
