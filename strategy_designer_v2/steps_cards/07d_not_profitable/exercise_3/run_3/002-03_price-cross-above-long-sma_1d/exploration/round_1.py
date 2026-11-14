def explore(data):
    import pandas as pd, numpy as np
    out = {}
    # pooled book daily return: mean across coins per (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["win"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["win"].str[1:].astype(int)
    P = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    P = P.dropna(subset=["book_return"])
    eq = (1 + P["book_return"]).cumprod()
    dd_ = eq / eq.cummax() - 1
    P["dd"] = dd_.values
    out["max_dd_chain"] = float(dd_.min())
    out["ann_ret"] = float(eq.iloc[-1] ** (365 / len(P)) - 1)
    # worst drawdown by window
    wsum = P.groupby("wn").agg(book=("book_return", lambda x: (1 + x).prod() - 1),
                               coin=("coin_return", lambda x: (1 + x).prod() - 1),
                               mindd=("dd", "min"))
    out["by_window"] = wsum.round(3)
    # bar-level position gains with states
    B = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            cl = b["close"]
            b["r1"] = cl.shift(-1) / cl - 1
            b["gain"] = b["postRebalance_current_allocation"] * b["r1"]
            b["dist"] = b["debug_info.components.above_ma.last_history_value"]
            b["past20"] = cl / cl.shift(20) - 1
            b["fwd20"] = cl.shift(-20) / cl - 1
            b["vol20"] = cl.pct_change().rolling(20).std()
            b["dd60"] = cl / cl.rolling(60).max() - 1
            b["coin"] = c; b["wn"] = int(w[1:])
            b["pos"] = np.arange(len(b))
            B.append(b[["coin", "wn", "pos", "forecast", "postRebalance_current_allocation", "r1", "gain", "dist", "past20", "fwd20", "vol20", "dd60"]])
    B = pd.concat(B)
    A = B[B["postRebalance_current_allocation"] > 0].dropna(subset=["gain"])
    out["active_share"] = float((B["postRebalance_current_allocation"] > 0).mean())
    for col in ["forecast", "dist", "past20", "vol20", "dd60"]:
        q = pd.qcut(A[col], 5, duplicates="drop")
        g = A.groupby(q)["gain"].agg(["count", "mean", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["sum"] = A.groupby(q)["gain"].sum()
        out["gain_by_" + col] = g.round(5)
    # non-overlapping 20-bar fwd on grid, active
    G = B[(B["pos"] % 20 == 0) & (B["forecast"] > 0)].dropna(subset=["fwd20"])
    for col in ["dist", "past20", "dd60"]:
        q = pd.qcut(G[col], 4, duplicates="drop")
        out["fwd20_by_" + col] = G.groupby(q)["fwd20"].agg(["count", "mean", "median"]).round(4)
    # worst 5% book days: what state
    worst = A.nsmallest(int(len(A) * 0.05), "gain")
    out["worst5_state"] = worst[["forecast", "dist", "past20", "vol20", "dd60", "postRebalance_current_allocation"]].mean().round(4)
    out["all_active_state"] = A[["forecast", "dist", "past20", "vol20", "dd60", "postRebalance_current_allocation"]].mean().round(4)
    return out
