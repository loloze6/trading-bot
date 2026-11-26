def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            tr60 = c / c.shift(60) - 1
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            f10 = c.shift(-10) / c - 1
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"])
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                              "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                              "z": z, "r": r, "tr60": tr60, "f1": f1, "f5": f5, "f10": f10,
                              "clv": clv, "rc": (b["regime"] == "unknown"),
                              "alloc": b["postRebalance_current_allocation"]})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in ["f1", "f5", "f10"]:
        n = int(h[1:])
        g = D[D["pos"] % n == 0]
        D[h + "_mu"] = D["coin"].map(g.groupby("coin")[h].mean())
        D[h + "x"] = D[h] - D[h + "_mu"]

    def ct(x, y, day):
        m = x.notna() & y.notna()
        x, y, day = x[m].values, y[m].values, day[m].values
        if len(x) < 20: return (np.nan, np.nan, len(x))
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for dd in np.unique(day):
            idx = day == dd
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        G = len(np.unique(day))
        V = XtXi @ meat @ XtXi * G / (G - 1)
        return (beta[1], beta[1] / np.sqrt(V[1, 1]), len(x))

    out = {}
    g5 = D[D["pos"] % 5 == 0].copy()
    res = []
    for lab, sub in [("rc", g5[g5.rc]), ("notrc", g5[~g5.rc]),
                     ("notrc_up60", g5[(~g5.rc) & (g5.tr60 > 0.10)]),
                     ("notrc_chop60", g5[(~g5.rc) & (g5.tr60.abs() <= 0.10)]),
                     ("notrc_down60", g5[(~g5.rc) & (g5.tr60 < -0.10)])]:
        for side, s2 in [("up", sub[sub.z > 0]), ("down", sub[sub.z < 0]), ("all", sub)]:
            b_, t_, n_ = ct(s2["z"], s2["f5x"], s2["day"])
            res.append({"set": lab, "side": side, "slope": b_, "t": t_, "n": n_,
                        "mean_f5x": s2["f5x"].mean()})
    out["slope_f5x_on_z_by_set"] = pd.DataFrame(res)
    g5["zb"] = pd.cut(g5["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    tab = g5.groupby(["rc", "zb"], observed=True)["f5x"].agg(["mean", "count", "std"])
    tab["t"] = tab["mean"] / (tab["std"] / np.sqrt(tab["count"]))
    out["f5x_by_zbin_rc"] = tab
    # 1 day horizon all bars
    res = []
    for lab, sub in [("rc", D[D.rc]), ("notrc", D[~D.rc])]:
        for side, s2 in [("up", sub[sub.z > 0]), ("down", sub[sub.z < 0])]:
            b_, t_, n_ = ct(s2["z"], s2["f1x"], s2["day"])
            res.append({"set": lab, "side": side, "slope": b_, "t": t_, "n": n_})
    g10 = D[D["pos"] % 10 == 0]
    for lab, sub in [("rc", g10[g10.rc]), ("notrc", g10[~g10.rc])]:
        for side, s2 in [("up", sub[sub.z > 0]), ("down", sub[sub.z < 0])]:
            b_, t_, n_ = ct(s2["z"], s2["f10x"], s2["day"])
            res.append({"set": lab + "_h10", "side": side, "slope": b_, "t": t_, "n": n_})
    out["slope_h1_h10"] = pd.DataFrame(res)
    # close location
    res = []
    for lab, sub in [("rc", g5[g5.rc]), ("notrc", g5[~g5.rc])]:
        b_, t_, n_ = ct(sub["clv"], sub["f5x"], sub["day"])
        res.append({"set": lab, "slope_clv": b_, "t": t_, "n": n_})
    out["clv_slope"] = pd.DataFrame(res)
    # weekday
    wdt = D.groupby("wd")["f1x"].agg(["mean", "count", "std"])
    wdt["t"] = wdt["mean"] / (wdt["std"] / np.sqrt(wdt["count"]))
    out["weekday_next1"] = wdt
    # book gains
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, win=w))
    DD = pd.concat(dd)
    bk = DD.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk["yr"] = pd.to_datetime(bk.index.get_level_values("day")).year
    out["book_by_window"] = bk.groupby(level="win").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    out["book_by_year"] = bk.groupby("yr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    q = bk["book_return"]
    out["book_top_bottom_share"] = pd.Series({"sum_all": q.sum(), "sum_top20": q.nlargest(20).sum(), "sum_bot20": q.nsmallest(20).sum(), "n": len(q)})
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    T["fb"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    out["trades_by_entryfc"] = T.groupby("fb", observed=True)["net_profit_loss_percent"].agg(["mean", "count", "median"])
    out["share_rc_bars"] = float(D.rc.mean())
    return out
