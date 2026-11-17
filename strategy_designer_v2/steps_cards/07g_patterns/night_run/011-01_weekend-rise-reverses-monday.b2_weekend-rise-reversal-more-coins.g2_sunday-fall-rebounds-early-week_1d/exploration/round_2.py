def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=15).std()
            z = r1 / vol
            z2 = (c / c.shift(2) - 1) / (vol * np.sqrt(2))
            vr = b["volume"] / b["volume"].rolling(20, min_periods=15).mean()
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "wd": ts.dt.weekday, "year": ts.dt.year,
                "pos": np.arange(len(b)), "z": z, "z2": z2, "vr": vr, "vol": vol,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f3": c.shift(-3) / c - 1}))
    d = pd.concat(rows, ignore_index=True)
    for h in ["f1", "f2", "f3"]:
        d[h + "x"] = d[h] - d.groupby("coin")[h].transform("mean")
    d["vq"] = d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    def sl(sub, x, y):
        s = sub[[x, y]].dropna()
        if len(s) < 30: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(s)})
        r = stats.linregress(s[x], s[y]); return pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(s)})
    out = {}
    sun = d[d.wd == 6]
    out["sun_rise_vs_fall_f2x"] = pd.DataFrame({"rise": sl(sun[sun.z > 0], "z", "f2x"), "fall": sl(sun[sun.z < 0], "z", "f2x")}).T
    out["sun_slope_f2x_by_year"] = sun.groupby("year").apply(lambda g: sl(g, "z", "f2x"))
    out["sun_slope_f2x_by_coin"] = sun.groupby("coin").apply(lambda g: sl(g, "z", "f2x"))
    out["sun_slope_f2x_by_volq"] = sun.groupby("vq").apply(lambda g: sl(g, "z", "f2x"))
    # weekend 2-day (Sat+Sun) move on Sunday bar -> next 2 / 3 days
    out["weekend2d_slope"] = pd.DataFrame({"f2x": sl(sun, "z2", "f2x"), "f3x": sl(sun, "z2", "f3x")}).T
    # placebo: 2-day move ending Wed/Thu
    out["midweek2d_slope_f2x"] = d[d.wd.isin([2, 3])].groupby("wd").apply(lambda g: sl(g, "z2", "f2x"))
    sat = d[d.wd == 5]
    out["sat_slope_f1x_by_year"] = sat.groupby("year").apply(lambda g: sl(g, "z", "f1x"))
    fri = d[d.wd == 4]
    out["fri_slope_f1x_by_year"] = fri.groupby("year").apply(lambda g: sl(g, "z", "f1x"))
    # high-vol reversal all days grid2, by year
    gr = d[(d.pos % 2 == 0) & (d.vq == 2)]
    out["highvol_slope_f2x_by_year"] = gr.groupby("year").apply(lambda g: sl(g, "z", "f2x"))
    # weekday return effect by year: Wed/Fri/Sat bar return mean minus others
    d["bar_wd"] = (d.wd + 1) % 7
    d["good"] = d.bar_wd.isin([2, 4, 5])
    def diff(g):
        a = g.loc[g.good, "f1x"].dropna(); b = g.loc[~g.good, "f1x"].dropna()
        return pd.Series({"diff": a.mean() - b.mean(), "t": stats.ttest_ind(a, b, equal_var=False).statistic})
    out["wed_fri_sat_minus_rest_by_year"] = d.groupby("year").apply(diff)
    return out
