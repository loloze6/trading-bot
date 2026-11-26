def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "r1": r1, "sd": sd30,
                "z1": r1 / sd30,
                "z3": (c / c.shift(3) - 1) / sd30,
                "z3lag": (c.shift(1) / c.shift(4) - 1) / sd30,
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "inprof": (b["regime"] != "chop").astype(int),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "rng": (b["high"] - b["low"]) / c / sd30,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
            })
            d["f1z"] = d["f1"] / d["sd"]
            d["f3z"] = d["f3"] / (d["sd"] * np.sqrt(3))
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    out["share_in_profile"] = A["inprof"].mean()

    def summ(g, col):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    # 1-day horizon: today's scaled return quintile -> next-day scaled return, in/out profile
    B = A.dropna(subset=["z1", "f1z"]).copy()
    B["q"] = pd.qcut(B["z1"], 5, labels=False)
    out["z1q_next1_by_prof"] = B.groupby(["inprof", "q"]).apply(lambda g: summ(g, "f1z")).unstack(0)
    # brief theme: 3-day rise scaled -> next 3 days, grid pos%3==0
    C = A[(A["pos"] % 3 == 0)].dropna(subset=["z3", "f3z"]).copy()
    C["q"] = pd.qcut(C["z3"], 5, labels=False)
    out["z3q_next3_by_prof"] = C.groupby(["inprof", "q"]).apply(lambda g: summ(g, "f3z")).unstack(0)
    # in-profile correlation tests
    for name, D, x, y in [("in_z1_f1", B[B.inprof == 1], "z1", "f1z"), ("out_z1_f1", B[B.inprof == 0], "z1", "f1z"),
                          ("in_z3_f3", C[C.inprof == 1], "z3", "f3z"), ("out_z3_f3", C[C.inprof == 0], "z3", "f3z")]:
        rr, p = stats.spearmanr(D[x], D[y])
        out["corr_" + name] = f"rho {rr:.3f} p {p:.3f} n {len(D)}"
    # weekday next-day return, by profile
    out["weekday_next1_by_prof"] = B.groupby(["inprof", "wd"]).apply(lambda g: summ(g, "f1z")).unstack(0)
    # range and close position: wide range, close location -> next day
    E = B.dropna(subset=["rng", "clpos"]).copy()
    E["rq"] = pd.qcut(E["rng"], 3, labels=False)
    E["cq"] = pd.qcut(E["clpos"], 3, labels=False)
    out["range_close_next1_inprof"] = E[E.inprof == 1].groupby(["rq", "cq"]).apply(lambda g: summ(g, "f1z")).unstack(0)
    out["range_close_next1_outprof"] = E[E.inprof == 0].groupby(["rq", "cq"]).apply(lambda g: summ(g, "f1z")).unstack(0)
    # forecast quintile among active bars
    F = A[(A.fc < 0)].dropna(subset=["f1z"]).copy()
    F["q"] = pd.qcut(F["fc"], 4, labels=False, duplicates="drop")
    out["fc_q_next1z"] = F.groupby("q").apply(lambda g: summ(g, "f1z"))
    out["active_by_year"] = F.groupby("yr").apply(lambda g: summ(g, "f1z"))
    # book daily returns: largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    Dd = pd.concat(dd)
    bk = Dd.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["count", "mean", "sum"])
    return out
