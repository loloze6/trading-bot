def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            lv = np.log(b["volume"].astype(float).replace(0, np.nan))
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "wd": ts.dt.weekday, "year": ts.dt.year,
                "r1": r1, "r_next1": c.shift(-1)/c - 1, "r_next3": c.shift(-3)/c - 1,
                "vlr": lv - lv.rolling(20).mean(),
                "vlr5": lv.rolling(2).mean() - lv.rolling(20).mean(),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift3 = D[D["pos"] % 3 == 0].groupby("coin")["r_next3"].mean()
    D["ex3"] = D["r_next3"] - D["coin"].map(drift3)
    drift1 = D.groupby("coin")["r_next1"].mean()
    D["ex1"] = D["r_next1"] - D["coin"].map(drift1)
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    # weekday next-day effect robustness
    for wd in [1, 2]:
        sub = D[D["wd"] == wd]
        out[f"next1_ex_wd{wd}_by_year"] = sub.groupby("year")["ex1"].apply(tt).unstack()
        out[f"next1_ex_wd{wd}_by_coin"] = sub.groupby("coin")["ex1"].apply(tt).unstack()
    # Wednesday-close minus Tuesday-close difference, Welch
    a = D[D["wd"] == 1]["ex1"].dropna(); b_ = D[D["wd"] == 2]["ex1"].dropna()
    out["wd1_minus_wd2_welch_t"] = float(stats.ttest_ind(a, b_, equal_var=False).statistic)
    # volume surprise slope on grid3, by year and by coin
    G = D[D["pos"] % 3 == 0].copy()
    G["z"] = G.groupby("coin")["vlr"].transform(lambda x: (x - x.mean())/x.std())
    G["zr"] = G.groupby("coin")["r1"].transform(lambda x: (x - x.mean())/x.std())
    def sl(g):
        m = g["z"].notna() & g["ex3"].notna()
        if m.sum() < 20: return pd.Series({"n": m.sum(), "slope%": np.nan, "t": np.nan})
        s = stats.linregress(g["z"][m], g["ex3"][m])
        return pd.Series({"n": m.sum(), "slope%": 100*s.slope, "t": s.slope/s.stderr})
    out["vlr_slope_by_year"] = G.groupby("year").apply(sl)
    out["vlr_slope_by_coin"] = G.groupby("coin").apply(sl)
    # volume surprise split by sign of the day's return
    G["up"] = G["r1"] > 0
    out["vlr_slope_by_day_sign"] = G.groupby("up").apply(sl)
    # multiple regression ex3 on z(vlr) and z(r1)
    m = G["z"].notna() & G["zr"].notna() & G["ex3"].notna()
    X = np.column_stack([np.ones(m.sum()), G["z"][m], G["zr"][m]])
    y = G["ex3"][m].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    s2 = res @ res / (len(y) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["multi_reg_ex3_on_vlr_r1"] = pd.DataFrame({"coef%": 100*beta, "t": beta/se}, index=["const", "vlr", "r1"])
    # 1-day horizon volume slope (every bar, non-overlapping at h=1)
    D["z"] = D.groupby("coin")["vlr"].transform(lambda x: (x - x.mean())/x.std())
    mm = D["z"].notna() & D["ex1"].notna()
    s = stats.linregress(D["z"][mm], D["ex1"][mm])
    out["vlr_slope_ex1_all_bars"] = pd.Series({"n": int(mm.sum()), "slope%": 100*s.slope, "t": s.slope/s.stderr})
    # Sunday: rise x volume continuous
    S = D[D["wd"] == 6].copy()
    S["z"] = S.groupby("coin")["vlr5"].transform(lambda x: (x - x.mean())/x.std())
    for nm, sub in [("rise", S[S["r1"] > 0]), ("fall", S[S["r1"] < 0])]:
        mm = sub["z"].notna() & sub["ex3"].notna()
        s = stats.linregress(sub["z"][mm], sub["ex3"][mm])
        out[f"sunday_{nm}_ex3_slope_on_weekend_volume"] = pd.Series({"n": int(mm.sum()), "slope%": 100*s.slope, "t": s.slope/s.stderr})
    # Sunday signed return x weekend volume interaction: ex3 on r1*z
    S["zr"] = S.groupby("coin")["r1"].transform(lambda x: (x - x.mean())/x.std())
    mm = S["z"].notna() & S["zr"].notna() & S["ex3"].notna()
    X = np.column_stack([np.ones(mm.sum()), S["zr"][mm], S["z"][mm], (S["zr"]*S["z"])[mm]])
    y = S["ex3"][mm].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    se = np.sqrt(np.diag(res @ res / (len(y) - 4) * np.linalg.inv(X.T @ X)))
    out["sunday_ex3_on_r1_vol_interaction"] = pd.DataFrame({"coef%": 100*beta, "t": beta/se}, index=["const", "r1", "wkvol", "r1xwkvol"])
    return out
