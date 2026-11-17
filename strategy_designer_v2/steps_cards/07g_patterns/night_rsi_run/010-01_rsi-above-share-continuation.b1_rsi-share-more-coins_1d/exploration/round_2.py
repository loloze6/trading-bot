def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = 14
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            n = len(cl)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r1 = pd.Series(cl).pct_change()
            sd = r1.rolling(30, min_periods=20).std().values
            for i in range(0, n - H, H):
                d = {"coin": c, "win": w, "yr": yr[i], "fwd": cl[i + H] / cl[i] - 1}
                for L in (3, 7):
                    d[f"past{L}"] = cl[i] / cl[i - L] - 1 if i >= L else np.nan
                    d[f"zpast{L}"] = d[f"past{L}"] / (sd[i] * np.sqrt(L)) if i >= L and sd[i] > 0 else np.nan
                rows.append(d)
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def tt(s, col):
        s = s[[col, "ex"]].dropna()
        if len(s) < 10: return np.nan, len(s)
        lr = stats.linregress(s[col], s["ex"]); return lr.slope / lr.stderr, len(s)
    pc = []
    for c, s0 in g.groupby("coin"):
        t7, n7 = tt(s0, "past7"); t3, _ = tt(s0, "past3"); tz, _ = tt(s0, "zpast7")
        pc.append({"coin": c, "n": n7, "t_past7": t7, "t_past3": t3, "t_zpast7": tz})
    out["14d fwd on past7/3 per coin"] = pd.DataFrame(pc)
    py = []
    for y, s0 in g.groupby("yr"):
        t7, n7 = tt(s0, "past7"); tz, _ = tt(s0, "zpast7")
        py.append({"yr": y, "n": n7, "t_past7": t7, "t_zpast7": tz})
    out["14d fwd on past7 per year"] = pd.DataFrame(py)
    pooled = {}
    for col in ["zpast3", "zpast7"]:
        pooled[col] = tt(g, col)[0]
    # winsorised past7 check
    s = g[["past7", "ex"]].dropna().copy()
    s["p7w"] = s["past7"].clip(s["past7"].quantile(.02), s["past7"].quantile(.98))
    s["exw"] = s["ex"].clip(s["ex"].quantile(.02), s["ex"].quantile(.98))
    lr = stats.linregress(s["p7w"], s["exw"]); pooled["past7 winsorised"] = lr.slope / lr.stderr
    out["pooled t extra"] = pd.Series(pooled)
    s["q"] = s.groupby(g.loc[s.index, "coin"])["past7"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["past7 quintile -> 14d ex"] = s.groupby("q")["ex"].agg(["count", "mean", "median"])
    # daily reversal after big down day: per coin & per year, z<=-1
    dd = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            r = df["close"].pct_change()
            z = r / r.rolling(30, min_periods=20).std().shift(1)
            ts = pd.to_datetime(df["timestamp"])
            dd.append(pd.DataFrame({"coin": c, "z": z, "r": r, "nxt": r.shift(-1), "yr": ts.dt.year, "wd": ts.dt.weekday}))
    D = pd.concat(dd)
    D["nxt_ex"] = D["nxt"] - D.groupby("coin")["r"].transform("mean")
    D["r_ex"] = D["r"] - D.groupby("coin")["r"].transform("mean")
    def tm(x): x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/x.std()*np.sqrt(len(x))})
    big = D[D["z"] <= -1]
    out["after z<=-1 next day per coin"] = big.groupby("coin")["nxt_ex"].apply(tm).unstack()
    out["after z<=-1 next day per year"] = big.groupby("yr")["nxt_ex"].apply(tm).unstack()
    s2 = D[["z", "nxt_ex"]].dropna(); lr = stats.linregress(s2["z"].clip(-4, 4), s2["nxt_ex"])
    out["next day on z slope t"] = lr.slope / lr.stderr
    sat = D[D["wd"] == 5]
    out["saturday per coin"] = sat.groupby("coin")["r_ex"].apply(tm).unstack()
    out["saturday per year"] = sat.groupby("yr")["r_ex"].apply(tm).unstack()
    return out
