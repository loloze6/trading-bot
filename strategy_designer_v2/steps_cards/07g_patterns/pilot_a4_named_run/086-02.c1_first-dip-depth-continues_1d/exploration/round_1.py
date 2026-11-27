def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=15).std()
            fwd = c.shift(-H) / c - 1
            # up/down run length ending at bar
            up = (r1 > 0).astype(int)
            run = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            dn = (r1 < 0).astype(int)
            drun = dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn
            ret5 = c / c.shift(5) - 1
            ret10 = c / c.shift(10) - 1
            hi20 = c.rolling(20, min_periods=10).max()
            dhi = (c / hi20 - 1) / sd30
            rng = (b["high"] - b["low"]) / c / sd30
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            vol = b["volume"].astype(float)
            vrel = vol / vol.rolling(20, min_periods=10).mean()
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "inprof": b["regime"].astype(str) != "chop",
                "regime": b["regime"].astype(str),
                "fwd": fwd, "z1": r1 / sd30, "run": run, "drun": drun,
                "z5": ret5 / (sd30 * np.sqrt(5)), "z10": ret10 / (sd30 * np.sqrt(10)),
                "dhi": dhi, "rng": rng, "clpos": clpos, "vrel": vrel, "wd": wd,
                "sd30": sd30, "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    allgrid = d[d["pos"] % H == 0].dropna(subset=["fwd"])
    drift = allgrid.groupby("coin")["fwd"].mean()
    d["short_unusual"] = -(d["fwd"] - d["coin"].map(drift))
    g = d[(d["pos"] % H == 0)].dropna(subset=["fwd"])
    gp = g[g["inprof"]]
    out = {}
    out["profile share by coin"] = g.groupby("coin")["inprof"].agg(["mean", "size"])
    out["regime counts"] = d["regime"].value_counts()
    def summ(x, col):
        def f(s):
            v = s["short_unusual"].dropna()
            n = len(v)
            return pd.Series({"n": n, "mean": v.mean(), "t": v.mean() / (v.std() / np.sqrt(n)) if n > 2 else np.nan})
        return x.groupby(col).apply(f)
    out["inprof vs out"] = summ(g, "inprof")
    for col in ["z1", "z5", "z10", "dhi", "rng", "clpos", "vrel"]:
        q = gp.copy()
        q["b"] = pd.qcut(q[col], 4, labels=False, duplicates="drop")
        out["prof quartile " + col] = summ(q, "b")
    q = gp.copy(); q["b"] = q["run"].clip(upper=4)
    out["prof uprun"] = summ(q, "b")
    q = gp.copy(); q["b"] = q["drun"].clip(upper=3)
    out["prof downrun"] = summ(q, "b")
    out["prof weekday"] = summ(gp, "wd")
    out["prof by coin"] = summ(gp, "coin")
    # correlations in profile
    cs = {}
    for col in ["z1", "z5", "z10", "dhi", "rng", "clpos", "vrel"]:
        s = gp[[col, "short_unusual"]].dropna()
        cs[col] = stats.spearmanr(s[col], s["short_unusual"])[0]
        cs[col + "_n"] = len(s)
    out["prof spearman"] = pd.Series(cs)
    return out
