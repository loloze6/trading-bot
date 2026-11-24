import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            volr = vol / vol.rolling(180, min_periods=60).mean()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            clv = (b["close"] - b["low"]) / rng
            d = pd.DataFrame({
                "w": w, "pos": np.arange(len(b)),
                "r": r, "z": r / vol, "volr": volr, "clv": clv,
                "rngz": (rng / b["close"]) / vol,
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "n1": c.shift(-1) / c - 1,
                "n3": c.shift(-3) / c - 1,
                "n5": c.shift(-5) / c - 1,
                "n20": c.shift(-20) / c - 1,
                "p60": c / c.shift(60) - 1,
                "p5": c / c.shift(5) - 1,
                "alloc": b["postRebalance_current_allocation"],
                "fc": b["forecast"],
            })
            d["p60z"] = d["p60"] / (vol * np.sqrt(60))
            d["p5z"] = d["p5"] / (vol * np.sqrt(5))
            # streak of down days
            dn = (r < 0).astype(int)
            d["streak"] = dn.groupby((dn == 0).cumsum()).cumsum()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D["r"].mean()
    D["x1"] = D["n1"] - mu1

    def tstat(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})

    out = {}
    D["zbin"] = pd.qcut(D["z"], 10, labels=False)
    out["next1_excess_by_z_decile"] = D.groupby("zbin")["x1"].apply(tstat).unstack().join(D.groupby("zbin")["z"].mean().rename("zmean"))
    # up days only by volr tercile
    up = D[D["z"] > 1].copy(); dnn = D[D["z"] < -1].copy()
    out["bigup_z>1_next1_by_volr_tercile"] = up.groupby(pd.qcut(up["volr"], 3, labels=False))["x1"].apply(tstat).unstack()
    out["bigdown_z<-1_next1_by_volr_tercile"] = dnn.groupby(pd.qcut(dnn["volr"], 3, labels=False))["x1"].apply(tstat).unstack()
    # close location on down days
    dd = D[D["r"] < 0]
    out["down_days_next1_by_clv_tercile"] = dd.groupby(pd.qcut(dd["clv"], 3, labels=False))["x1"].apply(tstat).unstack()
    ud = D[D["r"] > 0]
    out["up_days_next1_by_clv_tercile"] = ud.groupby(pd.qcut(ud["clv"], 3, labels=False))["x1"].apply(tstat).unstack()
    # all days by clv and by range size
    out["all_next1_by_clv_quintile"] = D.groupby(pd.qcut(D["clv"], 5, labels=False))["x1"].apply(tstat).unstack()
    out["all_next1_by_rangez_quintile"] = D.groupby(pd.qcut(D["rngz"], 5, labels=False))["x1"].apply(tstat).unstack()
    # weekday of next day return (signal bar weekday)
    out["next1_excess_by_signal_weekday"] = D.groupby("wd")["x1"].apply(tstat).unstack()
    # streaks
    out["next1_by_down_streak"] = D.groupby(D["streak"].clip(upper=4))["x1"].apply(tstat).unstack()
    # 5-day scaled return quintile -> next 1 and next 5 (grid 5)
    g5 = D[D["pos"] % 5 == 0]
    mu5 = (D.loc[D["pos"] % 5 == 0, "n5"]).mean()
    g5 = g5.assign(x5=g5["n5"] - mu5)
    out["grid5_next5_by_p5z_quintile"] = g5.groupby(pd.qcut(g5["p5z"], 5, labels=False))["x5"].apply(tstat).unstack()
    # brief: 60d move -> next 20d (grid 20)
    g20 = D[D["pos"] % 20 == 0]
    mu20 = g20["n20"].mean()
    g20 = g20.assign(x20=g20["n20"] - mu20)
    out["grid20_next20_by_p60z_tercile"] = g20.groupby(pd.qcut(g20["p60z"], 3, labels=False))["x20"].apply(tstat).unstack()
    # big down days: next 1 split by 60-day trend tercile
    out["bigdown_next1_by_p60z_tercile"] = dnn.groupby(pd.qcut(dnn["p60z"], 3, labels=False))["x1"].apply(tstat).unstack()
    out["bigup_next1_by_p60z_tercile"] = up.groupby(pd.qcut(up["p60z"], 3, labels=False))["x1"].apply(tstat).unstack()
    # by year for big down
    out["bigdown_next1_by_year"] = dnn.groupby("yr")["x1"].apply(tstat).unstack()
    # book: daily returns, largest gains/losses context
    days = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            days.append(dy.assign(w=w))
    Y = pd.concat(days, ignore_index=True)
    Y["prev_coin"] = Y.groupby("w")["coin_return"].shift(1)
    q = Y["book_return"].quantile([0.02, 0.98])
    out["book_extreme_days_context"] = pd.DataFrame({
        "worst2%_mean_coin_ret": [Y.loc[Y["book_return"] <= q.iloc[0], "coin_return"].mean()],
        "worst2%_mean_prev_coin_ret": [Y.loc[Y["book_return"] <= q.iloc[0], "prev_coin"].mean()],
        "best2%_mean_coin_ret": [Y.loc[Y["book_return"] >= q.iloc[1], "coin_return"].mean()],
        "best2%_mean_prev_coin_ret": [Y.loc[Y["book_return"] >= q.iloc[1], "prev_coin"].mean()],
        "n_each": [int((Y["book_return"] <= q.iloc[0]).sum())],
    })
    out["mu1"] = float(mu1)
    return out
