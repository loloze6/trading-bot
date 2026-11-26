def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r3 = c / c.shift(3) - 1
            r1p = r1
            f3 = c.shift(-3) / c - 1
            f1 = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "inprof": (b["regime"] == "unknown").values,
                               "s3": (r3 / sd30).values, "s1": (r1p / sd30).values,
                               "f3": f3.values, "f1": f1.values,
                               "rng_s": (rng / sd30).values, "clv": clv.values,
                               "sd30": sd30.values,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
                               "ts": pd.to_datetime(b["timestamp"]).values})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    g3 = A[A["pos"] % 3 == 0].copy()
    drift = g3.groupby("coin")["f3"].mean()
    g3["u3"] = g3["f3"] - g3["coin"].map(drift)
    sdc = g3.groupby("coin")["f3"].std()
    g3["z3"] = g3["u3"] / g3["coin"].map(sdc)
    g3["day"] = pd.to_datetime(g3["ts"]).dt.floor("D")

    def summ(d, col="u3"):
        d = d.dropna(subset=[col])
        if len(d) < 5:
            return pd.Series({"n": len(d), "mean": np.nan, "t_day": np.nan, "days": 0})
        s = d.groupby("day")[col].sum()
        G = len(s); n = len(d); m = d[col].mean()
        se = np.sqrt(((s - s.index.map(lambda x: 0)) ** 0).sum()) if False else None
        dev = d[col] - m
        sdev = dev.groupby(d["day"]).sum()
        se = np.sqrt((sdev ** 2).sum() * G / max(G - 1, 1)) / n
        return pd.Series({"n": n, "mean": m, "t_day": m / se if se > 0 else np.nan, "days": G})

    out = {}
    g3v = g3.dropna(subset=["s3", "u3"]).copy()
    g3v["s3q"] = pd.qcut(g3v["s3"], 5, labels=["q1low", "q2", "q3", "q4", "q5high"])
    out["fwd3 unusual by s3 quintile x inprofile"] = g3v.groupby(["inprof", "s3q"]).apply(summ).round(4)
    out["s3 quintile edges"] = pd.Series(pd.qcut(g3v["s3"], 5, retbins=True)[1]).round(3)
    # s1 (one-day move scaled)
    g3v["s1q"] = pd.qcut(g3v["s1"], 5, labels=["q1low", "q2", "q3", "q4", "q5high"])
    out["fwd3 unusual by s1 quintile x inprofile"] = g3v.groupby(["inprof", "s1q"]).apply(summ).round(4)
    # range & close location
    g3v["clvq"] = pd.qcut(g3v["clv"], 3, labels=["lowclose", "mid", "highclose"])
    out["fwd3 by close location x inprofile"] = g3v.groupby(["inprof", "clvq"]).apply(summ).round(4)
    # vol level
    g3v["volq"] = g3v.groupby("coin")["sd30"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["fwd3 by own vol tercile"] = g3v.groupby("volq").apply(summ).round(4)
    out["fwd3 by weekday"] = g3v.groupby("wd").apply(summ).round(4)
    out["fwd3 by window"] = g3v.groupby("w").apply(summ).round(4)
    # correlation s3 vs z3 per inprof
    cc = {}
    for k, d in g3v.groupby("inprof"):
        r, p = stats.spearmanr(d["s3"], d["z3"])
        cc[str(k)] = f"rho {r:.3f} p {p:.3f} n {len(d)}"
    out["spearman s3 vs fwd3 z"] = pd.Series(cc)
    # 1-day horizon, every bar (non-overlap h=1)
    A1 = A.dropna(subset=["s1", "f1"]).copy()
    d1 = A1.groupby("coin")["f1"].mean()
    A1["u1"] = A1["f1"] - A1["coin"].map(d1)
    A1["day"] = pd.to_datetime(A1["ts"]).dt.floor("D")
    A1["s1q"] = pd.qcut(A1["s1"], 5, labels=["q1low", "q2", "q3", "q4", "q5high"])
    out["fwd1 unusual by s1 quintile x inprofile"] = A1.groupby(["inprof", "s1q"]).apply(lambda d: summ(d, "u1")).round(4)
    out["fwd1 by weekday"] = A1.groupby("wd").apply(lambda d: summ(d, "u1")).round(4)
    out["share inprof bars"] = float(A["inprof"].mean())
    return out
