def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            rng = h - l
            sd30 = r.rolling(30, min_periods=30).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "nxt": c.shift(-1) / c - 1,
                "nxt2": c.shift(-2) / c.shift(-1) - 1,
                "loc": (c - l) / rng.replace(0, np.nan),
                "wid": rng / rng.rolling(30, min_periods=30).mean(),
                "rstd": (rng / c) / sd30,
                "tr60": c / c.shift(60) - 1,
                "agi": sd30 / sd30.expanding(min_periods=20).median(),
                "inprof": b["regime"].astype(str) != "chop",
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].transform("mean")
    d["unx"] = d["nxt"] - drift
    d["unx2"] = d["nxt2"] - drift
    d["day"] = d["ts"].dt.floor("D")
    d["year"] = d["ts"].dt.year

    def ct(x, days):
        x = pd.Series(x).dropna(); days = days.loc[x.index]
        n = len(x)
        if n < 5: return pd.Series({"n": n, "days": days.nunique(), "mean%": np.nan, "t": np.nan})
        m = x.mean(); rd = (x - m).groupby(days).sum(); D = len(rd)
        se = np.sqrt((rd ** 2).sum() * D / max(D - 1, 1)) / n
        return pd.Series({"n": n, "days": D, "mean%": 100 * m, "t": m / se if se > 0 else np.nan})

    out = {}
    v = d.dropna(subset=["unx", "loc", "wid", "tr60"])
    fall = v[v["tr60"] < -0.1]
    fw = fall[fall["wid"] >= 1]
    # high close (loc>=0.5) in falling wide: signed short
    hc = fw[fw["loc"] >= 0.5].copy()
    hc["s"] = -hc["unx"]
    out["fall wide upper-half close, short-signed unx"] = ct(hc["s"], hc["day"])
    out["same, next-next day"] = ct(-hc["unx2"], hc["day"])
    hc["aq"] = pd.qcut(hc["agi"], 2, labels=["calmer", "agitated"])
    out["fall wide upper close by agitation proxy"] = hc.groupby("aq", observed=True).apply(lambda g: ct(g["s"], g["day"]))
    hc["wq"] = pd.qcut(hc["rstd"], 3, labels=False, duplicates="drop")
    out["fall wide upper close by rstd tercile"] = hc.groupby("wq").apply(lambda g: ct(g["s"], g["day"]))
    hc["lq"] = pd.cut(hc["loc"], [0.49, .7, .85, 1.01], labels=False)
    out["fall wide upper close by loc"] = hc.groupby("lq").apply(lambda g: ct(g["s"], g["day"]))
    out["fall wide upper close by year"] = hc.groupby("year").apply(lambda g: ct(g["s"], g["day"]))
    out["fall wide upper close by coin"] = hc.groupby("coin").apply(lambda g: ct(g["s"], g["day"]))
    # graded score across all falling days: score = (loc-0.5)*rstd
    fall = fall.dropna(subset=["rstd"]).copy()
    fall["score"] = (fall["loc"] - 0.5) * fall["rstd"]
    fall["sq"] = pd.qcut(fall["score"], 5, labels=False)
    out["falling all days: unx by score quintile"] = fall.groupby("sq").apply(lambda g: ct(g["unx"], g["day"]))
    rho, p = stats.spearmanr(fall["score"], fall["unx"])
    out["falling: spearman score vs unx"] = f"rho {rho:.4f} p {p:.4f} n {len(fall)}"
    # rising: same score
    rise = v[(v["tr60"] > 0.1)].dropna(subset=["rstd"]).copy()
    rise["score"] = (rise["loc"] - 0.5) * rise["rstd"]
    rise["sq"] = pd.qcut(rise["score"], 5, labels=False)
    out["rising all days: unx by score quintile"] = rise.groupby("sq").apply(lambda g: ct(g["unx"], g["day"]))
    # all profiles wide low close by year
    wl = v[(v["wid"] >= 1) & (v["loc"] < 0.25)]
    out["all wide low close by year"] = wl.groupby("year").apply(lambda g: ct(g["unx"], g["day"]))
    return out
