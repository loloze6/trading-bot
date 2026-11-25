def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            sd = r.rolling(30).std()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r": r, "z": r / sd, "sd": sd,
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "tr60": c / c.shift(60) - 1,
                "r5p": c.shift(1) / c.shift(6) - 1,
                "clv": (c - b["low"]) / (b["high"] - b["low"]),
                "rng": (b["high"] - b["low"]) / c.shift(1),
                "fc": b["forecast"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    for h in ["f1", "f2", "f3"]:
        m = D.groupby("coin")[h].mean()
        D["x" + h] = D[h] - D["coin"].map(m)

    def ct(s, days):
        s = pd.Series(s.values, index=days.values).dropna()
        n = len(s)
        if n < 5:
            return pd.Series({"n": n, "mean%": np.nan, "t": np.nan, "days": 0})
        dev = (s - s.mean()).groupby(level=0).sum()
        D_ = len(dev)
        se = np.sqrt(D_ / (D_ - 1) * (dev ** 2).sum()) / n
        return pd.Series({"n": n, "mean%": 100 * s.mean(), "t": s.mean() / se, "days": D_})

    def tab(df, by, col="xf1"):
        return df.groupby(by, observed=True).apply(lambda g: ct(g[col], g["day"]))

    out = {}
    D["zb"] = pd.cut(D["z"], [-99, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3, 99])
    out["next1d_by_z"] = tab(D, "zb")
    out["next2d_by_z"] = tab(D, "zb", "xf2")
    out["next3d_by_z"] = tab(D, "zb", "xf3")
    F = D[D["z"] <= -1].copy()
    F["clvb"] = pd.cut(F["clv"], [-0.01, 0.15, 0.35, 0.6, 1.01])
    out["falls_by_closeloc"] = tab(F, "clvb")
    F["trb"] = pd.cut(F["tr60"], [-9, -0.1, 0.1, 99])
    out["falls_by_trend60"] = tab(F, "trb")
    F["r5b"] = pd.qcut(F["r5p"], 3)
    out["falls_by_prior5d"] = tab(F, "r5b")
    F["sdb"] = pd.qcut(F["sd"] / F["coin"].map(D.groupby("coin")["sd"].median()), 3)
    out["falls_by_swinglevel"] = tab(F, "sdb")
    out["falls_by_weekday"] = tab(F, F["ts"].dt.weekday)
    out["falls_by_coin"] = tab(F, "coin")
    out["falls_by_window"] = tab(F, "win")
    # all days by weekday
    out["all_by_weekday"] = tab(D, D["ts"].dt.weekday)
    # rises
    U = D[D["z"] >= 1].copy()
    U["clvb"] = pd.cut(U["clv"], [-0.01, 0.4, 0.65, 0.85, 1.01])
    out["rises_by_closeloc"] = tab(U, "clvb")
    # all days by close location
    D["clvb"] = pd.cut(D["clv"], [-0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 1.01])
    out["all_by_closeloc"] = tab(D, "clvb")
    return out
