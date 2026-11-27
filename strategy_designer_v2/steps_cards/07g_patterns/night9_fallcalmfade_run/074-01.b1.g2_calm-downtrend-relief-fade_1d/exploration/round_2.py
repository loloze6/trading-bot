def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            df["r0"] = r
            for h in (1, 2, 3, 5):
                df["r%d" % h] = c.shift(-h)/c - 1
            df["sd30"] = r.shift(1).rolling(30, min_periods=20).std()
            df["tr60"] = c/c.shift(60) - 1
            down = (r < 0).astype(int).values
            run = np.zeros(len(c), int); loss = np.zeros(len(c))
            for i in range(1, len(c)):
                k = 0; j = i-1
                while j >= 1 and down[j] == 1 and k < 30:
                    k += 1; j -= 1
                run[i] = k
                loss[i] = (c.iloc[i-1]/c.iloc[i-1-k] - 1) if k > 0 else 0.0
            df["run"] = run; df["loss"] = loss
            df["depth"] = -df["loss"]/df["sd30"]
            df["reg"] = b["regime"].astype(str).values
            df["day"] = df["ts"].dt.floor("D")
            df["pos"] = np.arange(len(c))
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["r1"].mean()
    D["mu"] = D["coin"].map(mu)
    for h in (1, 2, 3, 5):
        D["x%d" % h] = D["r%d" % h] - h*D["mu"]
    fcalm = D["reg"].isin(["mean_reversion", "unknown"])
    tr = np.where(D["tr60"] > 0.10, "rising", np.where(D["tr60"] < -0.10, "falling", np.where(D["tr60"].notna(), "choppy", "na")))
    D["prof"] = np.where(fcalm, "falling_calm", np.where(tr == "falling", "falling_agit", tr))
    def ct(v, d):
        m = pd.DataFrame({"v": v, "d": d}).dropna()
        if len(m) < 5: return pd.Series({"n": len(m), "days": 0, "mean": np.nan, "t": np.nan})
        mean = m["v"].mean()
        S = (m["v"]-mean).groupby(m["d"]).sum()
        se = np.sqrt((S**2).sum())/len(m)
        return pd.Series({"n": len(m), "days": m["d"].nunique(), "mean": mean, "t": mean/se if se > 0 else np.nan})
    out = {}
    out["regime_counts"] = D["reg"].value_counts()
    out["prof_counts"] = D["prof"].value_counts()
    rb = D[(D["r0"] > 0) & (D["run"] >= 2)].copy()
    res = {}
    for h in (1, 2, 3, 5):
        res["x%d" % h] = rb.groupby("prof").apply(lambda g: ct(-g["x%d" % h], g["day"]))
    out["rb2_short_by_prof_horizon"] = pd.concat(res, axis=1).round(4)
    rb["dh"] = pd.qcut(rb["depth"], 2, labels=["shallow", "deep"])
    res = {}
    for h in (1, 3):
        res["x%d" % h] = rb.groupby(["prof", "dh"]).apply(lambda g: ct(-g["x%d" % h], g["day"]))
    out["rb2_short_by_prof_depthhalf"] = pd.concat(res, axis=1).round(4)
    # slope of short x3 on depth by profile
    sl = {}
    for p, g in rb.dropna(subset=["depth", "x3"]).groupby("prof"):
        if len(g) > 10:
            s = np.polyfit(g["depth"], -g["x3"], 1)[0]
            rho = g["depth"].corr(-g["x3"], method="spearman")
            sl[p] = {"n": len(g), "slope": s, "spearman": rho}
    out["rb2_x3_slope_on_depth_by_prof"] = pd.DataFrame(sl).T.round(4)
    # falling agitated + choppy by window: x3, non-overlap not enforced but count
    fa = rb[rb.prof.isin(["falling_agit", "choppy"])]
    out["rb2_fa_choppy_short_x3_by_window"] = fa.groupby("win").apply(lambda g: ct(-g["x3"], g["day"])).round(4)
    out["rb2_fa_choppy_short_x3_by_coin"] = fa.groupby("coin").apply(lambda g: ct(-g["x3"], g["day"])).round(4)
    # baseline: all days short x3 by prof (non-overlap grid every 3 bars)
    g3 = D[D["pos"] % 3 == 0]
    out["baseline_short_x3_grid_by_prof"] = g3.groupby("prof").apply(lambda g: ct(-g["x3"], g["day"])).round(4)
    # non-overlap check for rb2 in falling_agit+choppy: keep cases on 3-bar grid
    rbg = rb[(rb["pos"] % 3 == 0)]
    out["rb2_grid3_short_x3_by_prof"] = rbg.groupby("prof").apply(lambda g: ct(-g["x3"], g["day"])).round(4)
    return out
