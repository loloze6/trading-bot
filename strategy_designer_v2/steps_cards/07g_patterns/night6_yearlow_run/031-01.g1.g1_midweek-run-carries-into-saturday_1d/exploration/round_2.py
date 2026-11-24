import pandas as pd, numpy as np

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
                "coin": coin, "win": w, "date": ts.dt.normalize(), "year": ts.dt.year,
                "wd": ts.dt.weekday,
                "fwd1": c.shift(-1) / c - 1,
                "fwd2": c.shift(-2) / c - 1,
                "r1z": r / vol,
                "r3lag1z": (c.shift(1) / c.shift(4) - 1) / vol.shift(1),
                "r5z": (c / c.shift(5) - 1) / vol,
                "r7z": (c / c.shift(7) - 1) / vol,
                "r14z": (c / c.shift(14) - 1) / vol,
                "vol": vol,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["ex1"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    D["ex2"] = D["fwd2"] - D.groupby("coin")["fwd1"].transform("mean") * 2

    def ct(v, dates):
        m = v.notna(); v, dates = v[m], dates[m]; n = len(v)
        if n < 10: return (np.nan, np.nan, n, 0)
        dev = (v - v.mean()).groupby(dates).sum(); G = len(dev)
        se = np.sqrt(G / (G - 1) * (dev ** 2).sum()) / n
        return (v.mean(), v.mean() / se, n, G)
    cols = ["mean", "t", "n", "dates"]
    out = {}
    F = D[D.wd == 4].copy()  # Friday bars -> Saturday
    # grading by lookback for Saturday (1d) and Sat+Sun (2d grid: Fridays only, non-overlapping weekly)
    res = {}
    for name in ["r1z", "r3lag1z", "r5z", "r7z", "r14z"]:
        z = F[name].clip(-4, 4)
        a = ct(z * F["ex1"], F["date"]); b = ct(z * F["ex2"], F["date"])
        res[name] = (a[0], a[1], b[0], b[1], a[3])
    out["Friday signal x Sat excess (1d) and Sat+Sun excess (2d)"] = pd.DataFrame(res, index=["m1d", "t1d", "m2d", "t2d", "dates"]).T
    # quintiles of r5z on Fridays: Saturday excess
    q = F.dropna(subset=["r5z", "ex1"]).copy()
    q["qq"] = pd.qcut(q["r5z"], 5, labels=False)
    res = {k: ct(g["ex1"], g["date"]) for k, g in q.groupby("qq")}
    out["Saturday excess by Friday 5d-z quintile"] = pd.DataFrame(res, index=cols).T
    # stability: by year and by coin for r5z and r3lag1z
    res = {}
    for y, g in F.groupby("year"):
        a = ct(g["r5z"].clip(-4, 4) * g["ex1"], g["date"]); b = ct(g["r3lag1z"].clip(-4, 4) * g["ex1"], g["date"])
        res[y] = (a[0], a[1], b[0], b[1], a[3])
    out["by year: r5z / r3lag1z x Sat excess"] = pd.DataFrame(res, index=["m5", "t5", "m3l", "t3l", "dates"]).T
    res = {}
    for co, g in F.groupby("coin"):
        a = ct(g["r5z"].clip(-4, 4) * g["ex1"], g["date"]); b = ct(g["r3lag1z"].clip(-4, 4) * g["ex1"], g["date"])
        res[co] = (a[0], a[1], b[0], b[1], a[2])
    out["by coin: r5z / r3lag1z x Sat excess"] = pd.DataFrame(res, index=["m5", "t5", "m3l", "t3l", "n"]).T
    # vol regime on Fridays
    q = F.dropna(subset=["vol", "r5z", "ex1"]).copy()
    q["vr"] = q["vol"] / q.groupby("coin")["vol"].transform("median")
    q["vq"] = pd.qcut(q["vr"], 3, labels=False)
    res = {k: ct(g["r5z"].clip(-4, 4) * g["ex1"], g["date"]) for k, g in q.groupby("vq")}
    out["r5z x Sat excess by vol tercile"] = pd.DataFrame(res, index=cols).T
    # Saturday excess in % for |r5z| buckets, signed by direction
    q = F.dropna(subset=["r5z", "ex1"]).copy()
    q["s"] = np.sign(q["r5z"]) * q["ex1"]
    q["aq"] = pd.qcut(q["r5z"].abs(), 4, labels=False)
    res = {k: ct(g["s"], g["date"]) for k, g in q.groupby("aq")}
    out["signed Sat excess by |r5z| quartile"] = pd.DataFrame(res, index=cols).T
    # big down day reversal: next-day excess after bottom-decile r1z, by weekday of signal
    q = D.dropna(subset=["r1z", "ex1"]).copy()
    thr = q["r1z"].quantile(0.1)
    g = q[q.r1z <= thr]
    res = {k: ct(gg["ex1"], gg["date"]) for k, gg in g.groupby("wd")}
    res["all"] = ct(g["ex1"], g["date"])
    out["next excess after bottom-decile day, by signal weekday"] = pd.DataFrame(res, index=cols).T
    return out
