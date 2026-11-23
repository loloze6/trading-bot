def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    grid = []; hr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"]
            r1 = c.pct_change()
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=360).mean()
            vol = r1.rolling(720, min_periods=360).std()
            vol24 = r1.rolling(24).std()
            f24 = c.shift(-24) / c - 1
            f48 = c.shift(-48) / c - 1
            df = pd.DataFrame({"coin": coin, "win": w, "wd": ts.dt.dayofweek, "h": ts.dt.hour, "yr": ts.dt.year,
                               "s": (r24 / mabs).clip(-2, 2), "vol": vol, "vr": vol24 / vol,
                               "f24": f24, "f48": f48})
            # grid at every 24th row from window start
            grid.append(df.iloc[::24])
            # hourly: return of bars 20 and 21 together (from close of 19h bar to close of 21h bar), plus prior 24h
            r2 = c.shift(-2) / c - 1
            hr.append(pd.DataFrame({"coin": coin, "yr": ts.dt.year, "h": ts.dt.hour, "wd": ts.dt.dayofweek,
                                    "r1n": r1.shift(-1), "r2": r2, "s": (r24 / mabs).clip(-2, 2)}))
    G = pd.concat(grid).dropna(subset=["s", "f24", "f48", "vol", "vr"])
    G = G.copy()
    G["f24"] = G["f24"] - G.groupby("coin")["f24"].transform("mean")
    G["f48"] = G["f48"] - G.groupby("coin")["f48"].transform("mean")
    G["vrel"] = G["vol"] / G.groupby(["coin"])["vol"].transform("median")
    G["x"] = G["s"] * G["vrel"]
    def reg(g, xc, yc):
        lr = stats.linregress(g[xc], g[yc]); return lr.slope, lr.slope / lr.stderr, len(g)
    rows = []
    for co, g in G.groupby("coin"):
        a = reg(g, "x", "f24"); bb = reg(g, "s", "f24")
        rows.append({"coin": co, "n": a[2], "t_s_x_vol_f24": a[1], "t_s_f24": bb[1], "t_x_f48": reg(g, "x", "f48")[1]})
    out["all_days_reversal_by_coin"] = pd.DataFrame(rows)
    rows = []
    for y, g in G.groupby("yr"):
        rows.append({"yr": y, "n": len(g), "t_x_f24": reg(g, "x", "f24")[1], "slope": reg(g, "x", "f24")[0]})
    out["all_days_reversal_by_year"] = pd.DataFrame(rows)
    G["vq"] = G.groupby("coin")["vrel"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    rows = []
    for v, g in G.groupby("vq"):
        a = reg(g, "s", "f24"); rows.append({"vol_quint": v, "n": a[2], "slope_s_f24": a[0], "t": a[1], "mean_vrel": g["vrel"].mean()})
    out["all_days_reversal_by_vol_quintile"] = pd.DataFrame(rows)
    # within-day vol burst (24h vol vs 30d) as conditioner
    G["bq"] = pd.qcut(G["vr"].rank(method="first"), 3, labels=False)
    rows = []
    for v, g in G.groupby("bq"):
        a = reg(g, "s", "f24"); rows.append({"burst_terc": v, "n": a[2], "slope": a[0], "t": a[1]})
    out["reversal_by_24h_vol_burst"] = pd.DataFrame(rows)
    # weekend-vs-weekday comparison at same vol: day-of-week of grid row
    G["wkend"] = G["wd"].isin([5, 6]).astype(int)
    rows = []
    for k, g in G.groupby("wkend"):
        a = reg(g, "x", "f24"); rows.append({"start_weekend": k, "n": a[2], "slope": a[0], "t": a[1]})
    out["reversal_grid_weekend_vs_week"] = pd.DataFrame(rows)
    # hour 20-21 effect
    H = pd.concat(hr)
    H19 = H[H.h == 19].dropna(subset=["r2"])
    rows = []
    for co, g in H19.groupby("coin"):
        rows.append({"coin": co, "n": len(g), "mean_bps": g.r2.mean() * 1e4, "t": g.r2.mean() / (g.r2.std() / np.sqrt(len(g)))})
    out["h20_21_ret_by_coin"] = pd.DataFrame(rows)
    rows = []
    for y, g in H19.groupby("yr"):
        rows.append({"yr": y, "n": len(g), "mean_bps": g.r2.mean() * 1e4, "t": g.r2.mean() / (g.r2.std() / np.sqrt(len(g)))})
    out["h20_21_ret_by_year"] = pd.DataFrame(rows)
    rows = []
    for d, g in H19.groupby("wd"):
        rows.append({"wd": d, "n": len(g), "mean_bps": g.r2.mean() * 1e4, "t": g.r2.mean() / (g.r2.std() / np.sqrt(len(g)))})
    out["h20_21_ret_by_weekday"] = pd.DataFrame(rows)
    H19 = H19.dropna(subset=["s"])
    lr = stats.linregress(H19["s"], H19["r2"])
    out["h20_21_on_prior24h_scaled"] = pd.DataFrame([{"n": len(H19), "slope_bps": lr.slope * 1e4, "t": lr.slope / lr.stderr}])
    return out
