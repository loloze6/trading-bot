def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; trades = data["trades"]
    coins = list(bars.keys())
    bad = {"w1", "w2", "w3", "w5", "w9"}
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            rng = (hi - lo).rolling(180, min_periods=45).mean()
            r42 = cl / cl.shift(42) - 1
            r180 = cl / cl.shift(180) - 1
            vr = (hi - lo).rolling(42).mean() / rng
            dh = cl / hi.rolling(180, min_periods=45).max() - 1
            nxt = cl.shift(-1) / cl - 1
            a = b["postRebalance_current_allocation"].fillna(0)
            g = a * nxt
            f = pd.DataFrame({"r42": r42, "r180": r180, "vr": vr, "dh": dh, "a": a, "g": g, "nxt": nxt})
            f["coin"] = c; f["window"] = w; f["bad"] = w in bad
            recs.append(f.dropna())
    F = pd.concat(recs)
    L = F[F["a"] > 0]
    out["share_long_bars"] = pd.Series({"all": (F["a"] > 0).mean(), "bad_w": (F.loc[F.bad, "a"] > 0).mean(),
                                        "good_w": (F.loc[~F.bad, "a"] > 0).mean(),
                                        "mean_alloc_long": L["a"].mean()})
    def tab(col, bins):
        q = pd.cut(L[col], bins)
        t = L.groupby([q, "bad"], observed=True)["g"].agg(["mean", "sum", "count"]).unstack()
        return t
    out["by_r180"] = tab("r180", [-5, -0.2, -0.1, 0, 0.1, 0.2, 0.4, 10])
    out["by_dh"] = tab("dh", [-5, -0.3, -0.2, -0.1, -0.05, 0.001])
    out["by_vr"] = tab("vr", [0, 0.7, 0.85, 1.0, 1.2, 10])
    out["by_r42"] = tab("r42", [-5, -0.1, -0.05, 0, 0.05, 0.1, 0.2, 10])
    out["by_alloc"] = tab("a", [0, 0.5, 1, 1.5, 2.01])
    # t-stats of per-bar unusual gain on coin by r180 sign, using non-overlap? report mean nxt
    L2 = L.copy(); L2["pos180"] = L2["r180"] > 0
    out["nxt_by_r180sign"] = L2.groupby("pos180")["nxt"].agg(["mean", "std", "count"])
    # trades, entry r180 sign: pl and in bad windows
    tr = []
    for c in coins:
        for w, b in bars[c].items():
            t = trades[c].get(w)
            if t is None or len(t) == 0: continue
            bb = b.copy(); bb["ts"] = pd.to_datetime(bb["timestamp"])
            cl = bb["close"]; hi = bb["high"]
            bb["r180"] = cl / cl.shift(180) - 1
            bb["dh"] = cl / hi.rolling(180, min_periods=45).max() - 1
            t = t.copy(); t["et"] = pd.to_datetime(t["entry_time"])
            m = pd.merge_asof(t.sort_values("et"), bb[["ts", "r180", "dh"]].sort_values("ts"), left_on="et", right_on="ts")
            m["bad"] = w in bad
            tr.append(m)
    T = pd.concat(tr)
    T["pl"] = T["net_profit_loss_percent"]
    T["r180b"] = pd.cut(T["r180"], [-5, -0.15, 0, 0.15, 10])
    out["trades_r180_bad"] = T.groupby(["r180b", "bad"], observed=True)["pl"].agg(["mean", "count"]).unstack()
    return out
