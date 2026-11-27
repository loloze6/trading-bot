def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
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
                                "depth": depth, "rec": rec, "regime": reg, "r1": r1})
            for H in [1, 3, 5]:
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
    tab = []; deep = []; outl = []
    for H in [1, 3, 5]:
        S = A[A["pos"] % H == 0].dropna(subset=[f"f{H}", "d"]).copy()
        drift = S.groupby("coin")[f"f{H}"].mean()
        S["u"] = S[f"f{H}"] - S["coin"].map(drift)
        S = S[S.choppy].copy()
        lo, hi = S["u"].quantile([0.01, 0.99])
        S["uw"] = S["u"].clip(lo, hi)
        S["q"] = pd.qcut(S["d"], 5, labels=False)
        for name, m in [("up", S.up), ("down", ~S.up), ("all", S.up | ~S.up)]:
            T = S[m]
            b, t, n = clus(T["d"].values, T["u"].values, T["day"])
            bw, tw, _ = clus(T["d"].values, T["uw"].values, T["day"])
            rho, p = stats.spearmanr(T["d"], T["u"])
            dq = T[T.q == 0]["uw"]; rq = T[T.q > 0]["uw"]
            tt = stats.ttest_ind(dq, rq, equal_var=False)
            tab.append({"H": H, "set": name, "n": n, "t_raw": t, "t_wins": tw,
                        "spearman": rho, "sp_p": p, "deepQ_mean": dq.mean(),
                        "rest_mean": rq.mean(), "deep_minus_rest_t": tt.statistic,
                        "n_deep": len(dq)})
        top = S.loc[S["u"].abs().nlargest(3).index, ["coin", "win", "up", "q", "u"]]
        top["H"] = H
        outl.append(top)
        T = S[S.q == 0]
        g = T.groupby("win")["uw"].agg(["mean", "count"]); g["H"] = H
        deep.append(g.reset_index())
    res["robust"] = pd.DataFrame(tab)
    res["largest_moves"] = pd.concat(outl)
    res["deepQ_by_win"] = pd.concat(deep)
    return res
