def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            d = pd.DataFrame()
            d["ts"] = pd.to_datetime(b["timestamp"]); d["coin"] = coin; d["w"] = w
            h, l, c = b["high"], b["low"], b["close"]
            rng = h - l
            base = rng.rolling(20, min_periods=10).mean()
            d["clv"] = (c - l) / rng.replace(0, np.nan)
            d["width"] = rng / base
            d["sig"] = (h + l - 2 * c) / base
            d["r0"] = c.pct_change()
            d["r1"] = c.shift(-1) / c - 1
            d["r2"] = c.shift(-2) / c.shift(-1) - 1
            d["r12"] = c.shift(-2) / c - 1
            d["ret60"] = c / c.shift(60) - 1
            d["vol30"] = d["r0"].rolling(30, min_periods=20).std()
            d["vol365"] = d["vol30"].rolling(365, min_periods=60).median()
            d["pos"] = np.arange(len(d))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["r0"].mean()
    dm = D["coin"].map(drift)
    D["x1"] = D["r1"] - dm; D["x2"] = D["r2"] - dm; D["x12"] = D["r12"] - 2 * dm
    D["day"] = D["ts"].dt.floor("D")
    D["agit"] = np.where(D["vol30"] > D["vol365"], "agit", "calm")
    D.loc[D["vol365"].isna(), "agit"] = np.nan
    D["trend"] = pd.cut(D["ret60"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])

    def ct(df, col, xcol):
        z = df[[col, xcol, "day"]].dropna()
        x = z[xcol] - z[xcol].mean(); y = z[col]
        beta = (x * (y - y.mean())).sum() / (x ** 2).sum()
        e = y - y.mean() - beta * x
        s = (x * e).groupby(z["day"]).sum(); G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (x ** 2).sum()
        return pd.Series({"n": len(z), "days": G, "slope": beta, "t": beta / se})

    def summ(g, col):
        s = g[[col, "day"]].dropna()
        ds = s.groupby("day")[col].sum()
        dev = (s[col] - s[col].mean()).groupby(s["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"n": len(s), "mean%": 100 * s[col].mean(), "t_day": s[col].mean() / se})

    out = {}
    out["sig slope x1 / x2 / x12"] = pd.DataFrame({k: ct(D, k, "sig") for k in ["x1", "x2", "x12"]})
    D["fallq"] = pd.qcut(D["r0"], 10, labels=False)
    out["own-day return decile -> x1, x2"] = pd.DataFrame({
        "x1": D.groupby("fallq").apply(lambda g: summ(g, "x1"))["mean%"],
        "t1": D.groupby("fallq").apply(lambda g: summ(g, "x1"))["t_day"],
        "x2": D.groupby("fallq").apply(lambda g: summ(g, "x2"))["mean%"],
        "t2": D.groupby("fallq").apply(lambda g: summ(g, "x2"))["t_day"]})
    # asymmetry: low side vs high side slopes
    lo = D[D["sig"] > 0]; hi = D[D["sig"] < 0]
    out["slope on low-close side vs high-close side x1"] = pd.DataFrame({"low": ct(lo, "x1", "sig"), "high": ct(hi, "x1", "sig")})
    out["slope low side by agitation x1"] = lo.groupby("agit").apply(lambda g: ct(g, "x1", "sig"))
    out["slope low side by trend x1"] = lo.groupby("trend").apply(lambda g: ct(g, "x1", "sig"))
    out["slope all by profile x1"] = D.groupby(["trend", "agit"]).apply(lambda g: ct(g, "x1", "sig"))
    # day-2 giveback graded
    out["slope low side x2"] = ct(lo, "x2", "sig")
    out["slope high side x2"] = ct(hi, "x2", "sig")
    D["sq"] = pd.qcut(D["sig"], 5, labels=False)
    out["sig quintile x1/x2/x12 day-clustered"] = pd.concat({k: D.groupby("sq").apply(lambda g: summ(g, k)) for k in ["x1", "x2", "x12"]}, axis=1)
    # grid-based check x1 by agit on low side top quintile
    top = D[D["sq"] == 4]
    out["top sig quintile x1 by agitation"] = top.groupby("agit").apply(lambda g: summ(g, "x1"))
    out["top sig quintile x1 by year"] = top.groupby(top["ts"].dt.year).apply(lambda g: summ(g, "x1"))
    out["top sig quintile x1 by coin"] = top.groupby("coin").apply(lambda g: summ(g, "x1"))
    return out
