def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            b = data["bars"][coin][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            alloc = b.groupby("day")["postRebalance_current_allocation"].last()
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day")
            dd["alloc_prev"] = alloc.reindex(dd.index).shift(1)
            c = dd["close"]
            dd["ret14"] = c.shift(1) / c.shift(15) - 1
            dd["ret30"] = c.shift(1) / c.shift(31) - 1
            dd["vol20"] = dd["coin_return"].shift(1).rolling(20).std()
            dd["coin"] = coin; dd["w"] = w
            dd["wn"] = int(w[1:])
            rows.append(dd.reset_index())
    D = pd.concat(rows)
    # combined book
    B = D.groupby(["wn", "day"])["book_return"].mean().dropna().sort_index()
    eq = (1 + B).cumprod()
    peak = eq.cummax()
    ddn = eq / peak - 1
    out["max_dd"] = float(ddn.min())
    out["ann_ret"] = float(eq.iloc[-1] ** (365 / len(B)) - 1)
    # drawdown episodes
    ep = []
    inDD = False
    for i, (k, v) in enumerate(ddn.items()):
        if v < 0 and not inDD:
            inDD = True; start = i
        if v == 0 and inDD:
            inDD = False
            seg = ddn.iloc[start:i]
            ep.append((start, i, seg.min(), seg.idxmin()[0]))
    if inDD:
        seg = ddn.iloc[start:]
        ep.append((start, len(ddn), seg.min(), seg.idxmin()[0]))
    ep = sorted(ep, key=lambda x: x[2])[:6]
    out["top_dd"] = pd.DataFrame([{"depth": e[2], "days": e[1]-e[0], "trough_window": e[3]} for e in ep])
    # per coin daily: split by side
    D2 = D.dropna(subset=["book_return", "alloc_prev"]).copy()
    D2["side"] = np.sign(D2["alloc_prev"]).map({1: "long", -1: "short", 0: "flat"})
    g = D2.groupby("side")["book_return"]
    out["by_side"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "std": g.std(), "min": g.min(), "share_below_-3pct": g.apply(lambda s: (s < -0.03).mean())})
    D2["r30q"] = pd.qcut(D2["ret30"], 5, labels=False)
    out["by_ret30q_side"] = D2.groupby(["r30q", "side"])["book_return"].agg(["size", "mean", "std"])
    D2["volq"] = pd.qcut(D2["vol20"], 3, labels=False)
    out["by_volq_side"] = D2.groupby(["volq", "side"])["book_return"].agg(["size", "mean", "std"])
    out["by_coin_window_sum"] = D2.groupby(["coin"])["book_return"].agg(["size", "mean", "std"])
    # inside worst episodes: side and ret30
    rowsE = []
    idx = list(ddn.index)
    for e in ep[:4]:
        keys = idx[e[0]:min(e[1], len(idx))]
        sub = D2.set_index(["wn", "day"]).loc[lambda x: x.index.isin(keys)]
        for s, gg in sub.groupby("side"):
            rowsE.append({"depth": round(e[2], 3), "side": s, "n": len(gg), "sum_ret": gg["book_return"].sum(), "mean_ret30": gg["ret30"].mean(), "mean_coin_ret": gg["coin_return"].mean()})
    out["episodes_side"] = pd.DataFrame(rowsE)
    return out
