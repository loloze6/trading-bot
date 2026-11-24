def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            hi20 = hi.shift(1).rolling(20).max(); lo20 = lo.shift(1).rolling(20).min()
            hi60 = hi.shift(1).rolling(60).max()
            vol20 = r1.rolling(20).std()
            vol30 = r1.rolling(30).std(); vmed = vol30.rolling(365, min_periods=120).median()
            df = pd.DataFrame({"coin": coin, "win": w, "i": np.arange(n), "cell": np.arange(n) // H,
                               "day": ts.dt.floor("D"),
                               "fwd": c.shift(-H) / c - 1, "fwd10": c.shift(-10) / c - 1,
                               "dhi": c / hi20 - 1, "dhi60": c / hi60 - 1, "vol20": vol20,
                               "tr60": (c / c.shift(60) - 1) * 100, "tr20": c / c.shift(20) - 1,
                               "rng": (hi20 - lo20) / c, "agit": vol30 > vmed, "vmedna": vmed.isna(),
                               "nbrk": (c > hi20).astype(int).rolling(10).sum()})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    grid = A[(A["i"] % H == 0) & A["fwd"].notna()]
    drift = grid.groupby("coin")["fwd"].mean(); sd = grid.groupby("coin")["fwd"].std()
    A["un"] = A["fwd"] - A["coin"].map(drift)
    A["str"] = A["un"] / A["coin"].map(sd)
    def ct(x, col="un"):
        x = x.dropna(subset=[col])
        if len(x) < 3: return pd.Series({"n": len(x), "days": 0, "mean": np.nan, "t_day": np.nan, "strength": np.nan})
        m = x[col].mean(); dev = (x[col] - m).groupby(x["day"]).sum(); G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "days": G, "mean": m, "t_day": m / se, "strength": x["str"].mean()})
    out = {}
    up = A[(A["dhi"] > 0) & A["fwd"].notna()].sort_values("i").groupby(["coin", "win", "cell"]).head(1).copy()
    def slope(x, y):
        m = x.notna() & y.notna()
        r = stats.linregress(x[m], y[m]); return pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": m.sum()})
    out["up_slope_tr60"] = slope(up["tr60"], up["un"])
    out["up_slope_tr20"] = slope(up["tr20"], up["un"])
    out["up_slope_dhi60"] = slope(up["dhi60"], up["un"])
    out["up_slope_rng"] = slope(up["rng"], up["un"])
    out["up_slope_nbrk"] = slope(up["nbrk"], up["un"])
    up["tq"] = pd.qcut(up["tr60"], 4, labels=False, duplicates="drop")
    out["up_by_tr60_q"] = up.groupby("tq").apply(ct)
    up["rq"] = pd.qcut(up["rng"], 4, labels=False, duplicates="drop")
    out["up_by_range_width_q"] = up.groupby("rq").apply(ct)
    up["nq"] = up["nbrk"].clip(upper=4)
    out["up_by_breaks_last10d"] = up.groupby("nq").apply(ct)
    up["agit_l"] = np.where(up["vmedna"], "na", np.where(up["agit"], "agitated", "calm"))
    out["up_by_agitation"] = up.groupby("agit_l").apply(ct)
    # 60-day high break
    u60 = A[(A["dhi60"] > 0) & A["fwd"].notna()].sort_values("i").groupby(["coin", "win", "cell"]).head(1)
    out["up60_break_all"] = ct(u60)
    # 10-day horizon for up 20d breaks
    d10 = A[(A["i"] % 10 == 0) & A["fwd10"].notna()].groupby("coin")["fwd10"].mean()
    A["un10"] = A["fwd10"] - A["coin"].map(d10)
    up10 = A[(A["dhi"] > 0) & A["fwd10"].notna()].assign(c10=lambda x: x["i"] // 10).sort_values("i").groupby(["coin", "win", "c10"]).head(1)
    out["up_break_10d"] = ct(up10, "un10")
    return out
