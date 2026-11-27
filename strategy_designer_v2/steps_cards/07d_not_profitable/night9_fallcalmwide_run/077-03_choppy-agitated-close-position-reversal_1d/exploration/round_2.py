def explore(data):
    import pandas as pd, numpy as np
    out = {}
    B = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["coin"] = coin; b["wn"] = int(w[1:])
            c = b["close"]
            b["ret1"] = c.shift(-1) / c - 1
            b["ret2"] = c.shift(-2) / c - 1
            b["ret3"] = c.shift(-3) / c - 1
            r = c.pct_change()
            b["r1"] = r
            b["sd30"] = r.rolling(30).std()
            b["z1"] = r / b["sd30"]
            b["pos"] = b["postRebalance_current_allocation"]
            b["inprof"] = (b["regime"] == "unknown")
            b["fc"] = b["forecast"]
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            B.append(b)
    B = pd.concat(B)
    P = B[B["inprof"] & B["ret1"].notna()].copy()
    P["side"] = np.sign(P["fc"])
    P = P[P["side"] != 0]
    for h in ["ret1", "ret2", "ret3"]:
        P["d" + h] = P["side"] * P[h]
    P["afc"] = P["fc"].abs()
    P["fq"] = pd.qcut(P["afc"], 3, labels=["lo", "mid", "hi"])
    # day's own move in the signal's direction (neg = signal fades the day's move)
    P["zdir"] = P["side"] * P["z1"]
    P["zq"] = pd.cut(P["zdir"], [-99, -1.5, -0.5, 99], labels=["big_against", "against", "small_or_with"])
    def agg(g):
        return pd.Series({"n": len(g), "d1": g["dret1"].mean(), "t1": g["dret1"].mean() / (g["dret1"].std() / np.sqrt(len(g))),
                          "d2": g["dret2"].mean(), "d3": g["dret3"].mean(), "p01": g["dret1"].quantile(0.05)})
    out["by_side_fq"] = P.groupby(["side", "fq"]).apply(agg)
    out["by_side_zq"] = P.groupby(["side", "zq"]).apply(agg)
    # condition alone: in-profile bars with big |z1| but low |forecast| ; next-day return contrarian to the day
    Q = B[B["inprof"] & B["ret1"].notna() & B["z1"].notna()].copy()
    Q["contra1"] = -np.sign(Q["z1"]) * Q["ret1"]
    Q["bigday"] = Q["z1"].abs() > 1.5
    Q["sig"] = Q["fc"].abs() >= P["afc"].quantile(2 / 3)
    out["cond_vs_sig"] = Q.groupby(["bigday", "sig", np.sign(Q["z1"])])["contra1"].agg(["size", "mean"])
    # long-only vs short-only daily books from days table
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            pos = b["postRebalance_current_allocation"].shift(1).fillna(0)
            r = b["close"].pct_change().fillna(0)
            b["g"] = pos * r
            b["gl"] = pos.clip(lower=0) * r
            b["gs"] = pos.clip(upper=0) * r
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["wn"] = int(w[1:])
            rows.append(b[["wn", "day", "g", "gl", "gs"]])
    R = pd.concat(rows).groupby(["wn", "day"])[["g", "gl", "gs"]].mean().sort_index()
    res = {}
    for k in ["g", "gl", "gs"]:
        v = (1 + R[k]).cumprod(); dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(R)) - 1
        res[k] = {"yearly": yr, "maxdd": dd, "calmar": yr / abs(dd) if dd < 0 else np.nan,
                  "sharpe": R[k].mean() / R[k].std() * np.sqrt(365)}
    out["side_books_prefee"] = pd.DataFrame(res).T
    # worst 10 gross days: share from shorts
    w10 = R.nsmallest(10, "g")
    out["worst10_share_short"] = float(w10["gs"].sum() / w10["g"].sum())
    return out
