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
            d = pd.DataFrame({"coin": coin, "w": w, "wd": ts.dt.weekday, "year": ts.dt.year,
                              "z": z, "vr": vr, "sd": sd,
                              "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                              "f5": c.shift(-5) / c - 1, "r2": c / c.shift(2) - 1})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in ["f1", "f2", "f5"]:
        D["x" + k[1]] = D[k] - D.groupby("coin")[k].transform("mean")
    D = D.dropna(subset=["z", "x2"])
    tt = lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    out = {}
    t = []
    for wd, g in D.groupby("wd"):
        s = stats.linregress(g["z"], g["x2"])
        fa = g[g["z"] < 0]["x2"]; ri = g[g["z"] > 0]["x2"]
        t.append({"wd": wd, "n": len(g), "slope": s.slope, "t_slope": s.slope / s.stderr,
                  "x2_fall": fa.mean(), "t_fall": tt(fa), "x2_rise": ri.mean(), "t_rise": tt(ri)})
    out["reversal_by_signal_weekday"] = pd.DataFrame(t)
    D["nwd"] = (D["wd"] + 1) % 7
    out["next_day_excess_by_weekday"] = D.groupby("nwd")["x1"].agg(["mean", "count", tt])
    S = D[(D["wd"] == 6) & (D["z"] < 0)].copy()
    S["vq"] = pd.qcut(S["vr"], 3, labels=["lowvol", "mid", "highvol"])
    S["zq"] = pd.qcut(S["z"], 3, labels=["bigfall", "mid", "smallfall"])
    out["sun_fall_x2_by_volume"] = S.groupby("vq")["x2"].agg(["mean", "count", tt])
    out["sun_fall_x2_by_size"] = S.groupby("zq")["x2"].agg(["mean", "count", tt])
    out["sun_fall_x5_by_size"] = S.groupby("zq")["x5"].agg(["mean", "count", tt])
    out["sun_fall_x2_by_year"] = S.groupby("year")["x2"].agg(["mean", "count", tt])
    D["zb"] = pd.cut(D["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["x2_by_zbin_all_weekdays"] = D.groupby("zb", observed=True)["x2"].agg(["mean", "count", tt])
    D["volq"] = D.groupby("coin")["sd"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["x2_by_zbin_and_volq"] = D.pivot_table(index="zb", columns="volq", values="x2", aggfunc="mean", observed=True)
    E = D[D["wd"] == 6].dropna(subset=["r2"])
    s = stats.linregress(E["r2"], E["x2"])
    out["sun_weekend2d_slope"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(E)}"
    bk = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["wd"] = pd.to_datetime(d["day"]).dt.weekday; bk.append(d)
    B = pd.concat(bk).dropna(subset=["book_return"])
    out["book_by_weekday"] = B.groupby("wd")["book_return"].agg(["mean", "count", tt])
    return out
