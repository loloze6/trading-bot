def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi20 = c.shift(1).rolling(20).max()
            sd20 = r1.rolling(20).std()
            dist = (c - hi20) / hi20 / sd20
            tr60 = c / c.shift(60) - 1
            ret20 = c / c.shift(20) - 1
            fwd = c.shift(-H) / c - 1
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"])
            vol = b["volume"].astype(float)
            volz = vol / vol.rolling(20).mean()
            sd60 = r1.rolling(60).std()
            df = pd.DataFrame({"coin": coin, "w": w, "dist": dist, "tr60": tr60, "ret20": ret20,
                               "r1z": r1 / sd20, "fwd": fwd, "clv": clv, "volz": volz,
                               "volratio": sd20 / sd60, "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            df = df.iloc[::H]  # grid
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["fwd"])
    drift = d.groupby("coin")["fwd"].transform("mean")
    d["ex"] = d["fwd"] - drift
    d["prof"] = np.where(d["tr60"] > .10, "rising", np.where(d["tr60"] < -.10, "falling", "choppy"))
    d.loc[d["tr60"].isna(), "prof"] = np.nan

    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    dd = d.dropna(subset=["dist", "prof"])
    dd["dbin"] = pd.cut(dd["dist"], [-100, -6, -4, -2, -1, 0, 0.5, 1.5, 100])
    out["dist_bin_by_profile"] = dd.groupby(["prof", "dbin"]).apply(summ)
    out["spearman_dist_by_prof"] = dd.groupby("prof").apply(lambda g: pd.Series(stats.spearmanr(g["dist"], g["ex"], nan_policy="omit")[:2], index=["rho", "p"]))
    d2 = d.dropna(subset=["r1z"])
    d2["r1bin"] = pd.qcut(d2["r1z"], 6)
    out["last_day_move_swings"] = d2.groupby("r1bin").apply(summ)
    d3 = d.dropna(subset=["volratio"])
    d3["vbin"] = pd.qcut(d3["volratio"], 4)
    out["vol_ratio_20_60"] = d3.groupby("vbin").apply(summ)
    out["weekday"] = d.groupby("wd").apply(summ)
    d4 = d.dropna(subset=["ret20"]); d4["r20bin"] = pd.qcut(d4["ret20"], 6)
    out["ret20"] = d4.groupby("r20bin").apply(summ)
    d5 = d.dropna(subset=["volz"]); d5["vzb"] = pd.qcut(d5["volz"], 5)
    out["volume_vs_20d"] = d5.groupby("vzb").apply(summ)
    d6 = d.dropna(subset=["clv"]); d6["cb"] = pd.qcut(d6["clv"], 5)
    out["close_location"] = d6.groupby("cb").apply(summ)
    # breakout cases: volume and close location interaction
    bk = dd[(dd["dist"] > 0)]
    bk = bk.dropna(subset=["volz"])
    bk["vzb"] = pd.qcut(bk["volz"], 3)
    out["breakouts_by_volume_allprof"] = bk.groupby(["prof", "vzb"]).apply(summ)
    # book daily returns
    days = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; days.append(t)
    D = pd.concat(days)
    out["book_by_window"] = D.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    T["ef"] = pd.qcut(T["entry_forecast"].astype(float), 4, duplicates="drop")
    out["trades_by_entry_fc"] = T.groupby("ef")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trade_duration_days"] = (T["duration_minutes"] / 1440).describe()
    return out
