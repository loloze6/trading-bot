def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            o = b["open"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            # down-run count before current bar
            down = (r < 0).astype(int)
            run = np.zeros(len(c)); cnt = 0
            for i in range(len(c)):
                run[i] = cnt
                if r.iloc[i] < 0: cnt += 1
                else: cnt = 0 if not np.isnan(r.iloc[i]) else 0
            # run[i] = number of consecutive down closes before bar i
            ret60 = c / c.shift(60) - 1
            ret5 = c / c.shift(5) - 1
            sd30 = r.rolling(30).std()
            rng = (h - l) / c
            clv = (c - l) / (h - l).replace(0, np.nan)
            d = pd.DataFrame({"coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]), "r": r, "nxt": nxt, "nxt2": nxt2,
                              "run": run, "ret60": ret60, "ret5": ret5, "sd30": sd30, "rngz": rng / sd30, "clv": clv,
                              "upz": r / sd30, "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"]})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mean_coin = D.groupby("coin")["nxt"].transform("mean")
    D["ex"] = D["nxt"] - mean_coin
    D["trend"] = np.where(D.ret60 > 0.10, "rising", np.where(D.ret60 < -0.10, "falling", np.where(D.ret60.notna(), "choppy", None)))
    D["day"] = D.ts.dt.floor("D")
    def tday(x):
        x = x.dropna(subset=["ex"])
        if len(x) < 5: return pd.Series({"n": len(x), "mean_ex": np.nan, "t": np.nan})
        s = x.groupby("day")["ex"].sum(); nd = x.groupby("day").size()
        m = s.sum() / nd.sum()
        dev = (x["ex"] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / nd.sum()
        return pd.Series({"n": len(x), "mean_ex": m, "t": m / se})
    brk = D[(D.r > 0) & (D.run >= 2)].copy()
    out = {}
    out["break_by_trend"] = brk.groupby("trend").apply(tday)
    brk["runb"] = pd.cut(brk.run, [1, 2, 3, 4, 30], labels=["2", "3", "4", "5+"])
    out["break_falling_by_run"] = brk[brk.trend == "falling"].groupby("runb").apply(tday)
    out["break_rising_by_run"] = brk[brk.trend == "rising"].groupby("runb").apply(tday)
    # up day size in falling
    f = brk[brk.trend == "falling"].copy()
    f["upq"] = pd.qcut(f.upz, 3, labels=["small", "mid", "large"])
    out["falling_break_by_upsize"] = f.groupby("upq").apply(tday)
    f["clvq"] = pd.qcut(f.clv, 3, labels=["lowclose", "mid", "highclose"])
    out["falling_break_by_closeloc"] = f.groupby("clvq").apply(tday)
    # all up days (any run, incl. 0/1) by trend, upsize in falling
    up = D[(D.r > 0)].copy()
    up["runb"] = pd.cut(up.run, [-1, 0, 1, 30], labels=["0", "1", "2+"])
    out["falling_upday_by_run"] = up[up.trend == "falling"].groupby("runb").apply(tday)
    # all days in falling by r z size
    fa = D[D.trend == "falling"].copy()
    fa["rq"] = pd.qcut(fa.upz, 5, labels=["q1", "q2", "q3", "q4", "q5"])
    out["falling_all_by_rz_quintile"] = fa.groupby("rq").apply(tday)
    ri = D[D.trend == "rising"].copy()
    ri["rq"] = pd.qcut(ri.upz, 5, labels=["q1", "q2", "q3", "q4", "q5"])
    out["rising_all_by_rz_quintile"] = ri.groupby("rq").apply(tday)
    ch = D[D.trend == "choppy"].copy()
    ch["rq"] = pd.qcut(ch.upz, 5, labels=["q1", "q2", "q3", "q4", "q5"])
    out["choppy_all_by_rz_quintile"] = ch.groupby("rq").apply(tday)
    # weekday in falling breaks and overall
    D["wd"] = D.ts.dt.dayofweek
    out["all_by_weekday"] = D.groupby("wd").apply(tday)
    out["falling_break_by_coin"] = f.groupby("coin").apply(tday)
    # book side: held positions
    pos = D[D.alloc.fillna(0) < 0]
    out["pos_by_year"] = pos.assign(y=pos.ts.dt.year).groupby("y").apply(tday)
    return out
