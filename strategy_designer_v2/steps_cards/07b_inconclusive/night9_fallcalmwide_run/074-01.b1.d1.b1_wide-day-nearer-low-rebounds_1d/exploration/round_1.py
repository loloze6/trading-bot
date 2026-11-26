def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    allret = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            rs.append(pd.Series(c).pct_change().dropna().values)
        allret[coin] = np.concatenate(rs).mean()
    for coin, wins in bars.items():
        mu = allret[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            r1 = pd.Series(c).pct_change()
            sd = r1.rolling(30).std()
            rng = (h - l) / c / sd
            loc = (h - c) / (h - l)
            n = len(df)
            for i in np.where(df["forecast"].values > 0)[0]:
                rec = {"coin": coin, "w": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                       "day": str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                       "fc": df["forecast"].iloc[i], "rng": rng.iloc[i], "loc": loc[i],
                       "r0": c[i] / c[i-1] - 1 if i > 0 else np.nan}
                for H in [1, 2, 3, 5, 10]:
                    rec[f"x{H}"] = (c[i+H] / c[i] - 1 - H * mu) if i + H < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="x1"):
        s = g[col].dropna()
        if len(s) < 3: return pd.Series({"n": len(s), "mean": s.mean(), "t": np.nan})
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s)))})
    out = {}
    out["horizons"] = pd.DataFrame({H: summ(d, f"x{H}") for H in [1, 2, 3, 5, 10]}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_window"] = d.groupby("w").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["locq"] = pd.qcut(d["loc"], 4, labels=False, duplicates="drop")
    d["rngq"] = pd.qcut(d["rng"], 4, labels=False, duplicates="drop")
    d["r0q"] = pd.qcut(d["r0"], 4, labels=False, duplicates="drop")
    out["by_loc_q"] = d.groupby("locq").apply(summ).join(d.groupby("locq")["loc"].mean())
    out["by_rng_q"] = d.groupby("rngq").apply(summ).join(d.groupby("rngq")["rng"].mean())
    out["by_r0_q"] = d.groupby("r0q").apply(summ).join(d.groupby("r0q")["r0"].mean())
    out["by_rng_q_x3"] = d.groupby("rngq").apply(lambda g: summ(g, "x3"))
    out["by_loc_q_x3"] = d.groupby("locq").apply(lambda g: summ(g, "x3"))
    out["corr"] = pd.DataFrame({"rng_x1": [stats.spearmanr(d["rng"], d["x1"], nan_policy="omit")[0]],
                                "loc_x1": [stats.spearmanr(d["loc"], d["x1"], nan_policy="omit")[0]],
                                "r0_x1": [stats.spearmanr(d["r0"], d["x1"], nan_policy="omit")[0]]})
    out["n_days"] = d["day"].nunique()
    return out
