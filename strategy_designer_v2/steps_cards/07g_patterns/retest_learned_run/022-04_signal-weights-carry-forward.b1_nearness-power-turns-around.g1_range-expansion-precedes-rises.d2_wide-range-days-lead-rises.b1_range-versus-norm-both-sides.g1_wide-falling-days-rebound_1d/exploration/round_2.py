def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; h = b["high"]; l = b["low"]
            r1 = c / c.shift(1) - 1
            rng = (h - l) / c
            rr = rng / rng.rolling(30, min_periods=15).mean()
            vol = r1.rolling(30, min_periods=15).std()
            clv = (c - l) / (h - l).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            al = b["postRebalance_current_allocation"]
            g1 = al * (c.shift(-1) / c - 1)
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r1": r1, "rr": rr,
                              "z1": r1 / vol.shift(1), "fr3": c.shift(-3) / c - 1,
                              "mom30": c / c.shift(30) - 1, "mom14": c / c.shift(14) - 1,
                              "clv": clv, "fc": b["forecast"], "alloc": al, "g1": g1,
                              "yr": ts.dt.year})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["pos"] % 3 == 0].dropna(subset=["fr3"]).copy()
    G["ex"] = G["fr3"] - G.groupby("coin")["fr3"].transform("mean")
    out = {}
    def tt(s):
        s = s.dropna(); return s.mean() / s.std() * np.sqrt(len(s)) if len(s) > 2 else np.nan
    dn = G[G.r1 < 0].dropna(subset=["rr", "clv", "ex"])
    import numpy.linalg as la
    X = np.column_stack([np.ones(len(dn)), dn["rr"], dn["clv"]])
    y = dn["ex"].values
    beta, *_ = la.lstsq(X, y, rcond=None)
    res = y - X @ beta
    s2 = res @ res / (len(y) - 3)
    se = np.sqrt(np.diag(s2 * la.inv(X.T @ X)))
    out["dn_multi_rr_clv"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "rr", "clv"])
    dn = dn.copy()
    dn["clvq"] = pd.qcut(dn["clv"], 5, labels=False)
    out["dn_clv_quint"] = dn.groupby("clvq")["ex"].agg(["mean", "count", tt])
    up = G[G.r1 > 0].dropna(subset=["z1", "ex"]).copy()
    up["zq"] = pd.qcut(up["z1"], 5, labels=False)
    out["up_z1_quint"] = up.groupby("zq")["ex"].agg(["mean", "count", tt])
    dz = G[G.r1 < 0].dropna(subset=["z1", "ex"]).copy()
    dz["zq"] = pd.qcut(dz["z1"], 5, labels=False)
    out["dn_z1_quint"] = dz.groupby("zq")["ex"].agg(["mean", "count", tt])
    M = G.dropna(subset=["mom30", "ex"]).copy()
    M["mq"] = pd.qcut(M["mom30"], 5, labels=False)
    out["mom30_quint"] = M.groupby("mq")["ex"].agg(["mean", "count", tt])
    yrs = {}
    for y_, df in M.groupby("yr"):
        s = stats.linregress(df["mom30"], df["ex"]); yrs[y_] = {"t": s.slope / s.stderr, "n": len(df)}
    out["mom30_by_year"] = pd.DataFrame(yrs).T
    cs = {}
    for c_, df in M.groupby("coin"):
        s = stats.linregress(df["mom30"], df["ex"]); cs[c_] = {"t": s.slope / s.stderr, "n": len(df)}
    out["mom30_by_coin"] = pd.DataFrame(cs).T
    # position gains by sign of allocation and forecast band
    P = A.dropna(subset=["g1"]).copy()
    P["side"] = np.sign(P["alloc"])
    P["fcb"] = pd.cut(P["fc"], [-21, -3, -1e-9, 1e-9, 3, 6, 21])
    out["gain_by_side"] = P.groupby("side")["g1"].agg(["mean", "count", tt])
    out["gain_by_fcband"] = P.groupby("fcb", observed=True)["g1"].agg(["mean", "count", tt])
    # book's largest days: what precedes
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk["book_return"].quantile([0.02, 0.98])
    out["book_extremes"] = pd.DataFrame({
        "worst2pct_coin_ret": [bk[bk.book_return <= q.iloc[0]]["coin_return"].mean()],
        "best2pct_coin_ret": [bk[bk.book_return >= q.iloc[1]]["coin_return"].mean()],
        "corr_book_coin": [bk.corr().iloc[0, 1]]})
    return out
