def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = pd.concat([w.sort_values("timestamp")["close"].pct_change() for w in wins.values()])
        mu = allr.mean(); sd = allr.std()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            d = pd.DataFrame()
            rng = b["high"] - b["low"]
            d["clv"] = (b["close"] - b["low"]) / rng.replace(0, np.nan)
            d["rr"] = rng / rng.shift(1).rolling(30, min_periods=20).mean()
            r = b["close"].pct_change()
            d["r0z"] = r / r.shift(1).rolling(30, min_periods=20).std()
            d["r0s"] = r / sd
            d["nx"] = b["close"].shift(-1) / b["close"] - 1
            d["ex"] = (d["nx"] - mu) / sd
            d["nx2"] = b["close"].shift(-2) / b["close"] - 1
            d["ex2"] = (d["nx2"] - 2 * mu) / (sd * np.sqrt(2))
            d["agit"] = (b["regime"] != "chop").astype(int)
            d["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            d["p2"] = np.arange(len(b)) % 2
            d["coin"] = coin; d["w"] = w
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["clv", "nx", "r0z", "rr"])
    out = {}
    def daysum_t(s, col):
        g = s.groupby("day")[col].sum()
        return pd.Series({"n": len(s), "days": len(g), "mean": s[col].mean(), "t_day": g.mean() / (g.std() / np.sqrt(len(g)))})
    def reg(s, cols, y="ex"):
        X = np.column_stack([np.ones(len(s))] + [s[c].values for c in cols]); yy = s[y].values
        b, *_ = np.linalg.lstsq(X, yy, rcond=None); res = yy - X @ b
        cov = np.linalg.inv(X.T @ X) * res.var(ddof=X.shape[1])
        return pd.Series(np.r_[b, b / np.sqrt(np.diag(cov))], index=["b0"] + ["b_" + c for c in cols] + ["t0"] + ["t_" + c for c in cols])
    D["neg"] = -D["r0z"]
    D["negxrr"] = -D["r0z"] * D["rr"]
    out["reg ex ~ -r0z(own 30d) + rr + clv"] = pd.DataFrame({a: reg(D[D.agit == a], ["neg", "rr", "clv"]) for a in [0, 1]})
    out["reg ex ~ -r0z*rr + clv"] = pd.DataFrame({a: reg(D[D.agit == a], ["negxrr", "clv"]) for a in [0, 1]})
    D["r0q"] = pd.qcut(D["r0z"], 5, labels=False)
    out["agit: r0z quintile day-sum t"] = D[D.agit == 1].groupby("r0q").apply(lambda s: daysum_t(s, "ex"))
    out["calm: r0z quintile day-sum t"] = D[D.agit == 0].groupby("r0q").apply(lambda s: daysum_t(s, "ex"))
    A = D[D.agit == 1].copy()
    A["rrq"] = pd.qcut(A["rr"], 3, labels=False)
    out["agit: r0q x rr tercile mean ex"] = A.groupby(["r0q", "rrq"])["ex"].mean().unstack()
    # within down days: clv effect?
    dn = A[A.r0z < 0].copy(); dn["clvq"] = pd.qcut(dn["clv"], 3, labels=False)
    out["agit down days: clv tercile"] = dn.groupby("clvq").apply(lambda s: daysum_t(s, "ex"))
    up = A[A.r0z > 0].copy(); up["clvq"] = pd.qcut(up["clv"], 3, labels=False)
    out["agit up days: clv tercile"] = up.groupby("clvq").apply(lambda s: daysum_t(s, "ex"))
    # 2-day non-overlap
    D2 = D[D.p2 == 0].dropna(subset=["ex2"])
    out["2d nonoverlap r0q x agit day-sum t"] = D2.groupby(["agit", "r0q"]).apply(lambda s: daysum_t(s, "ex2"))
    # weekday day-sum t
    D["wd"] = D["day"].dt.weekday
    out["weekday day-sum t"] = D.groupby("wd").apply(lambda s: daysum_t(s, "ex"))
    out["weekday by window-half"] = D.assign(h=D["w"].str[1:].astype(int) <= 12).groupby(["wd", "h"])["ex"].mean().unstack()
    return out
