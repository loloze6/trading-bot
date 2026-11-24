def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            b = b.sort_values("ts").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20, min_periods=15).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": b["ts"], "pos": np.arange(len(b)),
                "wd": b["ts"].dt.weekday, "year": b["ts"].dt.year,
                "r": r, "vol": vol,
                "z1": r / vol,
                "z3": (c / c.shift(3) - 1) / (vol * np.sqrt(3)),
                "z14": (c / c.shift(14) - 1) / (vol * np.sqrt(14)),
                "lo60": (c / b["low"].astype(float).rolling(60, min_periods=40).min() - 1) / (vol * np.sqrt(60)),
                "hi60": (c / b["high"].astype(float).rolling(60, min_periods=40).max() - 1) / (vol * np.sqrt(60)),
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            d["volrank"] = vol.rolling(60, min_periods=30).rank(pct=True)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # coin drifts on grids
    drift = {}
    for h in (1, 2, 3):
        g = D[D["pos"] % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
    for h in (1, 2, 3):
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(drift[h])

    def tday(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 5:
            return (np.nan, np.nan, len(s), 0)
        g = s.groupby("ts")[col].sum()
        m = s[col].mean()
        n_days = len(g)
        se = np.sqrt((g - g.mean() * 0).pow(2).sum() * 0 + ((s.groupby("ts")[col].sum() - s.groupby("ts")[col].count() * m) ** 2).sum()) / len(s)
        return (m, m / se if se > 0 else np.nan, len(s), n_days)

    out = {}
    # 1. weekday of next-day excess return (1-day, all bars)
    res = []
    for wd in range(7):
        m, t, n, nd = tday(D[D["wd"] == wd], "x1")
        res.append({"bar_weekday": wd, "mean_x1": m, "t": t, "n": n, "days": nd})
    out["next1d_excess_by_bar_weekday(0=Mon)"] = pd.DataFrame(res)

    # 2. z14 quintile vs forward 2-day excess: Friday vs other days (grid for others)
    res = []
    for lab, sub in [("fri", D[D["wd"] == 4]), ("mon-thu_grid2", D[(D["wd"].isin([0, 1, 2, 3])) & (D["pos"] % 2 == 0)]),
                     ("sat_sun_grid2", D[(D["wd"].isin([5, 6])) & (D["pos"] % 2 == 0)])]:
        s = sub.dropna(subset=["z14", "x2"]).copy()
        s["q"] = pd.qcut(s["z14"], 5, labels=False)
        for q in range(5):
            m, t, n, nd = tday(s[s["q"] == q], "x2")
            res.append({"set": lab, "z14_q": q, "z14_mean": s[s["q"] == q]["z14"].mean(), "mean_x2": m, "t": t, "n": n})
        rho, p = stats.spearmanr(s["z14"], s["x2"])
        res.append({"set": lab, "z14_q": "spearman", "z14_mean": rho, "mean_x2": p, "t": np.nan, "n": len(s)})
    out["z14_quintile_fwd2_excess"] = pd.DataFrame(res)

    # 3. after large daily moves (z1) next 1 and 3 day
    s = D.dropna(subset=["z1", "x1"]).copy()
    s["q"] = pd.qcut(s["z1"], 7, labels=False)
    res = []
    for q in range(7):
        ss = s[s["q"] == q]
        m1, t1, n, _ = tday(ss, "x1")
        m3, t3, n3, _ = tday(ss[ss["pos"] % 3 == 0], "x3")
        res.append({"z1_q": q, "z1": ss["z1"].mean(), "x1": m1, "t1": t1, "n": n, "x3_grid": m3, "t3": t3, "n3": n3})
    out["after_daily_move_z1"] = pd.DataFrame(res)

    # 4. distance from 60-day low/high, fwd 3-day (grid)
    res = []
    for col in ("lo60", "hi60"):
        s = D[D["pos"] % 3 == 0].dropna(subset=[col, "x3"]).copy()
        s["q"] = pd.qcut(s[col], 5, labels=False, duplicates="drop")
        for q in sorted(s["q"].unique()):
            m, t, n, _ = tday(s[s["q"] == q], "x3")
            res.append({"var": col, "q": q, "val": s[s["q"] == q][col].mean(), "x3": m, "t": t, "n": n})
    out["dist_60d_extreme_fwd3"] = pd.DataFrame(res)

    # 5. vol rank, fwd 3-day grid, and weekend by vol
    s = D[D["pos"] % 3 == 0].dropna(subset=["volrank", "x3"]).copy()
    s["q"] = pd.qcut(s["volrank"], 4, labels=False, duplicates="drop")
    res = []
    for q in sorted(s["q"].unique()):
        m, t, n, _ = tday(s[s["q"] == q], "x3")
        res.append({"volrank_q": q, "x3": m, "t": t, "n": n})
    out["volrank_fwd3"] = pd.DataFrame(res)

    # 6. Friday weekend excess by year (positive z14) and by coin
    f = D[(D["wd"] == 4)].dropna(subset=["z14", "x2"])
    res = []
    for y, ss in f[f["z14"] > 0].groupby("year"):
        m, t, n, _ = tday(ss, "x2")
        res.append({"year": y, "x2": m, "t": t, "n": n})
    out["fri_pos_z14_weekend_by_year"] = pd.DataFrame(res)
    res = []
    for cn, ss in f.groupby("coin"):
        a = ss[ss["z14"] > 0]; bneg = ss[ss["z14"] <= 0]
        res.append({"coin": cn, "pos_x2": a["x2"].mean(), "neg_x2": bneg["x2"].mean(), "n_pos": len(a), "n_neg": len(bneg),
                    "all_fri_x2": ss["x2"].mean()})
    out["fri_weekend_by_coin"] = pd.DataFrame(res)

    # 7. book daily returns by weekday, and largest gains/losses
    bd = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["win"] = w
            bd.append(x)
    B = pd.concat(bd, ignore_index=True)
    B["wd"] = pd.to_datetime(B["day"]).dt.weekday
    out["book_by_weekday"] = B.groupby("wd")[["book_return", "coin_return"]].agg(["mean", "count"])
    bb = B.dropna(subset=["book_return"])
    act = bb[bb["book_return"].abs() > 1e-9]
    q = act["book_return"].quantile([0.02, 0.98])
    out["book_tail_counts_by_wd"] = pd.DataFrame({
        "worst2pct": act[act["book_return"] <= q.iloc[0]].groupby("wd").size(),
        "best2pct": act[act["book_return"] >= q.iloc[1]].groupby("wd").size()})
    return out
