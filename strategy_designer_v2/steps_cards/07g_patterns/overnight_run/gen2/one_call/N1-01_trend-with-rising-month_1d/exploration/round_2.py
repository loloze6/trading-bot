def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            if b is None or len(b) < 30: continue
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            r = c.pct_change()
            f = b["forecast"].astype(float).fillna(0)
            vol20 = r.rolling(20).std()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "r": r, "f": f,
                              "vol20": vol20, "fwd1": c.shift(-1)/c-1, "fwd20": c.shift(-20)/c-1,
                              "wd": ts.dt.weekday, "hour": ts.dt.hour, "year": ts.dt.year,
                              "mom20": c/c.shift(20)-1,
                              "bv": b["postRebalance_total_value"].astype(float)})
            d["z"] = r / vol20.shift(1)
            d["bret_next"] = d["bv"].shift(-1)/d["bv"]-1
            d["wnext"] = d["wd"].shift(-1)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    def ts_(x):
        x = pd.Series(x).dropna()
        if len(x) < 3: return pd.Series({"n": len(x), "mean": np.nan, "t": np.nan})
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))})
    out["bar_hour_counts"] = D["hour"].value_counts().head(5)
    # weekday of the return itself (r is return ending on that bar)
    out["sat_minus_other_by_year"] = D.groupby("year").apply(lambda g: pd.Series({
        "sat_mean": g.loc[g.wd==5,"r"].mean(), "other_mean": g.loc[g.wd!=5,"r"].mean(),
        "t_sat": ts_(g.loc[g.wd==5,"r"])["t"]}))
    out["sat_by_coin"] = D[D.wd==5].groupby("coin")["r"].apply(ts_).unstack()
    out["fri_sat_by_coin"] = D[D.wd.isin([4,5])].groupby("coin")["r"].apply(ts_).unstack()
    out["wd_by_active"] = D.assign(act=D.f.shift(1)>0).groupby(["wd","act"])["r"].mean().unstack()
    # down-day rebound
    D["down"] = D["z"] < -1.5
    out["fwd1_after_down_by_coin"] = D[D.down].groupby("coin")["fwd1"].apply(ts_).unstack()
    out["fwd1_after_down_by_year"] = D[D.down].groupby("year")["fwd1"].apply(ts_).unstack()
    out["fwd1_after_down_by_trend"] = D[D.down].assign(tr=lambda x: x.mom20 > 0).groupby("tr")["fwd1"].apply(ts_).unstack()
    out["fwd1_after_down_by_weekday_of_down"] = D[D.down].groupby("wd")["fwd1"].apply(ts_).unstack()
    # fwd1 after big up days
    out["fwd1_after_up_by_trend"] = D[D.z > 1.5].assign(tr=lambda x: x.mom20 > 0).groupby("tr")["fwd1"].apply(ts_).unstack()
    # book's largest daily gains/losses: what preceded
    A = D.dropna(subset=["bret_next"]).copy()
    A = A[A.bret_next != 0]
    q_lo, q_hi = A.bret_next.quantile([0.05, 0.95])
    A["cls"] = np.where(A.bret_next <= q_lo, "worst5", np.where(A.bret_next >= q_hi, "best5", "mid"))
    out["before_book_extremes"] = A.groupby("cls").agg(n=("r","size"), r_today=("r","mean"), z_today=("z","mean"),
                                                      mom20=("mom20","mean"), f=("f","mean"), vol20=("vol20","mean"))
    # trades: short-held losers vs entry context
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if t is None or len(t)==0: continue
            t = t.copy(); t["coin"]=coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["ewd"] = pd.to_datetime(T["entry_time"]).dt.weekday
    T["xwd"] = pd.to_datetime(T["exit_time"]).dt.weekday
    T["ef"] = pd.cut(T["entry_forecast"].astype(float), [-1e9, 0.0001, 1, 2, 3, 1e9])
    out["trades_by_entry_forecast"] = T.groupby("ef")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades_by_entry_weekday"] = T.groupby("ewd")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median","sum"])
    return out
