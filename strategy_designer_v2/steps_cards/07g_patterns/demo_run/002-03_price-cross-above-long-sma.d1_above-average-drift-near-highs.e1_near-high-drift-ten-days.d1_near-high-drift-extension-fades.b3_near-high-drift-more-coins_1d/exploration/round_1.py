def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 10
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi20 = c.rolling(20).max(); lo20 = c.rolling(20).min()
            rng = (c - lo20) / (hi20 - lo20)
            ret30 = c / c.shift(30) - 1
            ret10 = c / c.shift(10) - 1
            vol20 = r1.rolling(20).std()
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "rng": rng, "ret30": ret30, "ret10": ret10, "vol20": vol20,
                               "r1": r1, "fwd": fwd, "fwd1": fwd1, "regime": b["regime"],
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "wd": ts.dt.weekday})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    cm = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(cm)
    def tab(df, col, q=5):
        d = df.dropna(subset=[col, "ex"]).copy()
        d["b"] = pd.qcut(d[col].rank(method="first"), q, labels=False)
        g = d.groupby("b")["ex"].agg(["mean", "std", "count"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["lo"] = d.groupby("b")[col].min(); g["hi"] = d.groupby("b")[col].max()
        return g.round(4)
    out = {}
    tr = G[G["regime"] == "trending"]; un = G[G["regime"] != "trending"]
    out["regime counts/mean ex"] = G.groupby("regime")["ex"].agg(["mean", "count"]).round(4)
    out["trend: rng quintile"] = tab(tr, "rng")
    out["nontrend: rng quintile"] = tab(un, "rng")
    out["trend: ret30 quintile"] = tab(tr, "ret30")
    out["nontrend: ret30 quintile"] = tab(un, "ret30")
    out["all: vol20 quintile"] = tab(G, "vol20")
    out["all: ret10 quintile"] = tab(G, "ret10")
    out["trend: forecast quintile"] = tab(tr, "fc")
    # next-day after large daily moves (all bars, h=1 non-overlapping)
    B = A.dropna(subset=["r1", "fwd1"]).copy()
    B["z"] = B["r1"] / B["vol20"]
    B = B.dropna(subset=["z"])
    B["zb"] = pd.cut(B["z"], [-99, -2, -1, 0, 1, 2, 99])
    g = B.groupby("zb", observed=True)["fwd1"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["next day by today z-move"] = g.round(4)
    g = A.dropna(subset=["fwd1"]).groupby("wd")["fwd1"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["next day by weekday"] = g.round(4)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D)
    bd = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    out["book mean/std/sharpe"] = pd.Series({"mean": bd.book_return.mean(), "std": bd.book_return.std(),
        "sh": bd.book_return.mean()/bd.book_return.std()*np.sqrt(365), "hold_mean": bd.coin_return.mean(), "n": len(bd)})
    # gain from exposure by side
    A["g"] = A["alloc"] * A["fwd1"]
    A["side"] = np.sign(A["alloc"].fillna(0))
    s = A.dropna(subset=["g"]).groupby(["regime", "side"])["g"].agg(["mean", "sum", "count"])
    out["position gain by regime/side"] = s
    return out
