def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 3
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            idx = np.arange(0, len(b) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            rng = (b["high"] - b["low"]) / c
            f = pd.DataFrame({
                "r1": c.pct_change(1), "r3": c.pct_change(3), "r7": c.pct_change(7),
                "r14": c.pct_change(14), "r30": c.pct_change(30),
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "rngrel": rng / rng.rolling(30).mean(),
                "volrel": b["volume"] / b["volume"].rolling(30).mean(),
                "dist20hi": c / b["high"].rolling(20).max() - 1,
                "dist20lo": c / b["low"].rolling(20).min() - 1,
                "vol30": c.pct_change().rolling(30).std(),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "inprof": (b["regime"] == "unknown").astype(int),
                "fc": b["forecast"],
            })
            f["r7s"] = f["r7"] / rng.rolling(30).mean()
            f["fwd"] = c.shift(-H) / c - 1
            f["fwd1"] = c.shift(-1) / c - 1
            f["coin"] = coin; f["w"] = w
            idx = np.arange(0, len(b) - H, H)
            g = f.iloc[idx].copy()
            g["short_unusual"] = -(g["fwd"] - drift[coin])
            rows.append(g)
    d = pd.concat(rows)
    p = d[d["inprof"] == 1].dropna(subset=["short_unusual"])
    out = {"n_grid_all": len(d), "n_grid_profile": len(p),
           "profile_mean_short_unusual": p["short_unusual"].mean(),
           "profile_t": stats.ttest_1samp(p["short_unusual"], 0).statistic}
    res = []
    for feat in ["r1", "r3", "r7", "r14", "r30", "r7s", "clv", "rngrel", "volrel", "dist20hi", "dist20lo", "vol30"]:
        q = p.dropna(subset=[feat])
        try:
            qb = pd.qcut(q[feat], 5, labels=False, duplicates="drop")
        except Exception:
            continue
        for k, grp in q.groupby(qb):
            x = grp["short_unusual"]
            res.append({"feat": feat, "q": k, "n": len(x), "featmean": grp[feat].mean(),
                        "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
        rr = stats.spearmanr(q[feat], q["short_unusual"])
        res.append({"feat": feat, "q": "rho", "n": len(q), "featmean": np.nan, "mean": rr.correlation, "t": rr.pvalue})
    out["quintiles_in_profile"] = pd.DataFrame(res).iloc[:40]
    out["quintiles_rest"] = pd.DataFrame(res).iloc[40:80]
    wdg = p.groupby("wd")["short_unusual"].agg(["count", "mean", "std"])
    wdg["t"] = wdg["mean"] / (wdg["std"] / np.sqrt(wdg["count"]))
    out["weekday"] = wdg
    cw = p.groupby(["coin"])["short_unusual"].agg(["count", "mean"])
    out["by_coin"] = cw
    ww = p.groupby("w")["short_unusual"].agg(["count", "mean"])
    out["by_window"] = ww
    return out
