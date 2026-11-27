def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            tr60 = c / c.shift(60) - 1
            hi30 = c.shift(1).rolling(30, min_periods=20).max()
            lo30 = c.shift(1).rolling(30, min_periods=20).min()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "wd": ts.dt.weekday, "year": ts.dt.year,
                               "z1": r1 / sd30, "z5": (c / c.shift(5) - 1) / (sd30 * np.sqrt(5)),
                               "z10": (c / c.shift(10) - 1) / (sd30 * np.sqrt(10)),
                               "dhi": (c - hi30) / hi30 / sd30, "dlo": (c - lo30) / lo30 / sd30,
                               "tr60": tr60, "fwd": c.shift(-H) / c - 1, "fwd2": c.shift(-2) / c - 1,
                               "sdrel": sd30 / sd30.rolling(90, min_periods=30).median()})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    usual = A[A.pos % H == 0].groupby("coin")["fwd"].std()
    A["ufwd"] = A["fwd"] - A["coin"].map(drift)
    A["s"] = A["ufwd"] / A["coin"].map(usual)
    A["trend"] = np.where(A.tr60 > 0.10, "rising", np.where(A.tr60 < -0.10, "falling", "choppy"))
    A.loc[A.tr60.isna(), "trend"] = np.nan
    G = A[(A.pos % H == 0)].dropna(subset=["ufwd", "z5", "trend"]).copy()
    out = {}
    def slope(g, x):
        g = g.dropna(subset=[x, "ufwd"])
        if len(g) < 10: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g[x], g["ufwd"])
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})
    res = {}
    for tr in ["choppy", "falling", "rising"]:
        for x in ["z1", "z5", "z10", "dhi", "dlo"]:
            res[(tr, x)] = slope(G[G.trend == tr], x)
    out["slopes of ufwd on situation, by trend"] = pd.DataFrame(res).T
    C = G[G.trend == "choppy"].copy()
    C["z10b"] = pd.qcut(C.z10, 4)
    def f(x):
        u = x["ufwd"]; return pd.Series({"n": len(u), "mean": u.mean(), "t": u.mean() / (u.std() / np.sqrt(len(u))), "strength": x["s"].mean()})
    out["choppy z10 quartiles"] = C.groupby("z10b").apply(f)
    C["neg"] = C.z10 < 0
    out["choppy z10<0 by year"] = C[C.neg].groupby("year").apply(f)
    out["choppy z10<0 by window"] = C[C.neg].groupby("w").apply(f)
    out["choppy z10<0 by coin"] = C[C.neg].groupby("coin").apply(f)
    out["choppy z10 slope by sdrel high/low"] = pd.DataFrame({k: slope(C[(C.sdrel > 1) == k], "z10") for k in [True, False]}).T
    G2 = G.copy()
    out["weekday by year (mean ufwd)"] = G2.groupby(["year", "wd"])["ufwd"].mean().unstack()
    # baseline per trend
    out["trend baseline"] = G.groupby("trend").apply(f)
    return out
