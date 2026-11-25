def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            hi20 = c.rolling(20, min_periods=20).max(); lo20 = c.rolling(20, min_periods=20).min()
            rp = (c - lo20) / (hi20 - lo20) * 2 - 1
            r1 = c.pct_change()
            r5b = c / c.shift(5) - 1
            r20b = c / c.shift(20) - 1
            vol20 = r1.rolling(20, min_periods=15).std()
            volrank = vol20.rolling(60, min_periods=20).rank(pct=True)
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            hl = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]) * 2 - 1
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "rp": rp, "fc": b["forecast"],
                              "r1": r1, "r5b": r5b, "r20b": r20b, "vol20": vol20, "volrank": volrank,
                              "f5": f5, "f1": f1, "hl": hl, "clv": clv, "wd": ts.dt.weekday, "yr": ts.dt.year,
                              "alloc": b["postRebalance_current_allocation"], "day": ts.dt.floor("D")})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift5 = D[D.pos % 5 == 0].groupby("coin")["f5"].mean()
    drift1 = D.groupby("coin")["f1"].mean()
    D["x5"] = D["f5"] - D["coin"].map(drift5)
    D["x1"] = D["f1"] - D["coin"].map(drift1)
    G = D[(D.pos % 5 == 0)].dropna(subset=["x5"])

    def tab(df, key, col="x5"):
        g = df.dropna(subset=[key, col]).groupby(key)[col]
        out = pd.DataFrame({"n": g.size(), "mean%": g.mean() * 100, "t": g.mean() / (g.std() / np.sqrt(g.size()))})
        # day-clustered t
        return out.round(3)

    res = {}
    G = G.copy()
    G["rp_q"] = pd.qcut(G["rp"], 5, labels=False, duplicates="drop")
    res["rp quintile -> x5"] = tab(G, "rp_q")
    G["r1_q"] = pd.qcut(G["r1"], 5, labels=False, duplicates="drop")
    res["1d ret quintile -> x5"] = tab(G, "r1_q")
    G["r5_q"] = pd.qcut(G["r5b"], 5, labels=False, duplicates="drop")
    res["past5d ret quintile -> x5"] = tab(G, "r5_q")
    G["r20_q"] = pd.qcut(G["r20b"], 5, labels=False, duplicates="drop")
    res["past20d ret quintile -> x5"] = tab(G, "r20_q")
    G["vr_q"] = pd.qcut(G["volrank"], 3, labels=False, duplicates="drop")
    res["volrank tercile -> x5"] = tab(G, "vr_q")
    G["hl_q"] = pd.qcut(G["hl"], 5, labels=False, duplicates="drop")
    res["day range quintile -> x5"] = tab(G, "hl_q")
    G["clv_q"] = pd.qcut(G["clv"], 5, labels=False, duplicates="drop")
    res["close-in-day quintile -> x5"] = tab(G, "clv_q")
    # rp effect by vol tercile and by 20d trend sign
    G["sig_x5"] = np.sign(G["rp"]) * G["x5"]
    res["sign(rp)*x5 by vol tercile"] = tab(G, "vr_q", "sig_x5")
    G["tr"] = pd.cut(G["r20b"], [-9, -0.1, 0.1, 9], labels=["down", "flat", "up"])
    res["sign(rp)*x5 by 20d trend"] = tab(G, "tr", "sig_x5")
    res["sign(rp)*x5 by window"] = tab(G, "w", "sig_x5")
    res["sign(rp)*x5 by coin"] = tab(G, "coin", "sig_x5")
    # weekday on daily excess
    res["weekday -> x1 (all bars)"] = tab(D.dropna(subset=["x1"]), "wd", "x1")
    # book daily
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(pd.DataFrame({"day": d["day"], "w": w, "br": d["book_return"], "cr": d["coin_return"]}))
    B = pd.concat(bd).dropna().groupby(["w", "day"])[["br", "cr"]].mean().reset_index()
    B["corr_info"] = 0
    res["book: corr br,cr; mean br%, sd"] = pd.Series({"corr": B.br.corr(B.cr), "mean%": B.br.mean() * 100, "sd%": B.br.std() * 100, "n": len(B)})
    q = B.br.quantile([0.05, 0.95])
    B["tail"] = np.where(B.br <= q.iloc[0], "worst5%", np.where(B.br >= q.iloc[1], "best5%", "mid"))
    res["book tails: coin ret on day"] = B.groupby("tail")["cr"].agg(["size", "mean", "std"]).mul([1, 100, 100]).round(3)
    res["book mean% by window"] = B.groupby("w")["br"].agg(lambda s: s.mean() * 100).round(3)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    res["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["size", "mean", "median"]).round(3)
    return res
