def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(b)
            L = b["low"].astype(float).rolling(30).min().shift(1).values
            lo = b["low"].astype(float).values; hi = b["high"].astype(float).values
            reg = b["regime"].astype(str).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            day = pd.to_datetime(b["timestamp"]).dt.floor("D").astype("int64").values
            r60 = pd.Series(c).pct_change(60).values
            for i in range(n):
                rec = {"coin": coin, "win": w, "pos": i, "year": yr[i], "day": day[i],
                       "reg": reg[i], "r60": r60[i]}
                for h in (1, 2, 3, 5, 10):
                    rec[f"f{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rec["pierce"] = (not np.isnan(L[i])) and lo[i] < L[i]
                rec["reclaim"] = rec["pierce"] and c[i] > L[i]
                rec["closebelow"] = rec["pierce"] and c[i] <= L[i]
                rec["str"] = (c[i]-L[i])/(hi[i]-lo[i]) if rec["reclaim"] and hi[i] > lo[i] else np.nan
                rows.append(rec)
    df = pd.DataFrame(rows)
    out = {}
    out["regime counts"] = df["reg"].value_counts()
    inprof = df["reg"].isin(["mean_reversion", "unknown"]) & ((df["r60"] < -0.10) | df["r60"].isna())
    df["inprof"] = inprof
    case = df["reg"] == "mean_reversion"
    # drift per coin for 5d on grid
    res = []
    for h in (1, 2, 3, 5, 10):
        g = df[df["pos"] % h == 0]
        drift = g.groupby("coin")[f"f{h}"].mean()
        for name, m in [("case(mr)", case), ("reclaim any profile", df["reclaim"]),
                        ("close below low, inprof", df["closebelow"] & df["inprof"]),
                        ("other inprof", df["inprof"] & ~case)]:
            s = g[m.loc[g.index]]
            x = (s[f"f{h}"] - s["coin"].map(drift)).dropna()
            d = x.groupby(s.loc[x.index, "day"]).sum()
            t = x.mean()/ (d.std(ddof=1)*np.sqrt(len(d))/len(x)) if len(d) > 2 else np.nan
            res.append({"h": h, "group": name, "n": len(x), "days": len(d),
                        "mean_excess": x.mean(), "t_dayclust": t})
    out["by horizon (excess over coin drift, grid)"] = pd.DataFrame(res)
    # all case events (overlapping) breakdowns at 5d
    ev = df[case].copy()
    drift5 = df[df["pos"] % 5 == 0].groupby("coin")["f5"].mean()
    ev["x5"] = ev["f5"] - ev["coin"].map(drift5)
    out["case by coin"] = ev.groupby("coin")["x5"].agg(["count", "mean"])
    out["case by year"] = ev.groupby("year")["x5"].agg(["count", "mean"])
    ev["sq"] = pd.qcut(ev["str"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["case by strength tercile"] = ev.groupby("sq")[["x5", "f1", "f3", "f10", "str"]].mean()
    out["case by strength count"] = ev.groupby("sq")["x5"].count()
    ev["r60q"] = pd.qcut(ev["r60"].rank(method="first"), 3, labels=["deepest", "mid", "shallow"])
    out["case by 60d depth"] = ev.groupby("r60q")[["x5", "f10", "r60"]].mean()
    out["spearman str vs x5, x10"] = pd.Series({"x5": stats.spearmanr(ev["str"], ev["x5"], nan_policy="omit")[0],
                                                "f10": stats.spearmanr(ev["str"], ev["f10"], nan_policy="omit")[0]})
    # reclaim days by profile class
    rc = df[df["reclaim"]].copy()
    rc["x5"] = rc["f5"] - rc["coin"].map(drift5)
    rc["cls"] = np.where(rc["reg"] == "mean_reversion", "falling agitated", np.where(rc["reg"] == "chop", "other profile", "unknown"))
    out["reclaim by profile"] = rc.groupby("cls")[["x5", "f10"]].agg(["count", "mean"])
    out["share hit x5>0 case"] = (ev["x5"] > 0).mean()
    out["median x5 case"] = ev["x5"].median()
    return out
