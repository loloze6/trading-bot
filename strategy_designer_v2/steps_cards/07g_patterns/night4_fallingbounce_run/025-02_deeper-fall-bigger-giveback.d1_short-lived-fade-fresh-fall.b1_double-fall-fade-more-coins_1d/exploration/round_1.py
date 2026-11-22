def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20, min_periods=10).std()
            z = r1 / sd
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "z": z, "r1": r1, "regime": b["regime"].values,
                               "fc": b["forecast"].astype(float).values,
                               "alloc": b["postRebalance_current_allocation"].astype(float).values,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
                               "year": pd.to_datetime(b["timestamp"]).dt.year.values,
                               "r5past": c / c.shift(5) - 1,
                               "volratio": sd / r1.rolling(60, min_periods=30).std()})
            for h in (1, 2, 5, 10):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # drift per coin per h on grid
    for h in (1, 2, 5, 10):
        g = A[A.pos % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"] = A[f"f{h}"] - A["coin"].map(dr)
    A["mr"] = A.regime == "mean_reversion"
    A["zb"] = pd.cut(A.z, [-np.inf, -3, -2, -1, 0, 1, 2, 3, np.inf])
    def tab(sub, h):
        g = sub[sub.pos % h == 0].dropna(subset=[f"x{h}", "z"])
        r = g.groupby(["mr", "zb"], observed=True)[f"x{h}"].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.drop(columns="std").round(4)
    out["x2 by regime and z bucket"] = tab(A, 2)
    out["x5 by regime and z bucket"] = tab(A, 5)
    out["x1 by regime and z bucket"] = tab(A, 1)
    # weekday, all bars, h=1
    g = A[A.pos % 1 == 0].dropna(subset=["x1"])
    r = g.groupby("wd")["x1"].agg(["mean", "count", "std"]); r["t"] = r["mean"]/(r["std"]/np.sqrt(r["count"]))
    out["x1 by weekday"] = r.drop(columns="std").round(4)
    # vol ratio buckets h=5
    g = A[A.pos % 5 == 0].dropna(subset=["x5", "volratio"])
    g["vb"] = pd.qcut(g.volratio, 5)
    r = g.groupby(["mr", "vb"], observed=True)["x5"].agg(["mean", "count", "std"]); r["t"] = r["mean"]/(r["std"]/np.sqrt(r["count"]))
    out["x5 by regime and vol ratio quintile"] = r.drop(columns="std").round(4)
    # past 5-day return buckets h=5
    g = A[A.pos % 5 == 0].dropna(subset=["x5", "r5past"])
    g["pb"] = pd.qcut(g.r5past, 5)
    r = g.groupby(["mr", "pb"], observed=True)["x5"].agg(["mean", "count", "std"]); r["t"] = r["mean"]/(r["std"]/np.sqrt(r["count"]))
    out["x5 by regime and past5 quintile"] = r.drop(columns="std").round(4)
    # book: share in position, gain by position sign
    A["pg"] = A["alloc"] * A["f1"]
    r = A.dropna(subset=["pg"]).groupby(np.sign(A["alloc"]).rename("side"))["pg"].agg(["mean", "count"])
    out["position gain per bar by side"] = r
    out["regime share of bars"] = A.groupby("year")["mr"].mean().round(3)
    return out
