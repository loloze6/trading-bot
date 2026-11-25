def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:] / c[:-1] - 1)
        drift = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c / c.shift(1) - 1
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            n1 = c.shift(-1) / c - 1
            n2 = c.shift(-2) / c - 1
            n3 = c.shift(-3) / c - 1
            pos = b["postRebalance_current_allocation"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "year": ts.dt.year, "regime": b["regime"].astype(str),
                               "z": z, "n1": n1 - drift, "n2": n2 - 2 * drift, "n3": n3 - 3 * drift, "pos": pos,
                               "gain": pos * (n1 - drift), "pos_i": np.arange(len(b)), "day": ts.dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["inprof"] = d["regime"].isin(["mean_reversion", "unknown"])
    d["zb"] = pd.cut(d["z"], [-np.inf, -2, -1, -0.5, 0, 0.33, 0.66, 1, 2, np.inf])

    def summ(g, col="n1"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean() if n else np.nan,
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    out = {}
    out["regime counts"] = d["regime"].value_counts()
    out["n1 by zbucket in profile"] = d[d.inprof].groupby("zb", observed=True).apply(summ)
    out["n1 by zbucket out of profile"] = d[~d.inprof].groupby("zb", observed=True).apply(summ)
    mr = d[d.regime == "mean_reversion"]
    out["MR n1 by coin"] = mr.groupby("coin").apply(summ)
    out["MR n1 by window"] = mr.groupby("win").apply(summ)
    out["MR n1 by year"] = mr.groupby("year").apply(summ)
    act = d[d.pos.abs() > 0]
    out["gain on active bars by coin"] = act.groupby("coin").apply(lambda g: summ(g, "gain"))
    out["gain on active bars by window"] = act.groupby("win").apply(lambda g: summ(g, "gain"))
    # horizons on non-overlapping grid, in-profile rises in (0,1]
    hz = {}
    for h, col in [(1, "n1"), (2, "n2"), (3, "n3")]:
        g = mr[mr.pos_i % h == 0][col].dropna()
        hz[f"h{h}"] = pd.Series({"n": len(g), "mean% (short side = -mean)": 100 * g.mean(),
                                 "t": g.mean() / (g.std() / np.sqrt(len(g)))})
    out["MR horizons"] = pd.DataFrame(hz).T
    # slope within MR
    m = mr.dropna(subset=["z", "n1"])
    sl = stats.linregress(m["z"], m["n1"])
    out["MR slope n1 on z"] = pd.Series({"slope%": 100 * sl.slope, "t": sl.slope / sl.stderr, "n": len(m)})
    # MR vs unknown-in-profile
    ub = d[(d.regime == "unknown")]["n1"].dropna()
    tt = stats.ttest_ind(mr["n1"].dropna(), ub, equal_var=False)
    out["MR minus other in-profile n1"] = pd.Series({"diff%": 100 * (mr["n1"].mean() - ub.mean()), "t": tt.statistic})
    # share of MR bars with zero position
    out["MR bars with zero position share"] = float((mr.pos.abs() == 0).mean())
    return out
