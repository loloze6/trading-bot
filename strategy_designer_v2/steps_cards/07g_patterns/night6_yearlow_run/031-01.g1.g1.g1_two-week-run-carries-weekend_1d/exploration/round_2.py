import pandas as pd, numpy as np

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "wd": ts.dt.weekday, "year": ts.dt.year, "sd20": sd20,
                               "z1": r1 / sd20})
            for L in [3, 7, 14, 28]:
                df["z%d" % L] = (c / c.shift(L) - 1) / (sd20 * np.sqrt(L))
            for h in [1, 2, 3]:
                df["f%d" % h] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in [1, 2, 3]:
        g = d[d["i"] % h == 0]
        d["u%d" % h] = d["f%d" % h] - d["coin"].map(g.groupby("coin")["f%d" % h].mean())
    out = {}
    # 1. z14 x next-day unusual move by weekday (which single day carries momentum)
    res = []
    for k in range(7):
        s = d[d.wd == k].dropna(subset=["z14", "u1"])
        p = s["z14"].clip(-3, 3) * s["u1"]
        res.append({"wd": k, "mean": p.mean(), "t_day": _t(p.groupby(s["day"]).sum()),
                    "corr": s["z14"].corr(s["u1"]), "days": s["day"].nunique()})
    out["z14 x next-day unusual by weekday of bar"] = pd.DataFrame(res).set_index("wd")
    # 2. lookback comparison on Thursday (2-day) and Friday (2-day)
    res = []
    for k in [3, 4]:
        for L in [3, 7, 14, 28]:
            s = d[d.wd == k].dropna(subset=["z%d" % L, "u2"])
            p = s["z%d" % L].clip(-3, 3) * s["u2"]
            res.append({"wd": k, "L": L, "mean": p.mean(), "t_day": _t(p.groupby(s["day"]).sum()),
                        "corr": s["z%d" % L].corr(s["u2"])})
    out["lookback x 2-day unusual, Thu and Fri"] = pd.DataFrame(res)
    # 3. Thursday 3-day (Fri+Sat+Sun) graded quintiles
    th = d[d.wd == 3].dropna(subset=["z14", "u3"]).copy()
    th["q"] = pd.qcut(th["z14"], 5, labels=False)
    g = th.groupby("q").agg(z=("z14", "mean"), u3=("u3", "mean"), n=("u3", "size"))
    p = th["z14"].clip(-3, 3) * th["u3"]
    out["thursday z14 quintile -> unusual 3-day move"] = g
    out["thursday z14 x u3 mean, t_day"] = pd.Series({"mean": p.mean(), "t": _t(p.groupby(th["day"]).sum()),
                                                     "days": th["day"].nunique()})
    # 4. z14 x u1 on weekdays Mon-Wed pooled vs Thu-Fri pooled
    s = d.dropna(subset=["z14", "u1"]).copy()
    s["grp"] = np.where(s.wd.isin([3, 4]), "thu_fri", np.where(s.wd.isin([5, 6]), "sat_sun", "mon_wed"))
    s["p"] = s["z14"].clip(-3, 3) * s["u1"]
    out["z14 x next-day by weekday group"] = pd.DataFrame({g: {"mean": x["p"].mean(), "t_day": _t(x.groupby("day")["p"].sum())}
                                                          for g, x in s.groupby("grp")}).T
    # 5. one-day reversal: z1 x u1 with t, all days and by vol tercile
    s = d.dropna(subset=["z1", "u1"]).copy()
    s["p"] = -s["z1"].clip(-4, 4) * s["u1"]
    s["vq"] = s.groupby("coin")["sd20"].transform(lambda x: pd.qcut(x, 3, labels=False))
    r = s.groupby("vq").apply(lambda x: pd.Series({"mean": x["p"].mean(), "t_day": _t(x.groupby("day")["p"].sum())}))
    r.loc["all"] = [s["p"].mean(), _t(s.groupby("day")["p"].sum())]
    out["reversal -z1 x next-day unusual, by vol tercile"] = r
    s["q"] = pd.qcut(s["z1"], 10, labels=False)
    out["z1 decile -> next-day unusual"] = s.groupby("q").agg(z=("z1", "mean"), u1=("u1", "mean"), n=("u1", "size"))
    return out
