def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; r = c.pct_change()
            sd20 = r.rolling(20).std()
            hh = b["high"].rolling(20).max()
            ll = b["low"].rolling(20).min()
            depth = (c - hh) / hh / sd20
            rng_pos = (c - ll) / (hh - ll)
            z1 = r / sd20.shift(1)
            ret5 = c / c.shift(5) - 1
            z5 = ret5 / (sd20 * np.sqrt(5))
            volrel = sd20 / r.rolling(60).std()
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            pos = np.arange(len(b))
            df = pd.DataFrame({"coin": coin, "win": w, "depth": depth, "rngpos": rng_pos,
                               "z1": z1, "z5": z5, "volrel": volrel, "f1": f1, "f3": f3,
                               "g1": pos % 1 == 0, "g3": pos % 3 == 0,
                               "chop": (b["regime"] == "unknown").values,
                               "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                               "yr": pd.to_datetime(b["timestamp"]).dt.year,
                               "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # drift per coin over all windows (non-overlapping)
    d1 = D.groupby("coin")["f1"].mean(); d3 = D[D.g3].groupby("coin")["f3"].mean()
    D["x1"] = D["f1"] - D["coin"].map(d1)
    D["x3"] = D["f3"] - D["coin"].map(d3)
    out = {}
    def tab(sub, key, col, q=5, grid="g1"):
        s = sub[sub[grid]].dropna(subset=[key, col]).copy()
        s["bin"] = pd.qcut(s[key], q, labels=False, duplicates="drop")
        g = s.groupby("bin")[col]
        res = pd.DataFrame({"keymean": s.groupby("bin")[key].mean(), "mean%": g.mean()*100,
                            "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()})
        return res.round(3)
    out["depth_q_x3_chop"] = tab(D[D.chop], "depth", "x3", 5, "g3")
    out["depth_q_x3_notchop"] = tab(D[~D.chop], "depth", "x3", 5, "g3")
    out["depth_q_x1_chop"] = tab(D[D.chop], "depth", "x1")
    out["z1_q_x1_all"] = tab(D, "z1", "x1", 10)
    out["z1_q_x1_chop"] = tab(D[D.chop], "z1", "x1", 5)
    out["z1_q_x1_notchop"] = tab(D[~D.chop], "z1", "x1", 5)
    out["z5_q_x3_all"] = tab(D, "z5", "x3", 5, "g3")
    out["rngpos_q_x3_all"] = tab(D, "rngpos", "x3", 5, "g3")
    out["volrel_q_x1"] = tab(D, "volrel", "x1", 5)
    s = D.dropna(subset=["x1"])
    g = s.groupby("wd")["x1"]
    out["weekday_x1"] = pd.DataFrame({"mean%": g.mean()*100, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()}).round(3)
    g = s.groupby("coin")["x1"]
    out["chop_share_by_coin"] = D.groupby("coin")["chop"].mean().round(3)
    # book: daily mean across coins
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, win=w))
    B = pd.concat(bk)
    bd = B.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bd.groupby("win").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), n=("book_return", "count")).assign(book_mean=lambda x: x.book_mean*100, coin_mean=lambda x: x.coin_mean*100).round(3)
    out["book_coin_corr"] = float(bd.corr().iloc[0, 1])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
