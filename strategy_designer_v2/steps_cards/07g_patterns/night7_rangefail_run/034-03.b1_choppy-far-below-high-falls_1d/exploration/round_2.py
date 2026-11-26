def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            hi = c.shift(1).rolling(20, min_periods=20).max()
            sd = r.rolling(20, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                "depth": (c - hi) / hi / sd, "tr60": c / c.shift(60) - 1,
                "z": r / sd.shift(1), "r5p": (c / c.shift(5) - 1) / (sd * np.sqrt(5)),
                "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1, "f5": c.shift(-5) / c - 1,
                "day": ts.dt.floor("D").values, "wd": ts.dt.weekday.values, "yr": ts.dt.year.values})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for h in (1, 3, 5):
        g = A[A.pos % h == 0]
        A["a%d" % h] = A["f%d" % h] - A["coin"].map(g.groupby("coin")["f%d" % h].mean())
    A["trend"] = pd.cut(A.tr60, [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])

    def clus(g, y, x=None):
        g = g.dropna(subset=[y] + ([x] if x else []))
        if x is None:
            s = g.groupby("day")[y].sum(); n = g.groupby("day")[y].size()
            m = s.sum() / n.sum()
            d = g.groupby("day").apply(lambda q: (q[y] - m).sum())
            se = np.sqrt((d ** 2).sum()) / n.sum()
            return pd.Series({"n": len(g), "days": g.day.nunique(), "mean%": 100 * m, "t_day": m / se if se > 0 else np.nan})
        xv = g[x] - g[x].mean(); b1 = (xv * g[y]).sum() / (xv ** 2).sum()
        res = g[y] - g[y].mean() - b1 * xv
        se = np.sqrt(((xv * res).groupby(g["day"]).sum() ** 2).sum()) / (xv ** 2).sum()
        rho = stats.spearmanr(g[x], g[y]).correlation
        return pd.Series({"n": len(g), "days": g.day.nunique(), "slope": b1, "t_day": b1 / se, "spearman": rho})

    out = {}
    # 1) prior-day shock -> next 1 and 3 days, drift adjusted, day-clustered
    D1 = A.dropna(subset=["z"])
    D1 = D1.assign(zq=pd.cut(D1.z, [-100, -2, -1, -0.3, 0.3, 1, 2, 100]))
    out["a1_by_z"] = D1.groupby("zq").apply(lambda g: clus(g, "a1")).round(3)
    D3 = D1[D1.pos % 3 == 0]
    out["a3_by_z_grid"] = D3.groupby("zq").apply(lambda g: clus(g, "a3")).round(3)
    neg = D1[D1.z < 0].copy()
    out["slope_a1_on_z_neg_by_trend"] = neg.groupby("trend").apply(lambda g: clus(g, "a1", "z")).round(4)
    out["slope_a1_on_z_neg_by_window"] = neg.groupby("w").apply(lambda g: clus(g, "a1", "z")).round(4)
    pos = D1[D1.z > 0]
    out["slope_a1_on_z_pos_by_trend"] = pos.groupby("trend").apply(lambda g: clus(g, "a1", "z")).round(4)
    # 2) weekday, day-clustered, by year
    out["a1_weekday"] = A.groupby("wd").apply(lambda g: clus(g, "a1")).round(3)
    out["a1_weekday_by_year_mean%"] = A.groupby(["yr", "wd"])["a1"].mean().unstack().mul(100).round(3)
    # 3) depth in chop / rise, grid 5, raw depth slope and by window
    G = A[(A.pos % 5 == 0)].dropna(subset=["depth", "a5"])
    out["slope_a5_on_depth_by_trend"] = G.groupby("trend").apply(lambda g: clus(g, "a5", "depth")).round(4)
    out["slope_a5_on_r5p_by_trend"] = G.dropna(subset=["r5p"]).groupby("trend").apply(lambda g: clus(g, "a5", "r5p")).round(4)
    ch = G[G.trend == "chop"]
    out["chop_depth_slope_by_window"] = ch.groupby("w").apply(lambda g: clus(g, "a5", "depth") if len(g) > 8 else pd.Series(dtype=float)).round(4)
    ri = G[(G.trend == "rise")].copy()
    ri["dq"] = pd.qcut(ri.depth, 5, labels=False, duplicates="drop")
    out["rise_depth_quintile"] = ri.groupby("dq").apply(lambda g: pd.concat([clus(g, "a5"), pd.Series({"depth_mid": g.depth.median()})])).round(3)
    return out
