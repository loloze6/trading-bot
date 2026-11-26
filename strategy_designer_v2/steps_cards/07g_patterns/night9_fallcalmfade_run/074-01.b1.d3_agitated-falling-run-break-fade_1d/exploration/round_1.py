def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            allr.append((c.shift(-1)/c-1).dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r0 = c.pct_change()
            nxt = c.shift(-1)/c-1
            r2 = c.shift(-2)/c-1
            ts = pd.to_datetime(b["timestamp"])
            # prior down run before today
            dn = (r0 < 0).astype(int); up = (r0 > 0).astype(int)
            rd = np.zeros(len(c)); ru = np.zeros(len(c))
            for i in range(1, len(c)):
                rd[i] = rd[i-1]+1 if dn.iloc[i] else 0
                ru[i] = ru[i-1]+1 if up.iloc[i] else 0
            prior_dn = pd.Series(rd).shift(1).fillna(0)
            prior_up = pd.Series(ru).shift(1).fillna(0)
            sd30 = r0.rolling(30, min_periods=20).std()
            tr60 = c/c.shift(60)-1
            df = pd.DataFrame({"coin": coin, "w": w, "r0": r0, "nxt": nxt, "x": nxt-mu, "r2": r2,
                               "pdn": prior_dn, "pup": prior_up, "regime": b["regime"].values,
                               "z0": r0/sd30, "tr60": tr60, "wd": ts.dt.weekday,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "day": ts.dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "r0"])
    d["inprof"] = d["regime"] != "chop"
    d["trend"] = np.where(d["tr60"] > 0.10, "rising", np.where(d["tr60"] < -0.10, "falling", np.where(d["tr60"].isna(), "na", "choppy")))

    def stat(g, col="x"):
        s = g.groupby("day")[col].sum()
        n = len(g); m = g[col].mean()
        t = s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s) > 2 else np.nan
        return pd.Series({"n": n, "days": len(s), "mean": m, "t_day": t})

    out = {}
    out["regime_counts"] = d["regime"].value_counts()
    rb = d[(d.r0 > 0) & (d.pdn >= 2)].copy()
    rb["runb"] = rb.pdn.clip(upper=5)
    out["runbreak_by_trend_runlen"] = rb.groupby(["trend", "runb"]).apply(stat)
    out["runbreak_inprof_vs_out"] = rb.groupby("inprof").apply(stat)
    # mirror: first down day after up run
    db = d[(d.r0 < 0) & (d.pup >= 2)].copy()
    db["runb"] = db.pup.clip(upper=5)
    out["downbreak_by_trend_runlen"] = db.groupby(["trend", "runb"]).apply(stat)
    # large moves by z bucket, in profile vs trend
    d["zb"] = pd.cut(d.z0, [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["next_by_z_trend"] = d.groupby(["trend", "zb"]).apply(stat)
    out["next_by_z_inprof"] = d[d.inprof].groupby("zb").apply(stat)
    out["weekday_inprof"] = d[d.inprof].groupby("wd").apply(stat)
    out["weekday_all"] = d.groupby("wd").apply(stat)
    # 2-day after run break in profile
    rbp = rb[rb.inprof].copy(); rbp["x2"] = rbp["r2"]
    out["runbreak_inprof_2day_raw"] = stat(rbp.dropna(subset=["x2"]), "x2")
    # runbreak size of up day
    rbp["upz"] = pd.qcut(rbp.z0, 3, labels=False, duplicates="drop")
    out["runbreak_inprof_by_upday_z"] = rbp.groupby("upz").apply(stat)
    return out
