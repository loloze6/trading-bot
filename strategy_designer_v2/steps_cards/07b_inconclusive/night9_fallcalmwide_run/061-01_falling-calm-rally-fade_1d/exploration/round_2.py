def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "win": w, "r": r, "z": r / sd,
                               "fc": b["forecast"].astype(float),
                               "inprof": (b["regime"] == "unknown"),
                               "yr": pd.to_datetime(b["timestamp"]).dt.year,
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            df["f1"] = c.shift(-1) / c - 1
            # test's cases: forecast falls by >=2 onto short side from lowest short level since last bet, reset at flat/long
            fc = df["fc"].values
            case = np.zeros(len(df), bool)
            ref = 0.0
            for i in range(len(df)):
                f = fc[i]
                if np.isnan(f) or f >= 0:
                    ref = 0.0
                    continue
                if ref - f >= 2:
                    case[i] = True
                    ref = f
            df["case"] = case
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["f1"].mean()
    d["d1"] = d["f1"] - d["coin"].map(drift)
    d["sd1"] = -d["d1"]  # short direction

    def st(x, days=None):
        x = x.dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    def dayt(q, col):
        q = q.dropna(subset=[col])
        m = q[col].mean()
        g = (q[col] - m).groupby(q["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(q)
        return pd.Series({"n": len(q), "days": q["day"].nunique(), "mean": m, "t_day": m / se})

    out = {}
    cs = d[d["case"]].copy()
    out["test_cases_BC_short_dir"] = dayt(cs, "sd1")
    cs["fq"] = pd.qcut(cs["fc"].abs(), 4, duplicates="drop")
    out["cases_by_absfc_quartile"] = cs.groupby("fq").apply(lambda q: dayt(q, "sd1"))
    cs["zb"] = pd.cut(cs["z"], [-99, 0, 0.5, 1, 1.5, 2, 99])
    out["cases_by_z"] = cs.groupby("zb").apply(lambda q: dayt(q, "sd1"))
    out["cases_by_year"] = cs.groupby("yr").apply(lambda q: dayt(q, "sd1"))
    out["cases_by_coin"] = cs.groupby("coin").apply(lambda q: dayt(q, "sd1"))
    p = d[d["inprof"] & d["z"].notna()].copy()
    out["inprof_all_days_d1"] = dayt(p, "d1")
    p["zb"] = pd.cut(p["z"], [-99, -1, 0, 1, 99])
    out["inprof_d1_by_z_by_year"] = p.groupby(["yr", "zb"])["d1"].mean().unstack()
    # rise relative to profile's own next-day mean
    pm = p["d1"].mean()
    big = p[p["z"] > 1]
    out["bigup_minus_inprof_mean"] = dayt(big.assign(x=big["d1"] - pm), "x")
    # within up days, slope of d1 on z
    up = p[p["z"] > 0].dropna(subset=["d1"])
    sl = np.polyfit(up["z"], up["d1"], 1)
    out["slope_d1_on_z_updays"] = float(sl[0])
    out["n_cases_inprof"] = float(cs["inprof"].mean())
    return out
