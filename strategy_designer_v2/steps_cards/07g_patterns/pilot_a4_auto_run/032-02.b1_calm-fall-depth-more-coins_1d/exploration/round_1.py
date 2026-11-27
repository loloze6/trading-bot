def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            inprof = (b["regime"] == "unknown").values
            ret1 = c.pct_change()
            for h in (1, 3, 5):
                b[f"f{h}"] = c.shift(-h) / c - 1
            b["r1"] = ret1
            b["r3"] = c / c.shift(3) - 1
            b["r10"] = c / c.shift(10) - 1
            b["depth"] = c / c.rolling(30, min_periods=10).max() - 1
            b["lowdist"] = c / c.rolling(30, min_periods=10).min() - 1
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["clpos"] = (b["close"] - b["low"]) / rng
            b["rngrel"] = (rng / c) / (rng / c).rolling(20, min_periods=10).mean()
            b["volrel"] = b["volume"] / b["volume"].rolling(20, min_periods=10).mean()
            b["vol10"] = ret1.rolling(10, min_periods=5).std() / ret1.rolling(60, min_periods=20).std()
            b["wd"] = ts.dt.weekday
            b["inprof"] = inprof
            b["coin"] = coin; b["win"] = w
            b["day"] = ts.dt.floor("D")
            b["pos"] = np.arange(n)
            rows.append(b)
    df = pd.concat(rows, ignore_index=True)
    out = {}
    # drift per coin, 3-bar grid over all windows
    g3 = df[(df.pos % 3 == 0) & df.f3.notna()]
    drift = g3.groupby("coin").f3.mean()
    out["drift3_by_coin"] = drift
    df["ex3"] = df.f3 - df.coin.map(drift)
    g3 = df[(df.pos % 3 == 0) & df.f3.notna()]
    p = g3[g3.inprof]
    out["n_inprof_grid_by_coin"] = p.groupby("coin").size()
    out["inprof_ex3_mean_t"] = pd.Series({"mean": p.ex3.mean(), "t": stats.ttest_1samp(p.ex3, 0).statistic, "n": len(p)})
    res = {}
    for f in ["depth", "lowdist", "r1", "r3", "r10", "clpos", "rngrel", "volrel", "vol10"]:
        q = p[[f, "ex3"]].dropna()
        if len(q) < 30: continue
        q = q.copy(); q["qt"] = pd.qcut(q[f], 4, labels=False, duplicates="drop")
        m = q.groupby("qt").ex3.mean()
        r, pv = stats.spearmanr(q[f], q.ex3)
        res[f] = {"Q1": m.get(0), "Q2": m.get(1), "Q3": m.get(2), "Q4": m.get(3), "rho": r, "p": pv, "n": len(q)}
    out["inprof_quartiles_ex3"] = pd.DataFrame(res).T
    out["inprof_by_weekday"] = p.groupby("wd").ex3.agg(["mean", "count"])
    out["inprof_by_window"] = p.groupby("win").ex3.agg(["mean", "count"])
    # 1-day grid for next-day effects
    d1 = df[df.f1.notna() & df.inprof].copy()
    res1 = {}
    for f in ["depth", "r1", "r3", "clpos", "volrel", "rngrel"]:
        q = d1[[f, "f1"]].dropna()
        r, pv = stats.spearmanr(q[f], q.f1)
        res1[f] = {"rho": r, "p": pv, "n": len(q)}
    out["inprof_next_day_rho"] = pd.DataFrame(res1).T
    out["outprof_ex3_mean"] = pd.Series({"mean": g3[~g3.inprof].ex3.mean(), "n": (~g3.inprof).sum()})
    return out
