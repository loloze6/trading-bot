def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r30": c / c.shift(30) - 1,
                "r60": c / c.shift(60) - 1,
                "r1": r1,
                "r5": c / c.shift(5) - 1,
                "vol30": r1.rolling(30).std(),
                "rng": (b["high"] - b["low"]) / c,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "f10": c.shift(-H) / c - 1,
                "f1": c.shift(-1) / c - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "pos": np.arange(len(b)),
            })
            df["vol_rel"] = df["vol30"] / df["vol30"].rolling(120, min_periods=60).median()
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["f10"].mean()
    A["u10"] = A["f10"] - A["coin"].map(drift)
    A["day"] = A.ts.dt.floor("D")
    G = A[(A.pos % H == 0)].dropna(subset=["u10", "r60", "r30"])
    G["trend"] = np.where(G.r60 > 0.1, "rising", np.where(G.r60 < -0.1, "falling", "choppy"))
    G["agit"] = np.where(G.vol_rel > 1, "agit", "calm")

    def tstat(s, days):
        d = pd.DataFrame({"v": s, "d": days}).groupby("d")["v"].sum()
        n = len(s)
        if n < 5: return np.nan
        se = np.sqrt((d ** 2).sum() - (s.mean() ** 2) * 0) / n
        # cluster SE about mean
        dd = pd.DataFrame({"v": s - s.mean(), "d": days}).groupby("d")["v"].sum()
        se = np.sqrt((dd ** 2).sum()) / n
        return s.mean() / se

    def tab(g, key):
        out = []
        for k, x in g.groupby(key):
            out.append({key if isinstance(key, str) else "k": k, "n": len(x), "mean_u10": x.u10.mean(),
                        "t": tstat(x.u10.values, x.day.values)})
        return pd.DataFrame(out)

    res = {}
    # r30 quintile by trend
    G["q30"] = G.groupby("trend")["r30"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out = []
    for (tr, q), x in G.groupby(["trend", "q30"]):
        out.append({"trend": tr, "q30": q, "n": len(x), "r30": x.r30.mean(), "u10": x.u10.mean(),
                    "t": tstat(x.u10.values, x.day.values)})
    res["u10_by_trend_r30quint"] = pd.DataFrame(out)
    # 5-day return quintile by trend
    G["q5"] = G.groupby("trend")["r5"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out = []
    for (tr, q), x in G.groupby(["trend", "q5"]):
        out.append({"trend": tr, "q5": q, "n": len(x), "r5": x.r5.mean(), "u10": x.u10.mean(),
                    "t": tstat(x.u10.values, x.day.values)})
    res["u10_by_trend_r5quint"] = pd.DataFrame(out)
    # agitation x trend
    out = []
    for (tr, ag), x in G.groupby(["trend", "agit"]):
        out.append({"trend": tr, "agit": ag, "n": len(x), "u10": x.u10.mean(),
                    "t": tstat(x.u10.values, x.day.values),
                    "corr_r30_u10": x[["r30", "u10"]].corr().iloc[0, 1]})
    res["profile_cells"] = pd.DataFrame(out)
    # weekday of daily returns, all bars
    A["wd"] = A.ts.dt.weekday
    res["f1_by_weekday"] = A.dropna(subset=["f1"]).groupby("wd")["f1"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # next day after large day moves (scaled by vol30), by trend
    A["z1"] = A.r1 / A.vol30
    A["trend"] = np.where(A.r60 > 0.1, "rising", np.where(A.r60 < -0.1, "falling", "choppy"))
    B = A.dropna(subset=["z1", "f1", "r60"]).copy()
    B["zq"] = pd.cut(B.z1, [-99, -2, -1, 1, 2, 99])
    B["f1z"] = B.f1 / B.vol30
    res["next_day_by_z1_trend"] = B.groupby(["trend", "zq"])["f1z"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # close position in range
    B["cq"] = pd.cut(B.clpos, [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    res["next_day_by_clpos_trend"] = B.groupby(["trend", "cq"])["f1z"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # book: short positions held - which side of r30 carries
    P = A[A.alloc < 0].dropna(subset=["f1"])
    P["g"] = -P.alloc * P.f1
    P["zr"] = pd.qcut(P.r30 / (P.vol30 * np.sqrt(30)), 4, labels=False)
    res["book_pos_gain_by_depthq"] = P.groupby("zr")["g"].agg(["count", "mean", "sum"])
    return res
