def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            rng = (b.high - b.low)
            cl = (b.close - b.low) / rng.replace(0, np.nan)
            r = b.close.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            width = (rng / b.close) / sd30
            nxt = b.close.shift(-1) / b.close - 1
            nxt2 = b.close.shift(-2) / b.close - 1
            tr60 = b.close / b.close.shift(60) - 1
            d = pd.DataFrame({"coin": coin, "w": w, "ts": b.timestamp, "regime": b.regime, "pos": np.arange(len(b)),
                              "cl": cl, "width": width, "nxt": nxt, "nxt2": nxt2, "r1": r, "tr60": tr60,
                              "alloc": b.postRebalance_current_allocation})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A = A[A.nxt.notna()].copy()
    drift = A.groupby("coin").nxt.mean()
    drift2 = A.groupby("coin").nxt2.mean()
    A["un"] = A.nxt - A.coin.map(drift)
    A["un2"] = A.nxt2 - A.coin.map(drift2)
    A["inprof"] = A.regime.isin(["mean_reversion", "unknown"])
    A["day"] = pd.to_datetime(A.ts).dt.floor("D")
    def tday(x, days):
        g = pd.DataFrame({"x": x - x.mean(), "d": days}).groupby("d").x.sum()
        G = len(g)
        if G < 3: return np.nan
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return x.mean() / se
    def summ(df, col, sign):
        x = sign * df[col]
        n = len(x)
        if n < 5: return pd.Series({"n": n})
        return pd.Series({"n": n, "mean": x.mean(), "t_day": tday(x.values, df.day.values), "hit": (x > 0).mean()})
    # state classification for bars with 60-day trend known
    def state(row):
        if row.inprof: return "choppy agitated"
        if pd.isna(row.tr60): return "out, trend unknown"
        if -0.10 <= row.tr60 <= 0.10: return "choppy calm"
        return "rising" if row.tr60 > 0.10 else "falling"
    A["state"] = A.apply(state, axis=1)
    out = {}
    hi = A[A.cl >= 0.75]; lo = A[A.cl <= 0.25]
    out["high-close short by state"] = hi.groupby("state").apply(lambda g: summ(g, "un", -1))
    out["low-close long by state"] = lo.groupby("state").apply(lambda g: summ(g, "un", 1))
    # width grading by state (wide = width above 1.25)
    for nm, sub, s in [("high", hi, -1), ("low", lo, 1)]:
        sub = sub.dropna(subset=["width"]).copy()
        sub["wide"] = np.where(sub.width >= sub.width.median(), "wide", "narrow")
        out[f"{nm}-close by state x width half"] = sub.groupby(["state", "wide"]).apply(lambda g: summ(g, "un", s))
    # non-signal bars in profile: does the profile alone earn?
    mid = A[(A.cl > 0.25) & (A.cl < 0.75)]
    out["mid-close bars, short sign, by state"] = mid.groupby("state").apply(lambda g: summ(g, "un", -1))
    out["all in-profile bars next-day unusual (long sign)"] = summ(A[A.inprof], "un", 1)
    # 2-day horizon in profile
    out["in-prof high close 2d short"] = summ(A[A.inprof & (A.cl >= 0.75)], "un2", -1)
    out["in-prof low close 2d long"] = summ(A[A.inprof & (A.cl <= 0.25)], "un2", 1)
    # deepest losing active bars
    act = A[A.regime == "mean_reversion"].copy()
    act["pnl"] = act.alloc * act.nxt
    act["pq"] = pd.qcut(act.pnl.rank(method="first"), 4, labels=["worst", "q2", "q3", "best"])
    out["active bars by pnl quartile"] = act.groupby("pq")[["pnl", "nxt", "r1", "width", "cl", "tr60", "alloc"]].mean()
    out["active by window: n, sum pnl"] = act.groupby("w").pnl.agg(["count", "sum", "min"])
    # profit if full-size: share of pnl lost to small allocation
    out["active alloc vs width corr"] = act[["alloc", "width"]].corr().iloc[0, 1]
    return out
