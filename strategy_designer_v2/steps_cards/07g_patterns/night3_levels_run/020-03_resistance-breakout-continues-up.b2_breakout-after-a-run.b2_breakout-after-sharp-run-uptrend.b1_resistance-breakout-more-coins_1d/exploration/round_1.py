def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    act = []
    for coin, wins in data["bars"].items():
        grids = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "r1": r1,
                "r3": c / c.shift(3) - 1,
                "r10": c / c.shift(10) - 1,
                "r30": c / c.shift(30) - 1,
                "vol20": r1.rolling(20, min_periods=15).std(),
                "dhi": c / c.rolling(60, min_periods=30).max() - 1,
                "rng": (b["high"] - b["low"]) / c,
                "volu": b["volume"] / b["volume"].rolling(20, min_periods=15).mean(),
                "fc": b["forecast"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "f5": c.shift(-5) / c - 1,
                "f10": c.shift(-10) / c - 1,
                "f20": c.shift(-20) / c - 1,
                "pos": np.arange(n),
            })
            df["fcprev"] = df["fc"].shift(1).fillna(0)
            # active onset bars
            on = df[(df["fc"] > 0) & (df["fcprev"] <= 0)]
            act.append(on)
            grids.append(df[df["pos"] % 5 == 0])
        g = pd.concat(grids)
        m5 = g["f5"].mean()
        g["x5"] = g["f5"] - m5
        rows.append(g)
        # drift for 10/20 on own grids
        for a in act:
            pass
    G = pd.concat(rows)
    A = pd.concat(act)
    # coin means
    cm5 = G.groupby("coin")["f5"].mean()
    A["x5"] = A["f5"] - A["coin"].map(cm5)
    def tab(df, col, q=5, y="x5"):
        d = df.dropna(subset=[col, y]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        r = d.groupby("q")[y].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.drop(columns="std").round(4)
    for col in ["r1", "r3", "r10", "r30", "vol20", "dhi", "rng", "volu"]:
        out["q_" + col] = tab(G, col)
    wd = G.dropna(subset=["x5"]).groupby("wd")["x5"].agg(["mean", "count", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday"] = wd.drop(columns="std").round(4)
    # activity onset follow-through
    res = {}
    for h in ["f5", "f10", "f20"]:
        s = A[h].dropna()
        base = G[h].dropna()
        res[h] = [s.mean(), len(s), s.mean() / (s.std() / np.sqrt(len(s))), base.mean()]
    out["onset_follow"] = pd.DataFrame(res, index=["mean", "n", "t", "grid_mean"]).T.round(4)
    out["onset_by_r10"] = tab(A, "r10", q=3)
    out["onset_by_vol"] = tab(A, "vol20", q=3)
    # book by window
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(pd.DataFrame({"win": w, "b": d["book_return"], "h": d["coin_return"]}))
    B = pd.concat(bk).dropna()
    bw = B.groupby("win")[["b", "h"]].sum()
    out["book_by_window_sumret_per_coin_avg"] = (bw / B.groupby("win").size().values[:, None] * 1).round(5)
    return out
