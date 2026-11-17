def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=10).std()
            v = b["volume"].astype(float)
            df = pd.DataFrame({
                "coin": coin, "win": w, "yr": ts.dt.year.values, "wd": ts.dt.weekday.values,
                "i": np.arange(len(b)),
                "r": r.values, "z": (r / sd).values,
                "f1": (c.shift(-1) / c - 1).values,
                "f2": (c.shift(-2) / c - 1).values,
                "f5": (c.shift(-5) / c - 1).values,
                "rv": (v / v.rolling(20, min_periods=10).median()).values,
                "vol": sd.values,
                "z5": ((c / c.shift(5) - 1) / (sd * np.sqrt(5))).values,
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["vq"] = D.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out = {}
    def reg(s, x, y):
        s = s.dropna(subset=[x, y])
        if len(s) < 30: return (np.nan, np.nan, len(s))
        lr = stats.linregress(s[x], s[y]); return (lr.slope, lr.slope / lr.stderr, len(s))
    # high-vol reversal by coin
    res = []
    for coin, s in D.groupby("coin"):
        for q in [0, 2]:
            sl, t, n = reg(s[s.vq == q], "z", "f1")
            res.append({"coin": coin, "vq": q, "slope": sl, "t": t, "n": n})
    out["f1 on z by coin, low(0)/high(2) vol tercile"] = pd.DataFrame(res).pivot(index="coin", columns="vq", values="t")
    res = []
    for yr, s in D.groupby("yr"):
        sl, t, n = reg(s[s.vq == 2], "z", "f1"); sl0, t0, n0 = reg(s[s.vq == 0], "z", "f1")
        res.append({"yr": yr, "t_high": t, "n_high": n, "t_low": t0, "n_low": n0})
    out["f1 on z by year, high/low vol"] = pd.DataFrame(res)
    # sign split in high vol
    s = D[D.vq == 2].dropna(subset=["z", "f1"])
    res = []
    for nm, ss in [("falls", s[s.z < 0]), ("rises", s[s.z > 0])]:
        sl, t, n = reg(ss, "z", "f1"); res.append({"side": nm, "slope": sl, "t": t, "n": n, "mean_f1": ss.f1.mean()})
    out["high vol reversal by sign"] = pd.DataFrame(res)
    # vol as continuous: interaction z*vol_rank
    s = D.dropna(subset=["z", "f1", "vol"]).copy()
    s["vr"] = s.groupby("coin")["vol"].rank(pct=True)
    s["zx"] = s["z"] * s["vr"]
    X = np.column_stack([np.ones(len(s)), s.z, s.vr, s.zx]); y = s.f1.values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None); e = y - X @ beta
    cov = np.linalg.inv(X.T @ X) * (e @ e) / (len(y) - 4)
    out["f1 ~ z + volrank + z*volrank (t)"] = pd.Series(beta / np.sqrt(np.diag(cov)), index=["c", "z", "vr", "z_x_vr"])
    # relvol effect on f1 split by sign of r
    res = []
    for nm, ss in [("down day", D[D.r < 0]), ("up day", D[D.r > 0])]:
        ss = ss.dropna(subset=["rv", "f1"]).copy(); ss["lrv"] = np.log(ss.rv)
        sl, t, n = reg(ss, "lrv", "f1"); res.append({"side": nm, "slope": sl, "t": t, "n": n})
    out["f1 on log relvol by sign of day"] = pd.DataFrame(res)
    # relvol by year
    res = []
    for yr, ss in D.dropna(subset=["rv", "f1"]).groupby("yr"):
        ss = ss.copy(); ss["lrv"] = np.log(ss.rv); sl, t, n = reg(ss, "lrv", "f1"); res.append({"yr": yr, "t": t, "n": n})
    out["f1 on log relvol by year"] = pd.DataFrame(res)
    # Sunday reversal by sign
    s = D[D.wd == 6]
    res = []
    for nm, ss in [("sun falls", s[s.z < 0]), ("sun rises", s[s.z > 0])]:
        for h in ["f1", "f2"]:
            sl, t, n = reg(ss, "z", h); res.append({"side": nm, "h": h, "slope": sl, "t": t, "n": n})
    out["Sunday slope by sign"] = pd.DataFrame(res)
    # 5d momentum on non-overlapping grid i%5==0
    s = D[(D.i % 5) == 0]
    res = []
    for q in [0, 1, 2]:
        sl, t, n = reg(s[s.vq == q], "z5", "f5"); res.append({"vq": q, "slope": sl, "t": t, "n": n})
    sl, t, n = reg(s, "z5", "f5"); res.append({"vq": "all", "slope": sl, "t": t, "n": n})
    out["5d on 5d z, grid, by vol tercile"] = pd.DataFrame(res)
    res = []
    for coin, ss in s.groupby("coin"):
        sl, t, n = reg(ss, "z5", "f5"); res.append({"coin": coin, "t": t, "n": n})
    out["5d momentum by coin"] = pd.DataFrame(res)
    return out
