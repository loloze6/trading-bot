def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            hh = hi.rolling(30).max(); ll = lo.rolling(30).min()
            rng = hh - ll
            net = (c - c.shift(29)).abs()
            ratio = net / rng
            pos = (c - (hh + ll) / 2) / rng          # -0.5..0.5 position in range
            r10 = c / c.shift(10) - 1
            r30 = c / c.shift(30) - 1
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60, min_periods=30).std()
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(n), "ratio": ratio, "pos": pos,
                               "r10": r10, "r30": r30, "r1z": r1 / vol20, "r1": r1,
                               "vr": vol20 / vol60, "vol20": vol20, "fwd": fwd, "fwd1": fwd1,
                               "wd": ts.dt.weekday, "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.i % H == 0].groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    d1 = A.groupby("coin")["fwd1"].mean()
    A["ex1"] = A["fwd1"] - A["coin"].map(d1)
    G = A[(A.i % H == 0)].dropna(subset=["ex"])
    out = {}
    def tab(df, key, col="ex"):
        g = df.groupby(key, observed=True)[col]
        r = g.agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.drop(columns="std").round(4)
    G = G.dropna(subset=["ratio", "pos", "r10"])
    G["flat"] = np.where(G.ratio <= 0.5, "flat", "trend")
    G["posq"] = pd.qcut(G.pos, 5, labels=False)
    G["r10q"] = pd.qcut(G.r10, 5, labels=False)
    out["ex5 by flat x range-position quintile"] = tab(G, ["flat", "posq"])
    out["ex5 by flat x r10 quintile"] = tab(G, ["flat", "r10q"])
    G["r30q"] = pd.qcut(G.r30, 5, labels=False)
    out["ex5 by r30 quintile"] = tab(G, "r30q")
    Gv = G.dropna(subset=["vr", "r1z"])
    Gv["vrq"] = pd.qcut(Gv.vr, 5, labels=False)
    out["ex5 by vol20/vol60 quintile"] = tab(Gv, "vrq")
    Gv["r1zq"] = pd.qcut(Gv.r1z, 5, labels=False)
    out["ex5 by last-day z quintile"] = tab(Gv, "r1zq")
    # daily, h=1 non-overlapping = every bar
    D = A.dropna(subset=["ex1"])
    out["ex1 by weekday"] = tab(D, "wd", "ex1")
    Dz = D.dropna(subset=["r1z"]).copy()
    Dz["zq"] = pd.qcut(Dz.r1z, 10, labels=False)
    out["ex1 by last-day z decile"] = tab(Dz, "zq", "ex1")
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, w=w))
    B = pd.concat(bk)
    bd = B.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window"] = bd.groupby(level=0).agg(["mean"]).round(5)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    T["fq"] = pd.qcut(T.entry_forecast, 4, labels=False, duplicates="drop")
    out["trades by entry forecast q"] = T.groupby("fq")["net_profit_loss_percent"].agg(["mean", "count", "median"]).round(3)
    return out
