def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r0": r, "z": r / vol, "vol": vol,
                "calm": (b["regime"] != "chop").astype(int),
                "clv": ((c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)),
                "rng": (b["high"] - b["low"]) / c / vol,
                "r1": c.shift(-1) / c - 1, "r2": c.shift(-2) / c.shift(-1) - 1,
                "r3": c.shift(-3) / c.shift(-2) - 1,
                "r5f": c.shift(-5) / c - 1, "r5p": c / c.shift(5) - 1,
                "alloc": b["postRebalance_current_allocation"],
                "pos": np.arange(len(b)),
            })
            df["r5p_z"] = df["r5p"] / (vol * np.sqrt(5))
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["wd"] = d["day"].dt.weekday
    d["yr"] = d["day"].dt.year
    mu = d.groupby("coin")["r0"].mean()
    for k in ["r1", "r2", "r3"]:
        d["x" + k] = d[k] - d["coin"].map(mu)
    d["xr5f"] = d["r5f"] - 5 * d["coin"].map(mu)
    def cmean(s, day):
        m = pd.DataFrame({"v": s, "d": day}).dropna()
        if len(m) < 5: return (np.nan, np.nan, len(m))
        mean = m["v"].mean()
        g = (m["v"] - mean).groupby(m["d"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(m)
        return (mean, mean / se if se > 0 else np.nan, len(m))
    def cslope(x, y, day):
        m = pd.DataFrame({"x": x, "y": y, "d": day}).dropna()
        if len(m) < 20: return (np.nan, np.nan, len(m))
        X = np.c_[np.ones(len(m)), m["x"]]
        beta = np.linalg.lstsq(X, m["y"].values, rcond=None)[0]
        e = m["y"].values - X @ beta
        S = pd.DataFrame(X * e[:, None]).groupby(m["d"].values).sum().values
        B = np.linalg.inv(X.T @ X)
        V = B @ (S.T @ S) @ B
        return (beta[1], beta[1] / np.sqrt(V[1, 1]), len(m))
    out = {}
    # 1. buckets of z by calm, effect on day1, day2, day3
    d["zb"] = pd.cut(d["z"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    res = []
    for (calm, zb), g in d.groupby(["calm", "zb"], observed=True):
        rr = {"calm": calm, "zb": str(zb)}
        for k in ["xr1", "xr2", "xr3"]:
            m, t, n = cmean(g[k], g["day"]); rr[k + "_bp"] = round(m * 1e4, 1); rr[k + "_t"] = round(t, 2)
        rr["n"] = len(g); res.append(rr)
    out["z_buckets"] = pd.DataFrame(res)
    # 2. slopes
    res = []
    for calm in [0, 1]:
        for side, sub in [("up", d[d.z > 0]), ("down", d[d.z < 0]), ("all", d)]:
            g = sub[sub.calm == calm]
            for k in ["xr1", "xr2", "xr3"]:
                b_, t, n = cslope(g["z"], g[k], g["day"])
                res.append({"calm": calm, "side": side, "y": k, "slope_bp": round(b_ * 1e4, 1), "t": round(t, 2), "n": n})
    out["slopes"] = pd.DataFrame(res)
    # 3. close location and range
    res = []
    for calm in [0, 1]:
        g = d[d.calm == calm]
        for xv in ["clv", "rng", "r5p_z"]:
            for k in ["xr1", "xr2"]:
                b_, t, n = cslope(g[xv], g[k], g["day"])
                res.append({"calm": calm, "x": xv, "y": k, "slope_bp": round(b_ * 1e4, 1), "t": round(t, 2), "n": n})
    # 5-day non-overlapping
    g5 = d[d.pos % 5 == 0]
    for calm in [0, 1, 2]:
        g = g5 if calm == 2 else g5[g5.calm == calm]
        b_, t, n = cslope(g["r5p_z"], g["xr5f"], g["day"])
        res.append({"calm": calm, "x": "r5p_z", "y": "xr5f", "slope_bp": round(b_ * 1e4, 1), "t": round(t, 2), "n": n})
    out["other_slopes"] = pd.DataFrame(res)
    # 4. weekday
    res = []
    for wd, g in d.groupby("wd"):
        m, t, n = cmean(g["xr1"], g["day"]); res.append({"wd_of_next": (wd + 1) % 7, "bp": round(m * 1e4, 1), "t": round(t, 2), "n": n})
    out["weekday"] = pd.DataFrame(res)
    # 5. vol level: vol tercile vs next day
    d["volq"] = d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    res = []
    for q, g in d.groupby("volq"):
        m, t, n = cmean(g["xr1"], g["day"]); res.append({"volq": q, "bp": round(m * 1e4, 1), "t": round(t, 2), "n": n})
    out["vol_tercile"] = pd.DataFrame(res)
    # 6. year stability of calm up second-day slope
    res = []
    g = d[(d.calm == 1) & (d.z > 0)]
    for y, gg in g.groupby("yr"):
        b_, t, n = cslope(gg["z"], gg["xr2"], gg["day"]); res.append({"yr": y, "slope_bp": round(b_ * 1e4, 1), "t": round(t, 2), "n": n})
    out["calm_up_r2_by_year"] = pd.DataFrame(res)
    # 7. book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, win=w))
    dd = pd.concat(dd)
    bk = dd.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    out["book_corr_with_coins"] = float(bk.corr().iloc[0, 1])
    q = bk["book_return"].quantile([0.02, 0.98])
    out["book_extremes_coin_ret_bp"] = pd.Series({
        "worst2pct_book_bp": bk.loc[bk.book_return <= q.iloc[0], "book_return"].mean() * 1e4,
        "worst2pct_coin_bp": bk.loc[bk.book_return <= q.iloc[0], "coin_return"].mean() * 1e4,
        "best2pct_book_bp": bk.loc[bk.book_return >= q.iloc[1], "book_return"].mean() * 1e4,
        "best2pct_coin_bp": bk.loc[bk.book_return >= q.iloc[1], "coin_return"].mean() * 1e4})
    out["calm_share"] = float(d["calm"].mean())
    return out
