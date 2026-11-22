def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 3, 5, 10, 20]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            hi = df["high"].values.astype(float); lo = df["low"].values.astype(float)
            n = len(c)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            col = "debug_info.components.ret30.last_history_value"
            for i in range(0, n, 5):
                f = df["forecast"].iloc[i]
                r30c = c[i]/c[i-30]-1 if i >= 30 else np.nan
                nmr = abs(c[i]-c[i-30])/(hi[i-30:i+1].max()-lo[i-30:i+1].min()) if i >= 30 else np.nan
                rec = {"coin": coin, "win": w, "year": yr[i], "f": f, "reg": df["regime"].iloc[i],
                       "ret30": df[col].iloc[i] if col in df else np.nan, "r30c": r30c, "nmr": nmr}
                for h in H:
                    rec["r%d" % h] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(rec)
    g = pd.DataFrame(rows)
    for h in H:
        g["u%d" % h] = g["r%d" % h] - g.groupby("coin")["r%d" % h].transform("mean")
    a = g[(g.reg == "trending") & (g.f != 0) & g.f.notna()].copy()
    a["x"] = a.f/10
    a["s"] = np.sign(a.f)
    def slope(d, col, xcol="x"):
        d = d[[col, xcol]].dropna()
        if len(d) < 20: return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan, "dirmean": np.nan, "t_dir": np.nan})
        r = stats.linregress(d[xcol], d[col])
        dm = d[col]*np.sign(d[xcol])
        return pd.Series({"n": len(d), "slope": r.slope, "t": r.slope/r.stderr,
                          "dirmean": dm.mean(), "t_dir": dm.mean()/(dm.std()/np.sqrt(len(dm)))})
    out = {}
    def safe(k, fn):
        try: out[k] = fn()
        except Exception as e: out[k] = "err: " + str(e)[:80]
    safe("by_horizon", lambda: pd.DataFrame({h: slope(a, "u%d" % h) for h in H}).T)
    safe("by_side_u5", lambda: a.groupby("s").apply(lambda d: slope(d, "u5")))
    safe("by_side_u10", lambda: a.groupby("s").apply(lambda d: slope(d, "u10")))
    safe("by_coin", lambda: a.groupby("coin").apply(lambda d: slope(d, "u5")))
    safe("by_year", lambda: a.groupby("year").apply(lambda d: slope(d, "u5")))
    def quart(d, v, k):
        d = d.copy(); d["q"] = pd.qcut(d[v].rank(method="first"), 4, labels=False)
        return d.groupby("q").apply(lambda e: pd.Series({
            "n": e.u5.notna().sum(), "mean_abs": e[v].mean(),
            "dirmean5": (e.u5*e.s).mean(), "t5": stats.ttest_1samp((e.u5*e.s).dropna(), 0).statistic,
            "dirmean10": (e.u10*e.s).mean(), "t10": stats.ttest_1samp((e.u10*e.s).dropna(), 0).statistic}))
    a["absf"] = a.f.abs()
    safe("by_absf_quartile", lambda: quart(a, "absf", "absf"))
    a["absr30"] = a.r30c.abs()
    safe("by_absret30_quartile", lambda: quart(a, "absr30", "absr30"))
    a["nmrv"] = a.nmr
    safe("by_nmr_quartile_in_regime", lambda: quart(a, "nmrv", "nmr"))
    # all bars with recomputed ret30: continuation slope by nmr bands
    b = g.dropna(subset=["r30c", "nmr"]).copy()
    b["z"] = b.r30c/b.r30c.std()
    b["nb"] = pd.cut(b.nmr, [0, 0.25, 0.5, 0.75, 1.01], include_lowest=True)
    safe("allbars_by_nmr_band_u5", lambda: b.groupby("nb").apply(lambda d: slope(d, "u5", "z")))
    safe("allbars_by_nmr_band_u10", lambda: b.groupby("nb").apply(lambda d: slope(d, "u10", "z")))
    safe("regime_counts", lambda: g.reg.value_counts())
    return out
