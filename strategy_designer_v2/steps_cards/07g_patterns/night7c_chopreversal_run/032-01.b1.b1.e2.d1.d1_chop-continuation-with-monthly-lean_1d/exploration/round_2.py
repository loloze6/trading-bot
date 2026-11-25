def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            absmove = c.diff().abs().rolling(30).sum()
            er = (c - c.shift(30)).abs() / absmove
            ret30 = c / c.shift(30) - 1
            ret7 = c / c.shift(7) - 1
            sd30 = r.rolling(30).std()
            mv7 = ret7 / (sd30 * np.sqrt(7))
            mv1 = r / sd30
            m30 = ret30 / (sd30 * np.sqrt(30))
            rng = (b["high"].astype(float) - b["low"].astype(float)) / c
            clv = (c - b["low"].astype(float)) / (b["high"].astype(float) - b["low"].astype(float))
            fwd7 = c.shift(-7) / c - 1
            fwd1 = c.shift(-1) / c - 1
            fwd3 = c.shift(-3) / c - 1
            sdrel = sd30 / sd30.rolling(90, min_periods=30).mean()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "er": er, "ret30": ret30,
                               "mv7": mv7, "mv1": mv1, "m30": m30, "clv": clv, "fwd7": fwd7, "fwd1": fwd1,
                               "fwd3": fwd3, "sdrel": sdrel, "yr": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    def tstat(x):
        x = x.dropna(); return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    def agg(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": tstat(x)})
    # 1-day reversal
    d1 = D.dropna(subset=["fwd1", "mv1", "er", "sdrel"]).copy()
    d1["u1"] = d1["fwd1"] - d1["coin"].map(d1.groupby("coin")["fwd1"].mean())
    d1["rev"] = -np.sign(d1["mv1"]) * d1["u1"]
    d1["mq"] = pd.qcut(d1["mv1"].abs(), 4, labels=["a1", "a2", "a3", "a4"])
    d1["side"] = np.where(d1["mv1"] > 0, "up", "down")
    out["1d reversal by |mv1| quartile x side"] = d1.groupby(["side", "mq"])["rev"].apply(agg).unstack()
    d1["chop"] = np.where(d1["er"] < 0.3, "chop", "trend")
    big = d1[d1["mq"] == "a4"]
    out["1d reversal large days by chop x side"] = big.groupby(["chop", "side"])["rev"].apply(agg).unstack()
    out["1d reversal large days by coin"] = big.groupby("coin")["rev"].apply(agg).unstack()
    out["1d reversal large days by year"] = big.groupby("yr")["rev"].apply(agg).unstack()
    # 3-day grid reversal after large down days (non overlapping grid of 3)
    g3 = D[D["pos"] % 3 == 0].dropna(subset=["fwd3", "mv1"]).copy()
    g3["u3"] = g3["fwd3"] - g3["coin"].map(g3.groupby("coin")["fwd3"].mean())
    g3["rev3"] = -np.sign(g3["mv1"]) * g3["u3"]
    g3["mq"] = pd.qcut(g3["mv1"].abs(), 4, labels=["a1", "a2", "a3", "a4"])
    g3["side"] = np.where(g3["mv1"] > 0, "up", "down")
    out["3d reversal by |mv1| quartile x side"] = g3.groupby(["side", "mq"])["rev3"].apply(agg).unstack()
    # 7-day grid: chop aligned by side
    g = D[D["pos"] % 7 == 0].dropna(subset=["fwd7", "mv7", "er", "ret30"]).copy()
    g["u7"] = g["fwd7"] - g["coin"].map(g.groupby("coin")["fwd7"].mean())
    g["s"] = np.sign(g["mv7"])
    ca = g[(g["er"] < 0.3) & (np.sign(g["ret30"]) == g["s"])]
    ca = ca.assign(side=np.where(ca["s"] > 0, "up", "down"), ud=ca["u7"] * ca["s"])
    out["chop aligned by side"] = ca.groupby("side")["ud"].apply(agg).unstack()
    out["chop aligned by year"] = ca.groupby("yr")["ud"].apply(agg).unstack()
    # 30d momentum graded by m30, in ER middle
    g["u30"] = g["u7"] * np.sign(g["ret30"])
    g["m30q"] = pd.qcut(g["m30"].abs(), 4, labels=["b1", "b2", "b3", "b4"])
    g["erq"] = pd.qcut(g["er"], 4, labels=["er1", "er2", "er3", "er4"])
    out["7d move in ret30 dir by |m30| quartile"] = g.groupby("m30q")["u30"].apply(agg).unstack()
    out["7d move in ret30 dir by ER quartile x side"] = g.groupby(["erq", np.where(g["ret30"] > 0, "up", "down")])["u30"].apply(agg).unstack()
    # book largest gains/losses days
    days = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; days.append(dd)
    Dy = pd.concat(days).dropna(subset=["book_return", "coin_return"])
    q = Dy["book_return"].quantile([0.01, 0.99])
    out["book extremes"] = pd.DataFrame({
        "worst1pct": Dy[Dy["book_return"] <= q[0.01]][["book_return", "coin_return"]].mean(),
        "best1pct": Dy[Dy["book_return"] >= q[0.99]][["book_return", "coin_return"]].mean()})
    out["share of book gain from best 5% days"] = float(Dy[Dy["book_return"] >= Dy["book_return"].quantile(0.95)]["book_return"].sum() / Dy["book_return"].sum())
    return out
