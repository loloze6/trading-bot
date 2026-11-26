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
            sd30l = r1.rolling(30, min_periods=20).std()
            # agitation proxy: 30d sd vs its own expanding/365 median within window
            agit = sd30 > sd30.rolling(365, min_periods=60).median()
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "s1": r1 / sd30,
                "s7": (c / c.shift(7) - 1) / (sd30 * np.sqrt(7)),
                "s7lag": (c.shift(7) / c.shift(14) - 1) / (sd30.shift(7) * np.sqrt(7)),
                "tr60": c / c.shift(60) - 1,
                "f2": c.shift(-2) / c - 1, "f3": c.shift(-3) / c - 1,
                "f7": c.shift(-7) / c - 1,
                "agit": np.where(sd30.rolling(365, min_periods=60).median().isna(), np.nan, agit.astype(float)),
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["trend"] = pd.cut(D["tr60"], [-99, -0.10, 0.10, 99], labels=["falling", "choppy", "rising"])
    def tstat(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean%": 100 * s.mean(),
                          "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    def slope(sub, x, y):
        sub = sub.dropna(subset=[x, y])
        if len(sub) < 8: return pd.Series({"n": len(sub), "slope": np.nan, "t": np.nan})
        sl = stats.linregress(sub[x], sub[y])
        return pd.Series({"n": len(sub), "slope": sl.slope, "t": sl.slope / sl.stderr})
    g7 = D[D["pos"] % 7 == 0].dropna(subset=["f7", "s7", "trend"]).copy()
    g7["x"] = g7["f7"] - g7["coin"].map(g7.groupby("coin")["f7"].mean())
    ch = g7[g7["trend"] == "choppy"]
    out["B1_choppy_s7_slope_by_agit"] = ch.groupby("agit").apply(lambda s: slope(s, "s7", "x"))
    out["B2_choppy_s7_slope_by_year"] = ch.groupby("yr").apply(lambda s: slope(s, "s7", "x"))
    out["B3_choppy_s7_slope_by_coin"] = ch.groupby("coin").apply(lambda s: slope(s, "s7", "x"))
    out["B4_choppy_s7_up_only"] = slope(ch[ch["s7"] > 0], "s7", "x")
    out["B5_choppy_s7_down_only"] = slope(ch[ch["s7"] < 0], "s7", "x")
    out["B6_choppy_s7lag_slope"] = slope(ch, "s7lag", "x")
    # day-level t (cases of one day together)
    ch2 = ch.copy(); ch2["dev"] = ch2["x"] * np.sign(ch2["s7"])
    out["B7_choppy_signed_dev_mean"] = tstat(ch2["dev"])
    # falling rally fade
    g3 = D[D["pos"] % 3 == 0].dropna(subset=["f3", "s1", "trend"]).copy()
    g3["x"] = g3["f3"] - g3["coin"].map(g3.groupby("coin")["f3"].mean())
    fa = g3[(g3["trend"] == "falling") & (g3["s1"] > 0)]
    out["C1_falling_up_s1_slope_h3"] = slope(fa, "s1", "x")
    out["C2_falling_up_by_agit"] = fa.groupby("agit").apply(lambda s: slope(s, "s1", "x"))
    big = fa[fa["s1"] > 1]
    out["C3_falling_bigup_by_year"] = big.groupby("yr")["x"].apply(tstat).unstack()
    out["C4_falling_bigup_by_agit"] = big.groupby("agit")["x"].apply(tstat).unstack()
    out["C5_falling_bigup_by_coin"] = big.groupby("coin")["x"].apply(tstat).unstack()
    return out
