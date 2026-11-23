def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy()
            d["day"] = pd.to_datetime(d["day"])
            d = d.sort_values("day").reset_index(drop=True)
            r = d["coin_return"]
            scale = r.abs().rolling(30, min_periods=20).mean().shift(0)
            vol = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "w": w, "wd": d["day"].dt.weekday, "yr": d["day"].dt.year,
                "r": r, "z": r / scale, "vol": vol,
                "next1": r.shift(-1), "next2": (1 + r.shift(-1)) * (1 + r.shift(-2)) - 1,
                "past3": (1 + r).rolling(3).apply(np.prod, raw=True) - 1,
                "book": d["book_return"]})
            df["volrank"] = df["vol"] / df["vol"].rolling(365, min_periods=60).median()
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # 1 weekday means
    g = D.dropna(subset=["r"]).groupby("wd")["r"]
    out["weekday_mean_ret"] = pd.DataFrame({"mean": g.mean(), "n": g.count(),
                                            "t": g.mean() / (g.std() / np.sqrt(g.count()))})
    # 2 next-day reaction to scaled move, by weekday of move
    res = []
    for wd, s in D.dropna(subset=["z", "next1"]).groupby("wd"):
        c, p = stats.pearsonr(s["z"], s["next1"])
        up = s[s.z > 1]["next1"]; dn = s[s.z < -1]["next1"]
        res.append({"wd": wd, "corr": c, "t_corr": c * np.sqrt((len(s) - 2) / (1 - c * c)), "n": len(s),
                    "next_after_up_gt1": up.mean(), "n_up": len(up),
                    "next_after_dn_lt-1": dn.mean(), "n_dn": len(dn)})
    out["next1_vs_z_by_weekday"] = pd.DataFrame(res)
    # 3 all days: z quintile -> next1
    A = D.dropna(subset=["z", "next1"]).copy()
    A["zq"] = pd.qcut(A["z"], 5, labels=False)
    g = A.groupby("zq")["next1"]
    out["next1_by_z_quintile"] = pd.DataFrame({"zmean": A.groupby("zq")["z"].mean(), "mean": g.mean(),
                                               "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count()})
    # 4 vol regime: z quintile x volrank high/low
    A2 = A.dropna(subset=["volrank"]).copy()
    A2["hv"] = (A2["volrank"] > 1).astype(int)
    res = []
    for hv, s in A2.groupby("hv"):
        c, _ = stats.pearsonr(s["z"], s["next1"])
        res.append({"highvol": hv, "corr_z_next1": c, "t": c * np.sqrt((len(s) - 2) / (1 - c * c)), "n": len(s),
                    "mean_next1": s.next1.mean()})
    out["vol_regime_reaction"] = pd.DataFrame(res)
    # 5 vol level -> next day return
    A2["vq"] = A2.groupby("coin")["volrank"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    g = A2.groupby("vq")["next1"]
    out["next1_by_volrank_quintile"] = pd.DataFrame({"mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.count())), "n": g.count()})
    # 6 hour-of-day hourly returns and Sunday forecast buckets
    hr = []; sun = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            ret1 = pd.Series(c).pct_change().shift(-1).values  # next bar return
            hr.append(pd.DataFrame({"h": ts.dt.hour.values, "wd": ts.dt.weekday.values, "r": ret1}))
            idx = np.where((ts.dt.weekday.values == 6) & (ts.dt.hour.values == 23))[0]
            idx = idx[idx + 48 < len(c)]
            fc = b["forecast"].values
            for i in idx:
                past = c[i] / c[i - 24] - 1 if i >= 24 else np.nan
                sun.append({"coin": coin, "f": fc[i], "past24": past,
                            "n24": c[i + 24] / c[i] - 1, "n48": c[i + 48] / c[i] - 1,
                            "n96": c[i + 96] / c[i] - 1 if i + 96 < len(c) else np.nan})
    H = pd.concat(hr).dropna()
    g = H.groupby("h")["r"]
    out["hour_mean_ret_bp"] = pd.DataFrame({"mean_bp": g.mean() * 1e4, "t": g.mean() / (g.std() / np.sqrt(g.count()))})
    S = pd.DataFrame(sun)
    S["fb"] = pd.cut(S["f"], [-0.1, 0.001, 1, 2, 4, 21], labels=["0", "0-1", "1-2", "2-4", "4+"])
    g = S.groupby("fb")
    out["sunday_by_forecast"] = pd.DataFrame({"n": g.size(), "past24": g["past24"].mean(), "n24": g["n24"].mean(),
                                              "n48": g["n48"].mean(), "t48": g["n48"].mean() / (g["n48"].std() / np.sqrt(g.size())),
                                              "n96": g["n96"].mean()})
    # 7 book's largest days: coin's prior and same day
    B = D.dropna(subset=["book"]).copy()
    B = B[B.book != 0]
    q = B["book"].quantile([0.02, 0.98])
    out["book_extremes"] = pd.DataFrame({
        "worst2pct": B[B.book <= q.iloc[0]][["r", "past3", "wd"]].mean(),
        "best2pct": B[B.book >= q.iloc[1]][["r", "past3", "wd"]].mean()})
    g = B.groupby("yr")["book"]
    out["book_by_year"] = pd.DataFrame({"mean_bp": g.mean() * 1e4, "n": g.count()})
    return out
