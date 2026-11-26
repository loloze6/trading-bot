def explore(data):
    import numpy as np, pandas as pd
    rows = []
    bookrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sgn = np.sign(r1).fillna(0)
            streak = np.zeros(len(c))
            for i in range(1, len(c)):
                s = sgn.iloc[i]
                if s == 0: streak[i] = 0
                elif np.sign(streak[i-1]) == s: streak[i] = streak[i-1] + s
                else: streak[i] = s
            vol60 = r1.rolling(60, min_periods=60).std()
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "pos": np.arange(len(c)), "r1": r1, "streak": streak, "vol60": vol60,
                               "r5": r5, "r20": r20, "alloc": b["postRebalance_current_allocation"].astype(float)})
            for h in (1, 2, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
        for w, d in data["days"][coin].items():
            bookrows.append(d.assign(coin=coin, win=w))
    A = pd.concat(rows, ignore_index=True)
    A["wd"] = A["day"].dt.weekday
    A["yr"] = A["day"].dt.year
    A["z1"] = A["r1"] / A["vol60"]
    out = {}

    def ctab(sub, h, key):
        sub = sub.dropna(subset=[f"x{h}", key])
        res = []
        for k, g in sub.groupby(key):
            m = g[f"x{h}"].mean()
            dsum = (g[f"x{h}"] - m).groupby(g["day"]).sum()
            se = np.sqrt((dsum ** 2).sum()) / len(g)
            res.append({key: k, "n": len(g), "days": g["day"].nunique(),
                        "mean_excess_%": round(100 * m, 3), "t": round(m / se, 2) if se > 0 else np.nan})
        return pd.DataFrame(res)

    for h in (2, 5):
        G = A[A["pos"] % h == 0].copy()
        G[f"x{h}"] = G[f"f{h}"] - G.groupby("coin")[f"f{h}"].transform("mean")
        G["r1dec"] = G.groupby("coin")["r1"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
        G["z1q"] = pd.qcut(G["z1"], 10, labels=False, duplicates="drop")
        G["stk"] = G["streak"].clip(-5, 5)
        G["r20q"] = G.groupby("coin")["r20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        G["r5q"] = G.groupby("coin")["r5"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        G["volt"] = G.groupby("coin")["vol60"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
        out[f"h{h} by r1 decile (per coin)"] = ctab(G, h, "r1dec")
        out[f"h{h} by streak"] = ctab(G, h, "stk")
        out[f"h{h} by r20 quintile"] = ctab(G, h, "r20q")
        if h == 2:
            out["h2 by z1 decile"] = ctab(G, h, "z1q")
            out["h2 by r5 quintile"] = ctab(G, h, "r5q")
            out["h2 by vol tercile"] = ctab(G, h, "volt")
            G["volt_r20"] = G["volt"].astype(str) + "_" + G["r20q"].astype(str)
            out["h2 by vol tercile x r20q"] = ctab(G, h, "volt_r20")
    G1 = A[A["pos"] % 1 == 0].copy()
    G1["x1"] = G1["f1"] - G1.groupby("coin")["f1"].transform("mean")
    out["h1 by weekday"] = ctab(G1, 1, "wd")
    # book
    B = pd.concat(bookrows, ignore_index=True)
    bd = B.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    bd["yr"] = pd.to_datetime(bd.index.get_level_values("day")).year
    out["book by year"] = bd.groupby("yr").agg(n=("book_return", "size"),
        book_mean_bp=("book_return", lambda s: 1e4 * s.mean()),
        hold_mean_bp=("coin_return", lambda s: 1e4 * s.mean()),
        corr=("book_return", lambda s: np.corrcoef(s, bd.loc[s.index, "coin_return"])[0, 1])).round(2)
    q = bd["book_return"].quantile([0.05, 0.95])
    bd["grp"] = np.where(bd["book_return"] <= q.iloc[0], "worst5%", np.where(bd["book_return"] >= q.iloc[1], "best5%", "mid"))
    out["book tails vs coin return"] = bd.groupby("grp").agg(n=("book_return", "size"),
        book_bp=("book_return", lambda s: 1e4 * s.mean()), coin_bp=("coin_return", lambda s: 1e4 * s.mean())).round(1)
    out["mean alloc"] = round(float(A["alloc"].mean()), 3)
    return out
