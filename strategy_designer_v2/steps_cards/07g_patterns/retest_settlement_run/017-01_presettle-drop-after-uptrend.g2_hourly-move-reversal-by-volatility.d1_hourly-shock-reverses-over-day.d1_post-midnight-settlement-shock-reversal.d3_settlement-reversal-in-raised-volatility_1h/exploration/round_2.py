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
            vol = b["volume"].astype(float)
            vrel = vol / vol.rolling(24*7, min_periods=48).mean()
            d = pd.DataFrame({"coin": coin, "win": w, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                              "year": ts.dt.year, "z": r1 / s24, "vrel": vrel,
                              "tr24": (c / c.shift(24) - 1) / (s24 * np.sqrt(24)),
                              "tr23": (c.shift(1) / c.shift(24) - 1) / (s24 * np.sqrt(24)),
                              "alloc": b["postRebalance_current_allocation"].astype(float)})
            for h in (4, 24):
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = {}
    for coin, wins in data["bars"].items():
        for h in (4, 24):
            vals = []
            for w, b in wins.items():
                cc = b.sort_values("timestamp")["close"].astype(float).values
                g = cc[::h]; vals.extend(list(g[1:] / g[:-1] - 1))
            drift[(coin, h)] = np.mean(vals)
    for h in (4, 24):
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(lambda k: drift[(k, h)])
    D = D.replace([np.inf, -np.inf], np.nan)
    def slope(df, y, x="z"):
        q = df[[x, y]].dropna(); q = q[q[x].abs() < 20]
        if len(q) < 50: return (np.nan, np.nan, len(q))
        r = stats.linregress(q[x], q[y]); return (r.slope * 1e4, r.slope / r.stderr, len(q))
    out = {}
    # prior 24h trend -> next 24h at each hour
    out["tr24_by_hour"] = pd.DataFrame([(h,) + slope(g, "x24", "tr24") for h, g in D.groupby("hour")], columns=["hour", "slope", "t", "n"]).set_index("hour")
    # joint regression at hour 0: z and tr23 (trend before the hour)
    H0 = D[D.hour == 0][["z", "tr23", "x24", "vrel", "wd", "year", "coin"]].dropna()
    H0 = H0[H0.z.abs() < 20]
    X = np.column_stack([np.ones(len(H0)), H0.z, H0.tr23]); y = H0.x24.values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ beta
    cov = np.linalg.inv(X.T @ X) * res.var(ddof=3)
    out["h0_joint_z_tr23"] = pd.DataFrame({"coef_bp": beta * 1e4, "t": beta / np.sqrt(np.diag(cov))}, index=["const", "z", "tr23"])
    # z slope at hour 0 by volume-relative tercile
    H0["vq"] = pd.qcut(H0.vrel, 3, labels=False)
    out["h0_by_vol_tercile"] = pd.DataFrame([(q, g.vrel.median()) + slope(g, "x24") for q, g in H0.groupby("vq")], columns=["vq", "vrel_med", "slope", "t", "n"])
    # weekend vs weekday at hour 0
    H0["we"] = (H0.wd >= 5).astype(int)
    out["h0_weekend"] = pd.DataFrame([(k,) + slope(g, "x24") for k, g in H0.groupby("we")], columns=["weekend", "slope", "t", "n"])
    # tr23 by year at hour 0
    out["h0_tr23_by_year"] = pd.DataFrame([(k,) + slope(g, "x24", "tr23") for k, g in H0.groupby("year")], columns=["year", "slope", "t", "n"])
    # 4h reversal pooled over hours 11, 18, 23, 5 by year (stability)
    S = D[D.hour.isin([5, 11, 18, 23])]
    out["h4rev_hours_5_11_18_23_by_year"] = pd.DataFrame([(k,) + slope(g, "x4") for k, g in S.groupby("year")], columns=["year", "slope", "t", "n"])
    out["4h_rev_all_hours_by_coin"] = pd.DataFrame([(k,) + slope(g[g.hour % 4 == 0], "x4") for k, g in D.groupby("coin")], columns=["coin", "slope", "t", "n"])
    # book: largest days
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; bd.append(d)
    B = pd.concat(bd)
    P = B.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna().reset_index()
    P["prev_cr"] = P.groupby("win")["cr"].shift(1)
    P["absprev"] = P.prev_cr.abs()
    P["dec"] = pd.qcut(P.br.rank(method="first"), 10, labels=False)
    out["book_decile_vs_coin"] = P.groupby("dec").agg(br=("br", "mean"), cr=("cr", "mean"), abs_cr=("cr", lambda s: s.abs().mean()), absprev=("absprev", "mean"))
    P["pq"] = pd.qcut(P.absprev, 5, labels=False)
    out["book_by_prev_day_absmove"] = P.groupby("pq").agg(br_mean=("br", "mean"), br_std=("br", "std"), n=("br", "size"))
    return out
