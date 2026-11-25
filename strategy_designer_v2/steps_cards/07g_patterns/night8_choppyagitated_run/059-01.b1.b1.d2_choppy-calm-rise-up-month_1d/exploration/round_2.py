def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=30).std()
            df["z1"] = r1 / sd30.shift(1)
            df["r60"] = c / c.shift(60) - 1
            df["r7"] = c / c.shift(7) - 1
            df["s7"] = df["r7"] / (sd30 * np.sqrt(7))
            df["f1"] = c.shift(-1) / c - 1
            df["f2"] = c.shift(-2) / c - 1
            df["f5"] = c.shift(-5) / c - 1
            df["pos"] = np.arange(len(df))
            df["coin"] = coin; df["win"] = w
            df["wd"] = pd.to_datetime(df["timestamp"]).dt.weekday
            df["yr"] = pd.to_datetime(df["timestamp"]).dt.year
            df["tr"] = np.where(df["r60"] > 0.10, "rising", np.where(df["r60"] < -0.10, "falling", np.where(df["r60"].notna(), "choppy", "na")))
            rows.append(df[["coin","win","pos","z1","r60","s7","f1","f2","f5","wd","yr","tr","regime"]])
    A = pd.concat(rows, ignore_index=True)
    for h in ["f1","f2","f5"]:
        A["u"+h[1:]] = A[h] - A.groupby("coin")[h].transform("mean")
    out = {}
    def tab(d, key, val):
        d = d.dropna(subset=[val])
        t = d.groupby(key)[val].agg(["count","mean","std"])
        t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
        return t.round(4)
    A["zq"] = pd.qcut(A["z1"], 5, labels=False)
    # weekday robustness
    W = A[A.wd == 2].dropna(subset=["u1"])
    out["wed u1 by window"] = tab(W, "win", "u1")
    out["wed u1 by coin"] = tab(W, "coin", "u1")
    out["wed u1 by year"] = tab(W, "yr", "u1")
    # big-down-day rebound by in-window 60d trend
    out["z1 bottom quint u1 by trend"] = tab(A[A.zq == 0], "tr", "u1")
    out["z1 top quint u1 by trend"] = tab(A[A.zq == 4], "tr", "u1")
    g2 = A[A.pos % 2 == 0]
    out["z1 top quint u2 by trend (2-grid)"] = tab(g2[g2.zq == 4], "tr", "u2")
    g5 = A[A.pos % 5 == 0].copy()
    g5["zq"] = pd.qcut(g5["z1"], 5, labels=False)
    out["falling: z1 quint -> u5 (5-grid)"] = tab(g5[g5.tr == "falling"], "zq", "u5")
    out["choppy: z1 quint -> u5 (5-grid)"] = tab(g5[g5.tr == "choppy"], "zq", "u5")
    # graded rebound: z1 deciles all, next day
    A["zd"] = pd.qcut(A["z1"], 10, labels=False)
    out["z1 decile -> u1 all"] = tab(A, "zd", "u1")
    out["z1 bottom quint u1 by window"] = tab(A[A.zq == 0], "win", "u1")
    # book concentration
    D = []
    for coin, wins in days.items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D).dropna(subset=["book_return"])
    nz = D[D.book_return != 0]["book_return"].sort_values()
    out["book nonzero days count"] = len(nz)
    out["sum all nonzero"] = round(nz.sum(), 4)
    out["sum excl top 5% days"] = round(nz.iloc[: int(len(nz)*0.95)].sum(), 4)
    out["sum of worst 5% days"] = round(nz.iloc[: int(len(nz)*0.05)].sum(), 4)
    return out
