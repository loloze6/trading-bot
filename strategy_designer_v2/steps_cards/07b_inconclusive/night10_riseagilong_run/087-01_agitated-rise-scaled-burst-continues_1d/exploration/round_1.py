def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []
    # coin mean h-return over all windows, grid-based
    coin_mean = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            coin_mean[(coin, h)] = np.mean(rs) if rs else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            vsr = (c / c.shift(3) - 1) / (sd * np.sqrt(3))
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for i in range(0, n, 3):
                rec = {"coin": coin, "win": w, "year": ts.iloc[i].year,
                       "day": ts.iloc[i].normalize(), "fc": df["forecast"].iloc[i],
                       "regime": df["regime"].iloc[i], "vsr": vsr.iloc[i]}
                for h in H:
                    if i + h < n:
                        rec[f"x{h}"] = c.iloc[i + h] / c.iloc[i] - 1 - coin_mean[(coin, h)]
                    else:
                        rec[f"x{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)

    def summ(g, col="x3"):
        g = g.dropna(subset=[col])
        if len(g) < 2:
            return pd.Series({"n": len(g), "mean": np.nan, "t_day": np.nan})
        dev = g[col] - g[col].mean()
        s = dev.groupby(g["day"]).sum()
        D = len(s)
        se = np.sqrt((s ** 2).sum() * D / max(D - 1, 1)) / len(g)
        return pd.Series({"n": len(g), "days": D, "mean": g[col].mean(), "t_day": g[col].mean() / se if se > 0 else np.nan})

    cases = d[d.fc > 0]
    out = {}
    out["regime counts"] = d.regime.value_counts()
    out["cases by coin"] = cases.groupby("coin").apply(summ)
    out["cases by window"] = cases.groupby("win").apply(summ)
    out["cases by horizon"] = pd.DataFrame({f"h{h}": summ(cases, f"x{h}") for h in H}).T
    inprof = d[d.regime.isin(["trending", "unknown"])].dropna(subset=["vsr"]).copy()
    inprof["vsr_bin"] = pd.cut(inprof.vsr, [-np.inf, -1, -0.5, 0, 0.5, 1.1547, 2, np.inf])
    out["in-profile by vsr bin, h3"] = inprof.groupby("vsr_bin").apply(summ)
    out["in-profile by vsr bin, h5"] = inprof.groupby("vsr_bin").apply(lambda g: summ(g, "x5"))
    out["in-profile by vsr bin, h10"] = inprof.groupby("vsr_bin").apply(lambda g: summ(g, "x10"))
    cases = cases.copy()
    cases["fq"] = pd.qcut(cases.fc.rank(method="first"), 3, labels=["low", "mid", "high"])
    out["cases by forecast tercile"] = cases.groupby("fq").apply(summ)
    vv = cases.dropna(subset=["vsr", "x3"])
    out["cases slope x3 on vsr"] = pd.Series(stats.linregress(vv.vsr, vv.x3)._asdict()).iloc[:4]
    out["chop bars, vsr>=1.1547, h3"] = summ(d[(d.regime == "chop") & (d.vsr >= 1.1547)])
    return out
