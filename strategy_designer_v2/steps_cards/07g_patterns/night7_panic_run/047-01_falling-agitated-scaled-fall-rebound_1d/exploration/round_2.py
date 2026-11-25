def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            r5 = c / c.shift(5) - 1
            r10 = c / c.shift(10) - 1
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                "z": r / sd, "z5": r5 / (sd * np.sqrt(5)), "z10": r10 / (sd * np.sqrt(10)),
                "tr60": c / c.shift(60) - 1,
                "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1,
                "inprof": (b["regime"] == "unknown").astype(int),
                "wd": ts.dt.weekday, "yr": ts.dt.year,
            }))
    A = pd.concat(rows, ignore_index=True)
    G = A[A.pos % 3 == 0].dropna(subset=["f3"]).copy()
    G["u3"] = G["f3"] - G["coin"].map(G.groupby("coin")["f3"].mean())

    def dayt(g, xcol, ycol="u3"):
        g = g.dropna(subset=[xcol, ycol])
        if len(g) < 10: return [len(g), np.nan, np.nan, np.nan]
        X = g[xcol] - g[xcol].mean()
        b = (X * g[ycol]).sum() / (X ** 2).sum()
        res = g[ycol] - g[ycol].mean() - b * X
        s = (X * res).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return [len(g), g["day"].nunique(), b, b / se]

    out = {}
    o = {}
    for p in (0, 1):
        for col in ("z", "z5", "z10"):
            o[f"prof{p}_{col}"] = dayt(G[G.inprof == p], col)
    out["slope u3 on scaled move, day-clustered t"] = pd.DataFrame(o, index=["n", "days", "slope", "t"]).T.round(4)
    # out of profile 5d momentum by year and by window
    g0 = G[G.inprof == 0]
    out["prof0 z5 slope by year"] = pd.DataFrame({y: dayt(gg, "z5") for y, gg in g0.groupby("yr")}, index=["n", "days", "slope", "t"]).T.round(4)
    out["prof0 z5 slope by window"] = pd.DataFrame({w: dayt(gg, "z5") for w, gg in g0.groupby("win")}, index=["n", "days", "slope", "t"]).T.round(4)
    out["prof0 z5 slope by coin"] = pd.DataFrame({w: dayt(gg, "z5") for w, gg in g0.groupby("coin")}, index=["n", "days", "slope", "t"]).T.round(4)
    # out of profile by trend sign
    g0 = g0.copy()
    g0["trb"] = pd.cut(g0["tr60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    out["prof0 z5 slope by trend"] = pd.DataFrame({str(k): dayt(gg, "z5") for k, gg in g0.groupby("trb")}, index=["n", "days", "slope", "t"]).T.round(4)
    # in profile: by year, z slope
    g1 = G[G.inprof == 1]
    out["prof1 z slope by year"] = pd.DataFrame({y: dayt(gg, "z") for y, gg in g1.groupby("yr")}, index=["n", "days", "slope", "t"]).T.round(4)
    out["prof1 z slope by coin"] = pd.DataFrame({y: dayt(gg, "z") for y, gg in g1.groupby("coin")}, index=["n", "days", "slope", "t"]).T.round(4)
    # weekday by year
    G1 = A.dropna(subset=["f1"]).copy()
    G1["u1"] = G1["f1"] - G1["coin"].map(G1.groupby("coin")["f1"].mean())
    G1["wk"] = G1["wd"].map({2: "wed", 3: "thu", 4: "fri"}).fillna("other")
    out["u1 mean by year x weekday group"] = G1.groupby(["yr", "wk"])["u1"].mean().unstack().round(4)
    out["u1 wed day-clustered t"] = pd.Series({k: (lambda s: s.mean() / (s.std() / np.sqrt(len(s))))(gg.groupby("day")["u1"].mean()) for k, gg in G1.groupby("wk")}).round(3)
    # book around largest gains/losses
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; D.append(d)
    D = pd.concat(D)
    B = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    q = B["book_return"].quantile([0.02, 0.98])
    out["book extremes vs coins"] = pd.DataFrame({
        "worst2%": B[B.book_return <= q.iloc[0]].mean(),
        "best2%": B[B.book_return >= q.iloc[1]].mean()}).round(4)
    return out
