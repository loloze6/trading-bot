def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    mus = {}
    for coin, wins in bars.items():
        rs = [pd.Series(df["close"].values).pct_change().dropna().values for df in wins.values()]
        mus[coin] = np.concatenate(rs).mean()
    rows = []; base = []
    for coin, wins in bars.items():
        mu = mus[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            r1 = pd.Series(c).pct_change(); sd = r1.rolling(30).std()
            rng = (h - l) / c / sd; loc = (h - c) / (h - l)
            n = len(df)
            fc = df["forecast"].values
            for i in range(30, n - 1):
                rec = {"coin": coin, "w": w, "day": str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                       "case": fc[i] > 0, "rng": rng.iloc[i], "loc": loc[i]}
                for H in [1, 3, 5]:
                    rec[f"x{H}"] = (c[i+H] / c[i] - 1 - H * mu) if i + H < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def ct(g, col):
        g = g.dropna(subset=[col])
        if len(g) < 3: return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean": g[col].mean(), "t_day": np.nan})
        m = g[col].mean()
        s = (g[col] - m).groupby(g["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(g)
        return pd.Series({"n": len(g), "days": G, "mean": m, "t_day": m / se})
    cs = d[d["case"]].copy()
    out = {}
    out["cases_clustered"] = pd.DataFrame({f"x{H}": ct(cs, f"x{H}") for H in [1, 3, 5]}).T
    cs["locq"] = pd.qcut(cs["loc"], 4, labels=False, duplicates="drop")
    out["locq_x1_clustered"] = cs.groupby("locq").apply(lambda g: ct(g, "x1"))
    out["locq_x3_clustered"] = cs.groupby("locq").apply(lambda g: ct(g, "x3"))
    # all non-case wide low-close days (any profile, approx) for contrast
    nc = d[(~d["case"]) & (d["rng"] >= 2) & (d["loc"] >= 0.5)]
    out["wide_lowclose_not_case"] = pd.DataFrame({f"x{H}": ct(nc, f"x{H}") for H in [1, 3]}).T
    out["all_days_x1"] = ct(d, "x1").to_frame().T
    # slope of x1 on loc inside cases
    s = cs.dropna(subset=["x1", "loc"])
    lr = stats.linregress(s["loc"], s["x1"])
    out["slope_loc_x1"] = pd.DataFrame({"slope": [lr.slope], "t": [lr.slope / lr.stderr]})
    s3 = cs.dropna(subset=["x3", "loc"])
    lr3 = stats.linregress(s3["loc"], s3["x3"])
    out["slope_loc_x3"] = pd.DataFrame({"slope": [lr3.slope], "t": [lr3.slope / lr3.stderr]})
    # share of cases on days shared by many coins
    out["cases_per_day_dist"] = cs.groupby("day").size().value_counts().sort_index()
    return out
