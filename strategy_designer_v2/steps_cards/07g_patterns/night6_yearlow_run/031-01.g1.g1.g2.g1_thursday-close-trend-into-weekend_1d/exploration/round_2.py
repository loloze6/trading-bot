def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            s = pd.Series(b["close"].astype(float).values)
            n = len(s)
            df = pd.DataFrame({"coin": coin, "win": w, "date": ts.dt.floor("D").values,
                               "year": ts.dt.year.values,
                               "wd_next": ((ts + pd.Timedelta(days=1)).dt.weekday).values,
                               "pos": np.arange(n)})
            df["r1"] = s.pct_change()
            df["vol20"] = df["r1"].rolling(20).std()
            df["r3"] = s / s.shift(3) - 1
            df["r14"] = s / s.shift(14) - 1
            df["f1"] = s.shift(-1) / s - 1
            df["f3"] = s.shift(-3) / s - 1
            lo20 = s.rolling(20).min()
            df["dlow20"] = s / lo20 - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 3):
        g = D[D["pos"] % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean(); sd = g.groupby("coin")[f"f{h}"].std()
        D[f"x{h}"] = (D[f"f{h}"] - D["coin"].map(m)) / D["coin"].map(sd)
    D["r1z"] = D["r1"] / D["vol20"]
    D["r3z"] = D["r3"] / (D["vol20"] * np.sqrt(3))

    def clu(g, xcol, ycol):
        g = g.dropna(subset=[xcol, ycol])
        X = g[xcol] - g[xcol].mean()
        beta = (X * g[ycol]).sum() / (X ** 2).sum()
        e = g[ycol] - g[ycol].mean() - beta * X
        sc = (X * e).groupby(g["date"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (X ** 2).sum()
        return pd.Series({"slope": beta, "t": beta / se, "days": g["date"].nunique(), "n": len(g)})

    out = {}
    dn = D[D["r1z"] < 0]
    up = D[D["r1z"] > 0]
    out["next1_on_down_day_size"] = clu(dn, "r1z", "x1")
    out["next1_on_up_day_size"] = clu(up, "r1z", "x1")
    out["next1_on_r1z_all"] = clu(D, "r1z", "x1")
    out["down_slope_by_year"] = dn.groupby("year").apply(lambda g: clu(g, "r1z", "x1"))
    out["down_slope_by_coin"] = dn.groupby("coin").apply(lambda g: clu(g, "r1z", "x1"))
    out["down_slope_by_nextwd"] = dn.groupby("wd_next").apply(lambda g: clu(g, "r1z", "x1"))
    D["vt"] = D.groupby("coin")["vol20"].transform(lambda v: pd.qcut(v, 3, labels=False, duplicates="drop"))
    out["down_slope_by_vol"] = D[D["r1z"] < 0].groupby("vt").apply(lambda g: clu(g, "r1z", "x1"))
    g3 = D[(D["pos"] % 3 == 0) & (D["r3z"] < 0)]
    out["next3_on_down3_size"] = clu(g3, "r3z", "x3")
    g3u = D[(D["pos"] % 3 == 0) & (D["r3z"] > 0)]
    out["next3_on_up3_size"] = clu(g3u, "r3z", "x3")
    # weekend gain graded by r14 z?
    D["r14z"] = D["r14"] / (D["vol20"] * np.sqrt(14))
    fr = D[D["wd_next"].isin([5])]
    out["sat_x1_on_r14z"] = clu(fr, "r14z", "x1")
    out["sat_x1_by_year"] = fr.groupby("year")["x1"].agg(["mean", "count"])
    th = D[D["wd_next"] == 3]
    out["thu_x1_by_year"] = th.groupby("year")["x1"].agg(["mean", "count"])
    return out
