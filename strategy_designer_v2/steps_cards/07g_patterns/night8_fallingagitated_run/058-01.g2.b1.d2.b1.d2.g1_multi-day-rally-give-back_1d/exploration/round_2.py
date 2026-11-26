def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            sd365med = sd30.rolling(365, min_periods=60).median()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "z3": (c / c.shift(3) - 1) / (sd30 * np.sqrt(3)),
                               "z5": (c / c.shift(5) - 1) / (sd30 * np.sqrt(5)),
                               "r60": c / c.shift(60) - 1,
                               "f3": c.shift(-3) / c - 1,
                               "f5": c.shift(-5) / c - 1,
                               "sdu": c.shift(-3) / c - 1,
                               "calm": (b["regime"] != "unknown").astype(int),
                               "inprof": (b["regime"] == "unknown").astype(int),
                               "yr": pd.to_datetime(b["timestamp"]).dt.year,
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            df["agit_proxy"] = (sd30 > sd365med).astype(float)
            df.loc[sd365med.isna(), "agit_proxy"] = np.nan
            df["grid3"] = df["pos"] % 3 == 0
            df["grid5"] = df["pos"] % 5 == 0
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    def summ(x, col):
        x = x.dropna(subset=[col]); n = len(x)
        if n < 3: return pd.Series({"n": n, "days": n, "mean": np.nan, "t": np.nan})
        m = x[col].mean()
        d = x.groupby("day")[col].apply(lambda s: (s - m).sum()); D = len(d)
        se = np.sqrt((d**2).sum() * D / max(D - 1, 1)) / n
        return pd.Series({"n": n, "days": D, "mean": m, "t": m / se})
    out = {}
    g = A[A.grid3 & A.f3.notna()].copy()
    g["u3"] = g.f3 - g.coin.map(g.groupby("coin").f3.mean())
    g["tr"] = pd.cut(g.r60, [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    # falling, not in profile (= falling calm mostly)
    fc = g[(g.tr == "fall") & (g.inprof == 0)].dropna(subset=["z3"])
    out["falling non-agitated: z3 quintile"] = fc.groupby(pd.qcut(fc.z3, 5, labels=False)).apply(lambda x: summ(x, "u3"))
    fneg = fc[fc.z3 < 0]
    out["falling non-agit, z3<0: by year"] = fneg.groupby("yr").apply(lambda x: summ(x, "u3"))
    out["falling non-agit, z3<0: corr z3,u3"] = float(np.corrcoef(fneg.z3, fneg.u3)[0, 1])
    out["falling non-agit, z3<0 by window"] = fneg.groupby("win").apply(lambda x: summ(x, "u3"))
    # in profile rally: by year
    ip = g[(g.inprof == 1)].dropna(subset=["z3"])
    ipp = ip[ip.z3 > 0]
    out["in profile z3>0: by year (u3 neg = give back)"] = ipp.groupby("yr").apply(lambda x: summ(x, "u3"))
    out["in profile z3>0: by z3 tercile"] = ipp.groupby(pd.qcut(ipp.z3, 3, labels=False)).apply(lambda x: summ(x, "u3"))
    # 5-day version in falling non-agitated
    g5 = A[A.grid5 & A.f5.notna()].copy()
    g5["u5"] = g5.f5 - g5.coin.map(g5.groupby("coin").f5.mean())
    g5["tr"] = pd.cut(g5.r60, [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    f5 = g5[(g5.tr == "fall") & (g5.inprof == 0)].dropna(subset=["z5"])
    out["falling non-agit: z5 quintile, 5d fwd"] = f5.groupby(pd.qcut(f5.z5, 5, labels=False)).apply(lambda x: summ(x, "u5"))
    # choppy agitated (proxy) shorts: z3 quintile
    ca = g[(g.tr == "chop") & (g.agit_proxy == 1)].dropna(subset=["z3"])
    out["choppy agitated(proxy): z3 tercile"] = ca.groupby(pd.qcut(ca.z3, 3, labels=False)).apply(lambda x: summ(x, "u3"))
    return out
