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
            df = pd.DataFrame({
                "coin": coin, "win": w, "wd": ts.dt.weekday.values,
                "r": r.values, "z": (r / sd).values,
                "f1": (c.shift(-1) / c - 1).values,
                "f2": (c.shift(-2) / c - 1).values,
                "f3": (c.shift(-3) / c - 1).values,
                "f5": (c.shift(-5) / c - 1).values,
                "rv": (b["volume"].astype(float) / b["volume"].astype(float).rolling(20, min_periods=10).median()).values,
                "vol": sd.values,
                "r5": (c / c.shift(5) - 1).values,
                "z5": ((c / c.shift(5) - 1) / (sd * np.sqrt(5))).values,
                "pos": b["postRebalance_current_allocation"].astype(float).values,
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    # weekday mean next-day return
    g = D.dropna(subset=["f1"]).groupby("wd")["f1"]
    out["next-day ret by weekday of signal bar (0=Mon)"] = pd.DataFrame({"mean": g.mean(), "n": g.count(), "t": g.mean() / (g.std() / np.sqrt(g.count()))})
    # slope of f1 on z by weekday, and f2
    res = []
    for wd in range(7):
        for h in ["f1", "f2", "f3", "f5"]:
            s = D[(D.wd == wd)].dropna(subset=["z", h])
            lr = stats.linregress(s["z"], s[h])
            res.append({"wd": wd, "h": h, "slope": lr.slope, "t": lr.slope / lr.stderr, "n": len(s)})
    out["slope fwd ret on own vol-scaled 1d ret, by weekday"] = pd.DataFrame(res).pivot(index="wd", columns="h", values="t")
    # 5-day momentum vs next 5 days (grid on weekday==0 => non-overlap)
    res = []
    for wd in range(7):
        s = D[D.wd == wd].dropna(subset=["z5", "f5"])
        lr = stats.linregress(s["z5"], s["f5"])
        s2 = s.dropna(subset=["f2"]); lr2 = stats.linregress(s2["z5"], s2["f2"])
        res.append({"wd": wd, "t_f5_on_z5": lr.slope / lr.stderr, "t_f2_on_z5": lr2.slope / lr2.stderr, "n": len(s)})
    out["slope on 5d vol-scaled return"] = pd.DataFrame(res)
    # Sunday: z x relvol interaction on f2
    s = D[D.wd == 6].dropna(subset=["z", "rv", "f2"]).copy()
    s["rvq"] = pd.qcut(s["rv"], 3, labels=["lowvol", "mid", "high"])
    res = []
    for q, ss in s.groupby("rvq"):
        lr = stats.linregress(ss["z"], ss["f2"])
        res.append({"rvq": q, "slope": lr.slope, "t": lr.slope / lr.stderr, "n": len(ss)})
    out["Sunday f2 on z by Sunday relative volume tercile"] = pd.DataFrame(res)
    # all-days: next-day on z by vol tercile (every bar non-overlapping for h=1)
    s = D.dropna(subset=["z", "f1", "vol"]).copy()
    s["vq"] = s.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    res = []
    for q, ss in s.groupby("vq"):
        lr = stats.linregress(ss["z"], ss["f1"])
        res.append({"volq": q, "slope": lr.slope, "t": lr.slope / lr.stderr, "mean_f1": ss.f1.mean(), "n": len(ss)})
    out["f1 on z by vol tercile (all days)"] = pd.DataFrame(res)
    # f1 on relvol all days
    s = D.dropna(subset=["rv", "f1"])
    lr = stats.linregress(np.log(s["rv"]), s["f1"])
    out["f1 on log relvol all days t"] = lr.slope / lr.stderr
    # per coin weekday means of daily return r
    out["mean daily ret by coin x weekday of bar (x1e4)"] = (D.dropna(subset=["r"]).groupby(["coin", "wd"])["r"].mean().unstack() * 1e4).round(1)
    # extreme moves: f1 after top/bottom 10% z by sign
    s = D.dropna(subset=["z", "f1", "f2"]).copy()
    s["zb"] = pd.cut(s["z"], [-99, -2, -1, 0, 1, 2, 99])
    g = s.groupby("zb")
    out["f1/f2 by z bucket (all days)"] = pd.DataFrame({"f1": g.f1.mean(), "t1": g.f1.mean() / (g.f1.std() / np.sqrt(g.f1.count())), "f2": g.f2.mean(), "n": g.f1.count()})
    # book daily return by weekday
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["wd"] = pd.to_datetime(x["day"]).dt.weekday; dd.append(x)
    DD = pd.concat(dd)
    g = DD.dropna(subset=["book_return"]).groupby("wd")["book_return"]
    out["book ret by weekday"] = pd.DataFrame({"mean": g.mean(), "n": g.count(), "share_nonzero": g.apply(lambda x: (x != 0).mean())})
    return out
