def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            if b is None or len(b) < 30: continue
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            f = b["forecast"].astype(float).fillna(0)
            mom20 = c / c.shift(20) - 1
            vol20 = r.rolling(20).std()
            fwd1 = c.shift(-1) / c - 1
            fwd5 = c.shift(-5) / c - 1
            fwd20 = c.shift(-20) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "r": r, "f": f,
                              "mom20": mom20, "vol20": vol20, "fwd1": fwd1, "fwd5": fwd5, "fwd20": fwd20,
                              "wd": ts.dt.weekday, "year": ts.dt.year,
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "regime": b["regime"].astype(str)})
            # z of daily return vs trailing vol
            d["z"] = r / vol20.shift(1)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    def tstat(x):
        x = pd.Series(x).dropna()
        if len(x) < 3: return (len(x), np.nan, np.nan)
        return (len(x), x.mean(), x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))
    # forward 20 by forecast bucket, non-overlapping
    NO = D[D["i"] % 20 == 0].copy()
    NO["bucket"] = pd.cut(NO["f"], [-1e9, 0.0001, 0.5, 1.0, 1.5, 1e9], labels=["0", "0-.5", ".5-1", "1-1.5", ">1.5"])
    g = NO.groupby("bucket")["fwd20"].apply(lambda x: pd.Series(tstat(x), index=["n", "mean", "t"])).unstack()
    out["fwd20_by_forecast_bucket_nonoverlap"] = g
    # flat bars split by mom20 sign
    NO["state"] = np.where(NO["f"] > 0, "active", np.where(NO["mom20"] < 0, "flat_mom_neg", "flat_mom_pos"))
    out["fwd20_by_state"] = NO.groupby("state")["fwd20"].apply(lambda x: pd.Series(tstat(x), index=["n", "mean", "t"])).unstack()
    # next-day after large moves (each bar is a 1-bar sample -> non-overlapping)
    D["zb"] = pd.cut(D["z"], [-1e9, -2.5, -1.5, 1.5, 2.5, 1e9], labels=["<-2.5", "-2.5..-1.5", "mid", "1.5..2.5", ">2.5"])
    out["fwd1_by_today_z"] = D.groupby("zb")["fwd1"].apply(lambda x: pd.Series(tstat(x), index=["n", "mean", "t"])).unstack()
    N5 = D[D["i"] % 5 == 0]
    out["fwd5_by_today_z_nonoverlap"] = N5.groupby("zb")["fwd5"].apply(lambda x: pd.Series(tstat(x), index=["n", "mean", "t"])).unstack()
    # weekday
    out["ret_by_weekday"] = D.groupby("wd")["r"].apply(lambda x: pd.Series(tstat(x), index=["n", "mean", "t"])).unstack()
    # vol level terciles per coin
    D["volq"] = D.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["fwd20_by_volq_and_active_nonoverlap"] = D[D["i"] % 20 == 0].assign(act=lambda x: x["f"] > 0).groupby(["volq", "act"])["fwd20"].apply(lambda x: pd.Series(tstat(x), index=["n", "mean", "t"])).unstack()
    # by year active excess
    out["fwd20_active_by_year"] = NO[NO["f"] > 0].groupby("year")["fwd20"].apply(lambda x: pd.Series(tstat(x), index=["n", "mean", "t"])).unstack()
    out["fwd20_all_by_coin"] = NO.groupby(["coin", "state"])["fwd20"].mean().unstack()
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["durb"] = pd.cut(T["dur_d"], [-1, 1, 3, 10, 30, 1e9])
    out["trades_by_duration"] = T.groupby("durb")["net_profit_loss_percent"].agg(["count", "mean", "median", "sum"])
    out["trades_summary"] = pd.Series({"n": len(T), "win": (T["net_profit_loss_percent"] > 0).mean(),
                                       "mean": T["net_profit_loss_percent"].mean(),
                                       "top10pct_share_of_sum": T["net_profit_loss_percent"].nlargest(max(1, len(T)//10)).sum() / T["net_profit_loss_percent"].sum()})
    return out
