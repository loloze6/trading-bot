def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            sd30 = r.rolling(30).std()
            r5 = (cl / cl.shift(5) - 1) / sd30
            r3 = (cl / cl.shift(3) - 1) / sd30
            r10 = (cl / cl.shift(10) - 1) / sd30
            rng = (b["high"] - b["low"]) / cl / sd30
            df = pd.DataFrame({"coin": c, "wn": int(w[1:]), "day": b["timestamp"].astype(str).str[:10],
                               "f": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "reg": b["regime"], "nxt": cl.shift(-1) / cl - 1, "r5": r5, "r3": r3, "r10": r10,
                               "rng": rng, "up": r > 0, "prevdown": r.shift(1) <= 0, "ret": r})
            df["gain"] = -df["nxt"]
            df["pnl"] = df["alloc"] * df["nxt"]
            rows.append(df)
    C = pd.concat(rows, ignore_index=True).dropna(subset=["nxt"])
    A = C[C.f < 0]
    inprof = C[C.reg != "chop"]
    out["regime_counts"] = C.reg.value_counts()
    # condition alone: in profile, no signal
    noS = inprof[inprof.f == 0].dropna(subset=["r5"])
    def tb(df, name):
        g = df["gain"]
        return pd.Series({"mean": g.mean(), "n": len(g), "t": g.mean() / (g.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan}, name=name)
    res = []
    for col in ["r5", "r3", "r10"]:
        res.append(tb(A[A[col] < 0], f"signal & {col}<0"))
        res.append(tb(A[A[col] >= 0], f"signal & {col}>=0"))
        res.append(tb(noS[noS[col] < 0], f"profile nosignal & {col}<0"))
        res.append(tb(noS[noS[col] >= 0], f"profile nosignal & {col}>=0"))
    res.append(tb(noS, "profile nosignal all"))
    res.append(tb(noS[noS.up], "profile nosignal up day (later up days)"))
    out["condition_check"] = pd.DataFrame(res)
    # graded within r5<0 by rng
    S = A[A.r5 < 0]
    g = pd.qcut(S.rng, 3)
    t = S.groupby(g, observed=True)["gain"].agg(["mean", "count"]); t.index = t.index.astype(str)
    out["r5neg_by_rng"] = t
    # book pnl per day grouped by r5 sign of positions
    A2 = A.copy(); A2["r5neg"] = A2.r5 < 0
    out["pnl_by_r5sign"] = A2.groupby("r5neg")["pnl"].agg(["sum", "mean", "count"])
    # worst book days: positions details
    P = A.groupby(["wn", "day"]).agg(pnl=("pnl", "sum"), ncoins=("coin", "size"), meanr5=("r5", "mean"), meanrng=("rng", "mean"), meannxt=("nxt", "mean")).reset_index()
    out["worst_position_days"] = P.nsmallest(10, "pnl").drop(columns="day")
    out["pnl_by_ncoins"] = P.groupby("ncoins")["pnl"].agg(["sum", "mean", "count", "min"])
    # drawdown rebuild with r5<0 filter (approx pnl/6)
    for name, sub in [("all", A), ("r5neg", A[A.r5 < 0])]:
        d = sub.groupby(["wn", "day"])["pnl"].sum() / 6
        full = C.groupby(["wn", "day"]).size() * 0.0
        full.loc[d.index] = d.values
        full = full.sort_index()
        v = (1 + full).cumprod(); dd = (v / v.cummax() - 1).min()
        yrs = len(full) / 365
        out["approx_" + name] = pd.Series({"yearly": v.iloc[-1] ** (1 / yrs) - 1, "maxdd": dd, "calmar": (v.iloc[-1] ** (1 / yrs) - 1) / -dd})
    out["by_window_r5neg"] = A[A.r5 < 0].groupby("wn")["gain"].agg(["mean", "count"])
    return out
