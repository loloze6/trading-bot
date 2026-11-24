def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coin = list(data["bars"].keys())[0]
    rows = []
    for w, b in data["bars"][coin].items():
        b = b.sort_values("timestamp").reset_index(drop=True)
        c = b["close"].astype(float)
        r = c.pct_change()
        vol = r.rolling(30, min_periods=20).std().shift(1)
        hl = (b["high"] - b["low"]).replace(0, np.nan)
        df = pd.DataFrame({
            "w": w, "pos_i": np.arange(len(b)), "r": r, "z": r / vol, "vol": vol,
            "f1": c.shift(-1) / c - 1,
            "r60": c / c.shift(60) - 1, "r20": c / c.shift(20) - 1,
            "clv": (2 * b["close"] - b["high"] - b["low"]) / hl,
            "rz": (b["high"] - b["low"]) / b["close"] / vol,
            "alloc": b["postRebalance_current_allocation"].astype(float),
            "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            "yr": pd.to_datetime(b["timestamp"]).dt.year,
        })
        df["vol_rank"] = vol / vol.rolling(180, min_periods=60).median()
        df["vol5"] = r.rolling(5).std()
        df["vratio"] = df["vol5"] / vol
        rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d["f1"].mean()
    dd = d.dropna(subset=["z", "f1"]).copy()

    def reg(s, x):
        s = s.dropna(subset=[x, "f1"])
        sl = stats.linregress(s[x], s["f1"])
        return sl.slope, sl.slope / sl.stderr, len(s)

    # relative vol: finer, and its stability by half
    dv = dd.dropna(subset=["vol_rank"]).copy()
    dv["vr"] = pd.qcut(dv["vol_rank"], 5, labels=False)
    res = []
    for k, s in dv.groupby("vr"):
        a, t, n = reg(s, "z")
        res.append({"vr": k, "n": n, "vol_rank": s["vol_rank"].mean(), "slope": a, "t": t})
    out["z_slope_by_relvol_quintile"] = pd.DataFrame(res)
    dv["half"] = (dv["yr"] >= 2022).astype(int)
    dv["hi"] = (dv["vr"] >= 3).astype(int)
    res = []
    for (h, hi), s in dv.groupby(["half", "hi"]):
        a, t, n = reg(s, "z"); res.append({"half": h, "hi_relvol": hi, "n": n, "slope": a, "t": t})
    out["z_slope_relvol_by_half"] = pd.DataFrame(res)
    # interaction regression z * vol_rank
    dv["zx"] = dv["z"] * dv["vol_rank"]
    X = np.column_stack([np.ones(len(dv)), dv["z"], dv["vol_rank"], dv["zx"]])
    y = dv["f1"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    s2 = resid.var(ddof=4); cov = s2 * np.linalg.inv(X.T @ X)
    out["interaction_z_relvol"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["c", "z", "vr", "z*vr"])
    # short-term vol ratio (5d / 30d)
    dq = dd.dropna(subset=["vratio"]).copy()
    dq["b"] = pd.qcut(dq["vratio"], 3, labels=False)
    res = []
    for k, s in dq.groupby("b"):
        a, t, n = reg(s, "z"); res.append({"b": k, "n": n, "vratio": s["vratio"].mean(), "slope": a, "t": t})
    out["z_slope_by_vol5_over_vol30"] = pd.DataFrame(res)
    # close location value
    a, t, n = reg(dd, "clv"); out["clv_slope_all"] = pd.Series({"slope": a, "t": t, "n": n})
    dd["clvb"] = pd.qcut(dd["clv"], 5, labels=False, duplicates="drop")
    g = dd.groupby("clvb")["f1"].agg(["count", "mean", "std"]); g["t"] = g["mean"] / g["std"] * np.sqrt(g["count"])
    out["f1_by_clv_quintile"] = g
    # clv controlling for z
    s = dd.dropna(subset=["clv"])
    X = np.column_stack([np.ones(len(s)), s["z"], s["clv"], s["rz"]]); y = s["f1"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None); resid = y - X @ beta
    cov = resid.var(ddof=4) * np.linalg.inv(X.T @ X)
    out["multi_z_clv_rangez"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["c", "z", "clv", "rangez"])
    # trend regime: reversal on falls by r60 sign
    res = []
    for side, s0 in [("fall", dd[dd["z"] < 0]), ("rise", dd[dd["z"] > 0])]:
        for k, s in s0.dropna(subset=["r60"]).groupby(np.sign(s0["r60"].dropna())):
            a, t, n = reg(s, "z"); res.append({"side": side, "r60_sign": k, "n": n, "slope": a, "t": t})
    out["side_slope_by_r60_sign"] = pd.DataFrame(res)
    # weekday of next-day return by year half
    dd["half"] = (dd["yr"] >= 2022).astype(int)
    g = dd.groupby(["half", "wd"])["f1"].agg(["count", "mean", "std"]); g["t"] = g["mean"] / g["std"] * np.sqrt(g["count"])
    out["f1_by_weekday_half"] = g
    # book daily returns: drawdown profile
    br = []
    for w, dy in data["days"][coin].items():
        x = dy["book_return"].dropna(); br.append(pd.DataFrame({"w": w, "br": x.values}))
    br = pd.concat(br)
    out["book_by_window"] = br.groupby("w")["br"].agg(["count", "mean", "sum"]).sort_values("sum").head(8)
    return out
