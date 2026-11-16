def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.shift(-1) / c - 1
            pos = b["postRebalance_current_allocation"]
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            hi = c.rolling(20, min_periods=20).max(); lo = c.rolling(20, min_periods=20).min()
            rp = (c - lo) / (hi - lo)
            ret10p = c / c.shift(10) - 1
            ret30p = c / c.shift(30) - 1
            vol20 = c.pct_change().rolling(20).std()
            fwd10 = c.shift(-10) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "pos": pos, "g": pos * r1, "r1": r1, "fee": fee,
                               "regime": b["regime"], "rp": rp, "ret10p": ret10p, "ret30p": ret30p,
                               "vol20": vol20, "fwd10": fwd10, "i": np.arange(len(b))})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["net"] = A["g"] - A["fee"]
    out["fees total per bar mean, gross mean"] = pd.Series({"fee_mean": A["fee"].mean(), "gross_mean": A["g"].mean(),
                                                           "net_mean": A["net"].mean()})
    T = A[A["regime"] == "trending"].dropna(subset=["g"])
    T["side"] = np.sign(T["pos"])
    out["trending gain/fee by side"] = T.groupby("side").agg(n=("g", "size"), g=("g", "mean"), fee=("fee", "mean"), net=("net", "mean"), r1=("r1", "mean"))
    L = T[T["pos"] > 0].copy()
    L["r10q"] = pd.qcut(L["ret10p"], 5)
    out["long gain by past 10d return quintile"] = L.groupby("r10q").agg(n=("g", "size"), g=("g", "mean"), r1=("r1", "mean"), pos=("pos", "mean"))
    L["r30q"] = pd.qcut(L["ret30p"], 5)
    out["long gain by past 30d return quintile"] = L.groupby("r30q").agg(n=("g", "size"), g=("g", "mean"), r1=("r1", "mean"))
    L["vq"] = pd.qcut(L["vol20"], 5)
    out["long gain by vol20 quintile"] = L.groupby("vq").agg(n=("g", "size"), g=("g", "mean"), r1=("r1", "mean"), pos=("pos", "mean"))
    # grid 10-bar forward in trending by range pos and ret30p
    G = A[(A["regime"] == "trending") & (A["i"] % 10 == 0)].dropna(subset=["fwd10", "rp", "ret30p"])
    G["rpb"] = pd.cut(G["rp"], [-0.01, 0.5, 0.8, 1.0])
    G["r30b"] = pd.qcut(G["ret30p"], 3, labels=["low30", "mid30", "high30"])
    out["grid fwd10 by rp x ret30"] = G.groupby(["rpb", "r30b"]).agg(n=("fwd10", "size"), m=("fwd10", "mean"), t=("fwd10", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # worst book days: what was held
    S = A.dropna(subset=["g"]).copy()
    S["book_bar"] = S["net"]
    q = S["g"].quantile(0.02)
    W = S[S["g"] <= q]
    out["worst 2% position-bars: side and context"] = pd.Series({"n": len(W), "share_long": (W["pos"] > 0).mean(),
        "share_short": (W["pos"] < 0).mean(), "mean_rp": W["rp"].mean(), "mean_ret10p": W["ret10p"].mean(),
        "mean_ret30p": W["ret30p"].mean(), "mean_vol20": W["vol20"].mean(), "all_vol20": S["vol20"].mean(),
        "share_trending": (W["regime"] == "trending").mean()})
    # turnover/fees by regime transitions
    out["fee sum by side"] = S.groupby(np.sign(S["pos"]))["fee"].sum()
    return out
