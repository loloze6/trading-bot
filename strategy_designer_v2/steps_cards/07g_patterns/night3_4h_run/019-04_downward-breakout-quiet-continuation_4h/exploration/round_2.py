def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            if n < H + 2: continue
            fwd = c.shift(-H) / c - 1
            minlo = lo.shift(1).rolling(12).min(); maxhi = hi.shift(1).rolling(12).max()
            mbr = ((hi - lo) / c).rolling(180, min_periods=60).mean()
            width = ((maxhi - minlo) / c.shift(1)) / mbr
            r1 = np.log(c).diff()
            ts = pd.to_datetime(b["timestamp"])
            f = pd.DataFrame({
                "fwd": fwd, "width": width,
                "ret1d": c / c.shift(6) - 1,
                "volratio": r1.rolling(42).std() / r1.rolling(180, min_periods=60).std(),
                "wd": ts.dt.weekday, "year": ts.dt.year,
                "pos": np.arange(n),
            })
            f["coin"] = coin; f["win"] = w
            rows.append(f)
    full = pd.concat(rows, ignore_index=True)
    out = {}
    # drift and std per coin from offset-0 grid
    g0 = full[(full["pos"] % H == 0) & full["fwd"].notna()]
    drift = g0.groupby("coin")["fwd"].mean(); sd = g0.groupby("coin")["fwd"].std()
    full["ex"] = full["fwd"] - full["coin"].map(drift)
    full["z"] = full["ex"] / full["coin"].map(sd)
    res = []
    for off in [0, 3, 6, 9, 12, 15]:
        d = full[((full["pos"] - off) % H == 0) & full["fwd"].notna()].copy()
        r = {"off": off}
        for col in ["width", "ret1d", "volratio"]:
            dd = d[d[col].notna()].copy()
            dd["bin"] = dd.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
            lo_ = dd[dd["bin"] == 0]["ex"]; hi_ = dd[dd["bin"] == 4]["ex"]
            r[col + "_q0"] = lo_.mean(); r[col + "_q4"] = hi_.mean()
            r[col + "_t_q4mq0"] = stats.ttest_ind(hi_, lo_, equal_var=False)[0]
        s = d[d["wd"] == 6]["ex"]; o = d[d["wd"] != 6]["ex"]
        r["sun_minus_other"] = s.mean() - o.mean()
        r["sun_t"] = stats.ttest_ind(s, o, equal_var=False)[0]
        res.append(r)
    out["by_grid_offset"] = pd.DataFrame(res).set_index("off").T
    d = g0.copy(); d["ex"] = full.loc[d.index, "ex"]; d["z"] = full.loc[d.index, "z"]
    per = []
    for coin, x in d.groupby("coin"):
        r = {"coin": coin}
        for col in ["width", "ret1d", "volratio"]:
            xx = x[x[col].notna()]
            rho, p = stats.spearmanr(xx[col], xx["z"])
            r[col + "_rho"] = rho
        per.append(r)
    out["per_coin_rho"] = pd.DataFrame(per).set_index("coin")
    yr = []
    for y, x in d.groupby("year"):
        r = {"year": y, "n": len(x)}
        for col in ["width", "ret1d", "volratio"]:
            xx = x[x[col].notna()]
            r[col + "_rho"] = stats.spearmanr(xx[col], xx["z"])[0] if len(xx) > 30 else np.nan
        yr.append(r)
    out["per_year_rho"] = pd.DataFrame(yr).set_index("year")
    # ret1d quintiles: total move, strength
    dd = d[d["ret1d"].notna()].copy()
    dd["bin"] = dd.groupby("coin")["ret1d"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["ret1d_bins"] = dd.groupby("bin").agg(n=("ex", "size"), total=("fwd", "mean"), unusual=("ex", "mean"), strength=("z", "mean"))
    dd = d[d["width"].notna()].copy()
    dd["bin"] = dd.groupby("coin")["width"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["width_bins"] = dd.groupby("bin").agg(n=("ex", "size"), total=("fwd", "mean"), unusual=("ex", "mean"), strength=("z", "mean"))
    # book: days around largest losses
    dl = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; dl.append(x)
    D = pd.concat(dl, ignore_index=True).dropna(subset=["book_return", "coin_return"])
    out["book_vs_coin_corr"] = float(D["book_return"].corr(D["coin_return"]))
    out["book_by_coin"] = D.groupby("coin")["book_return"].agg(["mean", "std"])
    return out
