def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}; usual = {}
    for coin, wins in bars.items():
        g3 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 3, 3)
            g3.extend(list(c[idx + 3] / c[idx] - 1))
        drift[coin] = np.mean(g3); usual[coin] = np.std(g3, ddof=1)
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["wd"] = d["ts"].dt.weekday
            d["pos"] = np.arange(len(d))
            d["r1"] = d["close"].pct_change()
            d["r2"] = d["close"].pct_change(2)
            d["r3p"] = d["close"].pct_change(3)
            d["sma"] = d["close"].rolling(50).mean()
            d["dist"] = d["close"] / d["sma"] - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["f3"] = d["close"].shift(-3) / d["close"] - 1
            d["coin"] = coin; d["win"] = w; d["year"] = d["ts"].dt.year
            d["ex3"] = d["f3"] - drift[coin]
            d["s3"] = d["ex3"] / usual[coin]
            d["r1z"] = d["r1"] / d["vol20"]
            d["r2z"] = d["r2"] / d["vol20"]
            d["r3z"] = d["r3p"] / d["vol20"]
            rows.append(d[["coin","win","year","wd","pos","r1","r2","r3p","dist","vol20","f3","ex3","s3","r1z","r2z","r3z"]])
    A = pd.concat(rows, ignore_index=True).dropna(subset=["f3","r1","dist","vol20"])
    def summ(g):
        x = g["ex3"]; n = len(x)
        return pd.Series({"n": n, "mean_ex3_%": 100*x.mean(),
                          "t": x.mean()/(x.std(ddof=1)/np.sqrt(n)) if n > 2 else np.nan,
                          "strength": g["s3"].mean()})
    out = {}
    sun = A[A.wd == 6].copy()
    # Sunday rises below SMA: graded by size of the rise
    srb = sun[(sun.r1 > 0) & (sun.dist < 0)].copy()
    srb["q"] = pd.qcut(srb["r1z"], 4, labels=False)
    out["sun_rise_below_by_rise_quartile"] = srb.groupby("q").apply(lambda g: pd.concat([summ(g), pd.Series({"mean_r1z": g.r1z.mean()})]))
    out["sun_rise_below_by_year"] = srb.groupby("year").apply(summ)
    r = stats.linregress(srb["r1z"], srb["ex3"])
    out["sun_rise_below_slope"] = pd.Series({"n": len(srb), "slope": r.slope, "t": r.slope/r.stderr})
    # Sunday all: slope of ex3 on r1z, below vs above SMA
    sl = []
    for lab, g in [("below", sun[sun.dist < 0]), ("above", sun[sun.dist >= 0])]:
        rr = stats.linregress(g["r1z"], g["ex3"])
        sl.append({"side": lab, "n": len(g), "slope": rr.slope, "t": rr.slope/rr.stderr})
    out["sun_slope_by_sma_side"] = pd.DataFrame(sl)
    # Sunday slope by year
    sy = []
    for y, g in sun.groupby("year"):
        if len(g) > 30:
            rr = stats.linregress(g["r1z"], g["ex3"])
            sy.append({"year": y, "n": len(g), "slope": rr.slope, "t": rr.slope/rr.stderr})
    out["sun_slope_by_year"] = pd.DataFrame(sy)
    # Sunday: 2-day (weekend) return grading, below SMA, both signs
    sb = sun[sun.dist < 0].copy()
    sb["q"] = pd.qcut(sb["r2z"], 6, labels=False)
    out["sun_below_by_weekend2d_sextile"] = sb.groupby("q").apply(lambda g: pd.concat([summ(g), pd.Series({"mean_r2_%": 100*g.r2.mean()})]))
    # Wednesday momentum: graded by Wed 1d move, by year
    wed = A[A.wd == 2].copy()
    wed["q"] = pd.qcut(wed["r1z"], 6, labels=False)
    out["wed_by_r1z_sextile"] = wed.groupby("q").apply(lambda g: pd.concat([summ(g), pd.Series({"mean_r1z": g.r1z.mean()})]))
    wy = []
    for y, g in wed.groupby("year"):
        if len(g) > 30:
            rr = stats.linregress(g["r1z"], g["ex3"])
            wy.append({"year": y, "n": len(g), "slope": rr.slope, "t": rr.slope/rr.stderr})
    out["wed_slope_by_year"] = pd.DataFrame(wy)
    # past 3d momentum, non-overlapping grid
    G = A[A.pos % 3 == 0].dropna(subset=["r3z"]).copy()
    G["q"] = pd.qcut(G["r3z"], 6, labels=False)
    out["grid_by_past3d_z_sextile"] = G.groupby("q").apply(lambda g: pd.concat([summ(g), pd.Series({"mean_r3p_%": 100*g.r3p.mean()})]))
    # book: largest gain/loss days by weekday
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            d = df.copy(); d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            D.append(d[["wd","book_return"]])
    D = pd.concat(D).dropna()
    D = D[D.book_return != 0]
    out["book_nonzero_days_by_weekday"] = D.groupby("wd")["book_return"].agg(["count","mean","std"])
    return out
