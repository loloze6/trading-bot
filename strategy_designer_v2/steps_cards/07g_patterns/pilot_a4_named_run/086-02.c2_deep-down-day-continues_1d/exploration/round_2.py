def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    drift, usual = {}, {}
    for coin, wins in data["bars"].items():
        for h in (3, 5, 10):
            rs = []
            for w, b in wins.items():
                c = b["close"].values.astype(float)
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = float(np.mean(rs)) if len(rs) else np.nan
            usual[(coin, h)] = float(np.std(rs)) if len(rs) else np.nan
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            upv = (r > 0).astype(int).values
            run = np.zeros(len(upv), dtype=int)
            for i in range(len(upv)):
                run[i] = run[i - 1] + 1 if (upv[i] == 1 and i > 0) else (1 if upv[i] == 1 else 0)
            prevrun = np.r_[0, run[:-1]]
            cv = c.values
            rr = np.zeros(len(cv))
            for i in range(len(cv)):
                k = prevrun[i]
                if k > 0 and i - 1 - k >= 0:
                    rr[i] = cv[i - 1] / cv[i - 1 - k] - 1
            b["runlen"] = prevrun
            b["runz"] = rr / vol.values
            b["dz"] = (r / vol).values
            rng = (b["high"] - b["low"]).astype(float)
            b["clv"] = ((c - b["low"]) / rng.replace(0, np.nan)).values
            b["rngz"] = (rng / c / vol).values
            b["volrel"] = (b["volume"] / b["volume"].rolling(30, min_periods=10).median()).values
            b["dist20"] = ((c / c.rolling(20, min_periods=10).max() - 1) / vol).values
            b["ret5z"] = ((c / c.shift(5) - 1) / vol).values
            b["ret60"] = (c / c.shift(60) - 1).values
            b["inprof"] = (b["regime"] == "unknown").values
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday.values
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year.values
            for h in (3, 5, 10):
                f = c.shift(-h) / c - 1
                b[f"s{h}"] = (-(f - drift[(coin, h)])).values
                b[f"z{h}"] = b[f"s{h}"] / usual[(coin, h)]
            b["pos"] = np.arange(len(b))
            b["coin"] = coin; b["win"] = w
            b["alloc"] = b["postRebalance_current_allocation"].astype(float)
            b["gain"] = b["alloc"] * (c.shift(-1) / c - 1)
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    P = B[B["inprof"]]
    out["in-profile share / bars by coin"] = P.groupby("coin").size()
    out["in-profile share"] = float(B["inprof"].mean())
    def tt(x):
        x = x.dropna()
        return (len(x), x.mean(), x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan)
    feats = ["dz", "runlen", "runz", "clv", "rngz", "volrel", "dist20", "ret5z", "ret60"]
    res = []
    for h in (3, 5, 10):
        G = P[P["pos"] % h == 0]
        n, m, t = tt(G[f"s{h}"])
        res.append(["ALL", h, n, m, t, np.nan, np.nan])
        for f in feats:
            g = G.dropna(subset=[f, f"z{h}"])
            rho, p = stats.spearmanr(g[f], g[f"z{h}"])
            res.append([f, h, len(g), np.nan, np.nan, rho, p])
    out["short excess vs features (grid, in profile)"] = pd.DataFrame(res, columns=["feat", "h", "n", "mean", "t", "spearman", "p"])
    q = []
    for f in ["dz", "clv", "dist20", "ret5z", "runz", "volrel", "rngz"]:
        G = P[P["pos"] % 5 == 0].dropna(subset=[f, "s5"])
        G = G.assign(qq=pd.qcut(G[f].rank(method="first"), 4, labels=False))
        a = G.groupby("qq")["s5"].agg(["count", "mean", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["feat"] = f
        q.append(a.reset_index())
    out["quartiles h5 short excess"] = pd.concat(q)[["feat", "qq", "count", "mean", "t"]]
    a = []
    for prof, D in (("in", P), ("out", B[~B["inprof"]])):
        fd = D[(D["dz"] < 0) & (D["runlen"] >= 2)]
        for h in (3, 5, 10):
            g = fd.dropna(subset=[f"s{h}"]).copy()
            g["cell"] = g["pos"] // h
            g = g.drop_duplicates(["coin", "win", "cell"])
            n, m, t = tt(g[f"s{h}"])
            rho = stats.spearmanr(g["runz"], g[f"s{h}"])[0] if n > 5 else np.nan
            a.append([prof, h, n, m, t, rho])
    out["first down after run>=2 (in vs out profile)"] = pd.DataFrame(a, columns=["prof", "h", "n", "mean", "t", "rho_runz"])
    G = P[P["pos"] % 5 == 0].dropna(subset=["s5"])
    out["weekday h5 in profile"] = G.groupby("wd")["s5"].agg(["count", "mean"])
    out["coin h5 in profile"] = G.groupby("coin")["s5"].agg(["count", "mean"])
    out["year h5 in profile"] = G.groupby("yr")["s5"].agg(["count", "mean"])
    # large up days in profile -> short?
    u = P[P["pos"] % 3 == 0].dropna(subset=["dz", "s3", "s10"])
    u = u.assign(bk=pd.cut(u["dz"], [-99, -1.5, -0.5, 0.5, 1.5, 99]))
    out["dz bucket: short excess h3, h10"] = u.groupby("bk")[["s3", "s10"]].agg(["count", "mean"])
    # book: largest gain and loss days
    H = B[B["alloc"].abs() > 0].dropna(subset=["gain"])
    H = H.assign(gq=pd.qcut(H["gain"].rank(method="first"), 5, labels=False))
    out["book bars by gain quintile"] = H.groupby("gq")[["gain", "dz", "clv", "runlen", "ret5z", "rngz", "volrel"]].mean()
    return out
