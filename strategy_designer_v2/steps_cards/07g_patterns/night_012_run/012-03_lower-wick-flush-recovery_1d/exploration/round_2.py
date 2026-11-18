def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20, min_periods=20).std()
            z = r1 / sd
            vr = b["volume"] / b["volume"].shift(1).rolling(20, min_periods=20).mean()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            clr = (c - b["low"]) / rng
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "z": z, "vr": vr, "clr": clr,
                               "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1, "f7": c.shift(-7) / c - 1,
                               "r5": c / c.shift(5) - 1, "wd": ts.dt.weekday, "year": ts.dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h, col in [(1, "f1"), (3, "f3"), (7, "f7")]:
        m = d[d.pos % h == 0].groupby("coin")[col].mean()
        d["x%d" % h] = d[col] - d.coin.map(m)
    d["era"] = np.where(d.year <= 2021, "early", "late")

    def summ(g, col):
        g = g.dropna(subset=[col]); n = len(g)
        if n < 3: return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean": g[col].mean(), "t": g[col].mean() / (g[col].std() / np.sqrt(n))})

    def thin(ev, h):
        keep = []
        for (c_, w_), g in ev.sort_values("pos").groupby(["coin", "win"]):
            last = -10**9
            for i, p in zip(g.index, g.pos):
                if p - last >= h: keep.append(i); last = p
        return ev.loc[keep]

    out = {}
    # A: volume-burst sharp rises, thinned 7, by era and coin
    sr = thin(d[(d.z >= 2) & (d.vr >= 2)], 7)
    out["rise_vb_x7_era"] = sr.groupby("era").apply(lambda g: summ(g, "x7"))
    out["rise_vb_x7_coin"] = sr.groupby("coin").apply(lambda g: summ(g, "x7"))
    # graded: on z>=1 rises, x7 by vr bucket, thinned
    r = thin(d[d.z >= 1], 7).copy()
    r["vrb"] = pd.cut(r.vr, [0, 1, 1.5, 2, 3, np.inf])
    out["rise_x7_by_vr"] = r.groupby("vrb", observed=True).apply(lambda g: summ(g, "x7"))
    rr = r.dropna(subset=["vr", "x7"])
    s = stats.linregress(np.log(rr.vr), rr.x7)
    out["rise_x7_on_logvr_slope_t"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(rr)})
    # B: falls z<=-1, x3 by vr bucket, thinned 3
    f = thin(d[d.z <= -1], 3).copy()
    f["vrb"] = pd.cut(f.vr, [0, 1, 1.5, 2, 3, np.inf])
    out["fall_x3_by_vr"] = f.groupby("vrb", observed=True).apply(lambda g: summ(g, "x3"))
    ff = f.dropna(subset=["vr", "x3"])
    s = stats.linregress(np.log(ff.vr), ff.x3)
    out["fall_x3_on_logvr_slope_t"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(ff)})
    fvb = f[f.vr >= 2]
    out["fall_vb_x3_era"] = fvb.groupby("era").apply(lambda g: summ(g, "x3"))
    # C: any |z|>=1 with vr: signed x7 aligned with move sign (volume-burst moves continue or reverse?)
    a = thin(d[d.z.abs() >= 1], 7).copy()
    a["sx7"] = np.sign(a.z) * a.x7
    a["vrb"] = pd.cut(a.vr, [0, 1, 1.5, 2, 3, np.inf])
    out["abs_move_signed_x7_by_vr"] = a.groupby("vrb", observed=True).apply(lambda g: summ(g, "sx7"))
    # D: r5 momentum by era, grid 3
    g3 = d[d.pos % 3 == 0].copy()
    g3["r5q"] = g3.groupby("coin")["r5"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["x3_r5q_era"] = g3.groupby(["era", "r5q"]).apply(lambda g: summ(g, "x3")).unstack(0)
    gg = g3.dropna(subset=["r5", "x3"])
    s = stats.linregress(gg.r5, gg.x3)
    out["x3_on_r5_slope_t"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(gg)})
    # E: weekday by era
    out["x1_weekday_era_t"] = d.groupby(["wd", "era"]).apply(lambda g: summ(g, "x1")["t"]).unstack()
    return out
