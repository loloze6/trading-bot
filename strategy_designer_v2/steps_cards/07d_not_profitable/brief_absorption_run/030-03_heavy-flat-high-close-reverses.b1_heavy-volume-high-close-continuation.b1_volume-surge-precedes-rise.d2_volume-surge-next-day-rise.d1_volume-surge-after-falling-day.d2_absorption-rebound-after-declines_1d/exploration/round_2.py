def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, wd in data["bars"].items():
        for w, b in wd.items():
            b = b.copy().reset_index(drop=True)
            b["coin"] = c; b["wn"] = int(w[1:])
            cl = b["close"]
            b["r1"] = cl.shift(-1) / cl - 1
            b["ret1"] = cl.pct_change()
            b["ret20"] = cl / cl.shift(20) - 1
            b["vr"] = b["volume"] / b["volume"].shift(1).rolling(20).mean()
            b["sd20"] = b["ret1"].rolling(20).std()
            b["clv"] = (cl - b["low"]) / (b["high"] - b["low"])
            b["al"] = b["postRebalance_current_allocation"]
            b["pnl"] = b["al"] * b["r1"]
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["age"] = b.groupby((b["forecast"] <= 0).cumsum()).cumcount()
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["x1"] = B["r1"] - B["coin"].map(B.groupby("coin")["r1"].mean())
    S = B[B["forecast"] > 0].copy()
    # held bars pnl by age of position (bars since signal start) and by vr of signal day
    H = B[B["al"].abs() > 0].copy()
    H["vrb"] = pd.cut(H["vr"], [0, 1, 1.5, 2.5, 100])
    out["held pnl by vr"] = H.groupby("vrb")["pnl"].agg(["count", "mean", "sum"])
    out["held pnl by age"] = H.groupby(H["age"].clip(upper=5))["pnl"].agg(["count", "mean", "sum"])
    # window 16 and 17 dd anatomy
    for wn in [16, 17, 2, 18]:
        W = B[B["wn"] == wn]
        out[f"w{wn} by coin"] = W.groupby("coin").agg(pnl=("pnl", "sum"), coin=("ret1", "sum"),
                                                     held=("al", lambda a: (a.abs() > 0).mean()),
                                                     vr_held=("vr", "mean"))
    # signal x1 by vr and clv (close location from brief)
    S["vrb"] = pd.cut(S["vr"], [0, 1, 1.5, 2.5, 100])
    S["clvb"] = pd.cut(S["clv"], [-0.01, 0.33, 0.66, 1.01])
    out["signal x1 by vr x clv"] = S.groupby(["vrb", "clvb"])["x1"].agg(["count", "mean"]).unstack()
    # down day, prior-decline, no high vol vs high vol (condition check for vr)
    dn = B[(B["ret1"] < 0) & (B["ret20"] < 0)].copy()
    dn["hv"] = dn["vr"] > 1.5
    dn["sig"] = dn["forecast"] > 0
    out["down+decline by hv,sig"] = dn.groupby(["hv", "sig"])["x1"].agg(["count", "mean"])
    # simulated book variants: 1-day hold, size by alloc, fee 0.19% per round trip
    def sim(mask, name):
        X = B.copy()
        X["p"] = np.where(mask(X), X["al"].where(X["al"] > 0, 0).clip(lower=0), 0)
        X["p"] = np.where(mask(X) & (X["al"] <= 0), 1.0, X["p"])
        X["p"] = np.where(mask(X), np.minimum(X["p"], 2), 0)
        X["dp"] = X.groupby(["coin", "wn"])["p"].diff().abs().fillna(X["p"])
        X["g"] = X["p"] * X["r1"] - X["dp"] * 0.00095
        bk = X.dropna(subset=["r1"]).groupby(["wn", "day"])["g"].mean().reset_index().sort_values(["wn", "day"])
        r = bk["g"]
        v = (1 + r).cumprod(); dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(r)) - 1
        return pd.Series({"sharpe": r.mean() / r.std() * np.sqrt(365), "yearly": yr, "maxdd": dd,
                          "calmar": yr / -dd, "days in": (X["p"] > 0).mean()}, name=name)
    out["sim books"] = pd.DataFrame([
        sim(lambda X: X["forecast"] > 0, "all signal 1d"),
        sim(lambda X: (X["forecast"] > 0) & (X["vr"] > 1.5), "vr>1.5 1d"),
        sim(lambda X: (X["forecast"] >= 15), "fc>=15 1d"),
        sim(lambda X: (X["forecast"] > 0) & (X["vr"] > 1.5) & (X["ret20"] < -0.15), "vr>1.5 & r20<-15%"),
    ])
    return out
