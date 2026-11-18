def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            vol = r.rolling(20, min_periods=10).std()
            vol60 = r.rolling(60, min_periods=30).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "r": r, "z": r / vol.shift(1), "vol": vol,
                "vratio": vol / vol60,
                "fwd1": c.shift(-1) / c - 1,
                "r20": c / c.shift(20) - 1,
                "pos": b["postRebalance_current_allocation"],
                "prev": b["previous_allocation"],
                "tpv": b["total_portfolio_value"], "ptv": b["postRebalance_total_value"],
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            d["gain"] = d["pos"] * d["fwd1"]
            d["fee"] = (d["tpv"] - d["ptv"]) / d["tpv"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["ex1"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    def summ(g, col="ex1"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    D["vq"] = D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    D["zq"] = pd.qcut(D["z"], 5, labels=False)
    out["next1 by vol tercile x z quintile"] = D.groupby(["vq", "zq"]).apply(summ)
    # graded slope of ex1 on z within each vol tercile
    res = []
    for v, g in D.dropna(subset=["z", "ex1"]).groupby("vq"):
        s = stats.linregress(g["z"], g["ex1"])
        res.append({"vq": v, "n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    out["slope ex1 on z by vol tercile"] = pd.DataFrame(res)
    res = []
    for (cn, v), g in D.dropna(subset=["z", "ex1"]).groupby(["coin", "vq"]):
        s = stats.linregress(g["z"], g["ex1"])
        res.append({"coin": cn, "vq": v, "n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    out["slope by coin x vol tercile"] = pd.DataFrame(res)
    # interaction: ex1 on z*vol rank
    g = D.dropna(subset=["z", "ex1", "vol"]).copy()
    g["vr"] = g.groupby("coin")["vol"].rank(pct=True)
    X = np.column_stack([np.ones(len(g)), g["z"], g["vr"], g["z"] * g["vr"]])
    beta, *_ = np.linalg.lstsq(X, g["ex1"], rcond=None)
    resid = g["ex1"] - X @ beta
    cov = np.linalg.inv(X.T @ X) * resid.var()
    out["interaction reg"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["c", "z", "volrank", "z*volrank"])
    # high-vol slope by year
    res = []
    for y, gg in D[D["vq"] == 2].dropna(subset=["z", "ex1"]).groupby("yr"):
        s = stats.linregress(gg["z"], gg["ex1"])
        res.append({"yr": y, "n": len(gg), "slope": s.slope, "t": s.slope / s.stderr})
    out["high-vol slope by year"] = pd.DataFrame(res)
    # trend: up days in downtrend graded by z
    D["r20s"] = np.sign(D["r20"])
    out["next1 by r20 sign x z quintile"] = D.groupby(["r20s", "zq"]).apply(summ)
    # fees vs gain
    out["mean gain vs fee per bar"] = pd.Series({"gain": D["gain"].mean(), "fee": D["fee"].mean(),
                                                 "turnover": (D["pos"] - D["prev"]).abs().mean()})
    out["gain by vol tercile"] = D.groupby("vq")[["gain", "fee"]].mean()
    return out
