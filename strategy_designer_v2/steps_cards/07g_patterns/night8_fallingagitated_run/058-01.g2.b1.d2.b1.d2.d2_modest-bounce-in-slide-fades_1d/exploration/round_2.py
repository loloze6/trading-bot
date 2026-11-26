def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w,
                "inprof": b["regime"].astype(str) != "chop",
                "tr60": (c / c.shift(60) - 1) * 100,
                "z1": r / sd,
                "z4": (c.shift(1) / c.shift(5) - 1) / sd,
                "z5": (c / c.shift(5) - 1) / sd,
                "clo": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "usd": sd, "day": ts.dt.floor("D"), "yr": ts.dt.year, "pos": np.arange(len(b)),
            }))
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["f1"].mean()
    D["u1"] = D["f1"] - D["coin"].map(drift)
    D["u2"] = D["f2"] - 2 * D["coin"].map(drift)
    def summ(g, col="u1"):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series({"n": len(g)})
        dd = g.groupby("day")[col].sum()
        return pd.Series({"n": len(g), "days": len(dd), "mean": g[col].mean(),
                          "t_day": dd.mean() / (dd.std() / np.sqrt(len(dd)))})
    out = {}
    P = D[D["inprof"]].copy()
    U = P[P["z1"] > 0].copy()
    U["z4q"] = pd.qcut(U["z4"], 4)
    out["prof up days: next-day unusual by prior 4d z quartile"] = U.groupby("z4q", observed=True).apply(summ)
    Dn = P[P["z1"] <= 0].copy()
    Dn["z4q"] = pd.qcut(Dn["z4"], 4)
    out["prof down days: next-day by prior 4d z quartile"] = Dn.groupby("z4q", observed=True).apply(summ)
    U["z1q"] = pd.qcut(U["z1"], 4)
    out["prof up days, prior 4d<0: by today z"] = U[U["z4"] < 0].groupby("z1q", observed=True).apply(summ)
    U2 = U[(U["z4"] < 0)].copy()
    U2["cloq"] = pd.cut(U2["clo"], [0, 0.5, 0.8, 1.0], include_lowest=True)
    out["prof up after slide: by close location"] = U2.groupby("cloq", observed=True).apply(summ)
    # deep slide up days by year
    deep = U[U["z4"] < U["z4"].quantile(0.25)]
    out["deep-slide up days by year"] = deep.groupby("yr").apply(summ)
    # 2-day horizon non-overlap grid
    g2 = U[U["pos"] % 2 == 0]
    g2 = g2.assign(z4q=pd.qcut(g2["z4"], 4))
    out["prof up days 2-day (grid) by z4 quartile"] = g2.groupby("z4q", observed=True).apply(lambda g: summ(g, "u2"))
    # 5-day scaled return (incl today) in profile, all days
    P["z5q"] = pd.qcut(P["z5"], 5)
    out["prof all days by 5d z quintile"] = P.groupby("z5q", observed=True).apply(summ)
    # falling calm proxy: chop with tr60<-10
    FC = D[(~D["inprof"]) & (D["tr60"] < -10)].copy()
    FU = FC[FC["z1"] > 0].copy()
    FU["z4q"] = pd.qcut(FU["z4"], 4)
    out["falling calm proxy up days by z4"] = FU.groupby("z4q", observed=True).apply(summ)
    # choppy/rising (tr60 >= -10) up days by z4
    OU = D[(D["tr60"] >= -10) & (D["z1"] > 0)].copy()
    OU["z4q"] = pd.qcut(OU["z4"], 4)
    out["non-falling up days by z4"] = OU.groupby("z4q", observed=True).apply(summ)
    return out
