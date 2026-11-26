def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l).replace(0, np.nan)
            f = b["forecast"].astype(float).fillna(0)
            df = pd.DataFrame({"coin": coin, "win": w,
                               "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "ts": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "loc": (c - l) / rng, "r1": c / c.shift(1) - 1,
                               "wick": (h - c) / c, "rngpct": rng / c,
                               "n1": c.shift(-1) / c - 1,
                               "case": (-(f - f.shift(1).fillna(0))) >= 2,
                               "regime": b["regime"].astype(str)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    dr = d.groupby("coin")["n1"].mean()
    d["u"] = -(d["n1"] - d["coin"].map(dr))
    d = d.dropna(subset=["u", "loc", "r1"])
    def summ(x):
        n = len(x)
        if n < 5: return pd.Series({"n": n, "days": np.nan, "mean": np.nan, "t": np.nan})
        m = x["u"].mean()
        dev = (x["u"] - m).groupby(x["ts"]).sum(); G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n
        return pd.Series({"n": n, "days": G, "mean": m, "t": m / se})
    out = {}
    cs = d[d["case"]].copy()
    med = cs["loc"].median()
    cs["half"] = np.where(cs["loc"] > med, "upper", "lower")
    lo = cs[cs["half"] == "lower"]["u"]; hi = cs[cs["half"] == "upper"]["u"]
    out["cases_lower_minus_upper"] = pd.Series({"median_loc": med, "diff": lo.mean() - hi.mean(),
                                                "welch_t": stats.ttest_ind(lo, hi, equal_var=False)[0]})
    out["cases_half_by_year"] = cs.groupby(["half", "year"]).apply(summ)
    out["cases_half_by_coin"] = cs.groupby(["half", "coin"]).apply(summ)
    cc = cs.dropna(subset=["wick"])
    out["cases_spearman"] = pd.Series({"loc_vs_u": stats.spearmanr(cc["loc"], cc["u"])[0],
                                       "wick_vs_u": stats.spearmanr(cc["wick"], cc["u"])[0],
                                       "rng_vs_u": stats.spearmanr(cc["rngpct"], cc["u"])[0], "n": len(cc)})
    cc["wq"] = pd.qcut(cc["wick"], 4, labels=False)
    out["cases_by_wick_quartile"] = cc.groupby("wq").apply(summ)
    return out
