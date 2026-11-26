def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            b["r1"] = r1
            b["ret5p"] = c / c.shift(5) - 1
            b["ret30p"] = c / c.shift(30) - 1
            b["vr"] = v.rolling(30).mean().shift(30) / v.rolling(30).mean()
            b["vol30"] = r1.rolling(30).std()
            b["vol5"] = r1.rolling(5).std()
            b["z1"] = r1 / r1.rolling(30).std().shift(1)
            b["fwd5"] = c.shift(-H) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["rng"] = (b["high"] - b["low"]) / c
            b["clpos"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            b["v_z"] = np.log(v / v.rolling(30).mean().shift(1))
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            b["fc_raw"] = b.get("debug_info.components.thin_fall.last_history_value", np.nan)
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    G = B[B["pos"] % H == 0].dropna(subset=["fwd5"]).copy()
    G["ex5"] = G["fwd5"] - G.groupby("coin")["fwd5"].transform("mean")
    B["ex1"] = B["fwd1"] - B.groupby("coin")["fwd1"].transform("mean")
    def summ(df, col, key):
        g = df.dropna(subset=[col, key]).groupby(key)[col]
        r = g.agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.round(5)
    G["fc_on"] = G["regime"].eq("unknown")
    out["regime share grid"] = G["regime"].value_counts()
    out["ex5 by regime"] = summ(G, "ex5", "regime")
    FC = G[G["fc_on"]].copy()
    FC["q30"] = pd.qcut(FC["ret30p"], 4, labels=False, duplicates="drop")
    out["fallingcalm ex5 by ret30 quartile"] = summ(FC, "ex5", "q30")
    FC["qvr"] = pd.qcut(FC["vr"], 3, labels=False, duplicates="drop")
    out["fallingcalm ex5 by volratio tercile (high=thin)"] = summ(FC, "ex5", "qvr")
    FC["q5"] = pd.qcut(FC["ret5p"], 4, labels=False, duplicates="drop")
    out["fallingcalm ex5 by ret5 quartile"] = summ(FC, "ex5", "q5")
    CH = G[~G["fc_on"]].copy()
    CH["q30"] = pd.qcut(CH["ret30p"], 5, labels=False, duplicates="drop")
    out["other ex5 by ret30 quintile"] = summ(CH, "ex5", "q30")
    CH["q5"] = pd.qcut(CH["ret5p"], 5, labels=False, duplicates="drop")
    out["other ex5 by ret5 quintile"] = summ(CH, "ex5", "q5")
    CH["qv"] = pd.qcut(CH["vol30"], 4, labels=False, duplicates="drop")
    out["other ex5 by vol30 quartile"] = summ(CH, "ex5", "qv")
    # daily angles (overlap-free at 1 bar)
    B["qz"] = pd.cut(B["z1"], [-np.inf, -2, -1, 1, 2, np.inf])
    out["next-day ex by z1 bucket"] = summ(B, "ex1", "qz")
    B["qcl"] = pd.qcut(B["clpos"], 5, labels=False, duplicates="drop")
    out["next-day ex by close position quintile"] = summ(B, "ex1", "qcl")
    B["qvz"] = pd.qcut(B["v_z"], 5, labels=False, duplicates="drop")
    out["next-day ex by volume surprise quintile"] = summ(B, "ex1", "qvz")
    out["next-day ex by weekday"] = summ(B, "ex1", "wd")
    # interaction: big down day x volume surprise
    D = B[B["z1"] < -1.5].copy()
    D["qvz"] = pd.qcut(D["v_z"], 3, labels=False, duplicates="drop")
    out["after down>1.5sd: next-day ex by vol surprise"] = summ(D, "ex1", "qvz")
    U = B[B["z1"] > 1.5].copy()
    U["qvz"] = pd.qcut(U["v_z"], 3, labels=False, duplicates="drop")
    out["after up>1.5sd: next-day ex by vol surprise"] = summ(U, "ex1", "qvz")
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    DD = pd.concat(dd)
    bk = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book by window"] = bk.groupby(level=0).agg(["count", "mean", "std"]).round(5)
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; t["win"] = w; tr.append(t)
    T = pd.concat(tr)
    T["qf"] = pd.qcut(T["entry_forecast"], 3, labels=False, duplicates="drop")
    out["trades by entry forecast tercile"] = T.groupby("qf")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
    return out
