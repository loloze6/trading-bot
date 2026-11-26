def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; v = b["volume"]
            r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            df["active"] = (b["regime"] != "chop").values
            df["fc"] = b["forecast"].values
            df["r30"] = c / c.shift(30) - 1
            df["vol30"] = r1.rolling(30).std()
            df["z30"] = df["r30"] / (df["vol30"] * np.sqrt(30))
            df["r1"] = r1
            df["z1"] = r1 / r1.rolling(30).std().shift(1)
            df["volrat"] = v.rolling(10).mean() / v.rolling(60).mean()
            df["f5"] = c.shift(-5) / c - 1
            df["f1"] = c.shift(-1) / c - 1
            df["f3"] = c.shift(-3) / c - 1
            df["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday.values
            df["alloc"] = b["postRebalance_current_allocation"].values
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift5 = A[A.pos % 5 == 0].groupby("coin")["f5"].mean()
    A["x5"] = A["f5"] - A["coin"].map(drift5)
    drift1 = A.groupby("coin")["f1"].mean()
    A["x1"] = A["f1"] - A["coin"].map(drift1)
    G = A[(A.pos % 5 == 0)].dropna(subset=["x5", "z30"])
    out = {}
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    G["zq"] = pd.qcut(G["z30"], 5, labels=False)
    out["x5 by z30 quintile, all bars"] = G.groupby("zq").apply(lambda g: summ(g, "x5"))
    out["x5 by z30 quintile, active"] = G[G.active].groupby(pd.qcut(G[G.active]["z30"], 3, labels=False)).apply(lambda g: summ(g, "x5"))
    cs = G[G.active & (G.fc < 0)].dropna(subset=["volrat"])
    out["cases short x5 by volrat tercile"] = cs.groupby(pd.qcut(cs["volrat"], 3, labels=False)).apply(lambda g: summ(g.assign(s=-g.x5), "s"))
    falls = G[G.z30 < 0].dropna(subset=["volrat"])
    out["all falls: x5 by volrat tercile"] = falls.groupby(pd.qcut(falls["volrat"], 3, labels=False)).apply(lambda g: summ(g, "x5"))
    out["x5 by year-window"] = G.groupby("win").apply(lambda g: summ(g, "x5"))
    D = A.dropna(subset=["x1", "z1"])
    D["z1b"] = pd.cut(D["z1"], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])
    out["next day excess by today's z1"] = D.groupby("z1b").apply(lambda g: summ(g, "x1"))
    out["next day excess by weekday of the next day"] = A.dropna(subset=["x1"]).assign(nwd=lambda d: (d.wd + 1) % 7).groupby("nwd").apply(lambda g: summ(g, "x1"))
    out["share active"] = float(A.active.mean())
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    Dd = pd.concat(dd)
    Dd["year"] = pd.to_datetime(Dd["day"]).dt.year
    out["book by window"] = Dd.groupby("win").agg(br=("book_return", "mean"), cr=("coin_return", "mean"), n=("book_return", "count"))
    return out
