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
            sd = r1.rolling(24, min_periods=24).std()
            sdl = r1.rolling(720, min_periods=240).std()
            df = pd.DataFrame({"coin": coin, "win": w, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "year": ts.dt.year,
                               "z1": r1 / sd,
                               "z4": (c / c.shift(4) - 1) / (sd * 2),
                               "z12": (c / c.shift(12) - 1) / (sd * np.sqrt(12)),
                               "f24": c.shift(-24) / c - 1,
                               "volreg": sd / sdl})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    # coin drift from non-overlapping grid: hour-0 bars only (24h apart)
    drift = d[d.hour == 0].groupby("coin")["f24"].mean()
    d["f24x"] = d["f24"] - d["coin"].map(drift)
    d = d.dropna(subset=["f24x"])
    d["we"] = np.where(d["wd"] >= 5, "we", "wk")

    def reg(g, x):
        g = g.dropna(subset=[x, "f24x"])
        if len(g) < 100:
            return pd.Series({"n": len(g), "slope_bp": np.nan, "t": np.nan})
        s = stats.linregress(-g[x].clip(-6, 6), g["f24x"])
        return pd.Series({"n": len(g), "slope_bp": s.slope * 1e4, "t": s.slope / s.stderr})

    out = {}
    # one anchor hour per day = non-overlapping 24h cases
    res = []
    for x in ["z1", "z4", "z12"]:
        for h in [4, 8, 12, 16, 20]:
            for we in ["we", "wk"]:
                g = d[(d.hour == h) & (d.we == we)]
                r = reg(g, x); r["x"] = x; r["hour"] = h; r["we"] = we
                res.append(r)
    out["fade_anchor_hours"] = pd.DataFrame(res).set_index(["x", "hour", "we"])
    # weekend 4h-move fade at hour 12, by vol regime (non-overlapping)
    g = d[(d.hour == 12)].copy()
    g["vq"] = pd.qcut(g["volreg"], 3, labels=["low", "mid", "high"])
    out["z4_h12_by_vol_we"] = g.groupby(["vq", "we"]).apply(lambda q: reg(q, "z4")).unstack("we")
    # weekend z12 at hour 20 by year (stability)
    g = d[(d.hour == 20) & (d.we == "we")]
    out["z12_h20_we_by_year"] = g.groupby("year").apply(lambda q: reg(q, "z12"))
    out["z12_h20_we_by_coin"] = g.groupby("coin").apply(lambda q: reg(q, "z12"))
    # weekday with saturday/sunday split for z12 at h20
    g = d[(d.hour == 20)]
    out["z12_h20_by_wd"] = g.groupby("wd").apply(lambda q: reg(q, "z12"))
    return out
