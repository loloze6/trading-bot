def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []
    for coin, ws in bars.items():
        # normal drift per horizon over all windows
        recs = {h: [] for h in H}
        tmp = []
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values; o = df["open"].values
            rng = hi - lo
            ratio = rng / pd.Series(rng).rolling(30, min_periods=30).mean().values
            # past 5-day return
            past5 = pd.Series(c).pct_change(5).values
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    recs[h].append(c[i + h] / c[i] - 1)
            for i in range(0, n - 5, 5):
                r = {"coin": coin, "w": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "f": df["forecast"].iloc[i], "ratio": ratio[i],
                     "upday": float(np.sign(c[i] - o[i])), "past5": past5[i],
                     "dayret": c[i] / c[i - 1] - 1 if i > 0 else np.nan}
                for h in H:
                    r[f"r{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                tmp.append(r)
        drift = {h: np.mean(recs[h]) for h in H}
        for r in tmp:
            for h in H:
                r[f"x{h}"] = r[f"r{h}"] - drift[h]
            rows.append(r)
    d = pd.DataFrame(rows)
    a = d[d.f > 0].copy()
    z = d[d.f == 0]

    def tm(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean%": 100 * s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})

    def slope(g, x="x5"):
        g = g[["f", x]].dropna()
        if len(g) < 10: return pd.Series({"n": len(g), "slope_t": np.nan})
        res = stats.linregress(g.f, g[x])
        return pd.Series({"n": len(g), "slope_bp": 1e4 * res.slope, "slope_t": res.slope / res.stderr, "mean%": 100 * g[x].mean(),
                          "t_mean": g[x].mean() / (g[x].std() / np.sqrt(len(g)))})
    out = {}
    out["active_vs_flat"] = pd.DataFrame({"active": tm(a.x5), "flat": tm(z.x5)}).T
    out["by_coin"] = a.groupby("coin").apply(slope)
    out["by_year"] = a.groupby("year").apply(slope)
    a["fq"] = pd.qcut(a.f.rank(method="first"), 5, labels=False)
    out["by_fquintile"] = a.groupby("fq").apply(lambda g: pd.concat([tm(g.x5), pd.Series({"fmean": g.f.mean(), "ratio": g.ratio.mean()})]))
    out["by_dayside"] = a.groupby("upday").apply(lambda g: pd.concat([tm(g.x5), slope(g)[["slope_t"]]]))
    out["by_horizon"] = pd.DataFrame({h: slope(a, f"x{h}") for h in H}).T
    out["by_horizon_flat"] = pd.DataFrame({h: tm(z[f"x{h}"]) for h in H}).T
    # signed by day direction: excess times sign of day
    a["sx5"] = a.x5 * a.upday
    out["signed_by_day_dir"] = tm(a.sx5)
    # all cases ratio-1 vs x5 (both sides)
    d2 = d.dropna(subset=["ratio", "x5"])
    d2["rq"] = pd.qcut(d2.ratio, 5, labels=False)
    out["all_by_ratio_quintile"] = d2.groupby("rq").apply(lambda g: pd.concat([tm(g.x5), pd.Series({"ratio": g.ratio.mean()})]))
    out["all_ratio_x_upday"] = d2.groupby(["rq", "upday"]).apply(lambda g: tm(g.x5)).unstack()
    return out
