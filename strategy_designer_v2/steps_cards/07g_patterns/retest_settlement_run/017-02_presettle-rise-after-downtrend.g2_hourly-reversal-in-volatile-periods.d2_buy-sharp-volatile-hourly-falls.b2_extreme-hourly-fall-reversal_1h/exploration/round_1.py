def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    grid = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "r": r, "z": r / vol,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "year": ts.dt.year,
                               "vol": vol, "volume": b["volume"].astype(float),
                               "ret24p": c / c.shift(24) - 1,
                               "ret72p": c / c.shift(72) - 1,
                               "fwd24": c.shift(-24) / c - 1,
                               "fwd8": c.shift(-8) / c - 1,
                               "fwd1": r.shift(-1)})
            df["relvol"] = df["volume"] / df["volume"].rolling(24 * 7).median()
            rows.append(df)
            g = df.iloc[::24].copy()
            grid.append(g)
    A = pd.concat(rows, ignore_index=True)
    G = pd.concat(grid, ignore_index=True).dropna(subset=["fwd24"])
    # coin-level drift and usual move
    drift = G.groupby("coin")["fwd24"].mean()
    sd = G.groupby("coin")["fwd24"].std()
    G["u24"] = (G["fwd24"] - G["coin"].map(drift)) / G["coin"].map(sd)
    G["volq"] = G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    def tab(df, key, col):
        g = df.groupby(key)[col]
        t = g.mean() / (g.std() / np.sqrt(g.count()))
        return pd.DataFrame({"mean": g.mean(), "n": g.count(), "t": t})
    # 1. hour z bins vs fwd24 strength
    G["zbin"] = pd.cut(G["z"], [-99, -3, -2, -1, 0, 1, 2, 3, 99])
    out["fwd24 strength by hour z bin (grid)"] = tab(G, "zbin", "u24")
    # 2. past 24h and 72h return graded
    G["p24q"] = G.groupby("coin")["ret24p"].transform(lambda s: pd.qcut(s, 5, labels=False))
    G["p72q"] = G.groupby("coin")["ret72p"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["fwd24 strength by past24 quintile"] = tab(G, "p24q", "u24")
    out["fwd24 strength by past72 quintile"] = tab(G, "p72q", "u24")
    out["fwd24 strength by vol quintile"] = tab(G, "volq", "u24")
    # 3. hourly returns by hour (in own vol units)
    A["rz1"] = A["fwd1"] / A["vol"]
    out["next-hour return / vol by hour of close"] = tab(A.dropna(subset=["rz1"]), "hour", "rz1")
    # 4. funding interplay: sign of trend x hour
    A["tr"] = np.sign(A["ret24p"])
    A["rz_tr"] = A["rz1"] * A["tr"]
    out["next-hour return with trend sign by hour"] = tab(A.dropna(subset=["rz_tr"]), "hour", "rz_tr")
    out["relvol by hour"] = A.groupby("hour")["relvol"].median().to_frame("median relvol")
    # 5. weekday daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["coin daily return by weekday"] = tab(D.dropna(subset=["coin_return"]), "wd", "coin_return")
    D["excess"] = D["book_return"] - D["coin_return"]
    out["book minus coin daily by weekday"] = tab(D.dropna(subset=["excess"]), "wd", "excess")
    out["book daily by year (from bars year)"] = tab(D.assign(y=pd.to_datetime(D["day"]).dt.year).dropna(subset=["book_return"]), "y", "book_return")
    return out
