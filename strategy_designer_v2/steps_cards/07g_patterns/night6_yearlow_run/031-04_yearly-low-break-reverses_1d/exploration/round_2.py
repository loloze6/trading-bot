def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            feats = {}
            for L in [5, 10, 20, 30]:
                feats["mom%d" % L] = (c / c.shift(L) - 1) / (vol20 * np.sqrt(L))
            low60 = c.shift(1).rolling(60).min(); high60 = c.shift(1).rolling(60).max()
            feats["rng60"] = (c - low60) / (high60 - low60)
            low30 = c.shift(1).rolling(30).min(); high30 = c.shift(1).rolling(30).max()
            feats["rng30"] = (c - low30) / (high30 - low30)
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                row = {"coin": coin, "w": w, "fwd": c.iloc[i + H] / c.iloc[i] - 1,
                       "day": ts.iloc[i].normalize(), "year": ts.iloc[i].year, "vol20": vol20.iloc[i],
                       "mr": b["regime"].iloc[i] == "mean_reversion"}
                for k, v in feats.items():
                    row[k] = v.iloc[i]
                rows.append(row)
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby("coin")["fwd"].transform("mean")
    df["unus"] = df["fwd"] - df["drift"]
    usual = df.groupby("coin")["fwd"].transform("std")
    df["strength"] = df["unus"] / usual

    def clustered_slope(d, col):
        d = d.dropna(subset=[col, "unus"]).copy()
        d["x"] = d.groupby("coin")[col].transform(lambda s: (s.rank(pct=True) - 0.5))
        d["prod"] = d["x"] * d["strength"]
        g = d.groupby("day")["prod"].sum()
        D = len(g)
        t = g.mean() / (g.std(ddof=1) / np.sqrt(D))
        rho = stats.spearmanr(d[col], d["unus"])[0]
        return rho, t, D, len(d)

    summ = []
    for col in ["mom5", "mom10", "mom20", "mom30", "rng30", "rng60"]:
        rho, t, D, N = clustered_slope(df, col)
        summ.append({"feat": col, "spearman": rho, "t_dayclustered": t, "days": D, "cases": N})
    out["graded_summary"] = pd.DataFrame(summ).set_index("feat")

    # stability of mom10 & rng60: by year and by coin, spearman
    for col in ["mom10", "mom20", "rng60"]:
        d = df.dropna(subset=[col, "unus"])
        by_y = d.groupby("year").apply(lambda x: stats.spearmanr(x[col], x["unus"])[0])
        by_c = d.groupby("coin").apply(lambda x: stats.spearmanr(x[col], x["unus"])[0])
        out["spearman_by_year_" + col] = by_y
        out["spearman_by_coin_" + col] = by_c
        # quintile strength
        dd = d.copy()
        dd["q"] = dd.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        g = dd.groupby("q").agg(unus=("unus", "mean"), strength=("strength", "mean"), n=("unus", "count"))
        out["quint_" + col] = g
    # top quintile mom10 vs rest by vol half
    d = df.dropna(subset=["mom10", "vol20"]).copy()
    d["top"] = d.groupby("coin")["mom10"].transform(lambda s: s.rank(pct=True) > 0.8)
    d["vh"] = d.groupby("coin")["vol20"].transform(lambda s: s.rank(pct=True) > 0.5)
    out["top_mom10_by_volhalf"] = d.groupby(["vh", "top"])["unus"].agg(["mean", "count"])
    # breaks episode: cases in mr regime
    out["mr_cases"] = df[df["mr"]].groupby("coin")["unus"].agg(["mean", "count"])
    return out
