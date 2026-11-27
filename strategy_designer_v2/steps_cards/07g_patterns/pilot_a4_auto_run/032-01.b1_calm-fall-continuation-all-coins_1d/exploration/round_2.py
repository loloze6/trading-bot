def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "r1": (c.shift(-1)/c - 1).values,
                "r5": (c.shift(-5)/c - 1).values,
                "r10": (c.shift(-10)/c - 1).values,
                "ret30": (c/c.shift(30) - 1).values,
                "ret60": (c/c.shift(60) - 1).values,
                "pos30": ((c - c.rolling(30).min())/(c.rolling(30).max()-c.rolling(30).min())).values,
                "wd": ts.dt.weekday.values,
                "day": ts.dt.floor("D").values,
                "inprof": (b["regime"] == "unknown").values,
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 5, 10):
        g = D[D["pos"] % h == 0].groupby("coin")["r%d" % h].mean()
        D["x%d" % h] = D["r%d" % h] - D["coin"].map(g)
    F = D[D["inprof"]].copy()
    out = {}
    # weekday: in profile vs outside, Welch t vs other weekdays
    res = []
    for prof, S in (("in", F), ("out", D[~D["inprof"]])):
        S = S.dropna(subset=["x1"])
        for wd in range(7):
            a = S[S["wd"] == wd]["x1"]; o = S[S["wd"] != wd]["x1"]
            t = stats.ttest_ind(a, o, equal_var=False).statistic
            res.append([prof, wd, a.mean(), len(a), t])
    out["weekday x1 welch"] = pd.DataFrame(res, columns=["prof", "wd", "mean", "n", "t_vs_rest"])
    # longer horizons by ret30 and ret60 (grid), spearman
    res = []
    for h in (5, 10):
        S = F[F["pos"] % h == 0]
        for col in ("ret30", "ret60", "pos30"):
            T = S.dropna(subset=[col, "x%d" % h])
            r, p = stats.spearmanr(T[col], T["x%d" % h])
            m = T["x%d" % h].mean(); s = T["x%d" % h].std()
            res.append([h, col, len(T), r, p, m, m/(s/np.sqrt(len(T)))])
    out["long horizon rho"] = pd.DataFrame(res, columns=["h", "col", "n", "rho", "p", "mean_x", "t_mean"])
    # by window: mean x1 in profile
    out["x1 by window in profile"] = F.groupby("win")["x1"].agg(["mean", "count"])
    return out
