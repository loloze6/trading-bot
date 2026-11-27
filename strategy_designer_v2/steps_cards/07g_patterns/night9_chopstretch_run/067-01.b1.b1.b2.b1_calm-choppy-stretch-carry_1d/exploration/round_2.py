def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20).std()
            sma = c.rolling(20).mean()
            stretch = (c / sma - 1) / sd20
            ret60 = c / c.shift(60) - 1
            sd30 = r.rolling(30).std()
            for h in (1, 3, 10):
                fwd = c.shift(-h) / c - 1
                df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "h": h,
                                   "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                                   "fwd": fwd, "stretch": stretch, "r1": r / sd20,
                                   "calmprof": (b["regime"] == "unknown").astype(int),
                                   "ret60": ret60, "sd30": sd30, "ret20": c / c.shift(20) - 1,
                                   "yr": pd.to_datetime(b["timestamp"]).dt.year})
                df = df[df["pos"] % h == 0]
                rows.append(df)
    A = pd.concat(rows)
    A["drift"] = A.groupby(["coin", "h"])["fwd"].transform("mean")
    A["ex"] = A["fwd"] - A["drift"]
    A = A.dropna(subset=["fwd", "stretch"])
    A["trend"] = np.where(A["ret60"].isna(), "na", np.where(A["ret60"] > 0.10, "rising", np.where(A["ret60"] < -0.10, "falling", "choppy")))
    # agitation proxy: sd30 vs coin median of sd30 over all its bars
    A["agit"] = (A["sd30"] > A.groupby("coin")["sd30"].transform("median")).astype(int)

    def ct(x, d):
        g = pd.DataFrame({"x": x - 0, "d": d}).groupby("d")["x"].sum()
        n = len(x)
        m = x.mean()
        dev = pd.DataFrame({"x": x - m, "d": d}).groupby("d")["x"].sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return m, (m / se if se > 0 else np.nan), n, d.nunique()

    def summ(g, col="ex"):
        m, t, n, nd = ct(g[col], g["day"])
        return pd.Series({"n": n, "days": nd, "mean%": 100 * m, "t_day": t})

    # signed carry by trend x agitation proxy, h=10 and h=3
    for h in (3, 10):
        S = A[(A.h == h) & (A.trend != "na")].copy()
        S["sx"] = np.sign(S["stretch"]) * S["ex"]
        S["side"] = np.where(S["stretch"] > 0, "above", "below")
        out[f"carry_h{h}_trend_agit_side"] = S.groupby(["trend", "agit", "side"]).apply(lambda g: summ(g, "sx")).round(3)
    # graded: stretch tercile within trend, h10, excess return
    S = A[(A.h == 10) & (A.trend != "na")].copy()
    S["q"] = S.groupby("trend")["stretch"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["stretch_terc_h10_by_trend"] = S.groupby(["trend", "q"]).apply(summ).round(3)
    # big down day next-day by trend x agit
    S = A[(A.h == 1) & (A.trend != "na")].copy()
    S["q"] = pd.qcut(S["r1"], 5, labels=False)
    out["r1_h1_q_trend"] = S.groupby(["trend", "q"]).apply(summ).round(3)
    # big up day -> 10 days by year
    S = A[A.h == 10].copy()
    S["q"] = pd.qcut(S["r1"], 5, labels=False)
    out["r1_h10_q_year"] = S[S.q.isin([0, 4])].groupby(["q", "yr"]).apply(summ).round(3)
    # weekday h1 by year (Wednesday)
    S = A[A.h == 1].copy()
    S["wd"] = S["day"].dt.weekday
    S["wed"] = (S["wd"] == 2).astype(int)
    out["wed_by_year"] = S[S.wed == 1].groupby("yr").apply(summ).round(3)
    return out
