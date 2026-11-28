def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(df)),
                              "fc": df["forecast"].astype(float),
                              "alloc": df["postRebalance_current_allocation"].astype(float),
                              "inprof": (df["regime"] == "unknown").astype(int),
                              "yr": pd.to_datetime(df["timestamp"]).dt.year})
            for k in [3, 7, 14, 30]:
                d[f"r{k}"] = c / c.shift(k) - 1
            d["vol14"] = np.log(c).diff().rolling(14).std()
            for h in [1, 3, 5, 10]:
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # drift per coin
    drift = {}
    for h in [1, 3, 5, 10]:
        g = A[A.pos % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
    res = []
    for h in [1, 3, 5, 10]:
        g = A[(A.pos % h == 0)].copy()
        g["ex"] = g[f"f{h}"] - g.coin.map(drift[h])
        for prof in [1, 0]:
            s = g[(g.inprof == prof)].dropna(subset=["ex", "r30"])
            fallen = s[s.r30 < 0]
            rho, p = stats.spearmanr(fallen.r30, fallen.ex) if len(fallen) > 10 else (np.nan, np.nan)
            m = fallen.ex.mean(); t = m / (fallen.ex.std() / np.sqrt(len(fallen)))
            res.append({"h": h, "inprof": prof, "n": len(fallen), "mean_ex": m, "t": t, "spearman_r30_ex": rho, "p": p})
    out["excess_after_fall_by_horizon_profile"] = pd.DataFrame(res)
    # in-profile, terciles of r30, horizons
    res = []
    for h in [1, 3, 5, 10]:
        g = A[(A.pos % h == 0) & (A.inprof == 1)].copy()
        g["ex"] = g[f"f{h}"] - g.coin.map(drift[h])
        g = g.dropna(subset=["ex", "r30"])
        g["q"] = pd.qcut(g.r30, 3, labels=["deep", "mid", "shallow"])
        for q, s in g.groupby("q", observed=True):
            res.append({"h": h, "q": q, "n": len(s), "r30": s.r30.mean(), "mean_ex": s.ex.mean(),
                        "t": s.ex.mean() / (s.ex.std() / np.sqrt(len(s)))})
    out["inprof_r30_terciles"] = pd.DataFrame(res)
    # by coin and year, h=5
    h = 5
    g = A[(A.pos % h == 0) & (A.inprof == 1)].copy()
    g["ex"] = g[f"f{h}"] - g.coin.map(drift[h])
    g = g.dropna(subset=["ex", "r30"])
    out["h5_by_coin"] = g.groupby("coin").agg(n=("ex", "size"), mean_ex=("ex", "mean"), r30=("r30", "mean"))
    out["h5_by_year"] = g.groupby("yr").agg(n=("ex", "size"), mean_ex=("ex", "mean"))
    # other situation measures in-profile: short-term fall r3, r7, r14 vs fwd
    res = []
    for h in [1, 3, 5]:
        g = A[(A.pos % h == 0) & (A.inprof == 1)].copy()
        g["ex"] = g[f"f{h}"] - g.coin.map(drift[h])
        for k in ["r3", "r7", "r14", "r30", "vol14"]:
            s = g.dropna(subset=["ex", k])
            rho, p = stats.spearmanr(s[k], s.ex)
            res.append({"h": h, "x": k, "n": len(s), "spearman": rho, "p": p})
    out["inprof_spearman_predictors"] = pd.DataFrame(res)
    out["share_in_profile"] = A.inprof.mean()
    return out
