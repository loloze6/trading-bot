def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    recs = []
    for coin, wins in bars.items():
        # drift & sd per horizon over all windows
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            ts = pd.to_datetime(df["timestamp"]) + pd.Timedelta(hours=1)
            n = len(c)
            if n < 900: continue
            s = pd.Series(c)
            d = pd.DataFrame({"coin": coin, "win": w, "hour": ts.dt.hour.values,
                              "wd": ts.dt.weekday.values, "year": ts.dt.year.values, "pos": np.arange(n)})
            for L in (2, 8, 24, 72):
                r = s / s.shift(L) - 1
                d[f"p{L}"] = (r / r.abs().rolling(720, min_periods=360).mean()).values
            for H in (8, 24, 72):
                d[f"f{H}"] = (s.shift(-H) / s - 1).values
            r1 = s.pct_change()
            d["vol"] = r1.rolling(720, min_periods=360).std().values
            recs.append(d)
    D = pd.concat(recs, ignore_index=True)
    for H in (8, 24, 72):
        g = D[D["pos"] % H == 0]
        st = g.groupby("coin")[f"f{H}"].agg(["mean", "std"])
        D[f"x{H}"] = (D[f"f{H}"] - D["coin"].map(st["mean"])) / D["coin"].map(st["std"])
        D[f"e{H}"] = D[f"f{H}"] - D["coin"].map(st["mean"])
    # A: by hour, fall2h -> 8h excess, one per day per hour
    rows = []
    for h in range(24):
        g = D[(D["hour"] == h) & (D["p2"] < 0)].dropna(subset=["p2", "x8"])
        wgt = -g["p2"]
        m = (g["x8"] * wgt).sum() / wgt.sum()
        sl = stats.linregress(-g["p2"], g["x8"])
        rows.append({"hour": h, "n": len(g), "wstrength": m, "slope_t": sl.slope / sl.stderr,
                     "mean_e8_pct": 100 * g["e8"].mean()})
    out["A_fall2h_by_close_hour_8h"] = pd.DataFrame(rows)
    # B: lookback x horizon, all hours, grid
    rows = []
    for L in (2, 8, 24, 72):
        for H in (8, 24, 72):
            g = D[(D["pos"] % H == 0)].dropna(subset=[f"p{L}", f"x{H}"])
            f = g[g[f"p{L}"] < 0]; wgt = -f[f"p{L}"]
            q = g[f"p{L}"] <= g.groupby("coin")[f"p{L}"].transform(lambda x: x.quantile(0.2))
            sl = stats.linregress(g[f"p{L}"], g[f"x{H}"])
            rows.append({"L_h": L, "H_h": H, "n": len(g), "corr": np.corrcoef(g[f"p{L}"], g[f"x{H}"])[0, 1],
                         "slope_t": sl.slope / sl.stderr,
                         "fall_wstrength": (f[f"x{H}"] * wgt).sum() / wgt.sum(),
                         "bottom20_e_pct": 100 * g.loc[q, f"e{H}"].mean(),
                         "bottom20_tot_pct": 100 * g.loc[q, f"f{H}"].mean(),
                         "top20_e_pct": 100 * g.loc[g[f"p{L}"] >= g.groupby("coin")[f"p{L}"].transform(lambda x: x.quantile(0.8)), f"e{H}"].mean() * 100 / 100,
                         "n_b20": int(q.sum())})
    out["B_lookback_horizon_all_hours"] = pd.DataFrame(rows)
    # C: vol tercile, 24h fall -> 24h
    g = D[D["pos"] % 24 == 0].dropna(subset=["p24", "x24", "vol"]).copy()
    g["vt"] = g.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    rows = []
    for v, gg in g.groupby("vt"):
        sl = stats.linregress(gg["p24"], gg["x24"])
        rows.append({"vol_tercile": v, "n": len(gg), "slope": sl.slope, "slope_t": sl.slope / sl.stderr})
    out["C_p24_x24_by_vol"] = pd.DataFrame(rows)
    # D: by coin, 24h->24h
    rows = []
    for coin, gg in g.groupby("coin"):
        sl = stats.linregress(gg["p24"], gg["x24"])
        rows.append({"coin": coin, "n": len(gg), "slope_t": sl.slope / sl.stderr})
    out["D_p24_x24_by_coin"] = pd.DataFrame(rows)
    # E: plain hourly returns by hour of close (1h ahead excess), and weekday 24h
    g1 = D.copy()
    rows = []
    for h, gg in D.groupby("hour"):
        x = gg["e8"].dropna()
        rows.append({"hour": h, "mean_e8_pct": 100 * x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)), "n": len(x)})
    out["E_unconditional_8h_by_hour"] = pd.DataFrame(rows)
    gw = D[D["hour"] == 0].dropna(subset=["e24"])
    out["F_24h_excess_by_weekday"] = gw.groupby("wd")["e24"].agg(lambda x: 100 * x.mean()).to_frame("mean_pct").join(
        gw.groupby("wd")["e24"].agg(lambda x: x.mean() / x.std() * np.sqrt(len(x))).to_frame("t"))
    return out
