def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            r1 = pd.Series(c).pct_change()
            sd20 = r1.rolling(20).std().shift(1)
            sw = (r1 / sd20).values
            sd20b = r1.rolling(20).std().values
            sw2 = (r1 / pd.Series(sd20b)).values
            reg = df["regime"].astype(str).values
            for i in range(n):
                rec = {"coin": coin, "w": w, "i": i, "reg": reg[i], "sw": sw2[i], "sw_lag": sw[i],
                       "r1": r1.iloc[i], "yr": pd.Timestamp(df["timestamp"].iloc[i]).year}
                for h in (1, 3, 5, 10):
                    rec[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    # normal drift per coin, per horizon, non-overlapping grid
    drift = {}
    for h in (1, 3, 5, 10):
        g = d[(d["i"] % h == 0)]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
    for h in (1, 3, 5, 10):
        d[f"x{h}"] = d[f"f{h}"] - d["coin"].map(drift[h])
    out = {}
    out["regime counts"] = d["reg"].value_counts()
    fc = d[d["reg"] != "chop"].copy()  # falling calm bars (vetoes pass)
    out["falling calm bars"] = len(fc)
    def summ(sub, h, grid=True):
        s = sub[sub["i"] % h == 0] if grid else sub
        x = s[f"x{h}"].dropna()
        if len(x) < 3:
            return pd.Series({"n": len(x)})
        return pd.Series({"n": len(x), "mean_excess_up": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    # cases (rise >=2) at several horizons, every case bar (not grid) and grid
    cases = fc[fc["reg"] == "mean_reversion"]
    out["cases by horizon (all case bars, long direction)"] = pd.DataFrame({h: summ(cases, h, grid=False) for h in (1, 3, 5, 10)}).T
    # graded: falling calm bars by rise-in-swings bucket, 3d and 5d
    fc["b"] = pd.cut(fc["sw"], [-99, -2, -1, 0, 1, 2, 3, 99])
    tab = []
    for b, g in fc.groupby("b", observed=True):
        for h in (3, 5):
            s = summ(g, h, grid=False)
            s["bucket"] = str(b); s["h"] = h
            tab.append(s)
    out["falling calm by rise bucket (every bar, long dir)"] = pd.DataFrame(tab)
    # correlation of sw with forward excess in falling calm
    for h in (1, 3, 5):
        z = fc[["sw", f"x{h}"]].dropna()
        rr, p = stats.pearsonr(z["sw"], z[f"x{h}"])
        out[f"corr sw vs x{h} in falling calm"] = f"r={rr:.3f} p={p:.3f} n={len(z)}"
    # cases by coin and year, 3d
    out["cases by coin x3"] = cases.groupby("coin")["x3"].agg(["count", "mean"])
    out["cases by year x3"] = cases.groupby("yr")["x3"].agg(["count", "mean"])
    # all bars (any profile) rise>=2 for comparison
    big = d[d["sw"] >= 2]
    out["rise>=2 by profile-pass vs not, x3"] = big.groupby(big["reg"] == "chop")["x3"].agg(["count", "mean", "std"])
    return out
