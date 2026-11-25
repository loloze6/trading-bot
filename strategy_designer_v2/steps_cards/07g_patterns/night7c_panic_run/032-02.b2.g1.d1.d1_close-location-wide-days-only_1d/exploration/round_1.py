def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            h, l, c, o = b["high"], b["low"], b["close"], b["open"]
            rng = (h - l)
            mr = rng.shift(1).rolling(20, min_periods=20).mean()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "clv": (2*c - h - l) / rng.replace(0, np.nan),
                "rm": rng / mr,
                "r0": c.pct_change(),
                "r1": c.shift(-1)/c - 1,
                "r3": c.shift(-3)/c - 1,
                "r5": c.shift(-5)/c - 1,
                "ret20": c/c.shift(20) - 1,
                "low20": (c <= c.rolling(20, min_periods=20).min()).astype(float),
                "high20": (c >= c.rolling(20, min_periods=20).max()).astype(float),
                "vol20": c.pct_change().rolling(20, min_periods=20).std(),
                "pos": b["postRebalance_current_allocation"],
                "pos_i": np.arange(len(b)),
            })
            d.loc[mr.isna(), "rm"] = np.nan
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in ["r1", "r3", "r5"]:
        D[k + "x"] = D[k] - D.groupby("coin")[k].transform("mean")
    D["z0"] = D["r0"] / D["vol20"]

    def tday(df, col):
        g = df.groupby("day")[col].sum()
        df2 = df.dropna(subset=[col])
        if len(df2) < 10: return (np.nan, np.nan, 0)
        g = df2.groupby("day")[col].sum()
        n = df2.groupby("day")[col].size()
        m = g.sum() / n.sum()
        dev = (df2[col] - m).groupby(df2["day"]).sum()
        se = np.sqrt((dev**2).sum()) / n.sum()
        return (m, m/se, len(df2))
    out = {}
    # close-location bins x wide
    D["wide"] = (D["rm"] > 1)
    D["clvb"] = pd.cut(D["clv"], [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01], labels=["vlow","low","mid","high","vhigh"])
    res = []
    for (wd, cb), g in D.dropna(subset=["clvb", "rm"]).groupby(["wide", "clvb"]):
        m, t, n = tday(g, "r1x"); res.append([wd, cb, m, t, n])
    out["r1x by wide x clv"] = pd.DataFrame(res, columns=["wide", "clv", "mean", "t", "n"])
    # rev signal by range multiple quintile
    D["rev"] = -np.sign(D["clv"]) * D["r1x"]
    D["rmq"] = pd.qcut(D["rm"], 5, labels=False)
    res = []
    for q, g in D.dropna(subset=["rmq"]).groupby("rmq"):
        m, t, n = tday(g, "rev"); res.append([q, g["rm"].median(), m, t, n])
    out["reversal by rm quintile"] = pd.DataFrame(res, columns=["q", "rm_med", "mean", "t", "n"])
    # multi-day: non-overlapping grids for 3 and 5
    res = []
    for hz in [3, 5]:
        g = D[(D["pos_i"] % hz == 0) & D["wide"]].copy()
        g["rv"] = -np.sign(g["clv"]) * g[f"r{hz}x"]
        m, t, n = tday(g, "rv"); res.append([hz, m, t, n])
    out["reversal wide multi-day"] = pd.DataFrame(res, columns=["h", "mean", "t", "n"])
    # brief: monthly low in volatile decline
    D["volq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    res = []
    for hz in [1, 3, 5]:
        g = D[(D["pos_i"] % hz == 0)]
        for name, msk in [("low20 hivol down", (g["low20"] == 1) & (g["volq"] == 2) & (g["ret20"] < 0)),
                          ("other hivol down", (g["low20"] == 0) & (g["volq"] == 2) & (g["ret20"] < 0)),
                          ("high20 hivol up", (g["high20"] == 1) & (g["volq"] == 2) & (g["ret20"] > 0)),
                          ("low20 all", g["low20"] == 1), ("high20 all", g["high20"] == 1)]:
            m, t, n = tday(g[msk], f"r{hz}x"); res.append([name, hz, m, t, n])
    out["breakouts"] = pd.DataFrame(res, columns=["case", "h", "mean", "t", "n"])
    # after large moves: z0 quintile
    D["zq"] = pd.qcut(D["z0"], 5, labels=False)
    res = []
    for q, g in D.dropna(subset=["zq"]).groupby("zq"):
        m, t, n = tday(g, "r1x"); res.append([q, g["z0"].median(), m, t, n])
    out["r1x by z0 quintile"] = pd.DataFrame(res, columns=["q", "z_med", "mean", "t", "n"])
    # weekday
    res = []
    for k, g in D.groupby("wd"):
        m, t, n = tday(g, "r1x"); m2, t2, n2 = tday(g[g["wide"]], "rev")
        res.append([k, m, t, m2, t2, n2])
    out["weekday r1x and wide reversal"] = pd.DataFrame(res, columns=["wd", "r1x", "t", "rev_wide", "t_rev", "n_wide"])
    # reversal by ret20 sign (trend context) and vol tercile on wide days
    res = []
    W = D[D["wide"]]
    for (s, v), g in W.dropna(subset=["volq", "ret20"]).groupby([np.sign(W["ret20"]), "volq"]):
        m, t, n = tday(g, "rev"); res.append([s, v, m, t, n])
    out["wide reversal by ret20 sign x vol"] = pd.DataFrame(res, columns=["ret20sign", "volq", "mean", "t", "n"])
    # long vs short wide: clv sign
    res = []
    for s, g in W.groupby(np.sign(W["clv"])):
        m, t, n = tday(g, "rev"); res.append([s, m, t, n])
    out["wide reversal by clv side"] = pd.DataFrame(res, columns=["clvsign", "mean", "t", "n"])
    # trades
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
