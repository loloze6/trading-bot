def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r = c.pct_change()
            sd = r.rolling(60, min_periods=20).std()
            z = (r - r.rolling(60, min_periods=20).mean()) / sd
            vr = np.log(v / v.rolling(60, min_periods=20).mean())
            r3 = c / c.shift(3) - 1
            z3 = r3 / (sd * np.sqrt(3))
            d = pd.DataFrame({"coin": coin, "w": w, "wd": ts.dt.weekday, "year": ts.dt.year,
                              "pos": np.arange(len(b)), "z": z, "z3": z3, "vr": vr, "sd": sd,
                              "f2": c.shift(-2) / c - 1, "f1": c.shift(-1) / c - 1})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # drift on non-overlapping grid
    G = D[D["pos"] % 2 == 0]
    m2 = G.groupby("coin")["f2"].mean()
    D["x2"] = D["f2"] - D["coin"].map(m2)
    D["volq"] = D.groupby("coin")["sd"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    D = D.dropna(subset=["z", "x2"])
    tt = lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    out = {}
    S = D[D["wd"] == 6]
    R = S[S["z"] > 0].copy()
    R["zq"] = pd.qcut(R["z"], 3, labels=["smallrise", "mid", "bigrise"])
    out["sun_rise_x2_by_size"] = R.groupby("zq", observed=True)["x2"].agg(["mean", "count", tt])
    out["sun_rise_x2_by_year"] = R.groupby("year")["x2"].agg(["mean", "count", tt])
    R["vq"] = pd.qcut(R["vr"], 3, labels=["lowvol", "mid", "highvol"])
    out["sun_rise_x2_by_volume"] = R.groupby("vq", observed=True)["x2"].agg(["mean", "count", tt])
    sl = []
    for y, g in S.groupby("year"):
        s = stats.linregress(g["z"], g["x2"]); sl.append({"year": y, "slope": s.slope, "t": s.slope / s.stderr, "n": len(g)})
    out["sun_slope_by_year"] = pd.DataFrame(sl)
    # per-Sunday cross-coin mean t for rises
    ps = R.groupby(["w", "year", "pos"])["x2"].mean()
    out["sun_rise_persunday_t"] = f"mean {ps.mean():.5f} t {tt(ps):.2f} sundays {len(ps)}"
    ps2 = S.assign(sx=-S["z"].clip(upper=3, lower=-3) * S["x2"]).groupby(["w", "pos"])["sx"].mean()
    out["sun_signed_contrarian_persunday"] = f"mean {ps2.mean():.5f} t {tt(ps2):.2f} n {len(ps2)}"
    # non-overlapping grid, all weekdays: large fall by vol tercile
    Gd = D[D["pos"] % 2 == 0].copy()
    Gd["zb"] = pd.cut(Gd["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["grid_x2_by_zbin"] = Gd.groupby("zb", observed=True)["x2"].agg(["mean", "count", tt])
    out["grid_x2_zbin_volq_mean"] = Gd.pivot_table(index="zb", columns="volq", values="x2", aggfunc="mean", observed=True)
    out["grid_x2_zbin_volq_t"] = Gd.pivot_table(index="zb", columns="volq", values="x2", aggfunc=tt, observed=True)
    F = Gd[(Gd["z"] < -1.5) & (Gd["volq"] == 2)]
    out["bigfall_highvol_by_year"] = F.groupby("year")["x2"].agg(["mean", "count", tt])
    # weekday vs Sunday rise reversal on grid
    Gd["rise"] = Gd["z"] > 0
    out["grid_rise_x2_by_wd"] = Gd[Gd["rise"]].groupby("wd")["x2"].agg(["mean", "count", tt])
    # 3-day (Fri-Sun) weekend return at Sunday
    s = stats.linregress(S.dropna(subset=["z3"])["z3"], S.dropna(subset=["z3"])["x2"])
    out["sun_z3_slope"] = f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f}"
    return out
