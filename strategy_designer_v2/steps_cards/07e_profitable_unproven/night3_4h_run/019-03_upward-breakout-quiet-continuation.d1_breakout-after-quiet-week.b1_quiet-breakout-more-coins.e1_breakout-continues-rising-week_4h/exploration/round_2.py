def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    recs = {72: [], 36: [], 144: []}
    for h in recs:
        allret = {}
        tmp = []
        for c, wd in bars.items():
            for w, b in wd.items():
                b = b.reset_index(drop=True)
                fwd = b["close"].shift(-h) / b["close"] - 1
                allret.setdefault(c, []).append(fwd.iloc[::h].dropna())
                r42 = b["close"] / b["close"].shift(42) - 1
                r180 = b["close"] / b["close"].shift(180) - 1
                brk = b["close"] > b["high"].shift(1).rolling(12).max()
                g = pd.DataFrame({"fwd": fwd, "r42": r42, "r180": r180, "brk": brk, "c": c, "w": w,
                                  "pos": b["postRebalance_current_allocation"].fillna(0)}).iloc[::h]
                tmp.append(g)
        drift = {c: pd.concat(v).mean() for c, v in allret.items()}
        sd = {c: pd.concat(v).std() for c, v in allret.items()}
        G = pd.concat(tmp).dropna(subset=["fwd", "r42"])
        G["u"] = G.fwd - G.c.map(drift)
        G["r42z"] = G.r42 / G.c.map(sd)
        recs[h] = G
        def tt(x):
            return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        rows = []
        for name, sub in [("all", G), ("breakout", G[G.brk]), ("no_breakout", G[~G.brk])]:
            sl = stats.linregress(sub.r42z, sub.u)
            q = pd.qcut(sub.r42z, 5, labels=False)
            rows.append({"set": name, "n": len(sub), "slope_t_r42": sl.slope / sl.stderr,
                         "u_q0": sub.u[q == 0].mean(), "t_q0": tt(sub.u[q == 0]),
                         "u_q4": sub.u[q == 4].mean(), "t_q4": tt(sub.u[q == 4]),
                         "u_q4_minus_q0": sub.u[q == 4].mean() - sub.u[q == 0].mean()})
        G2 = G.dropna(subset=["r180"])
        G2 = G2.assign(r180z=G2.r180 / G2.c.map(sd))
        sl = stats.linregress(G2.r180z, G2.u)
        q = pd.qcut(G2.r180z, 5, labels=False)
        rows.append({"set": "all_r30d", "n": len(G2), "slope_t_r42": sl.slope / sl.stderr,
                     "u_q0": G2.u[q == 0].mean(), "t_q0": tt(G2.u[q == 0]),
                     "u_q4": G2.u[q == 4].mean(), "t_q4": tt(G2.u[q == 4]),
                     "u_q4_minus_q0": G2.u[q == 4].mean() - G2.u[q == 0].mean()})
        out[f"h{h}_momentum"] = pd.DataFrame(rows)
    # 72-bar: r42 quintile on all bars, split by half of coins per window (robustness: per year)
    G = recs[72].copy()
    G["q"] = G.groupby("c")["r42z"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    G["top_minus_bottom"] = np.where(G.q == 4, 1, np.where(G.q == 0, -1, 0))
    G["sig"] = G.top_minus_bottom * G.u
    out["h72_q4q0_by_coin"] = G[G.q.isin([0, 4])].groupby("c").apply(
        lambda s: pd.Series({"n": len(s), "u_q4": s.u[s.q == 4].mean(), "u_q0": s.u[s.q == 0].mean()}))
    out["h72_q4q0_by_window"] = G[G.q.isin([0, 4])].groupby("w").apply(
        lambda s: pd.Series({"n": len(s), "u_q4": s.u[s.q == 4].mean(), "u_q0": s.u[s.q == 0].mean()}))
    return out
