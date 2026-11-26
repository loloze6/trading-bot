def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = pd.concat([b["close"].pct_change() for b in wins.values()])
        drift = allr.mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            vol = r1.rolling(30).std()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "reg": b["regime"].astype(str),
                "r1s": r1 / vol,
                "uw": (b["high"] - c) / c / vol,
                "rng": (b["high"] - b["low"]) / c / vol,
                "r3s": (c / c.shift(3) - 1) / (vol * np.sqrt(3)),
                "r2s": (c / c.shift(2) - 1) / (vol * np.sqrt(2)),
                "tr60": c / c.shift(60) - 1,
                "fwd1": c.shift(-1) / c - 1 - drift,
                "fwd2": c.shift(-2) / c - 1 - 2 * drift,
                "fwd3": c.shift(-3) / c - 1 - 3 * drift,
                "pos": np.arange(len(b)),
                "bret": b["postRebalance_total_value"].pct_change().shift(-1),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["prof"] = D["reg"].isin(["trending", "unknown"])
    D["up"] = D["r1s"] > 0
    out = {}

    def clus(s, y):
        g = s.groupby("day")[y].sum()
        n = len(s); m = s[y].mean()
        dev = s[y] - m
        gd = dev.groupby(s["day"]).sum()
        G = len(gd)
        se = np.sqrt((gd ** 2).sum() * G / (G - 1)) / n
        return m, m / se, n, G

    def qt(s, feat, y, q=4):
        s = s.dropna(subset=[feat, y]).copy()
        s["qq"] = pd.qcut(s[feat].rank(method="first"), q, labels=False)
        res = []
        for k, g in s.groupby("qq"):
            m, t, n, G = clus(g, y)
            res.append([k, g[feat].mean(), m, t, n, G])
        m, t, n, G = clus(s, y)
        rho = stats.spearmanr(s[feat], s[y])[0]
        res.append(["all", rho, m, t, n, G])
        return pd.DataFrame(res, columns=["q", "featmean_or_rho", "mean", "t_day", "n", "days"]).round(5)

    P = D[D["prof"]]
    # brief theme: multi-day rises, non-overlapping grids
    for h, f, y in [(3, "r3s", "fwd3"), (2, "r2s", "fwd2"), (3, "r3s", "fwd1")]:
        s = P[(P[f] > 0)]
        if y != "fwd1":
            s = s[s["pos"] % h == 0]
        out[f"prof rises {f}->{y}"] = qt(s, f, y)
        so = D[(~D["prof"]) & (D[f] > 0)]
        if y != "fwd1":
            so = so[so["pos"] % h == 0]
        out[f"out rises {f}->{y}"] = qt(so, f, y)
    # up day range vs uw: partial
    s = P[P["up"]].dropna(subset=["uw", "rng", "r1s", "fwd1"])
    X = np.column_stack([np.ones(len(s)), s["uw"], s["rng"] - s["uw"], s["r1s"]])
    beta, *_ = np.linalg.lstsq(X, s["fwd1"].values, rcond=None)
    resid = s["fwd1"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * resid.var(ddof=4)
    out["prof up regression fwd1 ~ uw + lowerpart + r1s"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["const", "uw", "rng-uw", "r1s"]).round(5)
    # down days: uw beyond r1s
    s = P[~P["up"]].dropna(subset=["uw", "rng", "r1s", "fwd1"])
    X = np.column_stack([np.ones(len(s)), s["uw"], s["rng"] - s["uw"], s["r1s"]])
    beta, *_ = np.linalg.lstsq(X, s["fwd1"].values, rcond=None)
    resid = s["fwd1"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * resid.var(ddof=4)
    out["prof down regression"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["const", "uw", "rng-uw", "r1s"]).round(5)
    out["prof up uw quartiles clustered"] = qt(P[P["up"]], "uw", "fwd1")
    out["prof down uw quartiles clustered"] = qt(P[~P["up"]], "uw", "fwd1")
    # falling calm (out of profile, tr60<-0.1) : up day uw and r3s
    O = D[~D["prof"]].dropna(subset=["tr60"])
    fc = O[O["tr60"] < -0.1]
    out["falling-not-agitated up uw fwd1"] = qt(fc[fc["up"]], "uw", "fwd1")
    # by window: up-day uw top half vs bottom half in profile
    s = P[P["up"]].dropna(subset=["uw", "fwd1"]).copy()
    s["top"] = s["uw"] > s["uw"].median()
    out["prof up by window"] = s.groupby(["win", "top"])["fwd1"].agg(["mean", "count"]).unstack().round(4)
    # book: largest gains / losses
    B = D.dropna(subset=["bret"])
    B = B[B["bret"] != 0]
    lo = B["bret"].quantile(0.05); hi = B["bret"].quantile(0.95)
    out["book worst5% bars"] = B[B["bret"] <= lo][["uw", "rng", "r1s", "r3s", "fwd1"]].describe().loc[["count", "mean", "50%"]].round(4)
    out["book best5% bars"] = B[B["bret"] >= hi][["uw", "rng", "r1s", "r3s", "fwd1"]].describe().loc[["count", "mean", "50%"]].round(4)
    return out
