def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20, min_periods=15).std().shift(1)
            z = r / vol
            ret90 = c / c.shift(90) - 1
            fall = np.where(ret90.notna(), ret90 < 0, b["regime"].eq("mean_reversion"))
            ret30 = c / c.shift(30) - 1
            vol30 = r.rolling(30, min_periods=20).std()
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": z,
                              "fall": fall, "ret30": ret30, "m30": ret30 / (vol30 * np.sqrt(30)),
                              "yr": pd.to_datetime(b["timestamp"]).dt.year})
            for h in (1, 3, 5, 10):
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 3, 5, 10):
        g = D[D["pos"] % h == 0].groupby("coin")[f"f{h}"].mean()
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(g)
    def summ(df, col):
        x = df[col].dropna(); n = len(x)
        if n < 3: return pd.Series({"n": n, "mean%": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})
    def slope(df, xcol, ycol):
        s = df[[xcol, ycol]].dropna()
        if len(s) < 10: return pd.Series({"n": len(s), "slope%": np.nan, "t": np.nan, "spearman": np.nan})
        lr = stats.linregress(s[xcol], s[ycol])
        return pd.Series({"n": len(s), "slope%": 100 * lr.slope, "t": lr.slope / lr.stderr,
                          "spearman": stats.spearmanr(s[xcol], s[ycol])[0]})
    out = {}
    # A: rising-regime up days -> 5d continuation, graded
    A = D[(~D.fall) & (D.z > 0) & (D.pos % 5 == 0)]
    out["A rising: z>0 vs u5 slope, all"] = slope(A, "z", "u5").to_frame().T
    out["A rising: z>1 u5 by year"] = A[A.z > 1].groupby("yr").apply(lambda g: summ(g, "u5"))
    out["A rising: z>1 u5 by coin sign share"] = pd.Series({
        "coins with mean>0": (A[A.z > 1].groupby("coin")["u5"].mean() > 0).mean(),
        "n coins": A[A.z > 1]["coin"].nunique()})
    A10 = D[(~D.fall) & (D.z > 0) & (D.pos % 10 == 0)]
    out["A rising: z>0 vs u10 slope"] = slope(A10, "z", "u10").to_frame().T
    # B: falling-regime large drops -> 3d rebound
    B = D[(D.fall) & (D.z < 0) & (D.pos % 3 == 0)].copy()
    B["negz"] = -B["z"]
    out["B falling: -z vs u3 slope (z<0)"] = slope(B, "negz", "u3").to_frame().T
    out["B falling: z<-2 u3 by year"] = B[B.z < -2].groupby("yr").apply(lambda g: summ(g, "u3"))
    # C: 30d momentum, vol-scaled, graded, 5d and 10d
    for h in (5, 10):
        C = D[D.pos % h == 0]
        out[f"C m30 vs u{h} slope"] = slope(C, "m30", f"u{h}").to_frame().T
        out[f"C m30 vs u{h} slope by year"] = C.groupby("yr").apply(lambda g: slope(g, "m30", f"u{h}"))
    # D: falling bounce fade 1d by year (the tested idea), and with z graded
    F = D[(D.fall) & (D.z > 1)]
    out["D falling z>1 u1 by year"] = F.groupby("yr").apply(lambda g: summ(g, "u1"))
    out["D falling z>0 vs u1 slope"] = slope(D[(D.fall) & (D.z > 0)], "z", "u1").to_frame().T
    out["D rising z>0 vs u1 slope"] = slope(D[(~D.fall) & (D.z > 0)], "z", "u1").to_frame().T
    return out
