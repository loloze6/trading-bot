def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 70:
                continue
            hi = b["high"].rolling(20, min_periods=20).max()
            lo = b["low"].rolling(20, min_periods=20).min()
            pos = 2 * (b["close"] - lo) / (hi - lo) - 1
            r1 = b["close"].pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "i": np.arange(len(b)), "pos": pos,
                "s5": (b["close"] / b["close"].shift(5) - 1) / (vol20 * np.sqrt(5)),
                "r1s": r1 / vol20,
                "ret60": b["close"] / b["close"].shift(60) - 1,
                "fwd5": b["close"].shift(-5) / b["close"] - 1,
                "regime": b["regime"].values,
                "alloc": b["postRebalance_current_allocation"].values,
                "fwd1": b["close"].shift(-1) / b["close"] - 1,
                "dayk": ts.dt.floor("D").values,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.i % 5 == 0].groupby("coin")["fwd5"].mean()
    A["ex5"] = A["fwd5"] - A["coin"].map(drift)
    A["calm"] = np.where(A.regime == "unknown", "calm", "agit")
    A["tr"] = pd.cut(A.ret60, [-100, -0.1, 0.1, 100], labels=["fall", "chop", "rise"])
    G = A[(A.i % 5 == 0)].dropna(subset=["ex5", "pos", "s5", "tr"]).copy()

    def ct(g, col="ex5"):
        d = g.groupby("dayk")[col].apply(lambda s: (s - g[col].mean()).sum())
        se = np.sqrt((d ** 2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": g.dayk.nunique(),
                          "mean_%": 100 * g[col].mean(), "t_day": g[col].mean() / se if se > 0 else np.nan})
    out = {}
    G["pq"] = pd.cut(G.pos, [-1.01, -0.5, 0.5, 1.01], labels=["low", "mid", "high"])
    out["profile60_pos"] = G.groupby(["tr", "calm", "pq"], observed=True).apply(ct)
    # double sort: range position vs scaled 5-day move, calm only
    C = G[G.calm == "calm"].copy()
    C["s5q"] = pd.qcut(C.s5, 3, labels=["dn", "mid", "up"])
    out["calm_pos_x_s5"] = C.groupby(["pq", "s5q"], observed=True).apply(ct)
    # partial regression calm: ex5 on pos and s5 standardised
    X = np.column_stack([np.ones(len(C)), (C.pos - C.pos.mean()) / C.pos.std(), (C.s5 - C.s5.mean()) / C.s5.std()])
    beta, *_ = np.linalg.lstsq(X, C.ex5.values, rcond=None)
    res = C.ex5.values - X @ beta
    XtXi = np.linalg.inv(X.T @ X)
    meat = np.zeros((3, 3))
    for _, idx in C.reset_index(drop=True).groupby("dayk").groups.items():
        sc = X[idx].T @ res[idx]; meat += np.outer(sc, sc)
    se = np.sqrt(np.diag(XtXi @ meat @ XtXi))
    out["calm_partial"] = pd.DataFrame({"beta_%": 100 * beta, "t_day": beta / se}, index=["const", "pos", "s5"])
    # agitated: after large one-day falls/rises (scaled), by trend
    Ag = G[G.calm == "agit"].copy()
    Ag["r1q"] = pd.qcut(Ag.r1s, 3, labels=["dn", "mid", "up"])
    out["agit_trend_r1"] = Ag.groupby(["tr", "r1q"], observed=True).apply(ct)
    # windows consistency of calm high-minus-low
    out["calm_hi_minus_lo_by_win"] = C.groupby("win").apply(
        lambda g: pd.Series({"n": len(g), "diff_%": 100 * (g[g.pq == "high"].ex5.mean() - g[g.pq == "low"].ex5.mean())}))
    A["gain"] = A.alloc * A.fwd1
    out["book_gain_by_profile_side"] = A.dropna(subset=["gain", "tr"]).assign(side=np.sign(A.alloc)).query("side!=0").groupby(
        ["tr", "side"], observed=True)["gain"].agg(["count", "mean", "sum"])
    return out
