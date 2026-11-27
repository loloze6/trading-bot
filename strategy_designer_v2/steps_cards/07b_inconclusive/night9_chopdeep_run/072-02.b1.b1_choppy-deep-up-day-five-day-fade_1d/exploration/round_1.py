def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float); h = df["high"].astype(float)
            r1 = c.pct_change()
            hh = h.rolling(20, min_periods=20).max()
            sd = r1.rolling(20, min_periods=20).std()
            depth = (c - hh) / hh / sd
            rec = df.get("debug_info.components.depth.last_history_value")
            reg = df["regime"].astype(str)
            out = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(df)),
                                "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                                "depth": depth, "rec": rec, "regime": reg, "r1": r1,
                                "fc": df["forecast"]})
            for H in [1, 2, 3, 5, 10]:
                out[f"f{H}"] = c.shift(-H) / c - 1
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    A["choppy"] = A["regime"].isin(["mean_reversion", "unknown"])
    A["up"] = A["r1"] > 0
    A["d"] = A["rec"].where(A["regime"] == "mean_reversion", A["depth"])

    def clus(x, y, g):
        X = np.column_stack([np.ones(len(x)), x]); n = len(x)
        if n < 30: return (np.nan, np.nan, n)
        XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ y; e = y - X @ b
        G = pd.Series(range(n)).groupby(g.values).apply(lambda i: X[i.values].T @ e[i.values])
        M = sum(np.outer(s, s) for s in G); k = len(G)
        V = XtX @ M @ XtX * k / (k - 1) * (n - 1) / (n - 2)
        return (b[1], b[1] / np.sqrt(V[1, 1]), n)

    res = {}
    tab = []
    for H in [1, 2, 3, 5, 10]:
        S = A[A["pos"] % H == 0].dropna(subset=[f"f{H}", "d"]).copy()
        drift = S.groupby("coin")[f"f{H}"].mean()
        S["u"] = S[f"f{H}"] - S["coin"].map(drift)
        for name, m in [("choppy_up", S.choppy & S.up), ("choppy_down", S.choppy & ~S.up),
                        ("choppy_all", S.choppy), ("notchoppy_all", ~S.choppy)]:
            T = S[m]
            b, t, n = clus(T["d"].values, T["u"].values, T["day"])
            tab.append({"H": H, "set": name, "slope": b, "t": t, "n": n,
                        "mean_u_short": -T["u"].mean()})
    res["slopes"] = pd.DataFrame(tab)
    # quintiles at H=5 and H=1, choppy up / down
    q = []
    for H in [1, 5]:
        S = A[A["pos"] % H == 0].dropna(subset=[f"f{H}", "d"]).copy()
        drift = S.groupby("coin")[f"f{H}"].mean()
        S["u"] = S[f"f{H}"] - S["coin"].map(drift)
        S = S[S.choppy]
        S["q"] = pd.qcut(S["d"], 5, labels=False)
        g = S.groupby(["up", "q"])["u"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["H"] = H
        q.append(g.reset_index())
    res["quintiles"] = pd.concat(q)
    S = A[A["pos"] % 5 == 0].dropna(subset=["f5", "d"]).copy()
    drift = S.groupby("coin")["f5"].mean(); S["u"] = S["f5"] - S["coin"].map(drift)
    T = S[S.choppy & S.up]
    pc = []
    for k, G in T.groupby("coin"):
        b, t, n = clus(G["d"].values, G["u"].values, G["day"]) if len(G) >= 30 else (np.nan, np.nan, len(G))
        pc.append({"coin": k, "slope": b, "t": t, "n": n, "mean_u_short": -G["u"].mean()})
    res["by_coin_H5_up"] = pd.DataFrame(pc)
    pw = []
    for k, G in T.groupby("win"):
        b, t, n = clus(G["d"].values, G["u"].values, G["day"]) if len(G) >= 30 else (np.nan, np.nan, len(G))
        pw.append({"win": k, "slope": b, "t": t, "n": n, "mean_u_short": -G["u"].mean()})
    res["by_win_H5_up"] = pd.DataFrame(pw)
    res["regime_counts"] = A["regime"].value_counts()
    return res
