def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            r = c.pct_change()
            s30 = r.rolling(30, min_periods=20).std()
            pos = np.where(h > l, 2 * (c - (h + l) / 2) / (h - l), 0.0)
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "inprof": (b["regime"] == "unknown").astype(int),
                "pos": pos, "rngv": ((h - l) / c) / s30, "r0": r / s30,
                "ret60": c / c.shift(60) - 1,
                "vol_rel": s30 / r.rolling(120, min_periods=60).std(),
                "nxt": c.shift(-1) / c - 1,
                "nxt2": c.shift(-2) / c - 1,
            })
            df["s30"] = s30
            df["prod"] = df["pos"] * df["rngv"]
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - drift
    d["ex2"] = d["nxt2"] - 2 * drift
    d = d.dropna(subset=["ex", "prod", "s30", "ret60", "vol_rel"])
    d["trend"] = pd.cut(d["ret60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    d["agit"] = np.where(d["vol_rel"] > 1, "agit", "calm")
    d["day"] = d["ts"].dt.floor("D")
    out = {}

    def daytstat(g, col="ex"):
        g = g.dropna(subset=[col])
        if len(g) < 10: return pd.Series({"n": len(g), "days": np.nan, "mean%": np.nan, "t_day": np.nan})
        s = g.groupby("day")[col].sum(); n = len(g); m = g[col].mean()
        se = np.sqrt(((s - g.groupby("day")[col].count() * m) ** 2).sum()) / n
        return pd.Series({"n": n, "days": len(s), "mean%": 100 * m, "t_day": m / se})

    # high-close side only: graded by prod, by approx profile
    hc = d[d["pos"] > 0].copy()
    hc["hq"] = hc.groupby(["trend", "agit"])["prod"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["highclose next-day ex by profile x prod tercile"] = hc.groupby(["trend", "agit", "hq"]).apply(daytstat)
    lc = d[d["pos"] < 0].copy()
    lc["lq"] = lc.groupby(["trend", "agit"])["prod"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["lowclose next-day ex by profile x prod tercile"] = lc.groupby(["trend", "agit", "lq"]).apply(daytstat)

    # calm relative vol: next-day ex by trend within lowest vol_rel quintile
    d["vq"] = pd.qcut(d["vol_rel"], 5, labels=False, duplicates="drop")
    out["next-day ex, vol_rel quintile x trend"] = d.groupby(["vq", "trend"]).apply(daytstat)

    # big down day in usual moves, by profile (held? check where it lives)
    d["big"] = pd.qcut(d["r0"], 7, labels=False)
    out["biggest-down septile next-day ex by profile"] = d[d["big"] == 0].groupby(["trend", "agit"]).apply(daytstat)
    out["biggest-up septile next-day ex by profile"] = d[d["big"] == 6].groupby(["trend", "agit"]).apply(daytstat)
    # graded short: correlation of r0 with next-day exz among up days by profile
    up = d[d["r0"] > 0]
    def corr(g):
        if len(g) < 30: return pd.Series({"n": len(g), "corr": np.nan, "t": np.nan})
        rr = stats.spearmanr(g["r0"], g["ex"] / g["s30"])[0]
        return pd.Series({"n": len(g), "corr": rr, "t": rr * np.sqrt((len(g) - 2) / (1 - rr ** 2))})
    out["up days: rank corr of size with next-day ex, by profile"] = up.groupby(["trend", "agit"]).apply(corr)
    return out
