def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float)
            hi = d["high"].astype(float).rolling(20, min_periods=20).max()
            lo = d["low"].astype(float).rolling(20, min_periods=20).min()
            r1 = c.pct_change()
            out = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(d)),
                                "pos": (c - lo) / (hi - lo), "r1": r1,
                                "fc": d["forecast"].astype(float),
                                "alloc": d["postRebalance_current_allocation"].astype(float),
                                "tr60": c / c.shift(60) - 1,
                                "vol30": r1.rolling(30).std(),
                                "day": pd.to_datetime(d["timestamp"]).dt.floor("D").astype(str),
                                "year": pd.to_datetime(d["timestamp"]).dt.year,
                                "f1": c.shift(-1) / c - 1})
            out["volmed"] = out["vol30"].rolling(365, min_periods=60).median()
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    A["x1"] = A["f1"] - A["coin"].map(A.groupby("coin")["f1"].mean())
    res = {}
    def pooled_t(df, col):
        df = df.dropna(subset=[col])
        m = df[col].mean()
        dev = (df[col] - m).groupby(df["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(df)
        return m, m / se, len(df), G
    sh = A[A["fc"] < 0].dropna(subset=["x1"]).copy()
    sh["raw"] = sh["x1"] * (-sh["fc"] / 10)          # the plan's measure as written
    sh["shortgain"] = -sh["x1"] * (-sh["fc"] / 10)   # the short's excess gain
    out = {}
    for k in ("raw", "shortgain"):
        m, t, n, G = pooled_t(sh, k)
        out[k] = {"mean": m, "t": t, "cases": n, "days": G}
    res["main measure, both signs (pooled per day)"] = pd.DataFrame(out).T
    sh["trend"] = np.where(sh["tr60"] > 0.1, "rising", np.where(sh["tr60"] < -0.1, "falling", "choppy"))
    sh["agit"] = np.where(sh["vol30"] > sh["volmed"], "agitated", np.where(sh["volmed"].notna(), "calm", "na"))
    sh["prof"] = sh["trend"] + " " + sh["agit"]
    rr = []
    for p, g in sh.groupby("prof"):
        m, t, n, G = pooled_t(g, "shortgain"); rr.append((p, m, t, n))
    res["short gain by profile"] = pd.DataFrame(rr, columns=["profile", "mean", "t", "cases"]).set_index("profile")
    rr = []
    for p, g in sh.groupby("year"):
        m, t, n, G = pooled_t(g, "shortgain"); rr.append((p, m, t, n))
    res["short gain by year"] = pd.DataFrame(rr, columns=["year", "mean", "t", "cases"]).set_index("year")
    # book gain actually realised: alloc x next return on short bars
    sh["bookgain"] = sh["alloc"] * sh["f1"]
    res["book bar gain on short cases mean"] = float(sh["bookgain"].mean())
    # Spearman of forecast with x1 among cases
    res["spearman fc vs x1 among short cases"] = float(sh[["fc", "x1"]].corr(method="spearman").iloc[0, 1])
    return res
