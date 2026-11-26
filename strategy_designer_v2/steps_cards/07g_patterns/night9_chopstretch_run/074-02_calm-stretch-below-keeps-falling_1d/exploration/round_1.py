def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sma = c.rolling(20, min_periods=20).mean()
            sd = r.rolling(20, min_periods=20).std()
            st = (c - sma) / sma / sd
            fwd10 = c.shift(-10) / c - 1
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ret5 = c / c.shift(5) - 1
            tr60 = c / c.shift(60) - 1
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "st": st, "r": r,
                               "fwd10": fwd10, "fwd5": fwd5, "fwd1": fwd1, "ret5": ret5, "tr60": tr60,
                               "rng": rng, "clpos": clpos, "regime": b["regime"].values,
                               "fc": b["forecast"].astype(float),
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "sd": sd})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["calm"] = np.where(A["regime"] == "chop", "agit", "calm")
    out = {}
    # drift per coin over all windows (grid 10)
    g10 = A[A["pos"] % 10 == 0].dropna(subset=["fwd10"])
    drift = g10.groupby("coin")["fwd10"].mean()
    g10 = g10.assign(ex=g10["fwd10"] - g10["coin"].map(drift))
    gg = g10.dropna(subset=["st"]).copy()
    gg["q"] = pd.qcut(gg["st"], 5, labels=False)
    def summ(x):
        return pd.Series({"n": len(x), "mean_ex10": x["ex"].mean(), "t": x["ex"].mean() / (x["ex"].std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "st_mean": x["st"].mean()})
    out["10d_excess_by_stretch_quintile_and_regime"] = gg.groupby(["calm", "q"]).apply(summ)
    # slope by regime
    res = {}
    for reg, x in gg.groupby("calm"):
        for side, y in [("below", x[x["st"] < 0]), ("above", x[x["st"] > 0]), ("all", x)]:
            s = stats.linregress(y["st"], y["ex"])
            res[(reg, side)] = {"n": len(y), "slope": s.slope, "t": s.slope / s.stderr}
    out["slope_ex10_on_stretch"] = pd.DataFrame(res).T
    # trend profile split
    gg["trend"] = np.where(gg["tr60"] > 0.1, "rising", np.where(gg["tr60"] < -0.1, "falling", np.where(gg["tr60"].notna(), "choppy", "na")))
    res = {}
    for (reg, tr), x in gg.groupby(["calm", "trend"]):
        if len(x) > 20:
            s = stats.linregress(x["st"], x["ex"])
            res[(reg, tr)] = {"n": len(x), "mean_ex": x["ex"].mean(), "slope": s.slope, "t": s.slope / s.stderr}
    out["slope_by_profile"] = pd.DataFrame(res).T
    # 1-day returns after large moves, by regime
    d1 = A.dropna(subset=["fwd1", "r", "sd"]).copy()
    d1["z"] = d1["r"] / d1["sd"]
    d1["zq"] = pd.cut(d1["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["next1d_by_today_z_regime"] = d1.groupby(["calm", "zq"])["fwd1"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    # close position in range vs next 1d, 5d grid
    g5 = A[A["pos"] % 5 == 0].dropna(subset=["fwd5", "clpos"]).copy()
    d5 = g5.groupby("coin")["fwd5"].mean()
    g5["ex"] = g5["fwd5"] - g5["coin"].map(d5)
    g5["cq"] = pd.qcut(g5["clpos"], 5, labels=False)
    out["5d_ex_by_closepos_regime"] = g5.groupby(["calm", "cq"])["ex"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    # weekday
    out["next1d_by_weekday"] = d1.groupby("wd")["fwd1"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    # 5d momentum
    g5b = g5.dropna(subset=["ret5", "sd"]).copy()
    g5b["m"] = g5b["ret5"] / (g5b["sd"] * np.sqrt(5))
    g5b["mq"] = pd.qcut(g5b["m"], 5, labels=False)
    out["5d_ex_by_past5d_z_regime"] = g5b.groupby(["calm", "mq"])["ex"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    # book
    bd = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            bd.append(d.assign(coin=coin, w=w))
    D = pd.concat(bd).dropna(subset=["book_return"])
    out["book_by_window"] = D.groupby("w")["book_return"].agg(["count", "mean", "sum"])
    out["share_calm_bars"] = (A["calm"] == "calm").mean()
    return out
