def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float); v = df["volume"].astype(float)
            df["vr"] = v / v.shift(1).rolling(20, min_periods=20).mean()
            df["r1"] = c.pct_change()
            df["clv"] = (df["close"] - df["low"]) / (df["high"] - df["low"]).replace(0, np.nan)
            df["r5past"] = c / c.shift(5) - 1
            for h in [1, 2, 3, 5, 10]:
                df[f"f{h}"] = c.shift(-h) / c - 1
                df[f"g{h}"] = (np.arange(len(df)) % h == 0)
            df["inprof"] = df["regime"].isin(["trending", "unknown"])
            df["coin"] = coin; df["win"] = w
            df["year"] = pd.to_datetime(df["timestamp"]).dt.year
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for h in [1, 2, 3, 5, 10]:
        g = A[A[f"g{h}"]].groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(g)
    P = A[A["inprof"] & A["vr"].notna() & A["r1"].notna()].copy()
    P["up"] = P["r1"] > 0
    P["vrq"] = pd.qcut(P["vr"], 5, labels=["q1", "q2", "q3", "q4", "q5"])
    def summ(sub, h):
        s = sub[sub[f"g{h}"]][f"u{h}"].dropna()
        if len(s) < 3: return pd.Series({"n": len(s)})
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s)))})
    out = {}
    out["share_bars_in_profile_by_coin"] = A.groupby("coin")["inprof"].mean()
    t = []
    for h in [1, 2, 3, 5, 10]:
        for (up, q), sub in P.groupby(["up", "vrq"], observed=True):
            r = summ(sub, h); r["h"] = h; r["up"] = up; r["vrq"] = q; t.append(r)
    out["unusual_by_up_vrq_h"] = pd.DataFrame(t)
    H = P[P["up"] & (P["vr"] >= 1.5)]
    t = []
    for h in [1, 3, 5, 10]:
        for coin, sub in H.groupby("coin"):
            r = summ(sub, h); r["h"] = h; r["coin"] = coin; t.append(r)
    out["heavy_up_by_coin"] = pd.DataFrame(t)
    t = []
    for h in [1, 5]:
        for y, sub in H.groupby("year"):
            r = summ(sub, h); r["h"] = h; r["year"] = y; t.append(r)
    out["heavy_up_by_year"] = pd.DataFrame(t)
    # heavy-volume days by close location and day size
    HV = P[P["vr"] >= 1.5].copy()
    HV["clvb"] = pd.cut(HV["clv"], [-0.01, 0.33, 0.66, 1.01], labels=["lowclose", "mid", "highclose"])
    t = []
    for h in [1, 3, 5]:
        for k, sub in HV.groupby("clvb", observed=True):
            r = summ(sub, h); r["h"] = h; r["clv"] = k; t.append(r)
    out["heavy_vol_by_close_location"] = pd.DataFrame(t)
    HV["r1q"] = pd.qcut(HV["r1"], 4, labels=["r1_q1", "q2", "q3", "r1_q4"])
    t = []
    for h in [1, 3, 5]:
        for k, sub in HV.groupby("r1q", observed=True):
            r = summ(sub, h); r["h"] = h; r["r1q"] = k; r["r1mean"] = sub["r1"].mean(); t.append(r)
    out["heavy_vol_by_day_return_q"] = pd.DataFrame(t)
    # correlation vr vs forward among up days in profile (5d grid)
    U = P[P["up"] & P["g5"]].dropna(subset=["u5"])
    out["spearman_vr_u5_updays"] = f"rho {stats.spearmanr(U['vr'], U['u5'])[0]:.3f} n {len(U)}"
    D = P[(~P["up"]) & P["g5"]].dropna(subset=["u5"])
    out["spearman_vr_u5_downdays"] = f"rho {stats.spearmanr(D['vr'], D['u5'])[0]:.3f} n {len(D)}"
    return out
