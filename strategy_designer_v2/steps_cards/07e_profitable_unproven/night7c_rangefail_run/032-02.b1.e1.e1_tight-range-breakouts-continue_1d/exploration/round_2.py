def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    coins = list(bars.keys())
    recs = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"]
            hi = cl.shift(1).rolling(60).max(); lo = cl.shift(1).rolling(60).min()
            mad = cl.pct_change().abs().rolling(60).mean()
            W = (hi - lo) / cl / mad
            dist = cl / hi - 1
            vol = cl.pct_change().rolling(60).std()
            r60 = cl / cl.shift(60) - 1
            fc = b["forecast"]
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in [5, 10, 20]:
                fr = cl.shift(-h) / cl - 1
                idx = np.arange(len(b))
                df = pd.DataFrame({"brk": dist > 0, "fr": fr, "W": W, "lW": np.log(W), "dz": dist / vol, "r60": r60,
                                   "fc": fc, "cell": idx // h, "grid": (idx % h) == 0, "h": h, "coin": c, "win": w,
                                   "ts": b["timestamp"], "year": yr})
                recs.append(df)
    R = pd.concat(recs, ignore_index=True)
    drift = R[R.grid].dropna(subset=["fr"]).groupby(["coin", "h"])["fr"].mean()
    R["drift"] = [drift.get((c, h), np.nan) for c, h in zip(R.coin, R.h)]
    R["un"] = R.fr - R.drift
    cases = R[R.brk].dropna(subset=["fr", "W", "r60"]).groupby(["coin", "win", "h", "cell"]).first().reset_index()

    def clustered_slope(g, x):
        X = np.column_stack([np.ones(len(g)), g[x].values]); y = g.un.values
        beta = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ beta
        XtX = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, ix in g.groupby("ts").indices.items():
            s = X[ix].T @ e[ix]; meat += np.outer(s, s)
        V = XtX @ meat @ XtX
        return beta[1], beta[1] / np.sqrt(V[1, 1])
    res = []
    for h, g in cases.groupby("h"):
        row = {"h": h, "n": len(g), "corr_fc_W": stats.spearmanr(g.fc, g.W)[0]}
        for x in ["lW", "dz", "r60", "fc"]:
            s, t = clustered_slope(g, x); row["slope_" + x] = s; row["t_" + x] = t
        res.append(row)
    out["break cases: slopes, day-clustered t"] = pd.DataFrame(res).set_index("h")
    # non-break grid bars: does narrow range predict anything there? (h20)
    a = R[(R.h == 20) & R.grid & (~R.brk)].dropna(subset=["fr", "W"]).copy()
    a["q"] = pd.qcut(a.W, 3, labels=False)
    out["h20 non-break grid by W tercile"] = a.groupby("q").agg(n=("un", "size"), mean_un=("un", "mean"), W=("W", "mean"))
    # break cases h10 by year and by W tercile
    g = cases[cases.h == 10].copy()
    out["h10 cases by year"] = g.groupby("year").agg(n=("un", "size"), mean_un=("un", "mean"),
                                                     corr_W=("W", lambda s: stats.spearmanr(s, g.loc[s.index, "un"])[0]))
    g["q"] = pd.qcut(g.W, 3, labels=False)
    out["h10 cases by W tercile"] = g.groupby("q").agg(n=("un", "size"), mean_un=("un", "mean"), med_un=("un", "median"), W=("W", "mean"))
    g5 = cases[cases.h == 5].copy(); g5["q"] = pd.qcut(g5.W, 3, labels=False)
    out["h5 cases by W tercile"] = g5.groupby("q").agg(n=("un", "size"), mean_un=("un", "mean"), med_un=("un", "median"), W=("W", "mean"))
    # first break after a no-break stretch vs repeated breaks (h10)
    return out
