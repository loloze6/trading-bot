def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            lo = df["low"].astype(float); hi = df["high"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd5": c.shift(-5) / c - 1,
                "past5": c / c.shift(5) - 1,
                "past20": c / c.shift(20) - 1,
                "past1": r1,
                "vol20": r1.rolling(20, min_periods=15).std(),
                "dlow30": c / lo.rolling(30, min_periods=20).min() - 1,
                "dhigh30": c / hi.rolling(30, min_periods=20).max() - 1,
                "range1": (hi - lo) / c,
                "fc": df["forecast"].astype(float),
                "raw": df.get("debug_info.components.support_touches.last_history_value", pd.Series(np.nan, index=df.index)).astype(float),
                "pos": np.arange(len(df)),
            })
            f["vchg"] = f["vol20"] / f["vol20"].shift(20) - 1
            rows.append(f[f["pos"] % 5 == 0])
    g = pd.concat(rows, ignore_index=True)
    g = g.dropna(subset=["fwd5"])
    drift = g.groupby("coin")["fwd5"].agg(["mean", "std"])
    g["ex"] = g["fwd5"] - g["coin"].map(drift["mean"])
    g["z"] = g["ex"] / g["coin"].map(drift["std"])
    out = {"n_grid": len(g), "drift_by_coin": drift}
    feats = ["past1", "past5", "past20", "vol20", "dlow30", "dhigh30", "range1", "vchg", "raw"]
    summ = []
    for ft in feats:
        s = g.dropna(subset=[ft])
        rho, p = stats.spearmanr(s[ft], s["z"])
        s = s.copy()
        s["q"] = s.groupby("coin")[ft].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        m = s.groupby("q")["ex"].mean()
        top = s[s.q == 4]["ex"]; bot = s[s.q == 0]["ex"]
        t = stats.ttest_ind(top, bot, equal_var=False).statistic
        # per coin sign of spearman
        pc = s.groupby("coin").apply(lambda x: stats.spearmanr(x[ft], x["z"])[0])
        summ.append({"feat": ft, "n": len(s), "rho": rho, "p": p,
                     "q0": m.get(0), "q1": m.get(1), "q2": m.get(2), "q3": m.get(3), "q4": m.get(4),
                     "t_q4_q0": t, "coins_pos_rho": int((pc > 0).sum())})
    out["features"] = pd.DataFrame(summ).set_index("feat")
    # forecast active vs not
    act = g[g.fc > 0]["ex"]; ina = g[g.fc == 0]["ex"]
    out["fc_active_vs_flat"] = pd.Series({"n_act": len(act), "mean_act": act.mean(), "n_flat": len(ina),
                                          "mean_flat": ina.mean(), "t": stats.ttest_ind(act, ina, equal_var=False).statistic})
    # weekday of daily coin returns and book returns
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; dl.append(d)
    D = pd.concat(dl, ignore_index=True)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    wd = D.groupby("wd")["coin_return"].agg(["mean", "std", "count"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday_coin"] = wd
    out["by_year_ex_after_fall"] = g.assign(yr=None).dropna(subset=["past5"]).pipe(lambda s: s.assign(fall=(s.past5 < 0))).groupby("fall")["ex"].agg(["mean", "count"])
    return out
