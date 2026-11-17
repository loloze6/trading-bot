def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "r": r, "z": r / vol,
                "z2": (c / c.shift(2) - 1) / (vol * np.sqrt(2)),
                "vr": b["volume"].astype(float) / b["volume"].astype(float).rolling(20).mean(),
                "vlev": vol / vol.rolling(120, min_periods=60).median(),
                "n1": c.shift(-1) / c - 1,
                "n3": c.shift(-3) / c - 1,
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r"].mean()
    D["x1"] = D["n1"] - D["coin"].map(mu)
    D["x3"] = D["n3"] - 3 * D["coin"].map(mu)

    def slope(df, y="x1", x="z"):
        df = df[[x, y]].dropna()
        df = df[np.isfinite(df[x])]
        if len(df) < 30:
            return pd.Series({"slope": np.nan, "t": np.nan, "n": len(df)})
        res = stats.linregress(df[x], df[y])
        return pd.Series({"slope": res.slope, "t": res.slope / res.stderr, "n": len(df)})

    out = {}
    # slope of next-day return on z, by weekday of the signal bar
    out["slope_next1_on_z_by_wd"] = D.groupby("wd").apply(slope)

    # mean next-day excess return by weekday of the signal bar
    g = D.dropna(subset=["x1"]).groupby("wd")["x1"]
    out["mean_next1_by_wd"] = pd.DataFrame({
        "mean": g.mean(),
        "t": g.mean() / (g.std() / np.sqrt(g.count())),
        "n": g.count(),
    })

    # outcome by z quintile, all days
    D["zq"] = pd.qcut(D["z"].replace([np.inf, -np.inf], np.nan), 5, labels=False)
    g = D.dropna(subset=["x1"]).groupby("zq")["x1"]
    out["next1_by_zq_all"] = pd.DataFrame({
        "mean": g.mean(),
        "t": g.mean() / (g.std() / np.sqrt(g.count())),
        "n": g.count(),
    })

    # non-overlapping 3-day grid
    D3 = D[D["pos"] % 3 == 0].dropna(subset=["x3"])
    g = D3.groupby("zq")["x3"]
    out["next3_by_zq_grid"] = pd.DataFrame({
        "mean": g.mean(),
        "t": g.mean() / (g.std() / np.sqrt(g.count())),
        "n": g.count(),
    })

    # slope on z by volatility level tercile (all days)
    D["vq"] = pd.qcut(D["vlev"], 3, labels=False)
    out["slope_by_vol_tercile"] = D.groupby("vq").apply(slope)

    # slope on z by volume-ratio tercile (all days, then Sunday only)
    D["vrq"] = pd.qcut(D["vr"], 3, labels=False)
    out["slope_by_volratio_tercile_all"] = D.groupby("vrq").apply(slope)
    out["slope_by_volratio_tercile_sun"] = D[D["wd"] == 6].groupby("vrq").apply(slope)

    # Sunday slope by coin and by year
    out["sun_slope_by_coin"] = D[D["wd"] == 6].groupby("coin").apply(slope)
    out["sun_slope_by_year"] = D[D["wd"] == 6].groupby("year").apply(slope)

    # weekend two-day move (Fri->Sun close) vs next 1 day, and Sunday next 3 days
    out["sun_z2_slope_next1"] = slope(D[D["wd"] == 6], "x1", "z2")
    out["sun_slope_next3"] = slope(D[(D["wd"] == 6)], "x3", "z")

    # book: daily returns by weekday
    bd = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy()
            x["coin"] = coin
            bd.append(x)
    B = pd.concat(bd)
    B["wd"] = pd.to_datetime(B["day"]).dt.weekday
    daily = B.groupby(["day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), wd=("wd", "first"))
    g = daily.groupby("wd")["br"]
    out["book_by_wd"] = pd.DataFrame({"mean": g.mean(), "std": g.std(), "n": g.count()})
    return out
