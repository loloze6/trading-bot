def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 3, 5, 10, 20]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(0, n, 5):
                f = df["forecast"].iloc[i]
                rec = {"coin": coin, "win": w, "year": yr[i], "f": f, "reg": df["regime"].iloc[i],
                       "ret30": df["debug_info.components.ret30.last_history_value"].iloc[i] if "debug_info.components.ret30.last_history_value" in df else np.nan}
                for h in H:
                    rec["r%d" % h] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(rec)
    g = pd.DataFrame(rows)
    # drift per coin (all grid bars)
    for h in H:
        g["u%d" % h] = g["r%d" % h] - g.groupby("coin")["r%d" % h].transform("mean")
    a = g[(g.reg == "trending") & (g.f != 0) & g.f.notna()].copy()
    a["x"] = a.f/10
    a["s"] = np.sign(a.f)
    def slope(d, col):
        d = d[[col, "x"]].dropna()
        if len(d) < 20: return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan, "dirmean": np.nan})
        r = stats.linregress(d.x, d[col])
        return pd.Series({"n": len(d), "slope": r.slope, "t": r.slope/r.stderr,
                          "dirmean": (d[col]*np.sign(d.x)).mean()})
    out = {}
    out["by_horizon"] = pd.DataFrame({h: slope(a, "u%d" % h) for h in H}).T
    out["by_side"] = a.groupby("s").apply(lambda d: slope(d, "u5"))
    out["by_coin"] = a.groupby("coin").apply(lambda d: slope(d, "u5"))
    out["by_year"] = a.groupby("year").apply(lambda d: slope(d, "u5"))
    a["fq"] = pd.qcut(a.f.abs(), 4, labels=False)
    out["by_absf_quartile"] = a.groupby("fq").apply(lambda d: pd.Series({
        "n": d.u5.notna().sum(), "absf": d.f.abs().mean(),
        "dirmean5": (d.u5*d.s).mean(), "t5": stats.ttest_1samp((d.u5*d.s).dropna(), 0).statistic,
        "dirmean10": (d.u10*d.s).mean(), "t10": stats.ttest_1samp((d.u10*d.s).dropna(), 0).statistic}))
    out["by_side_horizon_dirmean"] = pd.DataFrame({h: a.groupby("s").apply(lambda d: (d["u%d" % h]*d.s).mean()) for h in H})
    a["r30q"] = pd.qcut(a.ret30.abs(), 4, labels=False)
    out["by_absret30_quartile"] = a.groupby("r30q").apply(lambda d: pd.Series({
        "n": d.u5.notna().sum(), "absret30": d.ret30.abs().mean(),
        "dirmean5": (d.u5*d.s).mean(), "t5": stats.ttest_1samp((d.u5*d.s).dropna(), 0).statistic}))
    # nontrending comparison: all grid bars with ret30 sign recomputed
    out["regime_counts"] = g.reg.value_counts()
    return out
