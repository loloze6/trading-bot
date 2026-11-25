def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            r5 = c / c.shift(5) - 1
            z5 = r5 / (sd * np.sqrt(5))
            r60 = c / c.shift(60) - 1
            ag = (b["regime"] != "chop").astype(int)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "z": z, "z5": z5,
                               "r60": r60, "ag": ag, "yr": ts.dt.year, "day": ts.dt.floor("D")})
            for h in (1, 2, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 3, 5):
        D[f"x{h}"] = D[f"f{h}"] - D.groupby("coin")[f"f{h}"].transform("mean")
    D["tr"] = np.where(D.r60 > 0.10, "rising", np.where(D.r60 < -0.10, "falling", "choppy"))
    D.loc[D.r60.isna(), "tr"] = "na"
    def grid(h):
        return D[(D["pos"] % h == 0) & D[f"f{h}"].notna() & D["z"].notna()].copy()
    def daycl_t(s, col):
        dsum = s.groupby("day")[col].sum()
        n = s.groupby("day")[col].count()
        m = s[col].mean()
        dev = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((dev**2).sum()) / len(s)
        return m / se, len(dsum)
    res = []
    # A: agitated, falls only (z<0), day-1 rebound: slope on -z, by coin/year/trend
    g = grid(1)
    a = g[(g.ag == 1) & (g.z < 0)].copy(); a["s"] = -a["z"]
    lr = stats.linregress(a["s"], a["x1"])
    t_d, nd = daycl_t(a.assign(pr=a["s"]*a["x1"]), "pr")
    res.append({"set": "ag falls x1 all", "n": len(a), "slope%": 100*lr.slope, "t": lr.slope/lr.stderr, "w_mean%": 100*np.average(a.x1, weights=a.s), "tday": t_d, "days": nd})
    c = g[(g.ag == 0) & (g.z < 0)].copy(); c["s"] = -c["z"]
    lr = stats.linregress(c["s"], c["x1"])
    res.append({"set": "calm falls x1 all", "n": len(c), "slope%": 100*lr.slope, "t": lr.slope/lr.stderr, "w_mean%": 100*np.average(c.x1, weights=c.s)})
    for key in ("coin", "yr", "tr"):
        for k, s in a.groupby(key):
            if len(s) < 20: continue
            lr = stats.linregress(s["s"], s["x1"])
            res.append({"set": f"ag falls x1 {key}={k}", "n": len(s), "slope%": 100*lr.slope, "t": lr.slope/lr.stderr, "w_mean%": 100*np.average(s.x1, weights=s.s)})
    out["ag_fall_day1"] = pd.DataFrame(res).round(3)
    # B: calm, z5 momentum at 5 days, by coin/year/trend, both signs
    res = []
    g = grid(5)
    cm = g[(g.ag == 0) & g.z5.notna()].copy()
    lr = stats.linregress(cm["z5"], cm["x5"])
    t_d, nd = daycl_t(cm.assign(pr=np.sign(cm.z5)*cm["x5"]), "pr")
    res.append({"set": "calm z5 x5 all", "n": len(cm), "slope%": 100*lr.slope, "t": lr.slope/lr.stderr, "signmean%": 100*(np.sign(cm.z5)*cm.x5).mean(), "tday": t_d, "days": nd})
    for side, s in (("up", cm[cm.z5 > 0]), ("down", cm[cm.z5 < 0])):
        lr = stats.linregress(s["z5"], s["x5"])
        res.append({"set": f"calm z5 {side}", "n": len(s), "slope%": 100*lr.slope, "t": lr.slope/lr.stderr, "signmean%": 100*(np.sign(s.z5)*s.x5).mean()})
    for key in ("coin", "yr", "tr"):
        for k, s in cm.groupby(key):
            if len(s) < 20: continue
            lr = stats.linregress(s["z5"], s["x5"])
            res.append({"set": f"calm z5 {key}={k}", "n": len(s), "slope%": 100*lr.slope, "t": lr.slope/lr.stderr, "signmean%": 100*(np.sign(s.z5)*s.x5).mean()})
    out["calm_z5_mom5"] = pd.DataFrame(res).round(3)
    # z5 buckets calm, x5
    cm["b"] = pd.cut(cm.z5, [-99, -1.5, -0.5, 0.5, 1.5, 99])
    q = cm.groupby("b", observed=True)["x5"].agg(["count", "mean", "std"]); q["t"] = q["mean"]/(q["std"]/np.sqrt(q["count"])); q["mean"] *= 100
    out["calm_z5_buckets_x5"] = q.round(3)
    # agitated z buckets with counts, x1
    g = grid(1); ga = g[g.ag == 1].copy()
    ga["b"] = pd.cut(ga.z, [-99, -2.5, -2, -1.5, -1, -0.5, 0])
    q = ga.groupby("b", observed=True)["x1"].agg(["count", "mean", "std"]); q["t"] = q["mean"]/(q["std"]/np.sqrt(q["count"])); q["mean"] *= 100
    out["ag_fall_buckets_x1"] = q.round(3)
    return out
