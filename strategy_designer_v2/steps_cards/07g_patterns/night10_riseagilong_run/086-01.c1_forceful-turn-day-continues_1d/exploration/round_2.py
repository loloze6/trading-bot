def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []; drift = {}
    for coin, wins in data["bars"].items():
        r3 = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c)-3, 3):
                r3.append(c[i+3]/c[i]-1)
        drift[coin] = (np.mean(r3), np.std(r3))
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; r1 = c.pct_change()
            vol = r1.rolling(30, min_periods=20).std()
            rng = b["high"]-b["low"]
            b["rngz"] = (rng/c.shift(1))/vol
            b["volz"] = b["volume"]/b["volume"].rolling(30, min_periods=20).mean()
            b["r5z"] = (c/c.shift(5)-1)/(vol*np.sqrt(5))
            b["z1"] = r1/vol
            b["clv"] = (c-b["low"])/rng.replace(0, np.nan)
            b["up"] = (r1 > 0)
            b["inprof"] = b["regime"].isin(["trending", "unknown"])
            b["fwd3"] = c.shift(-3)/c-1
            b["pos"] = np.arange(len(b)); b["coin"] = coin; b["win"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[(b["pos"] % 3 == 0) & b["fwd3"].notna()])
    df = pd.concat(rows)
    df["unu"] = df["fwd3"]-df["coin"].map(lambda k: drift[k][0])
    df["us"] = df["unu"]/df["coin"].map(lambda k: drift[k][1])
    P = df[df["inprof"]].dropna(subset=["rngz", "volz", "r5z"])
    def ct(x):
        s = x.groupby("day")["unu"].sum()
        G = len(s); n = len(x); m = x["unu"].mean()
        dev = (x["unu"]-m).groupby(x["day"]).sum()
        se = np.sqrt((dev**2).sum()*G/(G-1))/n
        return pd.Series({"mean": m, "strength": x["us"].mean(), "t_day": m/se, "n": n, "days": G})
    def slope(x, col):
        sl = stats.linregress(x[col], x["unu"]); return pd.Series({"slope": sl.slope, "t": sl.slope/sl.stderr, "n": len(x)})
    out = {}
    out["clustered by rngz quintile"] = P.assign(q=pd.qcut(P["rngz"].rank(method="first"), 5, labels=False)).groupby("q").apply(ct)
    out["clustered by volz quintile"] = P.assign(q=pd.qcut(P["volz"].rank(method="first"), 5, labels=False)).groupby("q").apply(ct)
    out["rngz slope by up/down day"] = P.groupby("up").apply(lambda x: slope(x, "rngz"))
    out["volz slope by up/down day"] = P.groupby("up").apply(lambda x: slope(x, "volz"))
    out["rngz slope by coin"] = P.groupby("coin").apply(lambda x: slope(x, "rngz"))
    out["rngz slope by year"] = P.groupby("yr").apply(lambda x: slope(x, "rngz"))
    out["volz slope by coin"] = P.groupby("coin").apply(lambda x: slope(x, "volz"))
    out["log rngz slope"] = slope(P.assign(l=np.log(P["rngz"])), "l")
    out["log volz slope"] = slope(P.assign(l=np.log(P["volz"])), "l")
    out["corr rngz volz r5z z1"] = P[["rngz", "volz", "r5z", "z1"]].corr()
    X = P[["rngz", "volz", "r5z"]].copy(); X = (X-X.mean())/X.std(); X["c"] = 1
    beta, *_ = np.linalg.lstsq(X.values, P["unu"].values, rcond=None)
    res = P["unu"].values - X.values@beta
    s2 = (res**2).sum()/(len(res)-4); cov = s2*np.linalg.inv(X.values.T@X.values)
    out["joint OLS t"] = pd.Series(beta/np.sqrt(np.diag(cov)), index=X.columns)
    top = P[P["rngz"] > P["rngz"].quantile(0.8)]
    out["top rngz quintile by up/down"] = top.groupby("up").apply(ct)
    out["top rngz quintile by clv half"] = top.groupby(top["clv"] > 0.5).apply(ct)
    out["out-of-profile rngz slope"] = slope(df[~df["inprof"]].dropna(subset=["rngz"]), "rngz")
    return out
