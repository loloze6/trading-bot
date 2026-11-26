def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            sd30 = r.rolling(30).std()
            df = pd.DataFrame({"coin": c, "wn": int(w[1:]), "day": b["timestamp"].astype(str).str[:10],
                               "f": b["forecast"], "alloc": b["postRebalance_current_allocation"], "reg": b["regime"],
                               "nxt": cl.shift(-1) / cl - 1, "nxt2": cl.shift(-2) / cl - 1,
                               "retz": r / sd30, "prevz": r.shift(1) / sd30, "r5": (cl / cl.shift(5) - 1) / sd30,
                               "rng": (b["high"] - b["low"]) / cl / sd30, "sd30": sd30,
                               "clpos": (cl - b["low"]) / (b["high"] - b["low"]), "up": r > 0})
            df["gain"] = -df["nxt"]; df["pnl"] = df["alloc"] * df["nxt"]
            rows.append(df)
    C = pd.concat(rows, ignore_index=True).dropna(subset=["nxt"])
    A = C[C.f < 0].copy()
    P = A.groupby(["wn", "day"])["pnl"].sum()
    wd = P.idxmin()
    out["worst_day_cases"] = A[(A.wn == wd[0]) & (A.day == wd[1])][["coin", "alloc", "f", "nxt", "retz", "prevz", "r5", "rng", "sd30", "clpos"]].reset_index(drop=True)
    out["alloc_by_f_quart"] = A.groupby(pd.qcut(A.f, 4), observed=True)[["alloc", "gain", "pnl"]].mean().set_axis(["q1","q2","q3","q4"])
    grid = C.groupby(["wn", "day"]).size() * 0.0
    def book(sub, col="pnl"):
        d = sub.groupby(["wn", "day"])[col].sum() / 6
        full = grid.copy(); full.loc[d.index] = d.values; full = full.sort_index()
        v = (1 + full).cumprod(); dd = (v / v.cummax() - 1).min()
        y = v.iloc[-1] ** (365 / len(full)) - 1
        return pd.Series({"yearly": y, "maxdd": dd, "calmar": y / -dd, "n": len(sub)})
    A["flat"] = -0.3 * A["nxt"]
    A["capped"] = A["alloc"].clip(lower=-0.3) * A["nxt"]
    A["inv"] = A["alloc"] * A["nxt"] * (0.0 + (A.rng >= 0.77))
    res = {"base": book(A), "equal_size_0.3": book(A, "flat"), "cap_0.3": book(A, "capped"),
           "drop_rng_low": book(A[A.rng >= 0.77]), "drop_retz_top": book(A[A.retz <= 0.88]),
           "drop_both": book(A[(A.rng >= 0.77) & (A.retz <= 0.88)])}
    out["variants"] = pd.DataFrame(res).T
    # condition alone: profile up days without signal, by retz
    U = C[(C.reg != "chop") & (C.f == 0) & C.up].dropna(subset=["retz"])
    out["nosignal_updays_by_retz"] = U.groupby(pd.qcut(U.retz, 3), observed=True)["gain"].agg(["mean", "count"]).set_axis(["low","mid","high"])
    out["nosignal_updays_by_rng"] = U.groupby(pd.qcut(U.rng, 3), observed=True)["gain"].agg(["mean", "count"]).set_axis(["low","mid","high"])
    S = A.dropna(subset=["retz"])
    out["signal_by_retz_rng"] = S.groupby([pd.qcut(S.retz, 2).astype(str), pd.qcut(S.rng, 2).astype(str)], observed=True)["gain"].agg(["mean", "count"])
    return out
