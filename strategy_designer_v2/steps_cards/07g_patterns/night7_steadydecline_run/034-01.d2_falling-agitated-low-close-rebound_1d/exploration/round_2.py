def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                              "cl": (h - c) / rng, "r0": c / c.shift(1) - 1,
                              "r1": c.shift(-1) / c - 1, "r2": c.shift(-2) / c - 1,
                              "inprof": (b["regime"] == "unknown").astype(int),
                              "alloc": b["postRebalance_current_allocation"].astype(float)})
            lr = np.log(c).diff()
            d["vol30"] = lr.rolling(30, min_periods=20).std()
            d["volrel"] = d["vol30"] / d["vol30"].rolling(120, min_periods=40).median()
            d["ret60"] = c / c.shift(60) - 1
            d["g1"] = d["alloc"] * d["r1"]
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    df["x1"] = df["r1"] - df.groupby("coin")["r1"].transform("mean")
    df["x2"] = df["r2"] - df.groupby("coin")["r2"].transform("mean")
    df["day"] = df["ts"].dt.floor("D")
    df["agit"] = (df["volrel"] > 1).astype(int)
    df["trend"] = np.select([df["ret60"] > 0.1, df["ret60"] < -0.1], ["rise", "fall"], "chop")
    df.loc[df["ret60"].isna(), "trend"] = np.nan
    df["year"] = df["ts"].dt.year
    out = {}
    def slope_t(s, col="x1", sig="cl"):
        s = s.dropna(subset=[col, sig]).copy()
        s["p"] = (s[sig] - 0.5) * s[col]
        dm = s.groupby("day")["p"].sum()
        return len(s), len(dm), (dm.mean() / (dm.std() / np.sqrt(len(dm))) if len(dm) > 2 else np.nan), s[[sig, col]].corr().iloc[0, 1]
    res = []
    for key in ["win", "coin", "year"]:
        for k, s in df[(df.agit == 1) & (df.trend == "fall")].groupby(key):
            n, nd, t, cr = slope_t(s)
            res.append({"by": key, "k": str(k), "n": n, "days": nd, "corr": cr, "t": t})
    out["fallagit_by"] = pd.DataFrame(res)
    res = []
    for (tr, ag), s in df.dropna(subset=["trend"]).groupby(["trend", "agit"]):
        n, nd, t, cr = slope_t(s, "x2")
        res.append({"trend": tr, "agit": ag, "n": n, "corr_x2": cr, "t_x2": t})
    out["h2"] = pd.DataFrame(res)
    # volrel graded within falling
    fa = df[df.trend == "fall"].dropna(subset=["volrel"]).copy()
    fa["vb"] = pd.qcut(fa["volrel"], 4, labels=False)
    res = []
    for k, s in fa.groupby("vb"):
        n, nd, t, cr = slope_t(s)
        res.append({"vb": k, "volrel_med": s.volrel.median(), "n": n, "corr": cr, "t": t})
    out["fall_by_volq"] = pd.DataFrame(res)
    # side split inside falling agitated: low half vs high half
    s = df[(df.agit == 1) & (df.trend == "fall")].dropna(subset=["x1", "cl"])
    for nm, ss in [("low_close_cl>0.5", s[s.cl > 0.5]), ("high_close_cl<=0.5", s[s.cl <= 0.5])]:
        dm = ss.groupby("day")["x1"].mean()
        out["side_" + nm] = pd.Series({"n": len(ss), "days": len(dm), "mean_x1_pct": 100 * ss.x1.mean(),
                                         "t": dm.mean() / (dm.std() / np.sqrt(len(dm)))})
    # close location vs day return in falling agitated: which carries it
    s = s.dropna(subset=["r0"]).copy()
    s["r0z"] = s.groupby("coin")["r0"].transform(lambda v: (v - v.mean()) / v.std())
    X = np.column_stack([np.ones(len(s)), s["cl"] - 0.5, s["r0z"]])
    beta, *_ = np.linalg.lstsq(X, s["x1"].values, rcond=None)
    resid = s["x1"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * resid.var(ddof=3)
    out["ols_cl_r0"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["c", "cl", "r0z"])
    # book in profile by side
    ip = df[df.inprof == 1].dropna(subset=["g1"])
    out["book_inprof_side"] = ip.groupby(np.sign(ip["alloc"]))["g1"].agg(["count", "mean", "sum"])
    return out
