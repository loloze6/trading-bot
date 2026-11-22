def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "z1": r1 / sd, "m30": (c / c.shift(30) - 1) / sd,
                "m10": (c / c.shift(10) - 1) / sd,
                "sd": sd, "fwd5": c.shift(-5) / c - 1, "fwd1": c.shift(-1) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["pos"] % 5 == 0].copy()
    drift = G.groupby("coin")["fwd5"].mean()
    G["ex5"] = G["fwd5"] - G["coin"].map(drift)
    G = G.dropna(subset=["ex5", "z1", "m30"])
    out = {}
    def summ(df, col="ex5"):
        x = df[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    G["zbin"] = pd.cut(G["z1"], [-np.inf, -2, -1, 1, 2, np.inf], labels=["<=-2", "-2..-1", "-1..1", "1..2", ">=2"])
    G["msign"] = np.where(G["m30"] > 0, "up30", "down30")
    out["ex5 by day move x month sign"] = G.groupby(["zbin", "msign"], observed=True).apply(summ)
    def slope(df, x="m30"):
        df = df.dropna(subset=[x, "ex5"])
        if len(df) < 10: return pd.Series({"n": len(df)})
        r = stats.linregress(df[x], df["ex5"])
        return pd.Series({"n": len(df), "slope": r.slope, "t": r.slope / r.stderr})
    out["slope ex5 on m30 by day-move bin"] = G.groupby("zbin", observed=True).apply(slope)
    out["slope ex5 on m10 by day-move bin"] = G.groupby("zbin", observed=True).apply(lambda d: slope(d, "m10"))
    out["slope ex5 on m30 all"] = slope(G)
    out["slope ex5 on m30 by coin"] = G.groupby("coin").apply(slope)
    out["slope ex5 on m30 by year"] = G.groupby("year").apply(slope)
    G["sdq"] = G.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["slope ex5 on m30 by vol tercile"] = G.groupby("sdq").apply(slope)
    out["ex5 by vol tercile"] = G.groupby("sdq").apply(summ)
    # weekday on daily coin returns
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    D = pd.concat(dd, ignore_index=True)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    out["coin daily return by weekday"] = D.groupby("wd").apply(lambda d: summ(d, "coin_return"))
    out["book daily return by weekday"] = D.groupby("wd").apply(lambda d: summ(d, "book_return"))
    # book extremes
    Db = D.dropna(subset=["book_return"])
    q_hi, q_lo = Db["book_return"].quantile([0.99, 0.01])
    D["prev_cr"] = D.groupby(["coin", "win"])["coin_return"].shift(1)
    hi = D[D["book_return"] >= q_hi]; lo = D[D["book_return"] <= q_lo]
    out["book extremes"] = pd.DataFrame({
        "n": [len(hi), len(lo)],
        "mean coin ret same day": [hi["coin_return"].mean(), lo["coin_return"].mean()],
        "mean coin ret prev day": [hi["prev_cr"].mean(), lo["prev_cr"].mean()],
        "share coin up same day": [(hi["coin_return"] > 0).mean(), (lo["coin_return"] > 0).mean()],
    }, index=["top1%", "bottom1%"])
    # position side
    act = A[A["alloc"].abs() > 1e-9]
    out["share of bars long/short/flat"] = pd.Series({"long": (A["alloc"] > 1e-9).mean(), "short": (A["alloc"] < -1e-9).mean(), "flat": (A["alloc"].abs() <= 1e-9).mean()})
    out["gain per bar by side"] = pd.DataFrame({
        "long": summ(act[act["alloc"] > 0].assign(g=lambda d: d["alloc"] * d["fwd1"]), "g"),
        "short": summ(act[act["alloc"] < 0].assign(g=lambda d: d["alloc"] * d["fwd1"]), "g")})
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median", lambda s: (s > 0).mean()])
    return out
