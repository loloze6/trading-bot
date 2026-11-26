def explore(data):
    import pandas as pd, numpy as np
    out = {}
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r = cl.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({"coin": c, "w": w, "z": r / sd30, "r": r,
                               "n1": cl.shift(-1) / cl - 1,
                               "n12": cl.shift(-2) / cl.shift(-1) - 1,
                               "r1next": cl.shift(-1) / cl - 1,
                               "alloc": b["postRebalance_current_allocation"].fillna(0),
                               "inprof": b["regime"] == "unknown",
                               "below20": cl / cl.rolling(20, min_periods=10).max() - 1,
                               "r60": cl / cl.shift(60) - 1,
                               "r5": (cl / cl.shift(5) - 1) / sd30})
            df["gain"] = df["alloc"] * df["n1"]
            recs.append(df)
    X = pd.concat(recs)
    mu = X.groupby("coin")["n1"].mean()
    X["drift"] = X["coin"].map(mu)
    X["u1"] = -(X["n1"] - X["drift"])
    A = X[X["inprof"]].dropna(subset=["n1", "z"]).copy()
    P = A[A["r"] > 0].copy()
    edges = P["z"].quantile([0.25, 0.5, 0.75]).values
    P["zq"] = np.digitize(P["z"], edges)
    def ag(g):
        v = g["u1"]
        return pd.Series({"n": len(v), "u1": v.mean(), "t": v.mean() / (v.std() / np.sqrt(len(v))),
                          "alloc": g["alloc"].mean(), "gain_sum": g["gain"].sum()})
    # depth below 20-day high after the rise: still inside the decline?
    P["deep"] = pd.qcut(P["below20"], 2, labels=["far_below_high", "near_high"])
    out["zq_by_below20high"] = P.groupby(["zq", "deep"]).apply(ag).round(4)
    # condition alone: profile bars (any day) with near/far from 20-day high
    A["deep"] = np.where(A["below20"] <= P["below20"].median(), "far_below_high", "near_high")
    out["condition_alone_all_profile_days"] = A.groupby("deep").apply(ag).round(4)
    out["condition_alone_profile_downdays"] = A[A["r"] <= 0].groupby("deep").apply(ag).round(4)
    # prior 5-day rise in swings, within profile up days
    P["r5q"] = pd.qcut(P["r5"], 3, labels=False)
    out["zq_by_r5"] = P.groupby(["zq", "r5q"]).apply(ag)[["n", "u1", "t"]].round(4)
    # extreme rise followed by another up day: fade from day+1
    T = P[P["zq"] == 3].copy()
    T["u_next2"] = -(T["n12"] - T["drift"])
    for lab, sub in [("next_up", T[T["r1next"] > 0]), ("next_down", T[T["r1next"] <= 0])]:
        v = sub["u_next2"].dropna()
        out["top_q_then_" + lab + "_fade_day2"] = pd.Series({"n": len(v), "mean": v.mean(),
                                                             "t": v.mean() / (v.std() / np.sqrt(len(v)))}).round(4)
    out["top_q_share_next_up"] = round((T["r1next"] > 0).mean(), 3)
    return out
