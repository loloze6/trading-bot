def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 30: continue
            d = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"])})
            o, h, l, c = [b[k].astype(float) for k in ["open","high","low","close"]]
            r = c / c.shift(1) - 1
            d["coin"] = coin; d["w"] = w; d["r"] = r
            d["nx1"] = c.shift(-1) / c - 1
            d["nx3"] = c.shift(-3) / c - 1
            d["pos"] = np.arange(len(b))
            rng = (h - l)
            d["rangeN"] = rng / c
            d["rangeRel"] = d["rangeN"] / d["rangeN"].shift(1).rolling(20, min_periods=10).mean()
            d["body"] = (c - o).abs() / rng.replace(0, np.nan)
            d["cl_low"] = (h - c) / rng.replace(0, np.nan)
            d["vol20"] = r.shift(1).rolling(20, min_periods=10).std()
            d["z"] = r / d["vol20"]
            d["run3"] = c.shift(0) / c.shift(3) - 1  # includes today
            d["prerun"] = c.shift(1) / c.shift(4) - 1
            # past rank of return (share of past returns >= current)
            rk = [np.nan] * len(b)
            rv = r.values
            for i in range(len(b)):
                past = rv[1:i+1]
                past = past[~np.isnan(past)]
                if len(past) >= 20 and not np.isnan(rv[i]):
                    rk[i] = (past >= rv[i]).mean()
            d["negpct"] = rk
            d["fc"] = b["forecast"].astype(float).values
            d["regime"] = b["regime"].astype(str).values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    mu1 = D.groupby("coin")["r"].mean()
    D["ex1"] = D["nx1"] - D["coin"].map(mu1)
    mu3 = D[D["pos"] % 3 == 0].groupby("coin")["nx3"].mean()
    D["ex3"] = D["nx3"] - D["coin"].map(mu3)

    def tst(df, col):
        df = df.dropna(subset=[col])
        n = len(df)
        if n < 5: return pd.Series({"n": n, "days": df["day"].nunique() if n else 0, "mean%": np.nan, "t": np.nan})
        m = df[col].mean()
        S = (df[col] - m).groupby(df["day"]).sum()
        se = np.sqrt((S**2).sum()) / n
        return pd.Series({"n": n, "days": df["day"].nunique(), "mean%": 100*m, "t": m/se})

    out = {}
    out["regime_counts"] = D["regime"].value_counts().head(10)
    out["forecast_nonzero"] = float((D["fc"].fillna(0) != 0).sum())
    out["negpct_ge95_count"] = float((D["negpct"] >= 0.95).sum())
    # next-day excess by z-score bin of today's return
    D["zbin"] = pd.cut(D["z"], [-np.inf, -3, -2, -1, 0, 1, 2, 3, np.inf])
    out["ex1_by_zbin"] = D.groupby("zbin", observed=True).apply(lambda g: tst(g, "ex1"))
    deep = D[D["negpct"] >= 0.95].copy()
    deep["clbin"] = pd.cut(deep["cl_low"], [-0.01, 0.2, 0.5, 1.01])
    out["deep_by_closeloc"] = deep.groupby("clbin", observed=True).apply(lambda g: tst(g, "ex1"))
    up = D[D["negpct"] <= 0.05].copy()
    up["clbin"] = pd.cut(up["cl_low"], [-0.01, 0.2, 0.5, 1.01])
    out["bigup_by_closeloc"] = up.groupby("clbin", observed=True).apply(lambda g: tst(g, "ex1"))
    # brief: wide flat day after run, 3-day grid, excess against run
    G = D[D["pos"] % 3 == 0].copy()
    G["runsign"] = np.sign(G["prerun"])
    G["against3"] = -G["runsign"] * G["ex3"]
    G["wide"] = pd.qcut(G["rangeRel"], 3, labels=["narrow","mid","wide"])
    G["flat"] = G["body"] < 0.25
    out["brief_flat_by_width_against3"] = G[G["flat"]].groupby("wide", observed=True).apply(lambda g: tst(g, "against3"))
    out["brief_nonflat_by_width_against3"] = G[~G["flat"]].groupby("wide", observed=True).apply(lambda g: tst(g, "against3"))
    # weekday
    D["wd"] = D["ts"].dt.dayofweek
    out["ex1_by_weekday"] = D.groupby("wd").apply(lambda g: tst(g, "ex1"))
    # vol regime quintile
    D["vq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ex1_by_volq"] = D.groupby("vq").apply(lambda g: tst(g, "ex1"))
    # 3-day: momentum of past 3d return z
    G["z3"] = G["prerun"] / (G["vol20"] * np.sqrt(3))
    G["z3bin"] = pd.cut(G["z3"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["ex3_by_past3z"] = G.groupby("z3bin", observed=True).apply(lambda g: tst(g, "ex3"))
    # year
    D["yr"] = D["ts"].dt.year
    out["ex1_after_zlt-2_by_year"] = D[D["z"] < -2].groupby("yr").apply(lambda g: tst(g, "ex1"))
    return out
