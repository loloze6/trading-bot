def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=30).std()
            z1 = r1 / sd30
            hl = (b["high"] - b["low"]).replace(0, np.nan)
            clo = (c - b["low"]) / hl
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "yr": pd.to_datetime(b["timestamp"]).dt.year,
                               "inprof": (b["regime"] == "unknown").values,
                               "z1": z1, "clo": clo, "r1": r1,
                               "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift1 = d["f1"].mean()
    drift2 = d.loc[d.pos % 2 == 0, "f2"].mean()
    out = {"drift1": drift1, "drift2": drift2}
    p = d[d.inprof].dropna(subset=["z1", "f1"]).copy()
    p["u1"] = p["f1"] - drift1
    up = p[p.z1 > 0].copy()

    def cl_t(s, val):
        g = s.groupby("day")[val].apply(lambda x: (x - s[val].mean()).sum())
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(s)
        return s[val].mean() / se, G

    t, G = cl_t(up, "u1")
    out["up_days_u1"] = pd.Series({"n": len(up), "mean_u1": up.u1.mean(), "t_clustered": t, "days": G,
                                   "raw_f1_mean": up.f1.mean()})
    sl = stats.linregress(up.z1.clip(upper=4), up.u1)
    out["up_slope_u1_on_z1"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr})
    allp = stats.linregress(p.z1.clip(-4, 4), p.u1)
    out["all_slope_u1_on_z1"] = pd.Series({"slope": allp.slope, "t": allp.slope / allp.stderr, "n": len(p)})
    out["up_by_coin"] = up.groupby("coin")["u1"].agg(["count", "mean"]).round(4)
    out["up_by_window"] = up.groupby("w")["u1"].agg(["count", "mean"]).round(4)
    out["up_by_year"] = up.groupby("yr")["u1"].agg(["count", "mean"]).round(4)
    up["q"] = pd.qcut(up.z1, 4, labels=False)
    g = up.groupby("q").agg(n=("u1", "size"), z=("z1", "mean"), u1=("u1", "mean"), sd=("u1", "std"))
    g["t"] = g.u1 / (g.sd / np.sqrt(g.n)); out["up_quartiles"] = g.round(4)
    # up day by close location
    up["cb"] = pd.cut(up.clo, [-0.01, 0.5, 0.8, 1.01])
    g = up.groupby("cb", observed=True)["u1"].agg(["count", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"])); out["up_by_closeloc"] = g.round(4)
    # 2-day horizon on grid
    p2 = d[d.inprof & (d.pos % 2 == 0)].dropna(subset=["z1", "f2"]).copy()
    p2["u2"] = p2.f2 - drift2
    u2 = p2[p2.z1 > 0]
    t2, G2 = cl_t(u2, "u2")
    out["up_u2"] = pd.Series({"n": len(u2), "mean": u2.u2.mean(), "t": t2, "days": G2})
    # same outside profile for contrast
    o = d[~d.inprof & (d.z1 > 0)].dropna(subset=["f1"]).copy(); o["u1"] = o.f1 - drift1
    to, Go = cl_t(o, "u1")
    out["up_outside_u1"] = pd.Series({"n": len(o), "mean": o.u1.mean(), "t": to})
    # down days in profile (already held rebound) for reference
    dn = p[p.z1 < 0]
    td, Gd = cl_t(dn, "u1")
    out["down_inprof_u1"] = pd.Series({"n": len(dn), "mean": dn.u1.mean(), "t": td})
    return out
