def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            df = pd.DataFrame({"close": c})
            df["r1"] = c.pct_change()
            df["r3"] = c / c.shift(3) - 1
            df["r7"] = c / c.shift(7) - 1
            df["r30"] = c / c.shift(30) - 1
            df["hi30"] = c / b["high"].astype(float).rolling(30).max() - 1
            df["vol20"] = df["r1"].rolling(20).std()
            df["f7"] = c.shift(-7) / c - 1
            df["f1"] = c.shift(-1) / c - 1
            df["f3"] = c.shift(-3) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df["wd"] = ts.dt.weekday; df["year"] = ts.dt.year; df["ts"] = ts
            df["coin"] = coin; df["win"] = w
            df["pos"] = np.arange(len(df))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["z1"] = A["r1"] / A["vol20"]
    out = {}
    cm1 = A.groupby("coin")["f1"].mean()
    A["f1d"] = A["f1"] - A["coin"].map(cm1)
    # weekday on cross-coin day averages (removes cross-coin correlation)
    day = A.dropna(subset=["f1d"]).groupby(["win", "ts"]).agg(f=("f1d", "mean"), wd=("wd", "first"), year=("year", "first")).reset_index()
    tf = lambda s: s.mean() / s.std() * np.sqrt(len(s))
    out["wd_dayavg"] = day.groupby("wd")["f"].agg(["mean", "count", tf])
    day["half"] = np.where(day.year <= 2021, "early", "late")
    out["wd_dayavg_half"] = day.pivot_table(index="wd", columns="half", values="f", aggfunc=tf)
    # down-day reversal: slope of f1d on z1 for z1<0, per coin, and on day-avg
    D = A.dropna(subset=["f1d", "z1"])
    res = {}
    for c in D.coin.unique():
        d = D[(D.coin == c) & (D.z1 < 0)]
        r = stats.linregress(d.z1, d.f1d); res[c] = {"slope": r.slope, "t": r.slope / r.stderr, "n": len(d)}
    d = D[D.z1 < 0]; r = stats.linregress(d.z1, d.f1d); res["pooled"] = {"slope": r.slope, "t": r.slope / r.stderr, "n": len(d)}
    out["down_z1_slope_f1"] = pd.DataFrame(res).T
    D2 = D.copy(); D2["half"] = np.where(D2.year <= 2021, "early", "late")
    D2["zb"] = pd.cut(D2.z1, [-np.inf, -2, -1, 0, 1, np.inf])
    # cluster by day: average within day-bucket
    g = D2.groupby(["zb", "win", "ts", "half"], observed=True)["f1d"].mean().reset_index()
    out["zbucket_dayclustered"] = g.pivot_table(index="zb", columns="half", values="f1d", aggfunc=[ "mean", tf], observed=True)
    # 3-day reversal after 3-day fall, non-overlapping grid of 3
    A["f3d"] = A["f3"] - A["coin"].map(A[A.pos % 3 == 0].groupby("coin")["f3"].mean())
    G3 = A[(A.pos % 3 == 0)].dropna(subset=["f3d", "r3", "vol20"])
    G3 = G3.assign(z3=G3.r3 / (G3.vol20 * np.sqrt(3)))
    for nm, d in [("z3<0", G3[G3.z3 < 0]), ("z3>0", G3[G3.z3 > 0])]:
        r = stats.linregress(d.z3, d.f3d); out["f3_on_z3_" + nm] = f"slope {r.slope:.5f} t {r.slope/r.stderr:.2f} n {len(d)}"
    # falling month: r30 reversal on 7d grid, per coin and half
    A["f7d"] = A["f7"] - A["coin"].map(A[A.pos % 7 == 0].groupby("coin")["f7"].mean())
    G = A[A.pos % 7 == 0].dropna(subset=["f7d", "r30", "hi30", "r7", "vol20"])
    res = {}
    F = G[G.r30 <= 0]
    for c in F.coin.unique():
        d = F[F.coin == c]; r = stats.linregress(d.r30, d.f7d); res[c] = {"slope": r.slope, "t": r.slope / r.stderr, "n": len(d)}
    for h, d in [("early", F[F.year <= 2021]), ("late", F[F.year > 2021])]:
        r = stats.linregress(d.r30, d.f7d); res[h] = {"slope": r.slope, "t": r.slope / r.stderr, "n": len(d)}
    out["falling_r30_slope"] = pd.DataFrame(res).T
    # rising month: r7 slope by vol tercile, and hi30 added to r7
    T = G[G.r30 > 0].copy()
    T["qv"] = T.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    res = {}
    for q, d in T.groupby("qv"):
        r = stats.linregress(d.r7, d.f7d); res[q] = {"slope": r.slope, "t": r.slope / r.stderr, "n": len(d)}
    out["rising_r7_by_vol"] = pd.DataFrame(res).T
    X = np.column_stack([np.ones(len(T)), T.r7, T.hi30]); y = T.f7d.values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None); e = y - X @ beta
    cov = np.linalg.inv(X.T @ X) * (e @ e) / (len(y) - 3)
    out["rising_r7_plus_hi30_t"] = f"r7 t {beta[1]/np.sqrt(cov[1,1]):.2f}, hi30 t {beta[2]/np.sqrt(cov[2,2]):.2f}, n {len(y)}"
    # rising: r7 normalised by vol
    T["z7"] = T.r7 / (T.vol20 * np.sqrt(7))
    r = stats.linregress(T.z7, T.f7d); out["rising_z7_slope"] = f"slope {r.slope:.5f} t {r.slope/r.stderr:.2f}"
    return out
