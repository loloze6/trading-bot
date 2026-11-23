def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        d2 = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - 2, 2):
                d2.append(c[i+2]/c[i]-1)
        drift2 = np.mean(d2); usual2 = np.std(d2)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"]; h = b["high"]; l = b["low"]; v = b["volume"]
            r1 = c/c.shift(1)-1
            mabs = r1.abs().rolling(60, min_periods=20).mean().shift(1)
            df = pd.DataFrame({"coin": coin, "win": w, "wd": ts.dt.weekday, "year": ts.dt.year,
                "z": r1/mabs, "z7": (c/c.shift(7)-1)/mabs, "z5": (c.shift(2)/c.shift(7)-1)/mabs,
                "loc": (c-l)/(h-l), "rng": ((h-l)/c)/mabs,
                "vol": mabs, "vr": v.rolling(60, min_periods=20).mean().shift(1)/v,
                "f1": c.shift(-1)/c-1, "t1": c.shift(-2)/c.shift(-1)-1,
                "f2x": c.shift(-2)/c-1-drift2, "u2": (c.shift(-2)/c-1-drift2)/usual2,
                "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    D = pd.concat(rows).dropna(subset=["z", "f2x"])
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    out = {}
    S = D[(D.wd == 6) & (D.z > 0)].copy()
    S["rev"] = -S["f2x"]
    out["sunrise_monday_day_vs_tuesday_day_raw"] = pd.DataFrame({"mon": tt(-S["f1"]), "tue": tt(-S["t1"])}).T
    # Sunday rise reversal graded by Mon-Fri (5 days before weekend) move
    S["q"] = pd.qcut(S["z5"], 5, labels=False)
    out["sunrise_rev_by_prior_weekdays_move_q"] = S.groupby("q")["rev"].apply(tt).unstack()
    S["q"] = pd.qcut(S["z7"], 5, labels=False)
    out["sunrise_rev_by_7d_move_q"] = S.groupby("q")["rev"].apply(tt).unstack()
    S["q"] = pd.qcut(S["loc"], 5, labels=False)
    out["sunrise_rev_by_close_location_q"] = S.groupby("q")["rev"].apply(tt).unstack()
    S["q"] = pd.qcut(S["vol"], 5, labels=False)
    out["sunrise_rev_by_vol_level_q"] = S.groupby("q")["rev"].apply(tt).unstack()
    # all Sundays: forward 2d excess by 7-day move quintile (graded reversal of the week?)
    A = D[D.wd == 6].copy()
    A["q"] = pd.qcut(A["z7"], 5, labels=False)
    out["allsun_fwd2_excess_by_7d_move_q"] = A.groupby("q")["f2x"].apply(tt).unstack()
    # Thu/Fri: continuation graded by size?
    for wd, nm in [(3, "thu"), (4, "fri")]:
        T = D[D.wd == wd].copy()
        T["q"] = pd.qcut(T["z"], 5, labels=False)
        out[nm + "_fwd2_excess_by_day_move_q"] = T.groupby("q")["f2x"].apply(tt).unstack()
    # Monday: forward 2 day excess by Monday move quintile
    M = D[D.wd == 0].copy()
    M["q"] = pd.qcut(M["z"], 5, labels=False)
    out["mon_fwd2_excess_by_day_move_q"] = M.groupby("q")["f2x"].apply(tt).unstack()
    # unconditional fwd 2 excess by weekday (calendar drift)
    out["fwd2_excess_by_weekday_all"] = D.groupby("wd")["f2x"].apply(tt).unstack()
    # book: daily returns by weekday, and largest days
    dr = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["win"] = w; x["coin"] = coin
            dr.append(x)
    R = pd.concat(dr).dropna()
    R["wd"] = pd.to_datetime(R["day"]).dt.weekday
    out["book_return_by_weekday_coin_pairs"] = R.groupby("wd")["book_return"].apply(tt).unstack()
    return out
