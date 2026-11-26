def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            b["fwd"] = c.shift(-H) / c - 1
            b["r1"] = c / c.shift(1) - 1
            b["r20"] = c / c.shift(20) - 1
            b["tr60"] = c / c.shift(60) - 1
            b["vr"] = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            s30 = b["r1"].rolling(30).std()
            b["agit"] = s30.rolling(min(len(b), 365), min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            b["falling"] = b["regime"] == "unknown"
            b["grid"] = (np.arange(len(b)) % H == 0)
            b["coin"] = coin; b["win"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    g = B[B["grid"] & B["fwd"].notna()].copy()
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["trend"] = np.where(g["falling"], "falling", np.where(g["tr60"] > 0.10, "rising", "choppy"))
    g["ag"] = np.where(g["agit"] > 0.5, "agitated", np.where(g["agit"].notna(), "calm", "na"))

    def ct(s, col="ex"):
        s = s.dropna(subset=[col])
        if len(s) < 5: return (np.nan, np.nan, len(s))
        m = s[col].mean(); d = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((d ** 2).sum()) / len(s)
        return (m, m / se, len(s))

    def slope(s, x):
        s = s.dropna(subset=[x, "ex"])
        if len(s) < 20: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(s)})
        X = np.column_stack([np.ones(len(s)), s[x].values]); y = s["ex"].values
        beta = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, idx in s.groupby("day").indices.items():
            u = X[idx].T @ e[idx]; meat += np.outer(u, u)
        V = XtXi @ meat @ XtXi
        return pd.Series({"slope": beta[1], "t": beta[1] / np.sqrt(V[1, 1]), "n": len(s)})

    res = {}
    res["slope_ex_on_vr_by_profile"] = g.groupby(["trend", "ag"]).apply(lambda s: slope(s, "vr"))
    res["slope_ex_on_vr_by_trend"] = g.groupby("trend").apply(lambda s: slope(s, "vr"))
    res["slope_ex_on_vr_all"] = slope(g, "vr").to_frame().T
    out = {}
    for (tr, ag), s in g.groupby(["trend", "ag"]):
        s = s.dropna(subset=["vr"])
        if len(s) < 30: continue
        lo = s[s["vr"] <= s["vr"].quantile(0.33)]; hi = s[s["vr"] >= s["vr"].quantile(0.67)]
        m1, t1, n1 = ct(lo); m2, t2, n2 = ct(hi)
        out[f"{tr} {ag}"] = {"low_vr_mean": m1, "low_t": t1, "n_low": n1, "high_vr_mean": m2, "high_t": t2, "n_high": n2}
    res["tercile_lowvr_highvr_by_profile"] = pd.DataFrame(out).T
    r = g[g["trend"] == "rising"]
    res["rising_vr_slope_by_year"] = r.groupby("yr").apply(lambda s: slope(s, "vr"))
    res["rising_vr_slope_by_coin"] = r.groupby("coin").apply(lambda s: slope(s, "vr"))
    f = g[g["trend"] == "falling"]
    res["falling_vr_slope_by_year"] = f.groupby("yr").apply(lambda s: slope(s, "vr"))
    # rising + falling as 'trend continues': signed by trend direction
    tf = g[g["trend"] != "choppy"].copy()
    tf["sgn"] = np.where(tf["trend"] == "rising", 1, -1)
    tf["ex_dir"] = tf["ex"] * tf["sgn"]
    tf2 = tf.copy(); tf2["ex"] = tf2["ex_dir"]
    res["trend_dir_ex_on_vr"] = slope(tf2, "vr").to_frame().T
    return res
