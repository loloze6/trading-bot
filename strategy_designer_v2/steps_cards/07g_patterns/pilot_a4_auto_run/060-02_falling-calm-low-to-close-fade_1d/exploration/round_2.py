def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # trades summary
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = coin; t["win"] = w; T.append(t)
    if T:
        T = pd.concat(T, ignore_index=True)
        g = T.groupby(["coin", "side"])["net_profit_loss_percent"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        out["trades_by_coin_side"] = g.drop(columns="std")
        T["dur_d"] = T["duration_minutes"] / 1440
        out["trade_duration"] = T["dur_d"].describe()
    # book daily returns, extremes, and what came before
    rows = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.reset_index(drop=True).copy()
            r = d["coin_return"]; v = r.rolling(30, min_periods=20).std()
            d["prev_ret_z"] = (r / v).shift(1)
            d["prev5_z"] = (d["close"].shift(1) / d["close"].shift(6) - 1) / (v.shift(1) * np.sqrt(5))
            d["coin"] = coin; d["win"] = w
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    act = D[D["book_return"].abs() > 1e-12].dropna(subset=["book_return"])
    out["active_days"] = pd.Series({"n": len(act), "mean": act["book_return"].mean(),
                                    "t": act["book_return"].mean() / (act["book_return"].std() / np.sqrt(len(act)))})
    act = act.assign(q=pd.qcut(act["book_return"].rank(method="first"), 5, labels=False))
    out["book_quintiles_context"] = act.groupby("q")[["book_return", "coin_return", "prev_ret_z", "prev5_z"]].mean()
    # by window book active mean
    gw = act.groupby("win")["book_return"].agg(["mean", "count"])
    out["book_by_window"] = gw
    # rank correlation of lift vs next-day return on profile bars, by coin (all bars, grid h=1)
    R = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change(); v = r1.rolling(30, min_periods=20).std()
            m = b["regime"] != "chop"
            R.append(pd.DataFrame({"coin": coin, "lift": ((c - b["low"]) / c / v)[m],
                                   "ret_z": (r1 / v)[m], "f1": (c.shift(-1) / c - 1)[m]}))
    R = pd.concat(R).dropna()
    res = {}
    for coin, g in R.groupby("coin"):
        rho, p = stats.spearmanr(g["lift"], g["f1"]); rho2, p2 = stats.spearmanr(g["ret_z"], g["f1"])
        res[coin] = {"n": len(g), "rho_lift": rho, "p_lift": p, "rho_retz": rho2, "p_retz": p2}
    out["spearman_by_coin"] = pd.DataFrame(res).T
    return out
