import pandas as pd, numpy as np

def tstat(x):
    x = pd.Series(x).dropna()
    if len(x) < 3: return np.nan
    return x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "wd": ts.dt.weekday, "year": ts.dt.year,
                "r": r, "z": r/vol,
                "f1": c.shift(-1)/c-1, "f2": c.shift(-2)/c-1,
                "r5": c/c.shift(5)-1, "z5": (c/c.shift(5)-1)/(vol*np.sqrt(5)),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    m1 = D.groupby("coin")["f1"].mean()
    m2 = D[D["pos"] % 2 == 0].groupby("coin")["f2"].mean()
    D["f1x"] = D["f1"] - D["coin"].map(m1)
    D["f2x"] = D["f2"] - D["coin"].map(m2)
    D["rev2"] = -np.sign(D["z"]) * D["f2x"]
    D["rev1"] = -np.sign(D["z"]) * D["f1x"]
    out = {}
    S = D[D["wd"] == 6].dropna(subset=["z", "f2x"]).copy()
    S["side"] = np.where(S["z"] > 0, "up", "down")
    out["sun_by_side"] = S.groupby("side")["f2x"].agg(["mean", "count", tstat])
    S["zq"] = pd.qcut(S["z"], 5, labels=False)
    out["sun_f2x_by_zq"] = S.groupby("zq").agg(zmean=("z", "mean"), f2x=("f2x", "mean"), n=("f2x", "count"), t=("f2x", tstat))
    out["sun_rev2_by_year"] = S.groupby("year")["rev2"].agg(["mean", "count", tstat])
    out["sun_rev2_by_coin"] = S.groupby("coin")["rev2"].agg(["mean", "count", tstat])
    # low z next-day reversal excluding sundays
    A = D[D["wd"] != 6].dropna(subset=["z", "f1x"]).copy()
    A["zq"] = pd.qcut(A["z"], 5, labels=False)
    out["nonsun_f1x_by_zq"] = A.groupby("zq").agg(zmean=("z", "mean"), f1x=("f1x", "mean"), n=("f1x", "count"), t=("f1x", tstat))
    lo = A[A["zq"] == 0]
    out["nonsun_lowz_by_year"] = lo.groupby("year")["f1x"].agg(["mean", "count", tstat])
    out["nonsun_lowz_by_coin"] = lo.groupby("coin")["f1x"].agg(["mean", "count", tstat])
    # Saturday-bar (bar starting Friday, f1) effect by year and coin
    F = D[D["wd"] == 4].dropna(subset=["f1x"])
    out["fri_bar_next_by_year"] = F.groupby("year")["f1x"].agg(["mean", "count", tstat])
    out["fri_bar_next_by_coin"] = F.groupby("coin")["f1x"].agg(["mean", "count", tstat])
    # 5-day momentum, z-scaled, quintiles, grid 2
    Q = D[D["pos"] % 2 == 0].dropna(subset=["z5", "f2x"]).copy()
    Q["q"] = pd.qcut(Q["z5"], 5, labels=False)
    out["f2x_by_z5_q"] = Q.groupby("q").agg(z5=("z5", "mean"), f2x=("f2x", "mean"), n=("f2x", "count"), t=("f2x", tstat))
    top = Q[Q["q"] == 4]
    out["z5top_by_year"] = top.groupby("year")["f2x"].agg(["mean", "count", tstat])
    return out
