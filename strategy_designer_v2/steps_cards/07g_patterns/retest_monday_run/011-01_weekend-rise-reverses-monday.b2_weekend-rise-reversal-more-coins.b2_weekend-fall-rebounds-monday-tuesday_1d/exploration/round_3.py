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
            r2 = c / c.shift(2) - 1
            z2 = r2 / (sd * np.sqrt(2))
            vr = np.log(v / v.rolling(60, min_periods=20).mean())
            vw = np.log((v + v.shift(1)) / (2 * v.rolling(60, min_periods=20).mean()))
            d = pd.DataFrame({"coin": coin, "w": w, "wd": ts.dt.weekday, "year": ts.dt.year,
                              "pos": np.arange(len(b)), "z": z, "z2": z2, "vr": vr, "vw": vw, "sd": sd,
                              "f2": c.shift(-2) / c - 1, "f1": c.shift(-1) / c - 1,
                              "f4": c.shift(-4) / c - 1})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    G = D[D["pos"] % 2 == 0]
    m2 = G.groupby("coin")["f2"].mean(); s2 = G.groupby("coin")["f2"].std()
    G4 = D[D["pos"] % 4 == 0]; m4 = G4.groupby("coin")["f4"].mean()
    G1 = D; m1 = D.groupby("coin")["f1"].mean()
    D["x2"] = D["f2"] - D["coin"].map(m2)
    D["x4"] = D["f4"] - D["coin"].map(m4)
    D["x1"] = D["f1"] - D["coin"].map(m1)
    D["st2"] = D["x2"] / D["coin"].map(s2)
    D = D.dropna(subset=["z", "x2"])
    tt = lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    out = {}
    S = D[D["wd"] == 6]
    R = S[S["z2"] > 0].copy()
    R["zq"] = pd.qcut(R["z2"], 3, labels=["small", "mid", "big"])
    out["sun_wkend2d_rise_x2_by_size"] = R.groupby("zq", observed=True)["x2"].agg(["mean", "count", tt])
    ps = R.groupby(["w", "pos"])["x2"].mean()
    out["sun_wkend2d_rise_persunday"] = f"mean {ps.mean():.5f} t {tt(ps):.2f} n {len(ps)}"
    R1 = S[S["z"] > 0]
    out["sun_rise_size"] = f"unusual(short) {-R1['x2'].mean():.5f} strength {-R1['st2'].mean():.4f} drift {R1['coin'].map(m2).mean():.5f} n {len(R1)}"
    out["sun_rise_x1_x4"] = f"x1 {R1['x1'].mean():.5f} t {tt(R1['x1']):.2f}; x4 {R1['x4'].mean():.5f} t {tt(R1['x4']):.2f}"
    R1 = R1.copy(); R1["half"] = np.where(R1["year"] <= 2021, "2018-2021", "2022-2025")
    out["sun_rise_by_half_persunday"] = R1.groupby("half").apply(lambda g: pd.Series({"mean": g.groupby(["w","pos"])["x2"].mean().mean(), "t": tt(g.groupby(["w","pos"])["x2"].mean()), "n": g.groupby(["w","pos"]).ngroups}))
    R1["vq"] = pd.qcut(R1["vw"], 3, labels=["lowvol", "mid", "highvol"])
    out["sun_rise_by_wkend_volume"] = R1.groupby("vq", observed=True)["x2"].agg(["mean", "count", tt])
    out["sun_rise_by_coin_tcount"] = f"coins neg {int((R1.groupby('coin')['x2'].mean()<0).sum())} of {R1['coin'].nunique()}"
    return out
