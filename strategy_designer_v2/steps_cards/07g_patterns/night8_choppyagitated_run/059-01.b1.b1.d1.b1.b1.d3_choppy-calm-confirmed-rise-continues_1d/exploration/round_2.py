def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "reg": b["regime"].astype(str),
                "s1": r1 / sd30, "s3": (c / c.shift(3) - 1) / (sd30 * np.sqrt(3)),
                "s7": (c / c.shift(7) - 1) / (sd30 * np.sqrt(7)),
                "tr60": c / c.shift(60) - 1,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1, "f5": c.shift(-5) / c - 1,
                "f7": c.shift(-7) / c - 1,
                "clo": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["inprof"] = D["reg"].isin(["trending", "unknown"])
    D["trend"] = pd.cut(D["tr60"], [-99, -0.10, 0.10, 99], labels=["falling", "choppy", "rising"])
    def tstat(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean%": 100 * s.mean(),
                          "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    # A: daily scaled move in choppy calm, several horizons, grid h
    for h in [1, 2, 3, 5]:
        g = D[(D["pos"] % h == 0)].dropna(subset=[f"f{h}", "s1"]).copy()
        g["x"] = g[f"f{h}"] - g["coin"].map(g.groupby("coin")[f"f{h}"].mean())
        gi = g[g["inprof"]]
        sl = stats.linregress(gi["s1"], gi["x"])
        out[f"A_inprof_s1_slope_h{h}"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(gi)}"
        up = gi[gi["s1"] > 0]
        sl2 = stats.linregress(up["s1"], up["x"])
        out[f"A_inprof_up_only_slope_h{h}"] = f"slope {sl2.slope:.5f} t {sl2.slope/sl2.stderr:.2f} n {len(up)}"
        if h == 3:
            gi = gi.copy()
            gi["q"] = pd.cut(gi["s1"], [-99, -1, 0, 1, 1.5, 2, 99])
            out["A_inprof_s1_bins_h3"] = gi.groupby("q", observed=True)["x"].apply(tstat).unstack()
            big = gi[gi["s1"] > 1.5]
            out["A_inprof_bigup_by_window_h3"] = big.groupby("w")["x"].apply(tstat).unstack()
            out["A_inprof_bigup_by_closeloc_h3"] = big.groupby(pd.cut(big["clo"], [0, 0.5, 1], include_lowest=True), observed=True)["x"].apply(tstat).unstack()
            # trend split, all bars by own 60d trend
            gg = g.dropna(subset=["trend"]).copy()
            gg["q"] = pd.cut(gg["s1"], [-99, -2, -1, 1, 2, 99])
            out["A_trend_s1_bins_h3"] = gg.groupby(["trend", "q"], observed=True)["x"].apply(tstat).unstack()
    # B: scaled weekly rise continuation, by own 60d trend
    g7 = D[D["pos"] % 7 == 0].dropna(subset=["f7", "s7", "trend"]).copy()
    g7["x"] = g7["f7"] - g7["coin"].map(g7.groupby("coin")["f7"].mean())
    res = {}
    for tr, sub in g7.groupby("trend", observed=True):
        sl = stats.linregress(sub["s7"], sub["x"])
        res[tr] = pd.Series({"n": len(sub), "slope": sl.slope, "t": sl.slope / sl.stderr})
    out["B_s7_slope_by_trend"] = pd.DataFrame(res).T
    g7["q"] = pd.cut(g7["s7"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    out["B_s7_bins_by_trend"] = g7.groupby(["trend", "q"], observed=True)["x"].apply(tstat).unstack()
    # C: weekday next-day by trend and by year
    D1 = D.dropna(subset=["f1"]).copy()
    D1["x"] = D1["f1"] - D1["coin"].map(D1.groupby("coin")["f1"].mean())
    out["C_weekday_by_trend_t"] = D1.dropna(subset=["trend"]).groupby(["wd", "trend"], observed=True)["x"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))).unstack()
    out["C_thufri_vs_rest_by_year"] = D1.groupby(["yr", D1["wd"].isin([3, 4])])["x"].apply(tstat).unstack()
    return out
