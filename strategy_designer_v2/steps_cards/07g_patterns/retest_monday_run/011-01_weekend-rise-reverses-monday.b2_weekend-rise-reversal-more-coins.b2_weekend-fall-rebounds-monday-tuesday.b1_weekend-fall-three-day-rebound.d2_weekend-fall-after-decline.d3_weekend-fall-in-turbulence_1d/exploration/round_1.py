def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []      # every bar with features
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "wd": pd.to_datetime(b["timestamp"], utc=True).dt.weekday,
                "year": pd.to_datetime(b["timestamp"], utc=True).dt.year,
                "r1": r1, "r_next1": c.shift(-1)/c - 1, "r_next3": c.shift(-3)/c - 1,
                "r7": c/c.shift(7) - 1, "r20": c/c.shift(20) - 1,
                "vol20": r1.rolling(20).std(), "vol60": r1.rolling(60).std(),
                "vlr": np.log(b["volume"].astype(float).replace(0, np.nan)) - np.log(b["volume"].astype(float).replace(0, np.nan)).rolling(20).mean(),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            d["volratio"] = d["vol20"]/d["vol60"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # coin drift over 3 days (non-overlapping grid)
    g3 = D[D["pos"] % 3 == 0]
    drift3 = g3.groupby("coin")["r_next3"].mean()
    D["ex3"] = D["r_next3"] - D["coin"].map(drift3)
    drift1 = D.groupby("coin")["r_next1"].mean()
    D["ex1"] = D["r_next1"] - D["coin"].map(drift1)
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # 1. next-day excess return by weekday of the bar (each bar counted once: 1-day horizon)
    out["next1_ex_by_weekday_of_bar"] = D.groupby("wd")["ex1"].apply(tt).unstack()
    # 2. next-3-day excess return from each weekday, by sign/size of that day's return (one per week per weekday: non-overlapping within weekday)
    D["r1q"] = D.groupby("wd")["r1"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["ex3_by_weekday_x_r1quintile_mean%"] = D.pivot_table(index="wd", columns="r1q", values="ex3", aggfunc=lambda x: 100*x.mean())
    out["ex3_by_weekday_x_r1quintile_t"] = D.pivot_table(index="wd", columns="r1q", values="ex3", aggfunc=lambda x: x.mean()/(x.std()/np.sqrt(x.count())))
    # 3. on grid 3: 7-day return quintile, 20-day return quintile, vol20 quintile, volume-surprise quintile
    G = D[D["pos"] % 3 == 0].copy()
    for f in ["r1", "r7", "r20", "vol20", "volratio", "vlr"]:
        G["q"] = G.groupby("coin")[f].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
        out[f"grid3_ex3_by_{f}_quintile"] = G.groupby("q")["ex3"].apply(tt).unstack()
    # 4. pooled regression slopes (per-coin standardised feature) on grid 3
    reg = {}
    for f in ["r1", "r7", "r20", "vol20", "volratio", "vlr"]:
        z = G.groupby("coin")[f].transform(lambda x: (x - x.mean())/x.std())
        m = z.notna() & G["ex3"].notna()
        s = stats.linregress(z[m], G["ex3"][m])
        reg[f] = {"slope%": 100*s.slope, "t": s.slope/s.stderr, "n": int(m.sum())}
    out["grid3_slope_ex3_on_feature"] = pd.DataFrame(reg).T
    # 5. Sunday cases: sunday return split by weekend volume surprise
    S = D[D["wd"] == 6].copy()
    S["fall"] = S["r1"] < 0
    S["vlr_hi"] = S["vlr"] > S.groupby("coin")["vlr"].transform("median")
    out["sunday_ex3_by_fall_x_volume"] = S.groupby(["fall", "vlr_hi"])["ex3"].apply(tt).unstack()
    # 6. book: by window position (year) and by coin
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(pd.DataFrame({"coin": coin, "win": w, "br": d["book_return"].values, "cr": d["coin_return"].values,
                                    "year": pd.to_datetime(d["day"]).dt.year.values}))
    B = pd.concat(bk)
    out["book_by_coin"] = B.groupby("coin").agg(n=("br", "count"), book_mean_bp=("br", lambda x: 1e4*x.mean()), coin_mean_bp=("cr", lambda x: 1e4*x.mean()))
    out["book_by_year"] = B.groupby("year").agg(n=("br", "count"), book_mean_bp=("br", lambda x: 1e4*x.mean()), coin_mean_bp=("cr", lambda x: 1e4*x.mean()))
    # 7. trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    T["ef_q"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    out["trades_by_entry_forecast_quartile"] = T.groupby("ef_q").agg(n=("net_profit_loss_percent", "count"),
        ef_mean=("entry_forecast", "mean"), net_mean=("net_profit_loss_percent", "mean"), gross_mean=("profit_loss_percent", "mean"),
        days=("duration_minutes", lambda x: x.mean()/1440))
    return out
