def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=30).std()
            hl = (b["high"] - b["low"]).replace(0, np.nan)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "inprof": (b["regime"] == "unknown").values,
                               "z1": r1 / sd30,
                               "zprev5": (c.shift(1) / c.shift(6) - 1) / (sd30 * np.sqrt(5)),
                               "r20": c / c.shift(20) - 1,
                               "sdrat": sd30 / r1.rolling(10, min_periods=10).std(),
                               "clo": (c - b["low"]) / hl,
                               "uwick": (b["high"] - c) / c / sd30,
                               "f1": c.shift(-1) / c - 1,
                               "a": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift1 = d["f1"].mean()
    p = d[d.inprof].dropna(subset=["z1", "f1"]).copy()
    p["u1"] = p.f1 - drift1
    up = p[p.z1 > 0].copy()
    out = {}

    def clslope(s, x, y):
        s = s.dropna(subset=[x, y])
        X = s[x] - s[x].mean(); Y = s[y]
        b1 = (X * (Y - Y.mean())).sum() / (X ** 2).sum()
        e = Y - Y.mean() - b1 * X
        g = (X * e).groupby(s["day"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / (X ** 2).sum()
        return pd.Series({"slope": b1, "t_cl": b1 / se, "n": len(s), "days": G})

    def clmean(s, y):
        g = (s[y] - s[y].mean()).groupby(s["day"]).sum(); G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"n": len(s), "mean": s[y].mean(), "t_cl": s[y].mean() / se, "days": G})

    for x in ["z1", "zprev5", "r20", "sdrat", "clo", "uwick"]:
        out["up_slope_" + x] = clslope(up, x, "u1")
    out["all_slope_z1_clustered"] = clslope(p.assign(z1=p.z1.clip(-4, 4)), "z1", "u1")
    # up days: prior 5-day move bins
    up["pb"] = pd.cut(up.zprev5, [-99, -1, 0, 1, 99])
    out["up_by_prev5"] = up.groupby("pb", observed=True)["u1"].agg(["count", "mean"]).round(4)
    up["rb"] = pd.qcut(up.r20, 3)
    out["up_by_r20_terciles"] = up.groupby("rb", observed=True)["u1"].agg(["count", "mean"]).round(4)
    # window consistency of up-day fade
    out["up_fade_by_window_t"] = up.groupby("w").apply(
        lambda s: pd.Series({"n": len(s), "mean": s.u1.mean()})).round(4)
    # book held short after up day: realised next-day gain
    out["short_held_next_day"] = clmean(p[p.a < 0], "u1")
    out["up_clustered"] = clmean(up, "u1")
    return out
