def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    allfwd = {}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi = c.rolling(20, min_periods=20).max().shift(1)
            sd = r1.rolling(20, min_periods=15).std()
            dist = (c / hi - 1) / sd
            ret5p = c / c.shift(5) - 1
            ret1 = r1
            rng = (b["high"] - b["low"]) / c
            rngz = rng / rng.rolling(20, min_periods=10).mean()
            fwd = c.shift(-H) / c - 1
            pos = np.arange(len(b))
            g = (pos % H == 0)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "w": w, "dist": dist, "fwd": fwd, "grid": g,
                "rising": (b["regime"] != "chop"), "fc": b["forecast"],
                "ret1": ret1, "ret5p": ret5p, "sd": sd, "rngz": rngz,
                "wd": ts.dt.weekday, "alloc": b["postRebalance_current_allocation"],
                "next1": c.shift(-1) / c - 1,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    coinmean = d[d.grid].groupby("coin")["fwd"].mean()
    d["ex"] = d["fwd"] - d["coin"].map(coinmean)
    gdf = d[d.grid].dropna(subset=["ex", "dist"])
    def summ(x):
        n = len(x); m = x.mean(); s = x.std(ddof=1)
        return pd.Series({"n": n, "mean_ex": m, "t": m / (s / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    bins = [-np.inf, -4, -2.5, -1.5, -0.75, -0.0001, 0.0001, 0.5, 1, np.inf]
    gdf["db"] = pd.cut(gdf["dist"], bins)
    out["dist_bins_rising"] = gdf[gdf.rising].groupby("db")["ex"].apply(summ).unstack()
    out["dist_bins_notrising"] = gdf[~gdf.rising].groupby("db")["ex"].apply(summ).unstack()
    # slope tests
    for lab, sub in [("rising", gdf[gdf.rising]), ("notrising", gdf[~gdf.rising]), ("all", gdf)]:
        s = stats.linregress(sub["dist"].clip(-6, 3), sub["ex"])
        out["slope_" + lab] = f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(sub)}"
    # past 5d return
    gdf["pb"] = pd.qcut(gdf["ret5p"], 5)
    out["past5_rising"] = gdf[gdf.rising].groupby("pb")["ex"].apply(summ).unstack()
    out["past5_notrising"] = gdf[~gdf.rising].groupby("pb")["ex"].apply(summ).unstack()
    gdf["r1z"] = gdf["ret1"] / gdf["sd"]
    gdf["r1b"] = pd.qcut(gdf["r1z"], 5)
    out["ret1z_all"] = gdf.groupby("r1b")["ex"].apply(summ).unstack()
    gdf["rgb"] = pd.qcut(gdf["rngz"], 5)
    out["rangez_all"] = gdf.groupby("rgb")["ex"].apply(summ).unstack()
    out["by_window"] = gdf[gdf.rising & (gdf.dist < 0)].groupby("w")["ex"].apply(summ).unstack()
    # daily next-day by weekday, all bars
    dd = d.dropna(subset=["next1"])
    out["weekday_next1"] = dd.groupby("wd")["next1"].apply(summ).unstack()
    return out
