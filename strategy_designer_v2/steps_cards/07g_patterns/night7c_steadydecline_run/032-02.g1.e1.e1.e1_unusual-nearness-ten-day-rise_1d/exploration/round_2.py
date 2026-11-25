def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- daily reversal after large moves, day-clustered t, graded, by window ----
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.sort_values("day").copy(); d["coin"] = coin; d["win"] = w
            c = d["close"].astype(float)
            d["r1"] = c.pct_change()
            d["f1"] = c.shift(-1) / c - 1
            d["f3"] = c.shift(-3) / c - 1
            d["sd60"] = d["r1"].rolling(60, min_periods=20).std().shift(1)
            d["z"] = d["r1"] / d["sd60"]
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    D["f1x"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")
    D["zb"] = pd.cut(D["z"], [-99, -3, -2, -1, 0, 1, 2, 3, 99])
    res = []
    for b, s in D.dropna(subset=["z", "f1x"]).groupby("zb", observed=True):
        dd = s.groupby("day")["f1x"].sum()
        t = dd.mean() / (dd.std(ddof=1) / np.sqrt(len(dd))) if len(dd) > 2 else np.nan
        res.append({"zbin": str(b), "n": len(s), "days": len(dd), "mean_next1": s["f1x"].mean(), "t_day": t})
    out["next1_by_z_own60sd"] = pd.DataFrame(res).round(4)
    # graded gain -z * next (signed) day-clustered
    s = D.dropna(subset=["z", "f1x"]).copy()
    s["g"] = -s["z"].clip(-5, 5) * s["f1x"]
    dd = s.groupby("day")["g"].sum()
    out["reversal_graded_t"] = pd.Series({"mean": s["g"].mean(), "t_day": dd.mean() / (dd.std() / np.sqrt(len(dd))), "days": len(dd)}).round(5)
    s["absz"] = s["z"].abs()
    s["ab"] = pd.cut(s["absz"], [0, 1, 2, 3, 99])
    out["reversal_by_absz"] = s.groupby("ab", observed=True)["g"].agg(["mean", "count"]).round(5)
    out["reversal_by_win"] = s.groupby("win")["g"].mean().round(5)
    out["reversal_by_coin"] = s.groupby("coin")["g"].mean().round(5)
    # down-only large falls, 3-day horizon nonoverlap not needed for event study: per event
    s["f3x"] = s["f3"] - s.groupby("coin")["f3"].transform("mean")
    out["next3_by_zbin"] = s.groupby(pd.cut(s["z"], [-99, -2, -1, 1, 2, 99]), observed=True)["f3x"].agg(["mean", "count"]).round(4)
    # weekday coin return t, day clustered
    D["dow"] = pd.to_datetime(D["day"]).dt.dayofweek
    wk = []
    for k, q in D.dropna(subset=["r1"]).groupby("dow"):
        dd = q.groupby("day")["r1"].mean()
        wk.append({"dow": k, "mean": dd.mean(), "t": dd.mean() / (dd.std() / np.sqrt(len(dd))), "days": len(dd)})
    out["weekday_coin_t"] = pd.DataFrame(wk).round(4)
    # ---- raw closeness to 28d high on 10-day grid, and beyond forecast ----
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            g = pd.DataFrame({"fc": df["forecast"].astype(float), "dh": c / c.rolling(28).max() - 1,
                              "fwd": c.shift(-10) / c - 1, "day": pd.to_datetime(df["timestamp"]).dt.floor("D")}).iloc[::10]
            g = g[g.fwd.notna()]; g["coin"] = coin; g["win"] = w; rows.append(g)
    G = pd.concat(rows, ignore_index=True)
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    G = G.dropna(subset=["dh"])
    G["dhz"] = G.groupby("coin")["dh"].transform(lambda x: (x - x.mean()) / x.std())
    G["g"] = G["dhz"] * G["ex"]
    dd = G.groupby("day")["g"].sum()
    out["dhigh_graded_t"] = pd.Series({"mean": G["g"].mean(), "t_day": dd.mean() / (dd.std() / np.sqrt(len(dd))), "days": len(dd), "n": len(G)}).round(5)
    X = np.column_stack([np.ones(len(G)), G["dhz"], G["fc"] / 10])
    b, *_ = np.linalg.lstsq(X, G["ex"].values, rcond=None)
    e = G["ex"].values - X @ b
    cov = np.linalg.inv(X.T @ X) * (e @ e) / (len(G) - 3)
    out["ols_ex_on_dhz_fc"] = pd.DataFrame({"b": b, "t": b / np.sqrt(np.diag(cov))}, index=["c", "dhz", "fc10"]).round(4)
    out["dhigh_by_win"] = G.groupby("win")["g"].mean().round(4)
    out["dhigh_by_coin"] = G.groupby("coin")["g"].mean().round(4)
    return out
