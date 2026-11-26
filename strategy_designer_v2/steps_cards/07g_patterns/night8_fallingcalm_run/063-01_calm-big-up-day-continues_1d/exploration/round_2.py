def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            z = r1 / sd
            tr60 = c / c.shift(60) - 1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            hl = (b["high"] - b["low"]).replace(0, np.nan)
            clv = (c - b["low"]) / hl
            vol = b["volume"].astype(float)
            vz = np.log(vol / vol.rolling(30, min_periods=20).mean())
            rngz = (hl / c) / (hl / c).rolling(30, min_periods=20).mean()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                              "z": z, "fwd": fwd, "fwd1": fwd1, "tr60": tr60,
                              "calm": (b["regime"] == "unknown"), "clv": clv, "vz": vz, "rngz": rngz,
                              "year": ts.dt.year, "wd": ts.dt.weekday})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A.pos % H == 0)].dropna(subset=["z", "ex", "clv"]).copy()
    def reg(g, cols):
        g = g.dropna(subset=cols + ["ex"])
        if len(g) < 30: return pd.Series({"n": len(g)})
        X = np.column_stack([np.ones(len(g))] + [g[c].values for c in cols])
        y = g.ex.values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ beta
        s2 = res @ res / (len(y) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        o = {"n": len(g)}
        for i, cn in enumerate(["const"] + cols):
            o["t_" + cn] = beta[i] / se[i]
        return pd.Series(o)
    out = {}
    G["zpos"] = G.z.clip(lower=0)
    G["zneg"] = G.z.clip(upper=0)
    G["sclv"] = G.z * (2 * G.clv - 1)  # signed close location times move
    G["clv_c"] = 2 * G.clv - 1
    out["calm_reg_zpos_zneg"] = G.groupby("calm").apply(lambda g: reg(g, ["zpos", "zneg"]))
    out["reg_z_and_clv"] = G.groupby("calm").apply(lambda g: reg(g, ["z", "clv_c"]))
    out["reg_clv_alone"] = G.groupby("calm").apply(lambda g: reg(g, ["clv_c"]))
    up = G[G.z > 0].copy()
    up["zvz"] = up.z * up.vz
    out["up_reg_z_vz"] = up.groupby("calm").apply(lambda g: reg(g, ["z", "vz"]))
    out["up_reg_z_rng"] = up.groupby("calm").apply(lambda g: reg(g, ["z", "rngz"]))
    out["clv_reg_by_year"] = G.groupby("year").apply(lambda g: reg(g, ["clv_c"]))
    out["clv_reg_by_coin"] = G.groupby("coin").apply(lambda g: reg(g, ["clv_c"]))
    G["clvq"] = pd.qcut(G.clv, 5, labels=False)
    out["ex_by_clv_quintile"] = G.groupby("clvq")["ex"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # weekday stability
    A["ex1"] = A.fwd1 - A.groupby("coin").fwd1.transform("mean")
    A["thfr"] = A.wd.isin([3, 4]).astype(int) - A.wd.isin([2]).astype(int)
    def t1(x):
        x = x.dropna(); return x.mean() / (x.std() / np.sqrt(len(x)))
    out["thu_fri_minus_wed_by_year_t"] = A.groupby("year").apply(lambda g: t1(g[g.wd.isin([3,4])].ex1) - 0) .to_frame("t_thufri")
    out["wed_by_year_t"] = A.groupby("year").apply(lambda g: t1(g[g.wd == 2].ex1)).to_frame("t_wed")
    return out
