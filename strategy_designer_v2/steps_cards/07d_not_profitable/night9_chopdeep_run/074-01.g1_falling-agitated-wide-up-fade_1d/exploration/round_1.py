def explore(data):
    import pandas as pd, numpy as np
    out = {}
    # book daily
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])["book_return"].mean().dropna().reset_index().sort_values(["wn", "day"])
    v = (1 + B["book_return"]).cumprod()
    dd = v / v.cummax() - 1
    B["dd"] = dd.values
    out["deepest_fall"] = float(dd.min())
    # drawdown episodes: top 5 by depth
    B["peak"] = v.cummax().values
    i = int(np.argmin(dd.values))
    B["idx"] = range(len(B))
    eps = []
    peakidx = 0; vals = v.values; cur_min = 0; start = 0
    epl = []
    for k in range(len(vals)):
        if vals[k] >= vals[start:k+1].max() and dd.values[k] == 0:
            if cur_min < 0: epl.append((start, k, cur_min))
            start = k; cur_min = 0
        else:
            cur_min = min(cur_min, dd.values[k])
    if cur_min < 0: epl.append((start, len(vals)-1, cur_min))
    epl = sorted(epl, key=lambda x: x[2])[:6]
    out["episodes"] = pd.DataFrame([{"window": "w%d" % B["wn"].iloc[s], "depth": m, "days": e - s,
                                     "worst_day": B["book_return"].iloc[s:e+1].min()} for s, e, m in epl])
    # per window book stats
    out["by_window"] = B.groupby("wn")["book_return"].agg(["mean", "std", "min", "count"])
    # cases
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; rng = b["high"] - b["low"]
            mult = rng / rng.rolling(20, min_periods=20).mean()
            r1 = cl.pct_change()
            nxt = cl.shift(-1) / cl - 1
            nxt2 = cl.shift(-2) / cl - 1
            r5 = cl / cl.shift(5) - 1
            r20 = cl / cl.shift(20) - 1
            r60 = cl / cl.shift(60) - 1
            clv = (cl - b["low"]) / rng
            upw = (b["high"] - cl) / rng  # upper wick share
            vol20 = r1.rolling(20).std()
            f = b["forecast"]
            sig = (f < 0) & ~(f.shift(1) < 0)
            alloc = b["postRebalance_current_allocation"]
            g = pd.DataFrame({"coin": c, "w": w, "nxt": nxt, "nxt2": nxt2, "mult": mult, "r1": r1, "r1z": r1 / vol20,
                              "r5": r5, "r20": r20, "r60": r60, "clv": clv, "alloc": alloc, "sig": sig, "f": f,
                              "rngpct": rng / cl / vol20})
            cs.append(g)
    G = pd.concat(cs)
    allm = G.groupby("coin")["nxt"].mean()
    G["drift"] = G["coin"].map(allm)
    G["un"] = -(G["nxt"] - G["drift"])
    G["pnl"] = -G["nxt"]
    S = G[G["sig"]].dropna(subset=["nxt"]).copy()
    out["n_cases"] = len(S)
    out["case_summary"] = S[["un", "pnl", "nxt2", "alloc"]].describe().T
    def q(col, n=4):
        t = S.copy(); t["q"] = pd.qcut(t[col], n, duplicates="drop")
        return t.groupby("q")["un"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    for col in ["mult", "r1", "r1z", "r5", "r20", "r60", "clv"]:
        out["by_" + col] = q(col)
    out["by_window_cases"] = S.groupby("w")["un"].agg(["mean", "count", "sum"])
    out["by_coin_cases"] = S.groupby("coin")["un"].agg(["mean", "count"])
    out["worst10"] = S.nsmallest(12, "pnl")[["coin", "w", "pnl", "mult", "r1", "r5", "r20", "r60", "clv", "alloc"]].reset_index(drop=True)
    return out
