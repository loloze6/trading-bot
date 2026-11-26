def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            hi = b["high"].astype(float).rolling(20, min_periods=20).max()
            lo = b["low"].astype(float).rolling(20, min_periods=20).min()
            rp = 2 * (c - lo) / (hi - lo) - 1
            fwd = c.shift(-H) / c - 1
            r1 = c.pct_change()
            tr60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30, min_periods=20).std()
            vol_rel = vol30 / vol30.expanding(min_periods=30).median()
            ret5 = c / c.shift(5) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "rp": rp, "fwd": fwd,
                               "tr60": tr60, "vol_rel": vol_rel, "ret5": ret5, "r1": r1,
                               "z1": r1 / vol30, "regime": b["regime"].values,
                               "fc": b["forecast"].astype(float), "wd": ts.dt.weekday,
                               "year": ts.dt.year, "day": ts.dt.floor("D")})
            rows.append(df)
    A = pd.concat(rows)
    allg = A[A["pos"] % H == 0].dropna(subset=["fwd"])
    drift = allg.groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A["pos"] % H == 0)].dropna(subset=["ex", "rp"]).copy()
    G["rpq"] = pd.cut(G["rp"], [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01], labels=["bot", "lo", "mid", "hi", "top"])
    G["in_prof"] = np.where(G["regime"] == "unknown", "risingcalm", "other")
    def tr_lab(x):
        if pd.isna(x): return "na"
        return "rising" if x > 0.1 else ("falling" if x < -0.1 else "choppy")
    G["trend"] = G["tr60"].map(tr_lab)
    G["agit"] = np.where(G["vol_rel"].isna(), "na", np.where(G["vol_rel"] > 1, "agit", "calm"))
    def agg(g):
        return pd.Series({"n": len(g), "mean_ex": g["ex"].mean(),
                          "t": g["ex"].mean() / (g["ex"].std(ddof=1) / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    out = {}
    out["rpq_by_profile"] = G.groupby(["in_prof", "rpq"]).apply(agg)
    out["rpq_by_trend_outside"] = G[G["in_prof"] == "other"].groupby(["trend", "rpq"]).apply(agg)
    out["rpq_by_agit_choppy"] = G[(G["trend"] == "choppy")].groupby(["agit", "rpq"]).apply(agg)
    # slope of ex on rp per trend/agit
    sl = {}
    for (t, a), g in G.groupby(["trend", "agit"]):
        if len(g) > 30:
            r = stats.linregress(g["rp"], g["ex"])
            sl[f"{t}_{a}"] = {"n": len(g), "slope": r.slope, "t": r.slope / r.stderr}
    out["slope_rp_by_trend_agit"] = pd.DataFrame(sl).T
    # large one-day moves: z1 deciles vs ex (all bars grid)
    G["zq"] = pd.qcut(G["z1"], 5, labels=False, duplicates="drop")
    out["after_1d_move_z_quint"] = G.groupby("zq").apply(agg)
    G["r5q"] = pd.qcut(G["ret5"], 5, labels=False, duplicates="drop")
    out["after_5d_ret_quint"] = G.groupby("r5q").apply(agg)
    out["after_5d_ret_quint_by_trend"] = G.groupby(["trend", "r5q"]).apply(agg)
    # book: days
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w; dl.append(dd)
    D = pd.concat(dl)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["coin_ret_by_weekday"] = D.groupby("wd")["coin_return"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    book = D.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = book.groupby(level=0).agg(["count", "mean", "std"])
    # trades
    tl = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tt = t.copy(); tt["coin"] = coin; tl.append(tt)
    T = pd.concat(tl)
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    T["efq"] = pd.qcut(T["entry_forecast"].abs(), 3, labels=False, duplicates="drop")
    out["trades_by_side_efq"] = T.groupby(["side", "efq"])["net_profit_loss_percent"].agg(["count", "mean"])
    return out
