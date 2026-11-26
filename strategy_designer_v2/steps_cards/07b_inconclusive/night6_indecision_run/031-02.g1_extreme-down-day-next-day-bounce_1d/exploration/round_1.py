def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    allret = {}
    for coin, wins in bars.items():
        r1 = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            # non-overlapping 1-day grid = all bars
            r = c[1:] / c[:-1] - 1
            r1.extend(list(r))
            ret = pd.Series(c).pct_change()
            sd20 = ret.rolling(20).std()
            z = ret / sd20
            rng = (df["high"] - df["low"]).replace(0, np.nan)
            cl = (df["high"] - df["close"]) / rng
            for t in range(n):
                f = df["forecast"].iloc[t]
                if not (f > 0):
                    continue
                d = {"coin": coin, "win": w, "day": pd.Timestamp(df["timestamp"].iloc[t]).floor("D"),
                     "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                     "f": f, "z": z.iloc[t], "cl": cl.iloc[t],
                     "rng_sd": (rng.iloc[t] / df["close"].iloc[t]) / sd20.iloc[t] if sd20.iloc[t] > 0 else np.nan,
                     "prior5": c[t] / c[t - 5] - 1 if t >= 5 else np.nan}
                for h in (1, 2, 3, 5):
                    d[f"r{h}"] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                rows.append(d)
        allret[coin] = np.mean(r1)
    cs = pd.DataFrame(rows)
    cs["mu"] = cs["coin"].map(allret)
    for h in (1, 2, 3, 5):
        cs[f"x{h}"] = cs[f"r{h}"] - cs["mu"] * h

    def ct(s, days):
        s = pd.Series(s.values, index=days.values).dropna()
        m = s.mean()
        dev = (s - m).groupby(level=0).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(s)
        return m, m / se, len(s), D

    def summ(g, col="x1"):
        m, t, n, D = ct(g[col], g["day"])
        return pd.Series({"mean": m, "t": t, "n": n, "days": D, "median": g[col].median(),
                          "hit": (g[col] > 0).mean()})

    out = {}
    out["horizons"] = pd.DataFrame({h: summ(cs, f"x{h}") for h in ("x1", "x2", "x3", "x5")}).T
    out["by_coin"] = cs.groupby("coin").apply(summ)
    out["by_year"] = cs.groupby("year").apply(summ)
    cs["fq"] = pd.qcut(cs["f"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_forecast_q"] = cs.groupby("fq").apply(summ)
    cs["zq"] = pd.qcut(cs["z"].rank(method="first"), 4, labels=["deepest", "z2", "z3", "shallow"])
    out["by_depth_q"] = cs.groupby("zq").apply(summ)
    cs["clq"] = pd.cut(cs["cl"], [-0.01, 0.5, 0.75, 0.9, 1.01])
    out["by_close_loc"] = cs.groupby("clq").apply(summ)
    cs["rq"] = pd.qcut(cs["rng_sd"].rank(method="first"), 3, labels=["narrow", "mid", "wide"])
    out["by_range"] = cs.groupby("rq").apply(summ)
    cs["pq"] = pd.qcut(cs["prior5"].rank(method="first"), 3, labels=["fell_most", "mid", "fell_least"])
    out["by_prior5"] = cs.groupby("pq").apply(summ)
    x = cs["x1"].dropna()
    out["tails"] = pd.Series({"std": x.std(), "max": x.max(), "min": x.min(),
                              "mean_trim5": x[(x > x.quantile(.05)) & (x < x.quantile(.95))].mean(),
                              "top5_share_of_sum": x.nlargest(5).sum() / x.sum()})
    return out
