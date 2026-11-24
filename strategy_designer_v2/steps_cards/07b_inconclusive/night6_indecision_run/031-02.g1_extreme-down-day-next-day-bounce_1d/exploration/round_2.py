def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    allret = {}
    for coin, wins in bars.items():
        r1 = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            r = c[1:] / c[:-1] - 1
            r1.extend(list(r))
            ret = pd.Series(c).pct_change()
            sd20 = ret.rolling(20).std()
            z = ret / sd20
            rng = (df["high"] - df["low"]).replace(0, np.nan)
            cl = (df["high"] - df["close"]) / rng
            for t in range(n):
                zt = z.iloc[t]
                f = df["forecast"].iloc[t]
                act = bool(f > 0)
                if not (act or (zt == zt and abs(zt) >= 2)):
                    continue
                ts = pd.Timestamp(df["timestamp"].iloc[t])
                d = {"coin": coin, "win": w, "day": ts.floor("D"), "year": ts.year,
                     "act": act, "f": f if act else 0.0, "z": zt, "cl": cl.iloc[t],
                     "rng_sd": (rng.iloc[t] / c[t]) / sd20.iloc[t] if sd20.iloc[t] > 0 else np.nan,
                     "prior5": c[t - 1] / c[t - 6] - 1 if t >= 6 else np.nan,
                     "prior20": c[t] / c[t - 20] - 1 if t >= 20 else np.nan,
                     "sd20": sd20.iloc[t]}
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
        if len(s) < 3:
            return np.nan, np.nan, len(s), 0
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
    A = cs[cs["act"]].copy()
    out["horizons_active"] = pd.DataFrame({h: summ(A, h) for h in ("x1", "x2", "x3", "x5")}).T
    up = cs[(cs["z"] >= 2)]
    up_short = up.copy()
    for h in ("x1", "x3"):
        up_short[h] = -up_short[h]
    out["up_days_z2_short_side"] = pd.DataFrame({h: summ(up_short, h) for h in ("x1", "x3")}).T
    out["by_coin"] = A.groupby("coin").apply(summ)
    out["by_year"] = A.groupby("year").apply(summ)
    A["fq"] = pd.qcut(A["f"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_forecast_q"] = A.groupby("fq").apply(summ)
    A["zq"] = pd.qcut(A["z"].rank(method="first"), 3, labels=["deepest", "mid", "shallow"])
    out["by_depth"] = A.groupby("zq").apply(summ)
    A["clq"] = pd.cut(A["cl"], [-0.01, 0.6, 0.85, 1.01], labels=["mid_or_high", "near_low", "at_low"])
    out["by_close_loc"] = A.groupby("clq").apply(summ)
    A["p20"] = np.where(A["prior20"] > 0, "after_20d_rise", "after_20d_fall")
    out["by_prior20"] = A.groupby("p20").apply(summ)
    out["by_prior20_x3"] = A.groupby("p20").apply(lambda g: summ(g, "x3"))
    A["vq"] = pd.qcut(A["sd20"].rank(method="first"), 3, labels=["calm", "mid", "wild"])
    out["by_vol"] = A.groupby("vq").apply(summ)
    x = A["x1"].dropna()
    out["tails"] = pd.Series({"std": x.std(), "max": x.max(), "min": x.min(),
                              "mean_trim5": x[(x > x.quantile(.05)) & (x < x.quantile(.95))].mean(),
                              "top5_share_of_sum": x.nlargest(5).sum() / x.sum(),
                              "corr_f_x1": A[["f", "x1"]].corr().iloc[0, 1],
                              "corr_cl_x1": A[["cl", "x1"]].corr().iloc[0, 1]})
    return out
