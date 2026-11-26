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
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                "sd": sd30, "z1": r1 / sd30,
                "z2": (c / c.shift(2) - 1) / sd30,
                "z3": (c / c.shift(3) - 1) / sd30,
                "z3lag": (c.shift(1) / c.shift(4) - 1) / sd30,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f3": c.shift(-3) / c - 1,
                "inprof": (b["regime"] != "chop").astype(int),
                "yr": ts.dt.year,
                "rng": (b["high"] - b["low"]) / c / sd30,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
            })
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # coin drift per horizon over all windows (non-overlapping grid)
    drift = {}
    for h in (1, 2, 3):
        g = A[A.pos % h == 0]
        drift[h] = g.groupby("coin")["f%d" % h].mean()
    for h in (1, 2, 3):
        A["u%d" % h] = A["f%d" % h] - A["coin"].map(drift[h])
        A["uz%d" % h] = A["u%d" % h] / (A["sd"] * np.sqrt(h))
    out = {}

    def daysum(g, col):
        x = g.dropna(subset=[col])
        s = x.groupby("day")[col].sum()
        n = len(s)
        return pd.Series({"cases": len(x), "days": n, "mean_case": x[col].mean(),
                          "t_day": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})

    P = A[A.inprof == 1]
    U = P[P.z1 > 0].copy()
    U["q"] = pd.qcut(U["z1"], 4, labels=False)
    out["in_up_days_q_next1"] = U.groupby("q").apply(lambda g: daysum(g, "u1"))
    out["in_up_days_q_next1_z"] = U.groupby("q").apply(lambda g: daysum(g, "uz1"))
    out["in_up_days_by_year"] = U.groupby("yr").apply(lambda g: daysum(g, "u1"))
    out["in_up_days_by_window"] = U.groupby("win").apply(lambda g: daysum(g, "u1"))
    out["in_up_rho_z1_u1"] = "rho %.3f p %.3f n %d" % stats.spearmanr(U["z1"], U["u1"], nan_policy="omit")[:2] + (len(U),)
    # out of profile up days, same
    O = A[(A.inprof == 0) & (A.z1 > 0)].copy()
    O["q"] = pd.qcut(O["z1"], 4, labels=False)
    out["out_up_days_q_next1"] = O.groupby("q").apply(lambda g: daysum(g, "u1"))
    # up day after 3-day fall vs after 3-day rise, in profile
    U["prior"] = np.where(U["z3lag"] < 0, "after_fall", "after_rise")
    out["in_up_by_prior_next1"] = U.groupby("prior").apply(lambda g: daysum(g, "u1"))
    # multi-day rise (2-day) on grid of 2, next 2 days, in profile
    G2 = P[(P.pos % 2 == 0) & (P.z2 > 0)].copy()
    G2["q"] = pd.qcut(G2["z2"], 3, labels=False)
    out["in_rise2_q_next2"] = G2.groupby("q").apply(lambda g: daysum(g, "u2"))
    G3 = P[(P.pos % 3 == 0) & (P.z3 > 0)].copy()
    G3["q"] = pd.qcut(G3["z3"], 3, labels=False)
    out["in_rise3_q_next3"] = G3.groupby("q").apply(lambda g: daysum(g, "u3"))
    out["in_rise3_by_year"] = G3.groupby("yr").apply(lambda g: daysum(g, "u3"))
    # in-profile up days: close position graded
    U2 = U.dropna(subset=["clpos"]).copy()
    U2["cq"] = pd.qcut(U2["clpos"], 3, labels=False)
    out["in_up_closepos_next1"] = U2.groupby("cq").apply(lambda g: daysum(g, "u1"))
    # by coin
    out["in_up_by_coin"] = U.groupby("coin").apply(lambda g: daysum(g, "u1"))
    return out
