def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []; hrows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].astype(float)
            lr = np.log(cl).diff()
            hc = (ts + pd.Timedelta(hours=1)).dt.hour
            r1 = cl.shift(-1)/cl - 1
            hrows.append(pd.DataFrame({"coin": c, "w": w, "yr": ts.dt.year, "hc": hc, "wd": ts.dt.dayofweek, "r1": r1}))
            p24 = cl/cl.shift(24) - 1
            vol24 = lr.rolling(24).std(); vol720 = lr.rolling(720, min_periods=200).std()
            maxshare = lr.abs().rolling(24).max()/lr.abs().rolling(24).sum()
            f24 = cl.shift(-24)/cl - 1; f72 = cl.shift(-72)/cl - 1
            g = np.arange(len(b)) % 24 == 0
            rows.append(pd.DataFrame({"coin": c, "w": w, "yr": ts.dt.year, "p24": p24, "z": p24/(vol720*np.sqrt(24)),
                                      "vr": vol24/vol720, "ms": maxshare, "f24": f24})[g])
    V = pd.concat(rows).dropna(subset=["p24", "z", "vr", "ms", "f24"])
    V["ex"] = V.f24 - V.groupby("coin").f24.transform("mean")
    def tm(s):
        s = s.dropna(); return pd.Series({"mean_bp": s.mean()*1e4, "t": s.mean()/(s.std()/np.sqrt(len(s))), "n": len(s)})
    out = {}
    V["zd"] = V.groupby("coin").z.transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    out["z_decile_next24_excess"] = V.groupby("zd").ex.apply(tm).unstack()
    def slope_t(d, x):
        r = stats.linregress(d[x], d.ex); return r.slope/r.stderr
    out["slope_z_by_coin"] = pd.Series({c: slope_t(d, "z") for c, d in V.groupby("coin")})
    out["slope_z_by_year"] = pd.Series({y: slope_t(d, "z") for y, d in V.groupby("yr")})
    # falls only: does vol ratio / jumpiness add?
    F = V[V.z < 0].copy()
    X = np.column_stack([np.ones(len(F)), F.z, np.log(F.vr), F.ms])
    beta, *_ = np.linalg.lstsq(X, F.ex.values, rcond=None)
    res = F.ex.values - X@beta; s2 = res@res/(len(F)-4)
    se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["falls_multi_t"] = pd.Series(beta/se, index=["const", "z", "logvr", "maxshare"])
    R = V[V.z > 0].copy()
    X = np.column_stack([np.ones(len(R)), R.z, np.log(R.vr), R.ms])
    beta, *_ = np.linalg.lstsq(X, R.ex.values, rcond=None)
    res = R.ex.values - X@beta; s2 = res@res/(len(R)-4)
    se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["rises_multi_t"] = pd.Series(beta/se, index=["const", "z", "logvr", "maxshare"])
    # high vol ratio within falls/rises
    V["vq"] = V.groupby("coin").vr.transform(lambda s: pd.qcut(s, 3, labels=False))
    V["sgn"] = np.sign(V.z)
    out["vq_by_sign"] = V.groupby(["sgn", "vq"]).ex.apply(tm).unstack()
    # late evening drift 20-22 UTC: 2-bar return starting at 20:00 close, nonoverlap one per day
    H = pd.concat(hrows)
    E = H[H.hc.isin([21, 22])]
    out["eve_by_coin"] = E.groupby("coin").r1.apply(tm).unstack()
    out["eve_by_year"] = E.groupby("yr").r1.apply(tm).unstack()
    out["eve_by_weekday"] = E.groupby("wd").r1.apply(tm).unstack()
    out["eve_windows_pos_share"] = E.groupby("w").r1.mean().gt(0).mean()
    out["h3_h14_by_year"] = H[H.hc.isin([3, 14])].groupby(["hc", "yr"]).r1.mean().unstack()*1e4
    return out
