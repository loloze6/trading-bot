def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            sd365 = sd.rolling(365, min_periods=120).median()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                "z": r / sd, "z5": (c / c.shift(5) - 1) / (sd * np.sqrt(5)),
                "tr60": c / c.shift(60) - 1, "agit": (sd > sd365).astype(float).where(sd365.notna()),
                "inprof": (b["regime"] == "unknown").astype(int), "yr": ts.dt.year,
            })
            for h in (2, 3, 5, 7):
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)

    def dayt(g, xcol, ycol):
        g = g.dropna(subset=[xcol, ycol])
        if len(g) < 10: return [len(g), np.nan, np.nan, np.nan, np.nan, np.nan]
        X = g[xcol] - g[xcol].mean()
        b = (X * g[ycol]).sum() / (X ** 2).sum()
        res = g[ycol] - g[ycol].mean() - b * X
        s = (X * res).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        m = g.groupby("day")[ycol].sum()
        dev = (g[ycol] - g[ycol].mean()).groupby(g["day"]).sum()
        tm = g[ycol].mean() / (np.sqrt((dev ** 2).sum()) / len(g))
        return [len(g), g["day"].nunique(), b, b / se, g[ycol].mean(), tm]

    idx = ["n", "days", "slope", "t_slope", "mean_u", "t_mean"]
    out = {}
    o = {}
    for h in (2, 3, 5, 7):
        G = A[A.pos % h == 0].dropna(subset=[f"f{h}"]).copy()
        G["u"] = G[f"f{h}"] - G["coin"].map(G.groupby("coin")[f"f{h}"].mean())
        g1 = G[G.inprof == 1]
        o[f"h{h}_prof_up"] = dayt(g1[g1.z > 0], "z", "u")
        o[f"h{h}_prof_down"] = dayt(g1[g1.z < 0], "z", "u")
        o[f"h{h}_prof_all"] = dayt(g1, "z", "u")
        # out of profile, non-rising trend, 5-day momentum
        g0 = G[(G.inprof == 0) & (G.tr60 <= 0.1)]
        o[f"h{h}_out_nonrising_z5"] = dayt(g0, "z5", "u")
        g0r = G[(G.inprof == 0) & (G.tr60 > 0.1)]
        o[f"h{h}_out_rising_z5"] = dayt(g0r, "z5", "u")
    out["slopes & means, day-clustered"] = pd.DataFrame(o, index=idx).T.round(4)
    # 5-day momentum outside profile in non-rising, by agitation and by year
    G = A[A.pos % 3 == 0].dropna(subset=["f3"]).copy()
    G["u"] = G["f3"] - G["coin"].map(G.groupby("coin")["f3"].mean())
    g0 = G[(G.inprof == 0) & (G.tr60 <= 0.1)]
    out["out nonrising z5 by agit"] = pd.DataFrame({str(k): dayt(gg, "z5", "u") for k, gg in g0.groupby("agit")}, index=idx).T.round(4)
    out["out nonrising z5 by year"] = pd.DataFrame({k: dayt(gg, "z5", "u") for k, gg in g0.groupby("yr")}, index=idx).T.round(4)
    g1 = G[(G.inprof == 1) & (G.z > 0)]
    out["prof up-day z by year"] = pd.DataFrame({k: dayt(gg, "z", "u") for k, gg in g1.groupby("yr")}, index=idx).T.round(4)
    return out
