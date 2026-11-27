def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            hi = c.rolling(20, min_periods=20).max()
            sd = r.rolling(20, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "day": ts.dt.floor("D"), "r": r,
                               "depth": (c / hi - 1) / sd, "nxt": c.shift(-1) / c - 1,
                               "nxt2": c.shift(-2) / c - 1,
                               "clpos": (b["close"] - b["low"]) / (b["high"] - b["low"]),
                               "rz": r / sd, "r60": c / c.shift(60) - 1,
                               "choppy": b["regime"] != "chop", "yr": ts.dt.year,
                               "pos": b["postRebalance_current_allocation"],
                               "bv": b["postRebalance_total_value"]})
            df["idx"] = np.arange(len(df))
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["nxt", "r", "depth"])
    d["ex"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d["up"] = d["r"] > 0

    def dayt(g, col="ex"):
        g = g.dropna(subset=[col])
        if len(g) < 5:
            return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean%": np.nan, "t_day": np.nan})
        m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean%": 100 * m, "t_day": m / se})

    out = {}
    ch = d[d.choppy].copy()
    nc = d[~d.choppy].copy()
    # choppy: close position terciles, by up/down
    ch["clt"] = pd.qcut(ch["clpos"].rank(method="first"), 3, labels=False)
    out["choppy close-pos tercile x up"] = ch.groupby(["up", "clt"]).apply(dayt)
    ch["rzt"] = pd.qcut(ch["rz"].rank(method="first"), 3, labels=False)
    out["choppy day-move tercile by year"] = ch.groupby(["yr", "rzt"]).apply(dayt)
    out["choppy close-pos tercile by year"] = ch.groupby(["yr", "clt"]).apply(dayt)
    # graded slopes: regression of ex on clpos and rz in choppy, per coin
    res = {}
    for name, g in [("choppy", ch), ("nonchoppy", nc)]:
        for col in ["clpos", "rz"]:
            gg = g[[col, "ex"]].dropna()
            sl = stats.linregress(gg[col], gg["ex"])
            res[(name, col)] = {"slope%": 100 * sl.slope, "t": sl.slope / sl.stderr, "n": len(gg)}
    out["slopes"] = pd.DataFrame(res).T
    cc = {}
    for coin, g in ch.groupby("coin"):
        gg = g[["clpos", "rz", "ex"]].dropna()
        cc[coin] = {"rho_clpos": stats.spearmanr(gg.clpos, gg.ex)[0], "rho_rz": stats.spearmanr(gg.rz, gg.ex)[0], "n": len(gg)}
    out["choppy per coin"] = pd.DataFrame(cc).T
    # nonchoppy up days deep below high: split by trend sign (r60 where available)
    nu = nc[nc.up].copy()
    nu["dt"] = pd.qcut(nu["depth"].rank(method="first"), 3, labels=False)
    nu["trend"] = np.where(nu["r60"].isna(), "na", np.where(nu["r60"] > 0, "rising", "falling"))
    out["nonchoppy up-day depth tercile x trend"] = nu.groupby(["trend", "dt"]).apply(dayt)
    out["nonchoppy up-day depth tercile by year"] = nu.groupby(["yr", "dt"]).apply(dayt)
    # choppy up days deep
    cu = ch[ch.up].copy()
    cu["dt"] = pd.qcut(cu["depth"].rank(method="first"), 3, labels=False)
    out["choppy up-day depth tercile"] = cu.groupby("dt").apply(dayt)
    out["choppy up-day depth tercile 2d"] = cu.assign(ex2=cu["nxt2"] - cu.groupby("coin")["nxt2"].transform("mean")).groupby("dt").apply(lambda g: dayt(g, "ex2"))
    # book: days in position, largest gains/losses context
    pos = d[d.pos.abs() > 0]
    pos = pos.assign(g=pos.pos * pos.nxt)
    pos["gq"] = pd.qcut(pos["g"].rank(method="first"), 5, labels=False)
    out["book bars by gain quintile: context"] = pos.groupby("gq")[["rz", "clpos", "depth", "g"]].mean()
    return out
