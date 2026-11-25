def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            lo = b["low"].astype(float).values; hi = b["high"].astype(float).values
            n = len(b)
            L = b["low"].astype(float).rolling(30).min().shift(1).values
            reg = b["regime"].astype(str).values
            day = pd.to_datetime(b["timestamp"]).dt.floor("D").astype("int64").values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            r60 = pd.Series(c).pct_change(60).values
            r10 = pd.Series(c).pct_change(10).values
            for i in range(n):
                rec = {"coin": coin, "win": w, "pos": i, "day": day[i], "year": yr[i], "reg": reg[i],
                       "r60": r60[i], "r10": r10[i]}
                for h in (3, 5, 10):
                    rec[f"f{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rec["reclaim"] = (not np.isnan(L[i])) and lo[i] < L[i] < c[i]
                rec["pdepth"] = (L[i]-lo[i])/L[i] if rec["reclaim"] else np.nan
                rec["clpos"] = (c[i]-lo[i])/(hi[i]-lo[i]) if hi[i] > lo[i] else np.nan
                rec["str"] = (c[i]-L[i])/(hi[i]-lo[i]) if rec["reclaim"] and hi[i] > lo[i] else np.nan
                rows.append(rec)
    df = pd.DataFrame(rows)
    df["inprof"] = df["reg"].isin(["mean_reversion", "unknown"]) & ((df["r60"] < -0.10) | df["r60"].isna())
    g5 = df[df["pos"] % 5 == 0]
    drift = g5.groupby("coin")["f5"].mean()
    df["x5"] = df["f5"] - df["coin"].map(drift)
    df["x10"] = df["f10"] - df["coin"].map(drift)*2
    case = df["reg"] == "mean_reversion"
    other = df["inprof"] & ~case
    ev = df[case]; ot = df[other]
    out = {}
    sp = {}
    for v in ["r60", "r10", "pdepth", "clpos", "str"]:
        a = stats.spearmanr(ev[v], ev["x5"], nan_policy="omit")
        sp[v] = {"case rho x5": a[0], "case p": a[1],
                 "case rho x10": stats.spearmanr(ev[v], ev["x10"], nan_policy="omit")[0]}
        if v in ("r60", "r10", "clpos"):
            b2 = stats.spearmanr(ot[v], ot["x5"], nan_policy="omit")
            sp[v]["other rho x5"] = b2[0]; sp[v]["other p"] = b2[1]
    out["spearman by grade variable"] = pd.DataFrame(sp).T
    # r60 bins comparing case vs other
    bins = [-1, -0.45, -0.25, -0.10]
    res = []
    for lab, m in [("case", case), ("other", other)]:
        s = df[m].copy()
        s["bin"] = pd.cut(s["r60"], bins, labels=["<-45%", "-45..-25", "-25..-10"])
        for bn, gg in s.groupby("bin", observed=True):
            x = gg["x5"].dropna()
            d = x.groupby(gg.loc[x.index, "day"]).sum()
            t = x.mean()/(d.std(ddof=1)*np.sqrt(len(d))/len(x)) if len(d) > 2 else np.nan
            res.append({"grp": lab, "bin": bn, "n": len(x), "days": len(d), "mean x5": x.mean(), "t": t})
    out["x5 by 60d depth bin, case vs other"] = pd.DataFrame(res)
    # case vs other at 10d and 3d overall (overlapping, day clustered)
    res = []
    for h in ("f3", "x5", "x10"):
        for lab, m in [("case", case), ("other", other)]:
            s = df[m]; x = s[h].dropna()
            d = x.groupby(s.loc[x.index, "day"]).sum()
            res.append({"h": h, "grp": lab, "n": len(x), "days": len(d), "mean": x.mean(),
                        "t": x.mean()/(d.std(ddof=1)*np.sqrt(len(d))/len(x))})
    out["case vs other overlapping"] = pd.DataFrame(res)
    out["case by window"] = ev.groupby("win")["x5"].agg(["count", "mean"])
    return out
