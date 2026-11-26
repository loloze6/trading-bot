def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            b["z3"] = (c / c.shift(3) - 1) / sd30
            b["z10"] = (c / c.shift(10) - 1) / (sd30 * np.sqrt(10))
            b["z20"] = (c / c.shift(20) - 1) / (sd30 * np.sqrt(20))
            b["r60"] = c / c.shift(60) - 1
            b["sd30"] = sd30
            b["fwd"] = c.shift(-H) / c - 1
            b["rc"] = (b["regime"] == "unknown").astype(int)
            ts = pd.to_datetime(b["timestamp"])
            b["day"] = ts.dt.floor("D")
            b["yr"] = ts.dt.year
            b["coin"] = coin; b["win"] = w
            b["grid"] = (np.arange(len(b)) % H == 0)
            rows.append(b)
    df = pd.concat(rows, ignore_index=True)
    med = df.groupby("coin")["sd30"].median()
    df["agit"] = (df["sd30"] > df["coin"].map(med)).astype(int)
    def prof(r):
        if r.rc == 1: return "rising calm"
        if pd.isna(r.r60): return "na"
        if r.r60 > 0.10: return "rising agitated"
        if r.r60 < -0.10: return "falling " + ("agitated" if r.agit else "calm")
        return "choppy " + ("agitated" if r.agit else "calm")
    df["prof"] = df.apply(prof, axis=1)
    g = df[df["grid"] & df["fwd"].notna()].copy()
    drift = g.groupby("coin")["fwd"].mean()
    usual = g.groupby("coin")["fwd"].std()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    g["exs"] = g["ex"] / g["coin"].map(usual)
    def slope(s, x):
        s = s.dropna(subset=[x, "ex"])
        if len(s) < 20: return (len(s), np.nan, np.nan)
        X = np.column_stack([np.ones(len(s)), s[x].values]); y = s["ex"].values
        XtX = np.linalg.inv(X.T @ X); bta = XtX @ X.T @ y; e = y - X @ bta
        meat = np.zeros((2, 2))
        for _, idx in s.groupby("day").indices.items():
            u = X[idx].T @ e[idx]; meat += np.outer(u, u)
        G = s["day"].nunique(); n = len(s)
        V = XtX @ meat @ XtX * G / (G - 1) * (n - 1) / (n - 2)
        return (n, bta[1], bta[1] / np.sqrt(V[1, 1]))
    res = []
    for p, s in g.groupby("prof"):
        for x in ["z3", "z10", "z20"]:
            n, b_, t_ = slope(s, x); res.append((p, x, n, b_, t_))
    out = {"slope ex on z, by profile (day-clustered t)": pd.DataFrame(res, columns=["prof", "x", "n", "slope", "t"])}
    # rising calm z3 by coin and year
    s = g[g.prof == "rising calm"]
    out["rc z3 slope by coin"] = pd.DataFrame([(c_,) + slope(x_, "z3") for c_, x_ in s.groupby("coin")], columns=["coin", "n", "slope", "t"])
    out["rc z3 slope by year"] = pd.DataFrame([(y_,) + slope(x_, "z3") for y_, x_ in s.groupby("yr")], columns=["yr", "n", "slope", "t"])
    # positive-z3 cases (rises) in rising calm: size
    s2 = s[s.z3 > 0]
    dsum = s2.groupby("day")["ex"].sum()
    out["rc rises: n, days, mean ex, t(day), strength"] = pd.Series({
        "n": len(s2), "days": len(dsum), "mean_ex": s2.ex.mean(),
        "t_day": dsum.mean() / (dsum.std() / np.sqrt(len(dsum))) * 1.0, "strength": s2.exs.mean()})
    # falls outside: short side in falling & choppy agitated, z10 bins
    for p in ["falling agitated", "choppy agitated", "falling calm", "rising agitated"]:
        ss = g[g.prof == p].dropna(subset=["z10"]).copy()
        if len(ss) > 50:
            ss["bin"] = pd.qcut(ss["z10"], 4, labels=False, duplicates="drop")
            t = ss.groupby("bin").agg(lo=("z10", "min"), hi=("z10", "max"), n=("ex", "size"), m=("ex", "mean"), sd=("ex", "std"))
            t["t"] = t.m / (t.sd / np.sqrt(t.n)); out["z10 bins " + p] = t.drop(columns="sd")
    out["profile counts grid"] = g["prof"].value_counts()
    return out
