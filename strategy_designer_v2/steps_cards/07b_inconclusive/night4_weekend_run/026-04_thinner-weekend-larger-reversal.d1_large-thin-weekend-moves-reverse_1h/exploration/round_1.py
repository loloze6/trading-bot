def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        # coin's normal drift / usual move over 48h, 24h, 96h on non-overlapping grids
        dd = {}
        for h in (24, 48, 96):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            dd[h] = (np.nanmean(rs), np.nanstd(rs))
        drift[coin] = dd
        for w, df in wins.items():
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values.astype(float)
            v = df["volume"].values.astype(float)
            n = len(c)
            s = pd.Series(c)
            r48 = s / s.shift(48) - 1
            usual = r48.abs().rolling(720, min_periods=360).mean()
            vs = pd.Series(v)
            far = vs.shift(48).rolling(120).mean()   # bars t-167..t-48
            near = vs.rolling(48).mean()            # bars t-47..t
            thin = far / near
            hr = ts.dt.hour.values
            wd = ts.dt.weekday.values
            sel = np.where(hr == 23)[0]
            for i in sel:
                rec = {"coin": coin, "win": w, "year": ts.iloc[i].year,
                       "wd": wd[i], "move": r48.iloc[i], "usual": usual.iloc[i],
                       "thin": thin.iloc[i]}
                for h in (24, 48, 96):
                    rec[f"f{h}"] = (c[i + h] / c[i] - 1 - drift[coin][h][0]) if i + h < n else np.nan
                rows.append(rec)
    D = pd.DataFrame(rows).dropna(subset=["move", "usual", "thin"])
    D["mz"] = D["move"] / D["usual"]
    D["x"] = -D["mz"] * D["thin"]
    out = {}

    def reg(d, xcol, ycol):
        d = d.dropna(subset=[xcol, ycol])
        if len(d) < 20:
            return (np.nan, np.nan, len(d))
        r = stats.linregress(d[xcol], d[ycol])
        return (r.slope, r.slope / r.stderr, len(d))

    # Sunday close (wd==6, hour 23) vs other weekday closes, horizons
    t = []
    for day in range(7):
        d = D[D.wd == day]
        for h in (24, 48, 96):
            s1 = reg(d, "x", f"f{h}")
            d2 = d.assign(nm=-d["mz"])
            s2 = reg(d2, "nm", f"f{h}")
            t.append({"day": day, "h": h, "slope_x": s1[0], "t_x": s1[1],
                      "slope_negmove": s2[0], "t_negmove": s2[1], "n": s1[2]})
    out["by_day_horizon (6=Sunday)"] = pd.DataFrame(t)

    S = D[D.wd == 6].copy()
    S["signed48"] = np.sign(S["x"]) * S["f48"]
    # by coin
    out["sunday_by_coin"] = pd.DataFrame([
        dict(coin=k, slope_t=reg(g, "x", "f48")[1], n=len(g),
             mean_signed=g["signed48"].mean(),
             t_signed=stats.ttest_1samp(g["signed48"].dropna(), 0).statistic)
        for k, g in S.groupby("coin")])
    out["sunday_by_year"] = pd.DataFrame([
        dict(year=k, slope_t=reg(g, "x", "f48")[1], n=len(g),
             mean_signed=g["signed48"].mean())
        for k, g in S.groupby("year")])
    # quintiles of |mz| and thinness
    S["q_move"] = pd.qcut(S["mz"].abs(), 5, labels=False)
    S["q_thin"] = pd.qcut(S["thin"], 5, labels=False)
    S["rev48"] = -np.sign(S["mz"]) * S["f48"]
    out["sunday_rev_by_move_q"] = S.groupby("q_move").agg(
        n=("rev48", "size"), mean_rev=("rev48", "mean"), mz=("mz", lambda x: x.abs().mean()))
    out["sunday_rev_by_thin_q"] = S.groupby("q_thin").agg(
        n=("rev48", "size"), mean_rev=("rev48", "mean"), thin=("thin", "mean"))
    out["sunday_rev_by_side (move up=1)"] = S.groupby(S["mz"] > 0).agg(
        n=("rev48", "size"), mean_rev=("rev48", "mean"),
        t=("rev48", lambda x: stats.ttest_1samp(x.dropna(), 0).statistic))
    out["thin_stats"] = S["thin"].describe()
    return out
