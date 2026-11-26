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
            v = df["volume"].values
            n = len(df)
            r30 = pd.Series(c).pct_change(30).values
            vr = pd.Series(v).rolling(30).mean().values / pd.Series(v).rolling(180, min_periods=60).mean().values
            for i in range(n):
                d = {"coin": coin, "win": w, "pos": i, "fc": df["forecast"].iloc[i],
                     "reg": df["regime"].iloc[i], "r30": r30[i], "vr": vr[i],
                     "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "day": pd.Timestamp(df["timestamp"].iloc[i]).floor("D")}
                for h in H:
                    d[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(d)
    A = pd.DataFrame(rows)
    out = {}
    # drift per coin per horizon from grid
    drift = {}
    for h in H:
        g = A[(A.pos % h == 0)]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
    def sig(sub, h):
        x = -(sub[f"f{h}"] - sub["coin"].map(drift[h]))
        x = x.dropna()
        if len(x) < 3: return (len(x), np.nan, np.nan)
        dd = x.groupby(sub.loc[x.index, "day"]).sum()
        t = x.mean() / (dd.std(ddof=1) * np.sqrt(len(dd)) / len(x)) if len(dd) > 1 else np.nan
        return (len(x), x.mean(), t)
    # main by horizon, in position
    res = []
    for h in H:
        g = A[(A.pos % h == 0) & (A.fc < 0)]
        n_, m, t = sig(g, h)
        res.append({"h": h, "n": n_, "mean_short_excess": m, "t": t})
    out["in_position_by_horizon"] = pd.DataFrame(res)
    g5 = A[(A.pos % 5 == 0) & (A.fc < 0)].copy()
    g5["sx"] = -(g5["f5"] - g5["coin"].map(drift[5]))
    out["by_coin"] = g5.groupby("coin")["sx"].agg(["count", "mean"])
    out["by_window"] = g5.groupby("win")["sx"].agg(["count", "mean"])
    out["by_year"] = g5.groupby("year")["sx"].agg(["count", "mean"])
    g5["fq"] = pd.qcut(g5["fc"].rank(method="first"), 4, labels=["deepest", "q2", "q3", "shallowest"])
    out["by_forecast_quartile"] = g5.groupby("fq")["sx"].agg(["count", "mean"])
    g5["r30q"] = pd.qcut(g5["r30"].rank(method="first"), 4, labels=["deepest", "q2", "q3", "shallowest"])
    out["by_r30_quartile"] = g5.groupby("r30q")["sx"].agg(["count", "mean"])
    g5v = g5.dropna(subset=["vr"]).copy()
    g5v["vq"] = pd.qcut(g5v["vr"].rank(method="first"), 3, labels=["quiet", "mid", "heavy"])
    out["by_volume_tercile"] = g5v.groupby("vq")["sx"].agg(["count", "mean"])
    out["vol_x_depth"] = g5v.groupby(["vq", g5v["r30"] < g5v["r30"].median()])["sx"].mean().unstack()
    # all bars with r30<0 by regime (in profile vs outside)
    ga = A[(A.pos % 5 == 0) & (A.r30 < 0)].copy()
    ga["sx"] = -(ga["f5"] - ga["coin"].map(drift[5]))
    ga["inprof"] = ga["reg"] != "chop"
    out["r30neg_by_inprofile"] = ga.groupby("inprof")["sx"].agg(["count", "mean"])
    # correlation depth vs forward in profile
    gg = g5.dropna(subset=["f5", "r30"])
    out["spearman_r30_vs_f5_inprof"] = float(stats.spearmanr(gg["r30"], gg["f5"]).correlation)
    return out
