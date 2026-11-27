def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        for h in (3, 5, 10):
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            up = (r > 0).astype(int)
            run = up.groupby((up == 0).cumsum()).cumsum()
            prevrun = run.shift(1)
            runret = (c.shift(1) / c.shift(1 + prevrun.fillna(0).astype(int).clip(lower=0)).values - 1)
            # simpler run return
            rr = []
            cv = c.values
            pr = prevrun.fillna(0).astype(int).values
            for i in range(len(cv)):
                k = pr[i]
                rr.append(cv[i - 1] / cv[i - 1 - k] - 1 if i - 1 - k >= 0 and k > 0 else 0.0)
            b["runlen"] = pr
            b["runz"] = np.array(rr) / vol.values
            b["dz"] = r / vol
            rng = (b["high"] - b["low"])
            b["clv"] = (c - b["low"]) / rng.replace(0, np.nan)
            b["rngz"] = rng / c / vol
            b["volrel"] = b["volume"] / b["volume"].rolling(30, min_periods=10).median()
            b["dist20"] = (c / c.rolling(20, min_periods=10).max() - 1) / vol
            b["ret5z"] = (c / c.shift(5) - 1) / vol
            b["ret60"] = c / c.shift(60) - 1
            b["inprof"] = b["regime"] == "unknown"
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            for h in (3, 5, 10):
                f = c.shift(-h) / c - 1
                b[f"s{h}"] = -(f - drift[(coin, h)])
            b["pos"] = np.arange(len(b))
            b["coin"] = coin; b["win"] = w
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    P = B[B["inprof"]]
    out["in-profile share of bars"] = float(B["inprof"].mean())
    out["in-profile bars by coin"] = P.groupby("coin").size()
    feats = ["dz", "runlen", "runz", "clv", "rngz", "volrel", "dist20", "ret5z", "ret60"]
    res = []
    for h in (3, 5, 10):
        G = P[(P["pos"] % h == 0)].dropna(subset=[f"s{h}"])
        m = G[f"s{h}"]
        res.append(["ALL", h, len(G), m.mean(), m.mean() / m.std() * np.sqrt(len(m)), np.nan])
        for f in feats:
            g = G.dropna(subset=[f])
            rho, p = stats.spearmanr(g[f], g[f"s{h}"])
            res.append([f, h, len(g), np.nan, np.nan, rho])
    out["short excess vs features (grid, in profile)"] = pd.DataFrame(res, columns=["feat", "h", "n", "mean", "t", "spearman"])
    q = []
    for f in ["dz", "clv", "dist20", "ret5z", "runz", "volrel", "rngz"]:
        G = P[(P["pos"] % 5 == 0)].dropna(subset=[f, "s5"])
        G = G.assign(qq=pd.qcut(G[f], 4, labels=False, duplicates="drop"))
        a = G.groupby("qq")["s5"].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["feat"] = f
        q.append(a.reset_index())
    out["quartiles h5 short excess"] = pd.concat(q)[["feat", "qq", "count", "mean", "t"]]
    # first down day after run
    fd = P[(P["dz"] < 0) & (P["runlen"] >= 2)]
    a = []
    for h in (3, 5, 10):
        g = fd.dropna(subset=[f"s{h}"])
        g = g.assign(cell=g["pos"] // h).drop_duplicates(["coin", "win", "cell"])
        a.append([h, len(g), g[f"s{h}"].mean(), g[f"s{h}"].mean() / g[f"s{h}"].std() * np.sqrt(len(g)), stats.spearmanr(g["runz"], g[f"s{h}"])[0]])
    out["first down after run>=2"] = pd.DataFrame(a, columns=["h", "n", "mean", "t", "rho_runz"])
    G = P[P["pos"] % 5 == 0].dropna(subset=["s5"])
    out["weekday h5"] = G.groupby("wd")["s5"].agg(["count", "mean"])
    return out
