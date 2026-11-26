def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            absd = c.diff().abs()
            er = (c - c.shift(30)).abs() / absd.rolling(30).sum()
            sd30 = r1.rolling(30).std()
            r7 = c / c.shift(7) - 1
            z = r7 / (sd30 * np.sqrt(7))
            r30 = c / c.shift(30) - 1
            vol_ratio = r1.rolling(7).std() / r1.rolling(90, min_periods=60).std()
            fwd7 = c.shift(-7) / c - 1
            fwd1 = c.shift(-1) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "er": er, "z": z, "r1": r1, "r30": r30,
                               "sd30": sd30, "vr": vol_ratio, "fwd7": fwd7, "fwd1": fwd1,
                               "z1": r1 / sd30,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float)})
            df["pos"] = np.arange(len(df))
            daily.append(df)
            rows.append(df[df["pos"] % 7 == 0])
    G = pd.concat(rows); D = pd.concat(daily)
    m7 = G.groupby("coin")["fwd7"].transform("mean")
    G["dm7"] = G["fwd7"] - m7
    G = G.dropna(subset=["er", "z", "dm7"])
    G["sz"] = np.sign(G["z"]) * G["dm7"]
    out = {}
    def tab(g, col):
        a = g.groupby(col, observed=True)[col if False else "sz"].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std").round(4)
    G["erb"] = pd.cut(G["er"], [0, .15, .3, .45, .6, 1.01])
    G["zb"] = pd.cut(G["z"].abs(), [0, .5, 1, 1.5, 2, 99])
    out["signed fwd7 by ER bucket"] = tab(G, "erb")
    out["signed fwd7 by |z| bucket, ER<=0.3"] = tab(G[G.er <= .3], "zb")
    out["signed fwd7 by |z| bucket, ER>0.3"] = tab(G[G.er > .3], "zb")
    G["vrb"] = pd.qcut(G["vr"], 4)
    out["signed fwd7 by 7d/90d vol ratio, ER<=0.3"] = tab(G[G.er <= .3].dropna(subset=["vr"]), "vrb")
    out["signed fwd7 by 7d/90d vol ratio, all"] = tab(G.dropna(subset=["vr"]), "vrb")
    G["sdb"] = G.groupby("coin")["sd30"].transform(lambda s: pd.qcut(s, 4, labels=False))
    out["signed fwd7 by sd30 quartile (per coin), all"] = tab(G, "sdb")
    # 30d trend sign continuation
    G["s30"] = np.sign(G["r30"]) * G["dm7"]
    a = G.groupby("erb", observed=True)["s30"].agg(["mean", "count", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"])); out["fwd7 in 30d-move direction by ER"] = a.round(4)
    # daily: after large daily moves (non-overlap fine for 1 day)
    D = D.dropna(subset=["z1", "fwd1"])
    D["dm1"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    D["z1b"] = pd.cut(D["z1"], [-99, -2, -1, 0, 1, 2, 99])
    a = D.groupby("z1b", observed=True)["dm1"].agg(["mean", "count", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"])); out["next-day demeaned ret by today's scaled move"] = a.round(4)
    a = D.groupby("wd")["dm1"].agg(["mean", "count", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"])); out["next-day ret by weekday of decision bar"] = a.round(4)
    # book
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(d.assign(coin=coin, w=w))
    B = pd.concat(bd).dropna(subset=["book_return"])
    bk = B.groupby(["w", "day"])["book_return"].mean()
    out["book by window"] = bk.groupby(level=0).agg(["mean", "std", "count"]).assign(
        sh=lambda x: x["mean"] / x["std"] * np.sqrt(365)).round(4)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    T["absf"] = T["entry_forecast"].abs()
    T["fb"] = pd.qcut(T["absf"], 4, duplicates="drop")
    out["trades by |entry forecast|"] = T.groupby(["fb", "side"], observed=True)["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
