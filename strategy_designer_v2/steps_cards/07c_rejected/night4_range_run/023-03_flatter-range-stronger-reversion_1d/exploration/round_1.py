def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            n = len(c)
            H = c.rolling(30).max(); L = c.rolling(30).min()
            pos = (c - L) / (H - L)
            d = 2 * pos - 1
            net = (c - c.shift(30)) / (H - L)
            flat = 1 - net.abs()
            r30 = c / c.shift(30) - 1
            fc = df["forecast"].astype(float).reset_index(drop=True)
            for i in range(0, n, 5):
                rec = dict(coin=coin, w=w, year=ts[i].year, d=d[i], flat=flat[i], netsigned=net[i], r30=r30[i], fc=fc[i])
                for h in (1, 3, 5, 10, 20):
                    rec["r%d" % h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    g = pd.DataFrame(rows).dropna(subset=["d", "flat"])
    out = {}
    # drift per coin per horizon (all grid)
    for h in (1, 3, 5, 10, 20):
        g["x%d" % h] = g["r%d" % h] - g.groupby("coin")["r%d" % h].transform("mean")
    # signed: return in the direction AWAY from middle (continuation) = sign(d)*x
    def tstat(s):
        s = s.dropna(); return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))), "n": len(s)})
    hz = {}
    for h in (1, 3, 5, 10, 20):
        hz["h%d" % h] = tstat(np.sign(g["d"]) * g["x%d" % h])
    out["continuation_away_from_mid_by_horizon"] = pd.DataFrame(hz).T
    g["fq"] = pd.qcut(g["flat"], 4, labels=["q1_trendiest", "q2", "q3", "q4_flattest"])
    g["dq"] = pd.qcut(g["d"].abs(), 3, labels=["near", "mid", "far"])
    tab = g.groupby(["fq"]).apply(lambda x: tstat(np.sign(x["d"]) * x["x5"]))
    out["cont5_by_flatness"] = tab
    out["cont5_by_dist"] = g.groupby("dq").apply(lambda x: tstat(np.sign(x["d"]) * x["x5"]))
    out["cont5_by_coin"] = g.groupby("coin").apply(lambda x: tstat(np.sign(x["d"]) * x["x5"]))
    out["cont5_by_year"] = g.groupby("year").apply(lambda x: tstat(np.sign(x["d"]) * x["x5"]))
    g["side"] = np.where(g["d"] > 0, "above_mid", "below_mid")
    out["cont5_by_side"] = g.groupby("side").apply(lambda x: tstat(np.sign(x["d"]) * x["x5"]))
    out["cont10_by_flat_x_dist"] = g.groupby(["fq", "dq"]).apply(lambda x: tstat(np.sign(x["d"]) * x["x10"])).unstack()["mean"]
    # 30-day momentum: signed by r30
    out["mom30_by_horizon"] = pd.DataFrame({ "h%d" % h: tstat(np.sign(g["r30"]) * g["x%d" % h]) for h in (5, 10, 20)}).T
    # graded: corr of d with x5
    out["spearman_d_x5"] = float(stats.spearmanr(g["d"], g["x5"], nan_policy="omit")[0])
    out["spearman_d_x10"] = float(stats.spearmanr(g["d"], g["x10"], nan_policy="omit")[0])
    return out
