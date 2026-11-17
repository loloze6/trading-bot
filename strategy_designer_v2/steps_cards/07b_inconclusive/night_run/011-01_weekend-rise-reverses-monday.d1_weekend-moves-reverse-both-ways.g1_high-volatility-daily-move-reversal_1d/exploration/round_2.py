def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            c = b["close"].astype(float).values
            n = len(c)
            r = np.full(n, np.nan); r[1:] = c[1:]/c[:-1]-1
            nxt = np.full(n, np.nan); nxt[:-1] = c[1:]/c[:-1]-1
            vol = pd.Series(r).rolling(20, min_periods=20).std().values
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "win": w, "r": r, "nxt": nxt - mu, "z": r/vol,
                "alloc": b["postRebalance_current_allocation"].astype(float).values,
                "act": (b["regime"] == "mean_reversion").values,
                "wd": ts.dt.weekday.values, "year": ts.dt.year.values}))
    d = pd.concat(rows, ignore_index=True).dropna(subset=["r", "nxt"])
    d = d[d.r != 0]
    d["rev"] = -np.sign(d.r) * d.nxt
    d["down"] = d.r < 0
    a = d[d.act]

    def dd(g):
        x = g.loc[g.down, "rev"].dropna(); y = g.loc[~g.down, "rev"].dropna()
        return pd.Series({"n_down": len(x), "n_up": len(y), "diff": x.mean()-y.mean(),
                          "welch_t": stats.ttest_ind(x, y, equal_var=False).statistic})
    out = {}
    out["down-up all active"] = dd(a)
    a = a.assign(big=a.z.abs() >= 1)
    out["down-up by |z|>=1"] = a.groupby("big").apply(dd)
    out["down-up by year"] = a.groupby("year").apply(dd)
    out["down-up big by year"] = a[a.big].groupby("year").apply(dd)
    out["down-up by weekend-move (Sat/Sun bars)"] = a.assign(we=a.wd >= 5).groupby("we").apply(dd)
    # graded: rev regressed on |z| by side, active
    res = {}
    for s, g in a.groupby("down"):
        g = g.dropna(subset=["z", "rev"])
        lr = stats.linregress(g.z.abs(), g.rev)
        res["down" if s else "up"] = pd.Series({"slope": lr.slope, "t": lr.slope/lr.stderr, "n": len(g)})
    out["rev on |z| slope by side"] = pd.DataFrame(res)
    return out
