def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd60 = r.rolling(60, min_periods=30).std()
            sd10 = r.rolling(10, min_periods=8).std()
            r5 = c / c.shift(5) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "z": r / sd60, "ratio": sd10 / sd60,
                "r5z": r5 / (sd60 * np.sqrt(5)),
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f5": c.shift(-5) / c - 1,
                "fc": b["forecast"].astype(float),
                "wd": ts.dt.weekday, "yr": ts.dt.year, "day": ts.dt.floor("D"),
                "wn": int(str(w)[1:]),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for h in [1, 2, 5]:
        m = A[A.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"] = A[f"f{h}"] - A["coin"].map(m)
    A["half"] = np.where(A.wn <= 12, "w1-w12", "w13-w24")

    def ctab(df, key, h):
        # day-clustered: sum deviations per (key, day), t over days
        g = df[df.pos % h == 0].dropna(subset=[f"x{h}"])
        if isinstance(key, list):
            pass
        res = []
        for k, gg in g.groupby(key):
            per_day = gg.groupby("day")[f"x{h}"].sum()
            n = len(gg); nd = len(per_day)
            mean = gg[f"x{h}"].mean()
            se = np.sqrt((per_day - per_day.size and 0) .pow(0).sum() * 0 + ((per_day - mean * gg.groupby("day").size()) ** 2).sum()) / n
            res.append({"key": str(k), "mean": mean, "cases": n, "days": nd, "t_clu": mean / se if se > 0 else np.nan})
        return pd.DataFrame(res).set_index("key")

    out["1d excess by weekday, day-clustered"] = ctab(A, "wd", 1)
    out["1d excess by weekday x half"] = ctab(A, ["half", "wd"], 1)
    out["1d excess by weekday x coin, Fri-Thu minus Mon-Wed"] = (
        A[A.wd.isin([3, 4])].groupby("coin")["x1"].mean() - A[A.wd.isin([0, 2])].groupby("coin")["x1"].mean())
    A["zq"] = pd.cut(A["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    out["1d excess by day z, clustered"] = ctab(A, "zq", 1)
    out["1d excess by day z x half"] = ctab(A, ["half", "zq"], 1)
    out["5d excess by day z, clustered"] = ctab(A, "zq", 5)
    A["r5q"] = pd.cut(A["r5z"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    out["2d excess by 5d return z, clustered"] = ctab(A, "r5q", 2)
    out["2d excess by 5d z x half"] = ctab(A[A.r5z > 0.5], ["half", "r5q"], 2)
    A["rq"] = pd.qcut(A["ratio"], 4, labels=["lowvol", "q2", "q3", "hivol"])
    out["2d excess, 5d z>0.5, by volratio"] = ctab(A[A.r5z > 0.5], "rq", 2)
    out["2d excess, z<-1, by volratio, clustered"] = ctab(A[A.z < -1], "rq", 2)
    out["2d excess, z<-1 hivol, by half"] = ctab(A[(A.z < -1) & (A.rq == "hivol")], "half", 2)
    A["fcq"] = pd.cut(A["fc"], [-1, 0, 15, 21])
    out["2d excess by forecast, clustered"] = ctab(A, "fcq", 2)
    return out
