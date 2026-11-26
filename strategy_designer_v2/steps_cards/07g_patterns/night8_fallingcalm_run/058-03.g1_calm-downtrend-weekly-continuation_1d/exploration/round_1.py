def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            b["ret5"] = c / c.shift(5) - 1
            b["ret1"] = c / c.shift(1) - 1
            b["ret20"] = c / c.shift(20) - 1
            b["fwd"] = c.shift(-H) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["volr"] = v.rolling(5).mean() / v.rolling(30).mean()
            b["vol10"] = b["ret1"].rolling(10).std()
            b["vol30"] = b["ret1"].rolling(30).std()
            b["inprof"] = (b["regime"] == "unknown").astype(int)
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["coin"] = coin; b["win"] = w
            b["grid"] = (np.arange(len(b)) % H == 0)
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["alloc"] = b["postRebalance_current_allocation"]
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    drift = B[B.grid].groupby("coin")["fwd"].mean()
    sd = B[B.grid].groupby("coin")["fwd"].std()
    B["ex"] = B["fwd"] - B["coin"].map(drift)
    B["z"] = B["ex"] / B["coin"].map(sd)
    G = B[B.grid].dropna(subset=["ret5", "fwd"]).copy()
    out = {}
    def summ(g, col="ex"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean() if n else np.nan,
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    # 1 ret5 quintiles, in and out of profile
    G["q5"] = G.groupby("inprof")["ret5"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ret5 quintile x inprof: next5 excess"] = G.groupby(["inprof", "q5"]).apply(summ).round(3)
    # 2 volume ratio interaction in profile, signed continuation
    G["sgn"] = np.sign(G["ret5"])
    G["cont"] = G["sgn"] * G["ex"]
    P = G[G.inprof == 1].copy()
    P["vq"] = pd.qcut(P["volr"], 3, labels=["lowvol", "midvol", "highvol"])
    out["inprof: continuation by volume tercile and side"] = P.groupby(["vq", "sgn"]).apply(lambda g: summ(g, "cont")).round(3)
    # 3 ret20 depth in profile
    P["dq"] = pd.qcut(P["ret20"], 4, labels=False, duplicates="drop")
    out["inprof: next5 excess by 20d return quartile"] = P.groupby("dq").apply(summ).round(3)
    # 4 out of profile: large 1d moves -> next 5d, by vol level
    O = G.copy()
    O["r1q"] = pd.qcut(O["ret1"], 5, labels=False, duplicates="drop")
    O["vlev"] = O.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 2, labels=["lowv", "highv"]))
    out["all: 1d return quintile x vol level -> next5 excess"] = O.groupby(["vlev", "r1q"]).apply(summ).round(3)
    # 5 weekday next-1d returns, all bars
    A = B.dropna(subset=["fwd1"])
    out["weekday next1d return (all bars)"] = A.groupby("wd").apply(lambda g: summ(g, "fwd1")).round(3)
    # 6 window-level of book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    out["book vs coin by window"] = D.groupby("win").agg(book=("book_return", lambda s: 100 * s.mean()),
                                                          coin=("coin_return", lambda s: 100 * s.mean()),
                                                          n=("book_return", "count")).round(3)
    # 7 trades by side
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median", "std"]).round(3)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
    # 8 in profile share
    out["share of bars in profile by coin"] = B.groupby("coin")["inprof"].mean().round(3)
    return out
