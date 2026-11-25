def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            b["ts"] = pd.to_datetime(b["timestamp"])
            c = b["close"]
            b["ret1"] = c / c.shift(1) - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["fwd2"] = c.shift(-2) / c - 1
            b["sd30"] = b["ret1"].rolling(30, min_periods=20).std()
            b["rng"] = (b["high"] - b["low"]) / c / b["sd30"]
            b["retz"] = b["ret1"] / b["sd30"]
            hl = (b["high"] - b["low"]).replace(0, np.nan)
            b["clv"] = (c - b["low"]) / hl
            b["ret60"] = c / c.shift(60) - 1
            lr = np.log(c).diff()
            b["sd30d"] = lr.rolling(30).std()
            b["pct"] = b["sd30d"].rolling(365, min_periods=120).apply(lambda s: (s <= s[-1]).mean(), raw=True)
            b["pos"] = b["postRebalance_current_allocation"]
            b["coin"] = coin; b["win"] = w
            b["year"] = b["ts"].dt.year
            b["day"] = b["ts"].dt.floor("D")
            b["i"] = np.arange(len(b))
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["fwd1"].mean()
    d["ex1"] = d["fwd1"] - d["coin"].map(drift)
    drift2 = d[d["i"] % 2 == 0].groupby("coin")["fwd2"].mean()
    d["ex2"] = d["fwd2"] - d["coin"].map(drift2)

    def summ(g, col="ex1"):
        x = g.dropna(subset=[col])
        if len(x) < 10: return pd.Series({"n": len(x)})
        s = x.groupby("day")[col].sum()
        t = s.mean() / (s.std(ddof=1) / np.sqrt(len(s)))
        return pd.Series({"n": len(x), "days": len(s), "mean%": 100 * x[col].mean(), "t_day": t})
    out = {}
    dn = d[d["ret1"] < 0].dropna(subset=["rng", "ex1"]).copy()
    dn["rq"] = dn.groupby("coin")["rng"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    w = dn[dn["rq"] == 4]
    out["wide down days (top range quintile of down days): by year"] = w.groupby("year").apply(summ)
    out["wide down days: by coin"] = w.groupby("coin").apply(summ)
    out["wide down days: by window"] = w.groupby("win").apply(summ)
    out["down days quintile, 2-day excess (grid)"] = dn[dn["i"] % 2 == 0].groupby("rq").apply(lambda g: summ(g, "ex2"))
    # grading: within down days, regress ex1 on rng and on retz together
    x = dn.dropna(subset=["rng", "retz", "ex1"])
    X = np.column_stack([np.ones(len(x)), x["rng"], x["retz"], x["clv"].fillna(0.5)])
    beta, *_ = np.linalg.lstsq(X, x["ex1"].values, rcond=None)
    res = x["ex1"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * res.var(ddof=4)
    out["down days OLS ex1 ~ rng + retz + clv (coef, t)"] = pd.DataFrame({"coef": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["const", "rng", "retz", "clv"])
    # signal: rng*(1-clv) graded "wide range closing low"
    d["lowwide"] = d["rng"] * (1 - d["clv"])
    d["lwq"] = d.groupby("coin")["lowwide"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["rng*(1-clv) quintile, next-day excess"] = d.groupby("lwq").apply(summ)
    # profile of wide down days
    d["tr"] = pd.cut(d["ret60"], [-10, -.1, .1, 100], labels=["falling", "choppy", "rising"])
    d["ag"] = np.where(d["pct"] > 0.5, "agitated", np.where(d["pct"].notna(), "calm", None))
    dn2 = d[d["ret1"] < 0].copy()
    dn2["rq"] = dn2.groupby("coin")["rng"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["wide down days by profile"] = dn2[dn2["rq"] == 4].groupby(["tr", "ag"]).apply(summ)
    # book: gain by position sign
    d["gain"] = d["pos"] * d["fwd1"]
    d["inpos"] = d["pos"].abs() > 1e-6
    out["position held: share short, mean gain% by up/down day"] = d[d["inpos"]].groupby(np.where(d.loc[d["inpos"], "ret1"] > 0, "after up", "after down")).agg(n=("gain", "size"), gain=("gain", lambda s: 100 * s.mean()), pos=("pos", "mean"))
    return out
