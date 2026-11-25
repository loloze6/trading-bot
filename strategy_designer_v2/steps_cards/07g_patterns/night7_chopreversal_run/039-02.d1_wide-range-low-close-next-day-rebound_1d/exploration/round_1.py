def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            allr.append(b["close"].pct_change())
        mu = pd.concat(allr).mean(); sd = pd.concat(allr).std()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            d = pd.DataFrame()
            rng = (b["high"] - b["low"])
            d["clv"] = ((b["close"] - b["low"]) / rng.replace(0, np.nan))
            d["rr"] = rng / rng.shift(1).rolling(30, min_periods=20).mean()
            d["r0"] = b["close"].pct_change()
            d["r5"] = b["close"] / b["close"].shift(5) - 1
            d["nx"] = b["close"].shift(-1) / b["close"] - 1
            d["nx3"] = b["close"].shift(-3) / b["close"] - 1
            d["ex"] = (d["nx"] - mu) / sd
            d["agit"] = (b["regime"] != "chop").astype(int)
            d["pos"] = b["postRebalance_current_allocation"]
            d["gain"] = d["pos"] * d["nx"]
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["r0z"] = d["r0"] / sd
            d["coin"] = coin; d["w"] = w; d["pos3"] = np.arange(len(b)) % 3
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["clv", "nx", "r0"])
    out = {}
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    D["clvq"] = pd.qcut(D["clv"], 5, labels=False)
    out["clv quintile x agit, std next ret"] = D.groupby(["agit", "clvq"])["ex"].apply(tt).unstack()
    D["rrq"] = pd.qcut(D["rr"], 3, labels=False)
    out["agit only: clvq x rr tercile mean ex"] = D[D.agit == 1].groupby(["clvq", "rrq"])["ex"].mean().unstack()
    D["r0q"] = pd.qcut(D["r0z"], 5, labels=False)
    out["r0 quintile x agit"] = D.groupby(["agit", "r0q"])["ex"].apply(tt).unstack()
    # regression next ex on clv and r0z per regime
    reg = {}
    for a in [0, 1]:
        s = D[D.agit == a].dropna(subset=["rr"])
        X = np.column_stack([np.ones(len(s)), s["clv"] - 0.5, s["r0z"], s["rr"]])
        y = s["ex"].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ beta
        cov = np.linalg.inv(X.T @ X) * res.var(ddof=4)
        reg[a] = pd.Series(np.r_[beta, beta / np.sqrt(np.diag(cov))], index=["b0", "b_clv", "b_r0", "b_rr", "t0", "t_clv", "t_r0", "t_rr"])
    out["regression ex ~ clv + r0z + rr by agit"] = pd.DataFrame(reg)
    D["r5q"] = pd.qcut(D["r5"] / D.groupby("coin")["r0"].transform("std"), 5, labels=False)
    out["5d ret quintile x agit"] = D.groupby(["agit", "r5q"])["ex"].mean().unstack()
    out["weekday x agit mean ex"] = D.groupby(["wd", "agit"])["ex"].mean().unstack()
    out["weekday t all"] = D.groupby("wd")["ex"].apply(tt).unstack()
    # 3-day horizon non-overlapping
    D3 = D[D.pos3 == 0].dropna(subset=["nx3"])
    out["clvq x agit nx3 (nonoverlap)"] = D3.groupby(["agit", "clvq"])["nx3"].apply(tt).unstack()
    # book gains by clv/held
    H = D[D.pos != 0]
    out["held: by clvq mean gain"] = H.groupby("clvq")["gain"].apply(tt).unstack()
    out["held: by coin mean gain"] = H.groupby("coin")["gain"].apply(tt).unstack()
    out["held: by window mean gain"] = H.groupby("w")["gain"].apply(tt).unstack()
    out["coin x agit clv slope corr"] = D.groupby(["coin", "agit"]).apply(lambda s: s["clv"].corr(s["ex"])).unstack()
    return out
