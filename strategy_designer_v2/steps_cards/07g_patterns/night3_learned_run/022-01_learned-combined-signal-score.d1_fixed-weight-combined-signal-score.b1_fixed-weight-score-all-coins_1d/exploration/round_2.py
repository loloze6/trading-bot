def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values)
            n = len(c)
            r1 = c.pct_change()
            vol = r1.rolling(30, min_periods=20).std()
            volrel = vol / vol.rolling(60, min_periods=20).mean()
            r3 = c.pct_change(3)
            ts = pd.to_datetime(b["timestamp"])
            for H in [1, 2, 5, 10]:
                for i in range(0, n - H, H):
                    recs.append({"coin": coin, "win": w, "H": H, "ts": ts.iloc[i], "i": i,
                                 "fwd": c[i + H] / c[i] - 1, "r1": r1[i], "r3": r3[i],
                                 "vol": vol[i], "volrel": volrel[i]})
    g = pd.DataFrame(recs).dropna(subset=["r1", "vol", "fwd"])
    g["ex"] = g["fwd"] - g.groupby(["coin", "H"])["fwd"].transform("mean")
    g["z"] = g["ex"] / g.groupby(["coin", "H"])["fwd"].transform("std")
    g["r1z"] = g["r1"] / g["vol"]
    g["r3z"] = g["r3"] / (g["vol"] * np.sqrt(3))
    g["vt"] = g.groupby(["coin", "H"])["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out = {}
    def clus_t(s, col):
        # mean across coins per date, then t over dates
        m = s.groupby("ts")[col].mean()
        return pd.Series({"n_dates": len(m), "mean": m.mean(), "t_date": m.mean() / (m.std() / np.sqrt(len(m)))})
    rows = {}
    for H in [1, 2, 5, 10]:
        for v in [0, 1, 2]:
            s = g[(g.H == H) & (g.vt == v)].copy()
            s["p"] = s["r1z"].clip(-4, 4) * s["z"]
            rows[(H, v)] = clus_t(s, "p")
    out["r1z_x_z_by_H_voltercile_clustered"] = pd.DataFrame(rows).T
    rows = {}
    for H in [5]:
        for v in [0, 1, 2]:
            s = g[(g.H == H) & (g.vt == v)].copy()
            s["p"] = s["r3z"].clip(-4, 4) * s["z"]
            rows[(H, v)] = clus_t(s.dropna(subset=["p"]), "p")
    out["r3z_x_z_H5_by_vol_clustered"] = pd.DataFrame(rows).T
    # graded interaction: z ~ r1z + r1z*volrank, H=5
    s = g[g.H == 5].dropna(subset=["volrel"]).copy()
    s["vr"] = s.groupby("coin")["vol"].rank(pct=True) - 0.5
    s["x"] = s["r1z"].clip(-4, 4)
    s["xi"] = s["x"] * s["vr"]
    s["p_int"] = s["xi"] * s["z"]
    out["interaction_H5_clustered"] = clus_t(s, "p_int")
    # same with volrel (vol relative to its 60-day mean, known at close)
    s["vr2"] = np.log(s["volrel"])
    s["p_int2"] = s["x"] * s["vr2"] * s["z"]
    out["interaction_volrel_H5_clustered"] = clus_t(s, "p_int2")
    # per coin sign of interaction (low vs high tercile)
    pc = {}
    for coin, sc in g[g.H == 5].groupby("coin"):
        lo = sc[sc.vt == 0]; hi = sc[sc.vt == 2]
        a = stats.spearmanr(lo["r1"], lo["z"])[0] if len(lo) > 10 else np.nan
        bb = stats.spearmanr(hi["r1"], hi["z"])[0] if len(hi) > 10 else np.nan
        pc[coin] = {"rho_lowvol": a, "rho_highvol": bb, "n": len(sc)}
    out["per_coin_r1_rho_H5"] = pd.DataFrame(pc).T
    # by year, high minus low tercile
    s5 = g[g.H == 5].copy()
    s5["year"] = s5["ts"].dt.year
    yr = {}
    for y, sy in s5.groupby("year"):
        lo = sy[sy.vt == 0]; hi = sy[sy.vt == 2]
        yr[y] = {"rho_low": stats.spearmanr(lo["r1"], lo["z"])[0], "rho_high": stats.spearmanr(hi["r1"], hi["z"])[0], "n": len(sy)}
    out["by_year_r1_rho_H5"] = pd.DataFrame(yr).T
    # weekday clustered by date, H=5
    s5["wd"] = s5["ts"].dt.weekday
    out["weekday_H5_clustered"] = s5.groupby("wd").apply(lambda x: clus_t(x, "ex"))
    # size: 5-day excess return in quintiles of r1z within high-vol tercile and low-vol tercile
    for v in [0, 2]:
        sv = s5[s5.vt == v].copy()
        sv["q"] = pd.qcut(sv["r1z"].rank(method="first"), 5, labels=False)
        out["H5_ex_by_r1z_q_vt%d" % v] = sv.groupby("q").apply(lambda x: clus_t(x, "ex"))
    return out
