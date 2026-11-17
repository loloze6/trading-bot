def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            hi30 = c.rolling(30, min_periods=20).max()
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)),
                              "r7": c / c.shift(7) - 1,
                              "r7z": (c / c.shift(7) - 1) / (vol30 * np.sqrt(7)),
                              "near": c / hi30 - 1,
                              "vrel": df["volume"] / df["volume"].rolling(30, min_periods=20).mean(),
                              "z": r1 / vol30,
                              "fwd3": c.shift(-3) / c - 1, "fwd1": c.shift(-1) / c - 1,
                              "fwd7": c.shift(-7) / c - 1,
                              "wd": ts.dt.weekday, "yr": ts.dt.year,
                              "alloc": df["postRebalance_current_allocation"]})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    for h in [1, 3, 7]:
        A[f"ex{h}"] = A[f"fwd{h}"] - A.groupby("coin")[f"fwd{h}"].transform("mean")
    G3 = A[A["pos"] % 3 == 0].dropna(subset=["ex3", "r7z"])
    G7 = A[A["pos"] % 7 == 0].dropna(subset=["ex7", "r7z"])
    out = {}
    res = []
    for coin, g in G3.groupby("coin"):
        s = stats.linregress(g["r7z"], g["ex3"])
        g7 = G7[G7["coin"] == coin]; s7 = stats.linregress(g7["r7z"], g7["ex7"])
        gv = g.dropna(subset=["vrel"]); sv = stats.linregress(np.log(gv["vrel"]), gv["ex3"])
        res.append([coin, len(g), s.slope / s.stderr, len(g7), s7.slope / s7.stderr, sv.slope / sv.stderr])
    s = stats.linregress(G3["r7z"], G3["ex3"]); s7 = stats.linregress(G7["r7z"], G7["ex7"])
    gv = G3.dropna(subset=["vrel"]); sv = stats.linregress(np.log(gv["vrel"]), gv["ex3"])
    res.append(["ALL", len(G3), s.slope / s.stderr, len(G7), s7.slope / s7.stderr, sv.slope / sv.stderr])
    out["slope_t_r7z_ex3_ex7_logvol_ex3"] = pd.DataFrame(res, columns=["coin", "n3", "t_r7z_3", "n7", "t_r7z_7", "t_logvol_3"])
    # r7z quintiles ex3 and ex7
    for nm, G, col in [("r7z_q_ex3", G3, "ex3"), ("r7z_q_ex7", G7, "ex7")]:
        g = G.copy(); g["b"] = pd.qcut(g["r7z"], 5, labels=False)
        t = g.groupby("b").agg(lo=("r7z", "min"), hi=("r7z", "max"), n=(col, "size"), mean=(col, "mean"), sd=(col, "std"))
        t["t"] = t["mean"] / (t["sd"] / np.sqrt(t["n"])); out[nm] = t.drop(columns="sd")
    # by year: r7z slope t
    yr = []
    for y, g in G3.groupby("yr"):
        s = stats.linregress(g["r7z"], g["ex3"]); yr.append([y, len(g), s.slope, s.slope / s.stderr])
    out["r7z_slope_by_year"] = pd.DataFrame(yr, columns=["yr", "n", "slope", "t"])
    # multivariate: ex3 on r7z, logvrel, z
    g = G3.dropna(subset=["vrel", "z"]).copy()
    X = np.column_stack([np.ones(len(g)), g["r7z"], np.log(g["vrel"]), g["z"]])
    y = g["ex3"].values
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b; s2 = e @ e / (len(y) - 4); se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["multi_ex3"] = pd.DataFrame({"b": b, "t": b / se}, index=["c", "r7z", "logvrel", "z"])
    # weekday by coin and by year halves
    A1 = A.dropna(subset=["ex1"])
    out["weekday_by_coin_mean"] = A1.pivot_table(index="wd", columns="coin", values="ex1", aggfunc="mean")
    A1 = A1.assign(half=np.where(A1["yr"] <= 2021, "18-21", "22-25"))
    wt = A1.groupby(["half", "wd"])["ex1"].agg(["size", "mean", "std"])
    wt["t"] = wt["mean"] / (wt["std"] / np.sqrt(wt["size"]))
    out["weekday_by_half"] = wt.drop(columns="std")
    # is the book long more after strong r7z? alloc mean by r7z quintile
    g = G3.copy(); g["b"] = pd.qcut(g["r7z"], 5, labels=False)
    out["alloc_by_r7z"] = g.groupby("b")["alloc"].mean()
    return out
