def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        g3 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 3, 3)
            g3.extend(list(c[idx + 3] / c[idx] - 1))
        drift[coin] = np.mean(g3) if g3 else np.nan
        usual[coin] = np.std(g3, ddof=1) if len(g3) > 2 else np.nan
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["wd"] = d["ts"].dt.weekday
            d["r1"] = d["close"].pct_change()
            d["r3p"] = d["close"].pct_change(3)
            d["sma"] = d["close"].rolling(50).mean()
            d["dist"] = d["close"] / d["sma"] - 1
            d["vratio"] = d["volume"] / d["volume"].rolling(28).mean()
            d["vol20"] = d["r1"].rolling(20).std()
            d["f1"] = d["close"].shift(-1) / d["close"] - 1
            d["f3"] = d["close"].shift(-3) / d["close"] - 1
            d["coin"] = coin; d["win"] = w
            d["year"] = d["ts"].dt.year
            d["ex3"] = d["f3"] - drift[coin]
            d["s3"] = d["ex3"] / usual[coin]
            d["r1z"] = d["r1"] / d["vol20"]
            rows.append(d[["coin","win","year","wd","r1","r3p","dist","vratio","vol20","f1","f3","ex3","s3","r1z","forecast","close","volume"]])
    A = pd.concat(rows, ignore_index=True)
    A = A.dropna(subset=["f3","r1","dist"])
    def summ(g):
        x = g["ex3"].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean_ex3_%": 100*x.mean(), "t": x.mean()/(x.std(ddof=1)/np.sqrt(n)) if n>2 else np.nan,
                          "strength": g["s3"].mean()})
    out = {}
    fb = A[(A.r1 < 0) & (A.dist < 0)]
    out["fall_below_sma_by_weekday"] = fb.groupby("wd").apply(summ)
    fa = A[(A.r1 < 0) & (A.dist >= 0)]
    out["fall_above_sma_by_weekday"] = fa.groupby("wd").apply(summ)
    rb = A[(A.r1 > 0) & (A.dist < 0)]
    out["rise_below_sma_by_weekday"] = rb.groupby("wd").apply(summ)
    # slope of ex3 on r1z by weekday, all bars
    sl = []
    for wd, g in A.dropna(subset=["r1z"]).groupby("wd"):
        r = stats.linregress(g["r1z"], g["ex3"])
        sl.append({"wd": wd, "n": len(g), "slope_ex3_on_r1z": r.slope, "t": r.slope/r.stderr})
    out["slope_ex3_on_1d_z_by_wd"] = pd.DataFrame(sl)
    # depth below sma grading, any weekday, falls
    fb2 = A[(A.r1 < 0)].copy()
    fb2["distq"] = pd.qcut(fb2["dist"], 6, labels=False)
    out["falls_by_dist_sextile"] = fb2.groupby("distq").apply(lambda g: pd.concat([summ(g), pd.Series({"mean_dist": g.dist.mean()})]))
    # 3-day past return grading (all days)
    A2 = A.dropna(subset=["r3p"]).copy()
    A2["r3q"] = pd.qcut(A2["r3p"], 6, labels=False)
    out["all_by_past3d_sextile"] = A2.groupby("r3q").apply(lambda g: pd.concat([summ(g), pd.Series({"mean_r3p": g.r3p.mean()})]))
    # Sunday falls below sma by volume ratio
    sun = fb[fb.wd == 6].dropna(subset=["vratio"]).copy()
    sun["vq"] = pd.qcut(sun["vratio"], 3, labels=False)
    out["sunday_cases_by_volratio_tercile"] = sun.groupby("vq").apply(summ)
    # by vol level
    A3 = A.dropna(subset=["vol20"]).copy()
    A3["vq"] = A3.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["fall_below_by_vol_tercile"] = A3[(A3.r1<0)&(A3.dist<0)].groupby("vq").apply(summ)
    out["sunday_cases_by_year"] = fb[fb.wd==6].groupby("year").apply(summ)
    return out
