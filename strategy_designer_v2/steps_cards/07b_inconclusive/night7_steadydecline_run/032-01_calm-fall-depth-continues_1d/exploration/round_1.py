def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    # coin drift over all windows (daily)
    for coin, ws in bars.items():
        allr = []
        for w, df in ws.items():
            c = df["close"].values
            allr.append(c[1:]/c[:-1]-1)
        drift[coin] = np.concatenate(allr).mean()
    hs = [1, 2, 3, 5, 10]
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            fc = df["forecast"].fillna(0).values
            reg = df["regime"].astype(str).values
            for i in range(n):
                rec = {"coin": coin, "w": w, "i": i, "year": yr[i], "fc": fc[i], "reg": reg[i],
                       "day": str(pd.to_datetime(df["timestamp"].iloc[i]).date())}
                rec["r30"] = c[i]/c[i-30]-1 if i >= 30 else np.nan
                for h in hs:
                    rec[f"r{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    d["drift"] = d["coin"].map(drift)
    d["ex1"] = d["r1"] - d["drift"]
    act = d[(d.fc < 0) & d.r1.notna()].copy()
    act["gain"] = (-act.fc/10) * -(act.ex1)
    def tday(sub, col):
        s = sub.groupby("day")[col].sum()
        return pd.Series({"mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan, "days": len(s), "cases": len(sub)})
    out = {}
    out["overall"] = tday(act, "gain")
    out["by_coin"] = act.groupby("coin").apply(lambda s: tday(s, "gain"))
    out["by_window"] = act.groupby("w").apply(lambda s: tday(s, "gain"))
    out["by_year"] = act.groupby("year").apply(lambda s: tday(s, "gain"))
    act["terc"] = pd.qcut(act.fc.rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["by_tercile_ex1"] = act.groupby("terc").apply(lambda s: pd.Series({"mean_ex1": s.ex1.mean(), "mean_r1": s.r1.mean(), "t": stats.ttest_1samp(s.ex1, 0).statistic, "n": len(s), "mean_fc": s.fc.mean()}))
    # horizons, non-overlapping grid
    hr = []
    for h in hs:
        g = d[(d.i % h == 0) & d[f"r{h}"].notna()]
        dr = g.groupby("coin")[f"r{h}"].mean()
        a = g[g.fc < 0].copy()
        a["ex"] = a[f"r{h}"] - a.coin.map(dr)
        a["g"] = (-a.fc/10) * -a.ex
        s = a.groupby("day")["g"].sum()
        hr.append({"h": h, "mean_gain": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))), "days": len(s),
                   "mean_short_ex": (-a.ex).mean(), "mean_short_total": (-a[f"r{h}"]).mean(), "cases": len(a)})
    out["horizons"] = pd.DataFrame(hr)
    # outside profile: 30-day fall depth vs next-day return
    o = d[d.r30.notna() & d.r1.notna()].copy()
    o["inprof"] = o.reg == "unknown"
    o["fall"] = o.r30.clip(upper=0)
    res = []
    for k, s in o[o.r30 < 0].groupby("inprof"):
        rr = stats.spearmanr(s.fall, s.ex1)
        res.append({"inprofile": k, "n": len(s), "spearman_fall_vs_ex1": rr.correlation, "p": rr.pvalue, "mean_ex1": s.ex1.mean()})
    out["fall_vs_next_by_profile"] = pd.DataFrame(res)
    o2 = o[o.r30 < 0].copy()
    o2["q"] = pd.qcut(o2.r30, 5, labels=False)
    out["outside_quintiles"] = o2.groupby(["inprof", "q"]).ex1.agg(["mean", "count"])
    out["regimes"] = d.reg.value_counts()
    return out
