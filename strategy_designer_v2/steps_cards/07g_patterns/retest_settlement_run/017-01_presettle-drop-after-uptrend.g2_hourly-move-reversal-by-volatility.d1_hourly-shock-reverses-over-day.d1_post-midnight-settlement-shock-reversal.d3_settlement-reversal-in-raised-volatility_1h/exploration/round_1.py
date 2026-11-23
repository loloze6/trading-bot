def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            s24 = r1.rolling(24).std()
            ratio = s24 / s24.rolling(720, min_periods=240).mean()
            vol = b["volume"].astype(float)
            vrel = vol / vol.rolling(24*7, min_periods=48).mean()
            d = pd.DataFrame({"coin": coin, "win": w, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                              "year": ts.dt.year, "z": r1 / s24, "ratio": ratio, "vrel": vrel})
            for h in (4, 8, 12, 24):
                d[f"f{h}"] = c.shift(-h) / c - 1
            # prior 24h trend in vol units
            d["tr24"] = (c / c.shift(24) - 1) / (s24 * np.sqrt(24))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # coin drift per horizon from grid
    drift = {}
    for coin, wins in data["bars"].items():
        for h in (4, 8, 12, 24):
            vals = []
            for w, b in wins.items():
                c = b.sort_values("timestamp")["close"].astype(float).values
                g = c[::h]
                vals.extend(list(g[1:] / g[:-1] - 1))
            drift[(coin, h)] = np.mean(vals)
    for h in (4, 8, 12, 24):
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(lambda k: drift[(k, h)])
    D = D.replace([np.inf, -np.inf], np.nan)
    def slope(df, y, x="z"):
        q = df[[x, y]].dropna()
        q = q[q[x].abs() < 20]
        if len(q) < 50: return (np.nan, np.nan, len(q))
        res = stats.linregress(q[x], q[y])
        return (res.slope * 1e4, res.slope / res.stderr, len(q))
    out = {}
    # by hour of day: 24h forward slope on z (negative => reversal)
    t = []
    for h, g in D.groupby("hour"):
        s, tt, n = slope(g, "x24"); s4, t4, _ = slope(g, "x4")
        t.append((h, s, tt, s4, t4, n, g["vrel"].mean()))
    out["by_hour_slope_bp_per_z"] = pd.DataFrame(t, columns=["hour", "slope24", "t24", "slope4", "t4", "n", "vol_rel"]).set_index("hour")
    H0 = D[D.hour == 0]
    # horizons
    out["h0_by_horizon"] = pd.DataFrame([(h,) + slope(H0, f"x{h}") for h in (4, 8, 12, 24)], columns=["h", "slope", "t", "n"])
    # by ratio quintile at hour 0, and at all other hours
    D["rq"] = pd.qcut(D["ratio"], 5, labels=False)
    t = []
    for q, g in D.groupby("rq"):
        a = slope(g[g.hour == 0], "x24"); o = slope(g[g.hour.isin([6, 12, 18])], "x24")
        t.append((q, g["ratio"].median(), a[0], a[1], o[0], o[1], a[2]))
    out["by_ratio_quintile"] = pd.DataFrame(t, columns=["rq", "ratio_med", "h0_slope", "h0_t", "h6_12_18_slope", "h6_12_18_t", "n"])
    # by year, by coin at hour 0
    out["h0_by_year"] = pd.DataFrame([(y,) + slope(g, "x24") for y, g in H0.groupby("year")], columns=["year", "slope", "t", "n"])
    out["h0_by_coin"] = pd.DataFrame([(k,) + slope(g, "x24") for k, g in H0.groupby("coin")], columns=["coin", "slope", "t", "n"])
    out["h0_by_weekday"] = pd.DataFrame([(k,) + slope(g, "x24") for k, g in H0.groupby("wd")], columns=["wd", "slope", "t", "n"])
    # prior 24h trend at hour 0 -> next 24h (trend reversal of the day before)
    out["h0_trend24_slope"] = pd.DataFrame([slope(H0, "x24", "tr24")], columns=["slope", "t", "n"])
    # book by year
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; bd.append(d)
    B = pd.concat(bd); B["year"] = pd.to_datetime(B["day"]).dt.year
    P = B.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), year=("year", "first")).dropna()
    out["book_by_year"] = P.groupby("year").apply(lambda g: pd.Series({"sharpe": g.br.mean() / g.br.std() * np.sqrt(365), "hold_sharpe": g.cr.mean() / g.cr.std() * np.sqrt(365), "days": len(g), "corr_coin": g.br.corr(g.cr)}))
    out["book_by_window"] = P.groupby("win").apply(lambda g: pd.Series({"sharpe": g.br.mean() / g.br.std() * np.sqrt(365), "sum": g.br.sum(), "corr_coin": g.br.corr(g.cr)}))
    return out
