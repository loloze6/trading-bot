def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); lo = b["low"].astype(float)
            ret30 = c / c.shift(30) - 1
            low10 = lo.shift(1).rolling(10).min()
            depth = c / low10 - 1
            r1 = np.log(c).diff().abs().rolling(20).mean()
            vol20 = c.pct_change().rolling(20).std()
            vol60 = c.pct_change().rolling(60).std()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "ret30": ret30, "depth": depth, "volratio": vol20 / vol60,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            for h in [1, 2, 3, 5, 10]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mean1 = d.groupby("coin")["f1"].mean()
    out = {}
    sit = d[(d.ret30 < 0) & (d.depth < 0)].copy()
    for h in [1, 2, 3, 5, 10]:
        drift = d[d.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        sit[f"x{h}"] = sit[f"f{h}"] - sit.coin.map(drift)
    # horizons on non-overlap grid
    hz = []
    for h in [1, 2, 3, 5, 10]:
        s = sit[sit.pos % h == 0][f"x{h}"].dropna()
        hz.append({"h": h, "n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s)))})
    out["horizons_situation_excess"] = pd.DataFrame(hz)
    s1 = sit.dropna(subset=["x1"])
    def g(col):
        return s1.groupby(col)["x1"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))]).rename(columns={"<lambda_0>": "t"})
    out["by_coin"] = g("coin")
    out["by_year"] = g("year")
    s1["dq"] = pd.qcut(s1.depth, 5, labels=False)
    out["by_depth_quintile_(0=deepest)"] = s1.groupby("dq").agg(n=("x1", "count"), mean=("x1", "mean"), depthmean=("depth", "mean"), x3=("x3", "mean"), x5=("x5", "mean"))
    s1["vq"] = pd.qcut(s1.volratio, 3, labels=False)
    out["by_volratio_tercile"] = s1.groupby("vq").agg(n=("x1", "count"), mean=("x1", "mean"), x3=("x3", "mean"), x5=("x5", "mean"))
    s1["rq"] = pd.qcut(s1.ret30, 3, labels=False)
    out["by_ret30_tercile_(0=most fallen)"] = s1.groupby("rq").agg(n=("x1", "count"), mean=("x1", "mean"), x3=("x3", "mean"), x5=("x5", "mean"))
    held = s1[s1.alloc > 0]
    out["held_vs_notheld"] = pd.DataFrame({"n": [len(held), len(s1) - len(held)], "mean": [held.x1.mean(), s1[s1.alloc <= 0].x1.mean()]}, index=["held", "not"])
    # median & trimmed
    out["x1_median_and_skew"] = pd.Series({"median": s1.x1.median(), "skew": s1.x1.skew(), "mean_trim5": stats.trim_mean(s1.x1, 0.05)})
    # first break (fresh) vs continuing
    out["corr_depth_x1_spearman"] = stats.spearmanr(s1.depth, s1.x1).correlation
    return out
