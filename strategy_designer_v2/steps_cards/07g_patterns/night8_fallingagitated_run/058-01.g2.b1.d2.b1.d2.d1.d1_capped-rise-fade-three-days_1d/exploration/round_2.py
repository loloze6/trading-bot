def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "regime": b["regime"].astype(str),
                "z1": r1 / sd,
                "z3": (c / c.shift(3) - 1) / (sd * np.sqrt(3)),
                "tr60": c / c.shift(60) - 1,
                "f3": c.shift(-3) / c - 1,
            })
            rows.append(df)
    P = pd.concat(rows, ignore_index=True)
    out = {}

    def prep(off):
        g = P[(P["pos"] % 3) == off].copy()
        drift = g.groupby("coin")["f3"].mean()
        usual = g.groupby("coin")["f3"].std()
        g["u3"] = g["f3"] - g["coin"].map(drift)
        g["s3"] = g["u3"] / g["coin"].map(usual)
        g["day"] = g["ts"].dt.floor("D")
        g["inprof"] = g["regime"] != "chop"
        return g

    def slope(x, col):
        x = x.dropna(subset=["s3", col])
        x = x[x[col].abs() < 4]
        if len(x) < 15:
            return pd.Series({"n": len(x), "days": np.nan, "slope": np.nan, "t_cl": np.nan})
        X = x[col].values; Y = x["s3"].values
        Xc = X - X.mean(); b = (Xc * (Y - Y.mean())).sum() / (Xc ** 2).sum()
        e = (Y - Y.mean()) - b * Xc
        sc = pd.Series(Xc * e).groupby(x["day"].values).sum()
        G = len(sc)
        se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (Xc ** 2).sum()
        return pd.Series({"n": len(x), "days": G, "slope": b, "t_cl": b / se})

    g = prep(0)
    res = {}
    for nm, sub in [("in profile", g[g["inprof"]]), ("out profile", g[~g["inprof"]]),
                    ("all", g),
                    ("falling60 (out prof, tr60<-10%)", g[(~g["inprof"]) & (g["tr60"] < -0.1)]),
                    ("choppy60", g[(g["tr60"] >= -0.1) & (g["tr60"] <= 0.1)]),
                    ("rising60", g[g["tr60"] > 0.1])]:
        for col in ["z1", "z3"]:
            res[(nm, col)] = slope(sub, col)
    out["slope of strength on scaled move (long direction)"] = pd.DataFrame(res).T

    # in profile, rises only, magnitude grading
    gp = g[g["inprof"]]
    res2 = {}
    for nm, sub in [("rises z1>0", gp[gp["z1"] > 0]), ("rises z1>0.5", gp[gp["z1"] > 0.5]),
                    ("falls z1<0", gp[gp["z1"] < 0]), ("rises z3>0", gp[gp["z3"] > 0]),
                    ("falls z3<0", gp[gp["z3"] < 0])]:
        for col in ["z1", "z3"]:
            res2[(nm, col)] = slope(sub, col)
    out["in profile, by side"] = pd.DataFrame(res2).T

    # robustness: other grid offsets
    res3 = {}
    for off in [0, 1, 2]:
        go = prep(off)
        res3[("in", off)] = slope(go[go["inprof"]], "z1")
        res3[("out", off)] = slope(go[~go["inprof"]], "z3")
    out["grid offsets"] = pd.DataFrame(res3).T

    # by year, in and out
    res4 = {}
    g["yr"] = g["ts"].dt.year
    for y, sub in g.groupby("yr"):
        res4[("in z1", y)] = slope(sub[sub["inprof"]], "z1")
        res4[("out z3", y)] = slope(sub[~sub["inprof"]], "z3")
    out["by year"] = pd.DataFrame(res4).T

    # in profile: z1 >1 vs (0,1] mean u3 difference
    a = gp[gp["z1"] > 1]["u3"].dropna(); bq = gp[(gp["z1"] > 0) & (gp["z1"] <= 1)]["u3"].dropna()
    from scipy import stats as st
    out["in prof z1>1 minus (0,1]"] = pd.Series({"n_a": len(a), "mean_a": a.mean(), "n_b": len(bq),
                                                 "mean_b": bq.mean(), "welch_t": st.ttest_ind(a, bq, equal_var=False).statistic})
    return out
