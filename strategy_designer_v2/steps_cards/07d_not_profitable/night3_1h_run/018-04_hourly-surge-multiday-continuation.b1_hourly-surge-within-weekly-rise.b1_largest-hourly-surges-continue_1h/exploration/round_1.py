def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    wins = [f"w{i}" for i in range(1, 25)]
    coins = list(data["days"].keys())
    # book daily returns chained in window order
    rows = []
    for w in wins:
        dfs = []
        for c in coins:
            if w in data["days"][c]:
                d = data["days"][c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                dfs.append(d)
        if not dfs: continue
        d = pd.concat(dfs)
        g = d.groupby("day").agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
        g["w"] = w
        rows.append(g)
    B = pd.concat(rows).dropna().reset_index(drop=True)
    eq = (1 + B["book"]).cumprod()
    pk = eq.cummax()
    dd = eq / pk - 1
    B["dd"] = dd.values
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["book_by_year"] = B.groupby("year").agg(n=("book", "size"), mean=("book", "mean"), sd=("book", "std"), hold=("hold", "mean"), mindd=("dd", "min"))
    # drawdown episodes
    eps = []
    i = 0
    n = len(B)
    in_dd = False
    for j in range(n):
        if dd.iloc[j] < 0 and not in_dd:
            in_dd = True; start = j
        if dd.iloc[j] == 0 and in_dd:
            in_dd = False
            seg = dd.iloc[start:j]
            eps.append((start, j, seg.min(), seg.idxmin()))
    if in_dd:
        seg = dd.iloc[start:]
        eps.append((start, n, seg.min(), seg.idxmin()))
    eps = sorted(eps, key=lambda e: e[2])[:5]
    er = []
    for (s, e, m, t) in eps:
        er.append({"depth": m, "days_to_trough": t - s + 1, "days_total": e - s,
                   "windows": ",".join(sorted(set(B["w"].iloc[s:t + 1]), key=lambda x: int(x[1:]))),
                   "year": int(B["year"].iloc[t]),
                   "hold_ret_to_trough": float((1 + B["hold"].iloc[s:t + 1]).prod() - 1)})
    out["deepest_falls"] = pd.DataFrame(er)
    out["calmar_parts"] = pd.Series({"yearly": (eq.iloc[-1]) ** (365 / n) - 1, "maxdd": dd.min()})
    # entries with features and forward path
    E = []
    for c in coins:
        for w, b in data["bars"][c].items():
            cl = b["close"].values.astype(float)
            al = b["postRebalance_current_allocation"].fillna(0).values
            pa = np.r_[0, al[:-1]]
            r24 = pd.Series(cl).pct_change(24)
            ratio = r24 / r24.abs().rolling(720, min_periods=120).mean()
            r168 = pd.Series(cl).pct_change(168)
            r720 = pd.Series(cl).pct_change(720)
            hi720 = pd.Series(cl).rolling(720, min_periods=120).max()
            lr = np.log(pd.Series(cl)).diff()
            vol_ratio = lr.rolling(168).std() / lr.rolling(1440, min_periods=500).std()
            idx = np.where((al > 0) & (pa <= 0))[0]
            for k in idx:
                if k + 120 >= len(cl): continue
                path = cl[k:k + 121] / cl[k] - 1
                E.append({"coin": c, "w": w, "ratio": ratio.iloc[k], "r168": r168.iloc[k], "r720": r720.iloc[k],
                          "offhi": cl[k] / hi720.iloc[k] - 1, "volr": vol_ratio.iloc[k], "alloc": al[k],
                          "fwd": path[-1], "minp": path.min(), "fwd24": path[24],
                          "hour": pd.Timestamp(b["timestamp"].iloc[k]).hour})
    E = pd.DataFrame(E)
    out["entries_n"] = len(E)
    for f in ["ratio", "r168", "r720", "offhi", "volr", "alloc"]:
        q = pd.qcut(E[f], 5, duplicates="drop")
        out["by_" + f] = E.groupby(q, observed=True).agg(n=("fwd", "size"), fwd=("fwd", "mean"),
                                                          t=("fwd", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))),
                                                          minp=("minp", "mean"), worst10=("fwd", lambda x: (x < -0.10).mean()))
    out["by_coin"] = E.groupby("coin").agg(n=("fwd", "size"), fwd=("fwd", "mean"), minp=("minp", "mean"))
    out["fwd24_vs_rest"] = E.groupby(pd.qcut(E["fwd24"], 5), observed=True).agg(n=("fwd", "size"), fwd=("fwd", "mean"), rest=("fwd", lambda x: 0))
    return out
