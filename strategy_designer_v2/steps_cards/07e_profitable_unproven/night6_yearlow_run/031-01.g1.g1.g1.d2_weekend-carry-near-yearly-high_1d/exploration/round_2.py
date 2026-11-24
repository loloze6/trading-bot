def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    out = {}
    drift = {}; drift1 = {}
    for c, ws in bars.items():
        r2 = []; r1 = []
        for w, b in ws.items():
            cl = b["close"].values
            g = cl[::2]; r2 += list(g[1:] / g[:-1] - 1); r1 += list(cl[1:] / cl[:-1] - 1)
        drift[c] = np.mean(r2); drift1[c] = np.mean(r1)
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"]
            hi365 = b["high"].rolling(365, min_periods=91).max()
            d = pd.DataFrame({"coin": c, "win": w, "wd": ts.dt.weekday, "year": ts.dt.year,
                "day": ts.dt.normalize(), "r14": cl / cl.shift(14) - 1,
                "dist": 1 - cl / hi365,
                "fwd2": cl.shift(-2) / cl - 1, "fwd1": cl.shift(-1) / cl - 1,
                "sun1": cl.shift(-2) / cl.shift(-1) - 1, "pos": np.arange(len(b))})
            d["ex2"] = d["fwd2"] - drift[c]; d["ex1"] = d["fwd1"] - drift1[c]; d["exsun"] = d["sun1"] - drift1[c]
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    def ct(s, dcol):
        x = pd.DataFrame({"v": s, "d": dcol}).dropna()
        if len(x) < 5: return pd.Series({"m": np.nan, "t": np.nan, "n": len(x), "days": 0})
        m = x["v"].mean(); g = (x["v"] - m).groupby(x["d"]).sum(); G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"m": m, "t": m / se, "n": len(x), "days": G})
    def slope(df, xcol, ycol):
        x = df[[xcol, ycol, "day"]].dropna()
        xm = x[xcol] - x[xcol].mean(); b = (xm * x[ycol]).sum() / (xm ** 2).sum()
        res = x[ycol] - x[ycol].mean() - b * xm
        g = (xm * res).groupby(x["day"]).sum(); G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / (xm ** 2).sum()
        return pd.Series({"slope": b, "t": b / se, "n": len(x), "days": G})
    # graded r14 slope on next-1-day excess, by weekday, non-overlapping not needed for 1d
    out["slope_ex1_on_r14_by_weekday"] = pd.DataFrame({k: slope(g, "r14", "ex1") for k, g in A.groupby("wd")}).T
    # all Fridays: slope on r14 of 2-day excess; of Sat-only; of Sun-only
    F = A[A["wd"] == 4]
    out["fri_slopes"] = pd.DataFrame({"ex2_on_r14": slope(F, "r14", "ex2"), "sat_on_r14": slope(F, "r14", "ex1"),
        "sun_on_r14": slope(F, "r14", "exsun"), "ex2_on_dist_up": slope(F[F.r14 > 0], "dist", "ex2"),
        "ex2_on_dist_all": slope(F, "dist", "ex2")}).T
    # r14 slope on next-day excess, all days, every bar
    out["slope_ex1_on_r14_alldays"] = slope(A, "r14", "ex1")
    # weekday ex1 by r14 sign up only
    out["ex1_up14_by_weekday"] = pd.DataFrame({k: ct(g["ex1"], g["day"]) for k, g in A[A.r14 > 0].groupby("wd")}).T
    out["ex1_down14_by_weekday"] = pd.DataFrame({k: ct(g["ex1"], g["day"]) for k, g in A[A.r14 <= 0].groupby("wd")}).T
    # book daily returns by year and window-leave, market part
    D = pd.concat([d.assign(coin=c, win=w) for c, ws in days.items() for w, d in ws.items()], ignore_index=True)
    D["day"] = pd.to_datetime(D["day"])
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    bk["year"] = bk["day"].dt.year
    out["book_daily_by_year"] = bk.groupby("year").agg(mean=("book_return", "mean"), sd=("book_return", "std"),
        hold=("coin_return", "mean"), n=("book_return", "size"))
    out["book_daily_by_weekday"] = bk.groupby(bk["day"].dt.weekday)["book_return"].agg(["mean", "count"])
    return out
