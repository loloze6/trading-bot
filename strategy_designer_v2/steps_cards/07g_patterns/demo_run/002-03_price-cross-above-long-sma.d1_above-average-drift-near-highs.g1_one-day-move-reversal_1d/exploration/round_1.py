def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=10).std()
            z = r1 / sd20
            nxt = c.shift(-1) / c - 1
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            sma50 = c.rolling(50, min_periods=30).mean()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "z": z, "nxt": nxt, "r1": r1,
                              "r5z": r5 / (sd20 * np.sqrt(5)), "r20z": r20 / (sd20 * np.sqrt(20)),
                              "above": (c > sma50).astype(float).where(sma50.notna()),
                              "vol": sd20, "wd": ts.dt.weekday, "year": ts.dt.year,
                              "pos": b["postRebalance_current_allocation"].astype(float),
                              "fc": b["forecast"].astype(float)})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["nxt"].transform("mean")
    D["ex"] = D["nxt"] - mu
    out = {}
    X = D.dropna(subset=["z", "ex"]).copy()
    X["zq"] = pd.qcut(X["z"], 10, labels=False)
    out["next_ex_by_z_decile"] = X.groupby("zq").agg(n=("ex", "size"), zmean=("z", "mean"), ex=("ex", "mean"),
        t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    # per coin slope t
    pc = {}
    for coin, g in X.groupby("coin"):
        s = stats.linregress(g["z"], g["ex"]); pc[coin] = s.slope / s.stderr
    out["slope_t_by_coin"] = pd.Series(pc)
    py = {}
    for y, g in X.groupby("year"):
        s = stats.linregress(g["z"], g["ex"]); py[y] = round(s.slope / s.stderr, 2)
    out["slope_t_by_year"] = pd.Series(py)
    # multi-day horizon momentum: 5d and 20d scaled return vs next day
    for col in ["r5z", "r20z"]:
        Y = D.dropna(subset=[col, "ex"]).copy()
        Y["q"] = pd.qcut(Y[col], 5, labels=False)
        out["next_ex_by_" + col] = Y.groupby("q").agg(n=("ex", "size"), x=(col, "mean"), ex=("ex", "mean"),
            t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    # reversal by trend state
    out["z_slope_by_above_sma50"] = X.dropna(subset=["above"]).groupby("above").apply(
        lambda g: pd.Series({"n": len(g), "t": (lambda s: s.slope / s.stderr)(stats.linregress(g["z"], g["ex"]))}))
    # vol level
    X["vq"] = X.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["z_slope_by_vol_tercile"] = X.groupby("vq").apply(
        lambda g: pd.Series({"n": len(g), "slope": stats.linregress(g["z"], g["ex"]).slope,
                             "t": (lambda s: s.slope / s.stderr)(stats.linregress(g["z"], g["ex"]))}))
    out["next_ex_by_weekday"] = X.groupby("wd").agg(n=("ex", "size"), ex=("ex", "mean"),
        t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    # book pnl by position sign and size
    D["g"] = D["pos"] * D["nxt"]
    D["mkt"] = D["pos"] * mu
    out["book_gain_by_side"] = D.dropna(subset=["g"]).assign(side=np.sign(D["pos"])).groupby("side").agg(
        n=("g", "size"), gain=("g", "mean"), mkt=("mkt", "mean"), pos=("pos", "mean"))
    out["pos_corr_fc"] = float(D[["pos", "fc"]].corr().iloc[0, 1])
    return out
