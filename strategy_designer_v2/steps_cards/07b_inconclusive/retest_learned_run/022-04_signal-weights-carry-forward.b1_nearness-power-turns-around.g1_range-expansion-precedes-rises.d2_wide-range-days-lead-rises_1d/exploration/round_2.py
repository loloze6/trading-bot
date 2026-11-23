def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [3, 5]
    rows = []
    for coin, ws in bars.items():
        recs = {h: [] for h in H}
        tmp = []
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values; o = df["open"].values
            rng = hi - lo
            mr = pd.Series(rng).rolling(30, min_periods=30).mean().values
            ratio = rng / mr
            raw = df["debug_info.components.range_excess.last_history_value"].values
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    recs[h].append(c[i + h] / c[i] - 1)
            for i in range(0, n, 5):
                r = {"coin": coin, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "f": df["forecast"].iloc[i], "ratio": ratio[i], "raw": raw[i],
                     "dayret": (c[i] / c[i - 1] - 1) if i > 0 else np.nan,
                     "clv": (2 * c[i] - hi[i] - lo[i]) / (hi[i] - lo[i]) if hi[i] > lo[i] else np.nan}
                for h in H:
                    r[f"r{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                tmp.append(r)
        drift = {h: np.mean(recs[h]) for h in H}
        for r in tmp:
            for h in H:
                r[f"x{h}"] = r[f"r{h}"] - drift[h]
            rows.append(r)
    d = pd.DataFrame(rows)
    d["lr"] = np.log(d.ratio)

    def sl(g, x, y):
        g = g[[x, y]].replace([np.inf, -np.inf], np.nan).dropna()
        if len(g) < 20: return pd.Series({"n": len(g)})
        res = stats.linregress(g[x], g[y])
        return pd.Series({"n": len(g), "slope": res.slope, "t": res.slope / res.stderr})
    out = {}
    a = d[d.f > 0]
    out["active_slopes"] = pd.DataFrame({
        "x5~ratio": sl(a, "ratio", "x5"), "x5~lr": sl(a, "lr", "x5"),
        "x3~ratio": sl(a, "ratio", "x3"), "x5~f_uncapped": sl(a[a.f < 20], "f", "x5")}).T
    out["all_slopes"] = pd.DataFrame({
        "x5~lr": sl(d, "lr", "x5"), "x3~lr": sl(d, "lr", "x3"),
        "x5~ratio": sl(d, "ratio", "x5"), "x3~ratio": sl(d, "ratio", "x3"),
        "x5~f_all": sl(d, "f", "x5")}).T
    out["all_lr_by_coin"] = d.groupby("coin").apply(lambda g: sl(g, "lr", "x5"))
    out["all_lr_by_year"] = d.groupby("year").apply(lambda g: sl(g, "lr", "x5"))
    # signed by close location: lr * clv
    d["lr_clv"] = d.lr.clip(lower=0) * d.clv
    out["wide_x_closeloc"] = pd.DataFrame({"x5": sl(d, "lr_clv", "x5"), "x3": sl(d, "lr_clv", "x3")}).T
    d["clvq"] = pd.cut(d.clv, [-1.01, -0.33, 0.33, 1.01], labels=["low", "mid", "high"])
    d["wide"] = d.ratio > 1
    out["mean_by_wide_closeloc"] = d.groupby(["wide", "clvq"]).apply(
        lambda g: pd.Series({"n": g.x5.notna().sum(), "mean%": 100 * g.x5.mean(),
                             "t": g.x5.mean() / (g.x5.std() / np.sqrt(g.x5.notna().sum()))}))
    # deciles of ratio, all cases
    d2 = d.dropna(subset=["ratio", "x5"])
    d2["dq"] = pd.qcut(d2.ratio, 10, labels=False)
    out["all_by_ratio_decile"] = d2.groupby("dq").apply(lambda g: pd.Series({
        "n": len(g), "ratio": g.ratio.mean(), "mean%": 100 * g.x5.mean(),
        "t": g.x5.mean() / (g.x5.std() / np.sqrt(len(g)))}))
    return out
