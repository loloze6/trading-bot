def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("ts").reset_index(drop=True)
            c = d["close"].astype(float)
            r = c.pct_change()
            d["coin"] = coin; d["win"] = w
            d["r_prev1"] = r
            d["fwd1"] = c.shift(-1) / c - 1
            d["r20"] = c / c.shift(20) - 1
            vol = r.rolling(30, min_periods=20).std()
            d["vol30"] = vol
            d["z20"] = d["r20"] / (vol * np.sqrt(20))
            d["z1"] = r / vol
            d["r5"] = c / c.shift(5) - 1
            d["z5"] = d["r5"] / (vol * np.sqrt(5))
            lo60 = c.rolling(60, min_periods=40).min()
            d["dist_lo"] = (c / lo60 - 1) / (vol * np.sqrt(20))
            d["next_wd"] = (d["ts"] + pd.Timedelta(days=1)).dt.weekday
            d["year"] = d["ts"].dt.year
            d["day"] = d["ts"].dt.floor("D")
            d["fc"] = d["forecast"].astype(float)
            d["alloc"] = d["postRebalance_current_allocation"].astype(float)
            rows.append(d[["coin","win","day","year","fwd1","r_prev1","z1","z5","z20","vol30","dist_lo","next_wd","fc","alloc"]])
    A = pd.concat(rows, ignore_index=True)
    A = A.dropna(subset=["fwd1"])
    drift = A.groupby("coin")["fwd1"].mean()
    A["ex"] = A["fwd1"] - A["coin"].map(drift)

    def ct(s, days):
        g = s.groupby(days).sum()
        n = len(g)
        if n < 3: return np.nan
        m = s.sum() / len(s)
        # day-clustered t on mean per case
        dev = (s - m).groupby(days).sum()
        se = np.sqrt((dev**2).sum() * n/(n-1)) / len(s)
        return m / se

    def summar(df, key):
        out = []
        for k, g in df.groupby(key, observed=True):
            out.append({key if isinstance(key,str) else "k": k, "n": len(g), "mean_ex_%": 100*g["ex"].mean(),
                        "t_day": ct(g["ex"], g["day"]), "days": g["day"].nunique()})
        return pd.DataFrame(out)

    res = {}
    res["by_next_weekday"] = summar(A, "next_wd")
    B = A.dropna(subset=["z20"]).copy()
    B["z20q"] = pd.qcut(B["z20"], 5, labels=False)
    B["sat"] = (B["next_wd"] == 5).astype(int)
    out = []
    for (s, q), g in B.groupby(["sat", "z20q"]):
        out.append({"sat": s, "z20q": q, "n": len(g), "mean_ex_%": 100*g["ex"].mean(), "t_day": ct(g["ex"], g["day"])})
    res["z20_quintile_by_sat"] = pd.DataFrame(out)
    out = []
    for wd, g in B.groupby("next_wd"):
        rho, p = stats.spearmanr(g["z20"], g["ex"])
        out.append({"next_wd": wd, "n": len(g), "spearman_z20_ex": rho, "p": p})
    res["z20_rank_corr_by_weekday"] = pd.DataFrame(out)
    C = A.dropna(subset=["z1"]).copy()
    C["z1q"] = pd.qcut(C["z1"], 5, labels=False)
    res["after_1d_move_quintile"] = summar(C, "z1q")
    C2 = A.dropna(subset=["z5"]).copy()
    C2["z5q"] = pd.qcut(C2["z5"], 5, labels=False)
    res["after_5d_move_quintile"] = summar(C2, "z5q")
    V = A.dropna(subset=["vol30"]).copy()
    V["volq"] = V.groupby("coin")["vol30"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    res["by_vol_tercile"] = summar(V, "volq")
    D = A.dropna(subset=["dist_lo"]).copy()
    D["loq"] = pd.qcut(D["dist_lo"], 5, labels=False, duplicates="drop")
    res["by_dist_60d_low_quintile"] = summar(D, "loq")
    # Saturday cases by year and coin
    S = A[(A["fc"] > 0)]
    res["cases_by_year"] = summar(S, "year")
    res["cases_by_coin"] = summar(S, "coin")
    # Saturday all bars (no forecast) by year
    res["sat_all_by_year"] = summar(A[A["next_wd"] == 5], "year")
    return res
