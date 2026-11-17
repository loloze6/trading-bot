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
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "wd": ts.dt.weekday, "year": ts.dt.year,
                "r": r, "z": r / vol,
                "vlev": vol / vol.rolling(120, min_periods=60).median(),
                "vr": b["volume"].astype(float) / b["volume"].astype(float).rolling(20).mean(),
                "n1": c.shift(-1) / c - 1, "n3": c.shift(-3) / c - 1,
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D[np.isfinite(D["z"])]
    mu = D.groupby("coin")["r"].mean()
    D["x1"] = D["n1"] - D["coin"].map(mu)
    D["x3"] = D["n3"] - 3 * D["coin"].map(mu)
    D["vq"] = pd.qcut(D["vlev"], 3, labels=False)

    def slope(df, y="x1", x="z"):
        df = df[[x, y]].dropna()
        if len(df) < 30:
            return pd.Series({"slope": np.nan, "t": np.nan, "n": len(df)})
        res = stats.linregress(df[x], df[y])
        return pd.Series({"slope": res.slope, "t": res.slope / res.stderr, "n": len(df)})

    out = {}
    D["grp"] = np.where(D["wd"].isin([5, 6]), "weekend", "weekday")
    out["slope_weekend_vs_weekday"] = D.groupby("grp").apply(slope)
    out["slope_all_by_year"] = D.groupby("year").apply(slope)
    out["slope_all_by_coin"] = D.groupby("coin").apply(slope)
    out["slope_by_vol_tercile_x_grp"] = D.groupby(["vq", "grp"]).apply(slope)
    out["slope_down_vs_up"] = D.groupby(D["z"] < 0).apply(slope)
    out["slope_down_up_by_vol"] = D.groupby([D["z"] < 0, "vq"]).apply(slope)
    # down-move reversal: next1 by z quintile within high vol tercile
    D["zq"] = pd.qcut(D["z"], 5, labels=False)
    g = D[D["vq"] == 2].dropna(subset=["x1"]).groupby("zq")["x1"]
    out["next1_by_zq_highvol"] = pd.DataFrame({"mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count()})
    # 3-day reversal on non-overlapping grid, all days
    D3 = D[D["pos"] % 3 == 0]
    out["slope_next3_grid_all"] = slope(D3, "x3", "z")
    out["slope_next3_grid_by_vol"] = D3.groupby("vq").apply(lambda x: slope(x, "x3", "z"))
    out["slope_next3_grid_by_year"] = D3.groupby("year").apply(lambda x: slope(x, "x3", "z"))
    # volume ratio interaction all days: z*vr
    D["vrq"] = pd.qcut(D["vr"], 3, labels=False)
    out["slope_by_vrq_x_vq"] = D.groupby(["vrq", "vq"]).apply(slope)
    return out
