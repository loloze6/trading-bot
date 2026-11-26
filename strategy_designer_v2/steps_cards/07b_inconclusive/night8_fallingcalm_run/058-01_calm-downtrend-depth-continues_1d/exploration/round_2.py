def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            v = df["volume"].values
            n = len(df)
            r30 = pd.Series(c).pct_change(30).values
            vr = pd.Series(v).rolling(30).mean().values / pd.Series(v).rolling(180, min_periods=60).mean().values
            for i in range(0, n, 5):
                rows.append({"coin": coin, "win": w, "fc": df["forecast"].iloc[i],
                             "reg": df["regime"].iloc[i], "r30": r30[i], "vr": vr[i],
                             "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                             "day": pd.Timestamp(df["timestamp"].iloc[i]).floor("D"),
                             "f5": c[i + 5] / c[i] - 1 if i + 5 < n else np.nan})
    A = pd.DataFrame(rows)
    drift = A.groupby("coin")["f5"].mean()
    A["sx"] = -(A["f5"] - A["coin"].map(drift))
    out = {}
    def tday(x, days):
        x = x.dropna(); d = days.loc[x.index]
        dd = (x - 0).groupby(d).sum()
        if len(dd) < 2: return np.nan, len(dd)
        return x.mean() / (dd.std(ddof=1) * np.sqrt(len(dd)) / len(x)), len(dd)
    inp = A[(A.fc < 0)].dropna(subset=["vr", "sx"]).copy()
    out_ = A[(A.r30 < 0) & (A.reg == "chop")].dropna(subset=["vr", "sx"]).copy()
    res = []
    for name, g in [("in_profile", inp), ("outside_profile_r30neg", out_)]:
        g = g.copy()
        g["vq"] = pd.qcut(g["vr"].rank(method="first"), 3, labels=["quiet", "mid", "heavy"])
        for q in ["quiet", "mid", "heavy"]:
            s = g[g.vq == q]
            t, nd = tday(s["sx"], s["day"])
            res.append({"set": name, "vq": q, "n": len(s), "days": nd, "mean": s["sx"].mean(), "t": t,
                        "spearman_depth_vs_sx": stats.spearmanr(-s["r30"], s["sx"]).correlation})
        q, h = g[g.vq == "quiet"]["sx"], g[g.vq == "heavy"]["sx"]
        res.append({"set": name, "vq": "quiet-heavy Welch t", "n": len(q) + len(h),
                    "mean": q.mean() - h.mean(), "t": stats.ttest_ind(q, h, equal_var=False).statistic})
        g["vqs"] = g["vq"]
        if name == "in_profile":
            inp = g
    out["volume_terciles"] = pd.DataFrame(res)
    out["inprof_spearman_vr_vs_sx"] = float(stats.spearmanr(inp["vr"], inp["sx"]).correlation)
    # graded score: depth x quietness
    inp["score"] = (-inp["r30"]) / inp["vr"]
    inp["sq"] = pd.qcut(inp["score"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["inprof_by_depth_over_volume"] = inp.groupby("sq")["sx"].agg(["count", "mean"])
    quiet = inp[inp.vq == "quiet"]
    out["quiet_by_year"] = quiet.groupby("year")["sx"].agg(["count", "mean"])
    out["quiet_by_coin"] = quiet.groupby("coin")["sx"].agg(["count", "mean"])
    out["heavy_by_year"] = inp[inp.vq == "heavy"].groupby("year")["sx"].agg(["count", "mean"])
    return out
