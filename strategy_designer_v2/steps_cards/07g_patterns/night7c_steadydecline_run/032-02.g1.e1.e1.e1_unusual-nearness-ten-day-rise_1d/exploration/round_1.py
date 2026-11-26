def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "fc": df["forecast"].astype(float),
                "r28": c / c.shift(28) - 1,
                "r10": c / c.shift(10) - 1,
                "r3": c / c.shift(3) - 1,
                "vol20": r1.rolling(20).std(),
                "volratio": r1.rolling(10).std() / r1.rolling(60, min_periods=30).std(),
                "rngratio": ((h - l) / c).rolling(10).mean() / ((h - l) / c).rolling(60, min_periods=30).mean(),
                "vlmratio": v.rolling(10).mean() / v.rolling(60, min_periods=30).mean(),
                "dlow": c / c.rolling(28).min() - 1,
                "dhigh": c / c.rolling(28).max() - 1,
                "dow": pd.to_datetime(df["timestamp"]).dt.dayofweek,
                "fwd": c.shift(-H) / c - 1,
                "pos": df["postRebalance_current_allocation"].astype(float),
            })
            f["day"] = pd.to_datetime(df["timestamp"]).dt.floor("D")
            g = f.iloc[::H].copy()
            g = g[g["fwd"].notna()]
            g["coin"] = coin; g["win"] = w
            rows.append(g)
    G = pd.concat(rows, ignore_index=True)
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    out = {}
    feats = ["fc", "r28", "r10", "r3", "vol20", "volratio", "rngratio", "vlmratio", "dlow", "dhigh"]
    corr = []
    for ft in feats:
        s = G[[ft, "ex", "coin"]].dropna()
        s["q"] = s.groupby("coin")[ft].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        rho, p = stats.spearmanr(s[ft], s["ex"])
        m = s.groupby("q")["ex"].agg(["mean", "count"])
        top = s[s.q == 4]["ex"]; bot = s[s.q == 0]["ex"]
        t = stats.ttest_ind(top, bot, equal_var=False).statistic
        corr.append({"feat": ft, "rho": rho, "p": p, "n": len(s), "q0": m["mean"].iloc[0], "q1": m["mean"].iloc[1],
                     "q2": m["mean"].iloc[2], "q3": m["mean"].iloc[3], "q4": m["mean"].iloc[4], "t_q4_q0": t})
    out["feature_quintiles_excess10d"] = pd.DataFrame(corr).round(4)
    # interaction: fc quintile within vol regime
    s = G.dropna(subset=["fc", "vol20"]).copy()
    s["volhi"] = s.groupby("coin")["vol20"].transform(lambda x: x > x.median())
    s["fcq"] = s.groupby("coin")["fc"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["ex_by_volhalf_fcterc"] = s.groupby(["volhi", "fcq"])["ex"].agg(["mean", "count"]).round(4)
    s["r28q"] = s.groupby("coin")["r28"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["ex_by_r28terc_fcterc"] = s.dropna(subset=["r28q"]).groupby(["r28q", "fcq"])["ex"].agg(["mean", "count"]).round(4)
    out["ex_by_coin_fcsign"] = G.groupby(["coin", np.sign(G["fc"])])["ex"].agg(["mean", "count"]).round(4).unstack()
    out["ex_by_win_fcsign"] = G.groupby(["win", np.sign(G["fc"])])["ex"].mean().round(4).unstack()
    # daily book and coin returns
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    D["dow"] = pd.to_datetime(D["day"]).dt.dayofweek
    dd = D.groupby("dow")[["book_return", "coin_return"]].agg(["mean", "std", "count"])
    out["daily_by_weekday"] = dd.round(5)
    # coin next-day return after large daily move
    D = D.sort_values(["coin", "win", "day"])
    D["next"] = D.groupby(["coin", "win"])["coin_return"].shift(-1)
    D["z"] = D["coin_return"] / D.groupby("coin")["coin_return"].transform("std")
    D["zb"] = pd.cut(D["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["next_day_after_move"] = D.groupby("zb")["next"].agg(["mean", "count", "std"]).round(5)
    return out
