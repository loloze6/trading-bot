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
                "vol": vol,
            })
            for L in [5, 14, 21, 30]:
                d[f"r{L}z"] = (c / c.shift(L) - 1) / vol
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["fwd1"].transform("mean")
    D["ex1"] = D["fwd1"] - mu
    D["ex2"] = D["fwd2"] - 2 * mu

    def ct(v, dates):
        m = v.notna(); v, dates = v[m], dates[m]; n = len(v)
        if n < 10: return (np.nan, np.nan, n, 0)
        dev = (v - v.mean()).groupby(dates).sum(); G = len(dev)
        se = np.sqrt(G / (G - 1) * (dev ** 2).sum()) / n
        return (v.mean(), v.mean() / se, n, G)
    cols = ["mean", "t", "n", "dates"]
    out = {}
    # 14d and 30d lookback: grading of next 2 days, by start weekday (2-day grid differs; use each weekday as its own grid, weekly spaced)
    for name in ["r14z", "r30z"]:
        res = {}
        for wd in range(7):
            s = D[D.wd == wd]
            z = s[name].clip(-4, 4)
            a = ct(z * s["ex1"], s["date"]); b = ct(z * s["ex2"], s["date"])
            res[wd] = (a[0], a[1], b[0], b[1], a[3])
        out[f"{name} x next 1d / 2d excess by signal weekday"] = pd.DataFrame(res, index=["m1", "t1", "m2", "t2", "dates"]).T
    F = D[D.wd == 4].copy()
    # signed % move over weekend (2d) by sign of r14z, and |r14z| quartile
    q = F.dropna(subset=["r14z", "ex2", "ex1"]).copy()
    q["s1"] = np.sign(q["r14z"]) * q["ex1"]; q["s2"] = np.sign(q["r14z"]) * q["ex2"]
    q["s2tot"] = np.sign(q["r14z"]) * q["fwd2"]
    q["aq"] = pd.qcut(q["r14z"].abs(), 4, labels=False)
    res = {}
    for k, g in q.groupby("aq"):
        a = ct(g["s1"], g["date"]); b = ct(g["s2"], g["date"]); c2 = ct(g["s2tot"], g["date"])
        res[k] = (a[0], a[1], b[0], b[1], c2[0], a[2])
    a = ct(q["s1"], q["date"]); b = ct(q["s2"], q["date"]); c2 = ct(q["s2tot"], q["date"])
    res["all"] = (a[0], a[1], b[0], b[1], c2[0], a[2])
    out["Fri: signed Sat / Sat+Sun excess by |r14z| quartile"] = pd.DataFrame(res, index=["sat", "t_sat", "wkend", "t_wkend", "wkend_total", "n"]).T
    # stability by year and coin for r14z x weekend excess
    res = {}
    for y, g in F.groupby("year"):
        res[y] = ct(g["r14z"].clip(-4, 4) * g["ex2"], g["date"])
    out["by year: r14z x weekend excess"] = pd.DataFrame(res, index=cols).T
    res = {}
    for co, g in F.groupby("coin"):
        res[co] = ct(g["r14z"].clip(-4, 4) * g["ex2"], g["date"])
    out["by coin: r14z x weekend excess"] = pd.DataFrame(res, index=cols).T
    # vol tercile x r14z for weekend, and signed % in top vol tercile
    q = F.dropna(subset=["vol", "r14z", "ex2"]).copy()
    q["vq"] = pd.qcut(q["vol"] / q.groupby("coin")["vol"].transform("median"), 3, labels=False)
    res = {}
    for k, g in q.groupby("vq"):
        a = ct(g["r14z"].clip(-4, 4) * g["ex2"], g["date"]); b = ct(np.sign(g["r14z"]) * g["ex2"], g["date"])
        res[k] = (a[0], a[1], b[0], b[1], a[2])
    out["Fri vol tercile: r14z x weekend excess, and signed % weekend"] = pd.DataFrame(res, index=["m", "t", "signed%", "t_signed", "n"]).T
    # usual 2-day move
    out["usual 2d move (std of fwd2 on Fridays)"] = float(F["fwd2"].std())
    return out
