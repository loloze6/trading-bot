def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            h, l, c = b["high"], b["low"], b["close"]
            rng = (h - l)
            mr = rng.shift(1).rolling(20, min_periods=20).mean()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "clv": (2*c - h - l) / rng.replace(0, np.nan),
                "rm": rng / mr,
                "r0": c.pct_change(),
                "r1": c.shift(-1)/c - 1,
                "r2": c.shift(-2)/c - 1,
                "r3": c.shift(-3)/c - 1,
                "ret20": c/c.shift(20) - 1,
                "vol20": c.pct_change().rolling(20, min_periods=20).std(),
                "pos_i": np.arange(len(b)),
            })
            d.loc[mr.isna(), "rm"] = np.nan
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in ["r1", "r2", "r3"]:
        D[k + "x"] = D[k] - D.groupby("coin")[k].transform("mean")
    D["z0"] = D["r0"] / D["vol20"]
    D["z20"] = D["ret20"] / (D["vol20"] * np.sqrt(20))

    def tday(df, col):
        df2 = df.dropna(subset=[col])
        if len(df2) < 10: return (np.nan, np.nan, 0)
        m = df2[col].mean()
        dev = (df2[col] - m).groupby(df2["day"]).sum()
        se = np.sqrt((dev**2).sum()) / len(df2)
        return (m, m/se, len(df2))
    def slope(df, x, y):
        df2 = df.dropna(subset=[x, y])
        X = df2[x] - df2[x].mean(); Y = df2[y]
        b = (X*Y).sum() / (X*X).sum()
        e = Y - Y.mean() - b*X
        s = (X*e).groupby(df2["day"]).sum()
        se = np.sqrt((s**2).sum()) / (X*X).sum()
        return (b, b/se, len(df2))
    out = {}
    L = D[(D["rm"] > 1) & (D["clv"] < 0)]
    S = D[(D["rm"] > 1) & (D["clv"] > 0)]
    # graded within the low-close wide side
    res = []
    for name, x in [("-clv", None), ("rm", "rm"), ("-z20", None), ("-z0", None)]:
        g = L.copy(); g["mclv"] = -g["clv"]; g["mz20"] = -g["z20"]; g["mz0"] = -g["z0"]
        col = {"-clv": "mclv", "rm": "rm", "-z20": "mz20", "-z0": "mz0"}[name]
        b, t, n = slope(g, col, "r1x"); res.append([name, b, t, n])
    out["low-close wide: slope of r1x on"] = pd.DataFrame(res, columns=["x", "slope", "t", "n"])
    # low-close wide by z20 tercile (depth of 20d fall, in vol units)
    L2 = L.dropna(subset=["z20"]).copy()
    L2["z20q"] = pd.qcut(L2["z20"], 4, labels=False)
    res = []
    for q, g in L2.groupby("z20q"):
        m, t, n = tday(g, "r1x"); res.append([q, g["z20"].median(), m, t, n])
    out["low-close wide r1x by z20 quartile"] = pd.DataFrame(res, columns=["q", "z20_med", "mean", "t", "n"])
    # all days: graded by -z20 * width * low close? product signal
    A = D.dropna(subset=["z20", "rm", "clv", "r1x"]).copy()
    A["sig"] = np.clip(-A["z20"], 0, None) * np.clip(-A["clv"], 0, None) * A["rm"]
    out["all days slope r1x on sig"] = pd.Series(slope(A[A["sig"] > 0], "sig", "r1x"), index=["slope", "t", "n"])
    # multi-day for low-close wide in falling context, non-overlapping grid
    res = []
    for hz in [1, 2, 3]:
        g = D[(D["pos_i"] % hz == 0) & (D["rm"] > 1) & (D["clv"] < 0)]
        for nm, msk in [("ret20<0", g["ret20"] < 0), ("ret20>0", g["ret20"] > 0)]:
            m, t, n = tday(g[msk], f"r{hz}x"); res.append([nm, hz, m, t, n])
    out["low-close wide multi-day"] = pd.DataFrame(res, columns=["ctx", "h", "mean", "t", "n"])
    # by window consistency
    res = []
    for w, g in L[L["ret20"] < 0].groupby("win"):
        m, t, n = tday(g, "r1x"); res.append([w, m, t, n])
    out["low-close wide falling by window"] = pd.DataFrame(res, columns=["win", "mean", "t", "n"])
    res = []
    for cn, g in L[L["ret20"] < 0].groupby("coin"):
        m, t, n = tday(g, "r1x"); res.append([cn, m, t, n])
    out["low-close wide falling by coin"] = pd.DataFrame(res, columns=["coin", "mean", "t", "n"])
    # high-close wide in rising context: short side
    res = []
    for nm, msk in [("ret20>0", S["ret20"] > 0), ("ret20<0", S["ret20"] < 0)]:
        g = S[msk].copy(); g["sx"] = -g["r1x"]
        m, t, n = tday(g, "sx"); res.append([nm, m, t, n])
    out["high-close wide short gain"] = pd.DataFrame(res, columns=["ctx", "mean", "t", "n"])
    # non-wide low close in falling context (does width matter?)
    N = D[(D["rm"] <= 1) & (D["clv"] < 0) & (D["ret20"] < 0)]
    out["low-close NOT wide falling"] = pd.Series(tday(N, "r1x"), index=["mean", "t", "n"])
    return out
