def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "regime": b["regime"], "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "cl": (h - c) / (h - l).replace(0, np.nan),
                "ret30": c / c.shift(30) - 1,
                "rng": (h - l) / c,
            })
            rec = b.get("debug_info.components.fall30.last_history_value")
            if rec is not None:
                df["ret30"] = rec.where(rec.notna(), df["ret30"])
            df["mbr"] = df["rng"].rolling(90).mean() / df["rng"].rolling(30).mean()
            for k in (1, 2, 3, 5):
                df[f"r{k}"] = c.shift(-k) / c - 1
            df["pos"] = np.arange(len(df))
            df["year"] = df["day"].dt.year
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)

    # each coin's normal drift: its mean return over all shown windows
    for k in (1, 2, 3, 5):
        d[f"x{k}"] = d[f"r{k}"] - d.groupby("coin")[f"r{k}"].transform("mean")

    def ct(s, days):
        s = s.dropna()
        days = days.loc[s.index]
        n = len(s)
        if n < 5:
            return (np.nan, np.nan, n)
        m = s.mean()
        S = (s - m).groupby(days).sum()
        se = np.sqrt((S ** 2).sum()) / n
        return (m, m / se, n)

    def tab(sub, key, col="x1"):
        out = {}
        for g, gg in sub.groupby(key, observed=True):
            m, t, n = ct(gg[col], gg["day"])
            out[g] = {"mean": m, "t": t, "n": n}
        return pd.DataFrame(out).T

    R = d[d["regime"] == "mean_reversion"].copy()
    R["cl_q"] = pd.qcut(R["cl"], 5, labels=False, duplicates="drop")
    R["f_q"] = pd.qcut(-R["ret30"], 3, labels=False, duplicates="drop")
    R["mbr_q"] = pd.qcut(R["mbr"], 3, labels=False, duplicates="drop")
    R["fc_q"] = pd.qcut(R["fc"].rank(method="first"), 3, labels=False)

    NR = d[d["regime"] != "mean_reversion"].copy()
    NR["cl_q"] = pd.qcut(NR["cl"], 5, labels=False, duplicates="drop")

    res = {}
    res["regime by close-location quintile (0=near high), next day excess"] = tab(R, "cl_q")
    res["regime by 30d fall tercile (2=deepest)"] = tab(R, "f_q")
    res["regime by mbr tercile (0=most widened)"] = tab(R, "mbr_q")
    res["regime by forecast tercile"] = tab(R, "fc_q")
    res["regime by coin"] = tab(R, "coin")
    res["regime by year"] = tab(R, "year")
    res["non-regime by close-location quintile"] = tab(NR, "cl_q")

    # horizons, non-overlapping grid on the top two close-location quintiles
    hz = {}
    for k in (1, 2, 3, 5):
        g = R[(R["pos"] % k == 0) & (R["cl_q"] >= 3)]
        m, t, n = ct(g[f"x{k}"], g["day"])
        hz[k] = {"mean": m, "t": t, "n": n}
    res["regime near-low closes (top 2 quintiles) by horizon"] = pd.DataFrame(hz).T

    # correlation of each graded input with next-day excess inside the regime
    res["corr cl,x1 regime"] = float(R[["cl", "x1"]].corr().iloc[0, 1])
    res["corr -ret30,x1 regime"] = float(pd.concat([-R["ret30"], R["x1"]], axis=1).corr().iloc[0, 1])
    return res
