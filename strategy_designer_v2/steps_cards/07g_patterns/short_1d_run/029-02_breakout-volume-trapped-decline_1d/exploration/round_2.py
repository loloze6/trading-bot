def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []; fb = []; days = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(allr); usual = np.std(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; v = b["volume"]
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            f = pd.DataFrame({"ret1": r1, "wd": ts.dt.dayofweek, "yr": ts.dt.year,
                              "vratio": v / v.rolling(20).mean(),
                              "fc": b["forecast"],
                              "raw": b.get("debug_info.components.fb_vol.last_history_value")})
            f["fwd"] = c.shift(-H) / c - 1
            f["unus"] = (f["fwd"] - drift) / usual
            f["fwd1"] = c.shift(-1) / c - 1 - drift / H
            f["coin"] = coin; f["win"] = w
            rows.append(f.iloc[np.arange(0, len(f), H)].dropna(subset=["fwd"]))
            # every-bar 1-day forward return by weekday (no overlap at h=1)
            days.append(f.dropna(subset=["fwd1"])[["wd", "fwd1", "coin", "yr"]])
            act = f[(f["fc"] < 0) & f["fwd"].notna()].copy()
            act["cell"] = act.index // H
            fb.append(act.groupby("cell").head(1))
    g = pd.concat(rows); a = pd.concat(fb); d1 = pd.concat(days)
    out = {}
    tt = lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    # weekday 5-day robustness
    g["monTue"] = g["wd"].isin([0, 1])
    out["5d unus Mon/Tue vs other by coin"] = g.groupby(["coin", "monTue"])["unus"].mean().unstack()
    out["5d unus Mon/Tue vs other by year"] = g.groupby(["yr", "monTue"])["unus"].mean().unstack()
    w = stats.ttest_ind(g[g.monTue]["unus"], g[~g.monTue]["unus"], equal_var=False)
    out["5d Mon/Tue minus other welch"] = pd.Series({"t": w.statistic, "n_montue": g.monTue.sum(), "n_other": (~g.monTue).sum()})
    # 1-day returns by weekday
    t1 = d1.groupby("wd")["fwd1"].agg(["size", "mean"]); t1["mean"] *= 100
    t1["t"] = d1.groupby("wd")["fwd1"].apply(tt)
    out["next-day ret pct by weekday of signal close"] = t1
    out["next-day ret by weekday, by coin (pct)"] = (d1.groupby(["coin", "wd"])["fwd1"].mean() * 100).unstack()
    # ret1 small-down-day pattern by coin
    g["q1"] = pd.qcut(g["ret1"], 5, labels=False)
    out["ret1 quintile unus by coin"] = g.groupby(["coin", "q1"])["unus"].mean().unstack()
    # fb cases: unus vs vratio regression
    aa = a.dropna(subset=["vratio", "unus"])
    lr = stats.linregress(np.log(aa["vratio"]), aa["unus"])
    out["fb unus on log vratio"] = pd.Series({"slope": lr.slope, "t": lr.slope / lr.stderr, "n": len(aa)})
    out["fb high-vratio tercile by coin"] = aa.assign(q=pd.qcut(aa["vratio"], 3, labels=False)).groupby(["coin", "q"])["unus"].mean().unstack()
    return out
