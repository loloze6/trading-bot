def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "wd": ts.dt.weekday,
                "year": ts.dt.year,
                "day": ts.dt.floor("D"),
                "r1": c.pct_change(),
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "vol20": c.pct_change().rolling(20).std(),
                "lowdist20": c / c.rolling(20).min() - 1,
                "highdist20": c / c.rolling(20).max() - 1,
                "fwd1": c.shift(-1) / c - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["fwd1"].transform("mean")
    d["ex1"] = d["fwd1"] - drift
    d["nextwd"] = (d["wd"] + 1) % 7
    out = {}

    def daytt(sub, col="ex1"):
        s = sub.dropna(subset=[col])
        g = s.groupby("day")[col].sum()
        n = len(s); D = len(g)
        if D < 3: return (np.nan, np.nan, D)
        m = s[col].mean()
        dev = s[col] - m
        gs = dev.groupby(s["day"]).sum()
        se = np.sqrt((gs**2).sum() * D / (D - 1)) / n
        return (m, m / se, D)

    # 1 mean excess return of the next day by weekday of next day
    r = []
    for wd, sub in d.groupby("nextwd"):
        m, t, D = daytt(sub)
        r.append((wd, m, t, D))
    out["next-day excess by next weekday (0=Mon)"] = pd.DataFrame(r, columns=["nextwd", "mean", "t", "days"])

    # 2 slope of next-day excess on z(r5) by next weekday
    d["z5"] = d["r5"] / (d["vol20"] * np.sqrt(5))
    r = []
    for wd, sub in d.groupby("nextwd"):
        s = sub.dropna(subset=["z5", "ex1"])
        s = s.assign(x=s["z5"] * s["ex1"])
        m, t, D = daytt(s, "x")
        corr = s["z5"].corr(s["ex1"])
        r.append((wd, m, t, corr, D))
    out["z5 x next excess by next weekday"] = pd.DataFrame(r, columns=["nextwd", "mean_prod", "t", "corr", "days"])

    # 3 terciles of r5 on Friday bars (next Sat) vs other days
    r = []
    for lab, sub in [("into Sat", d[d.nextwd == 5]), ("into Sun", d[d.nextwd == 6]), ("weekdays", d[d.nextwd.isin([0,1,2,3,4])])]:
        s = sub.dropna(subset=["z5", "ex1"]).copy()
        s["q"] = pd.qcut(s["z5"], 5, labels=False)
        for q, ss in s.groupby("q"):
            m, t, D = daytt(ss)
            r.append((lab, q, m, t, len(ss)))
    out["next excess by z5 quintile"] = pd.DataFrame(r, columns=["grp", "q", "mean", "t", "n"])

    # 4 after large daily moves (|z1|), by sign
    d["z1"] = d["r1"] / d["vol20"]
    s = d.dropna(subset=["z1", "ex1"]).copy()
    s["b"] = pd.cut(s["z1"], [-99, -2, -1, 0, 1, 2, 99])
    r = []
    for q, ss in s.groupby("b", observed=True):
        m, t, D = daytt(ss); r.append((str(q), m, t, len(ss)))
    out["next excess by today's z1"] = pd.DataFrame(r, columns=["bin", "mean", "t", "n"])

    # 5 position in 20-day range
    s = d.dropna(subset=["lowdist20", "highdist20", "ex1"]).copy()
    s["pos"] = s["lowdist20"] / (s["lowdist20"] - s["highdist20"]).replace(0, np.nan)
    s["q"] = pd.qcut(s["pos"], 5, labels=False, duplicates="drop")
    r = []
    for q, ss in s.groupby("q"):
        m, t, D = daytt(ss); r.append((q, m, t, len(ss)))
    out["next excess by pos in 20d range"] = pd.DataFrame(r, columns=["q", "mean", "t", "n"])

    # 6 volatility tercile
    s = d.dropna(subset=["vol20", "ex1"]).copy()
    s["q"] = s.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False))
    r = []
    for q, ss in s.groupby("q"):
        m, t, D = daytt(ss); a = daytt(ss[ss.nextwd == 5])
        r.append((q, m, t, a[0], a[1], len(ss)))
    out["by vol tercile: all / into Sat"] = pd.DataFrame(r, columns=["q", "mean", "t", "satmean", "satt", "n"])

    # 7 Saturday signal by year and by coin
    sat = d[(d.nextwd == 5) & (d.fc > 0)]
    r = []
    for y, ss in sat.groupby("year"):
        m, t, D = daytt(ss); r.append((y, m, t, len(ss)))
    out["Sat cases by year"] = pd.DataFrame(r, columns=["year", "mean", "t", "n"])
    r = []
    for cn, ss in sat.groupby("coin"):
        m, t, D = daytt(ss); r.append((cn, m, t, len(ss)))
    out["Sat cases by coin"] = pd.DataFrame(r, columns=["coin", "mean", "t", "n"])

    # 8 20-day momentum next-day by weekday
    d["z20"] = d["r20"] / (d["vol20"] * np.sqrt(20))
    r = []
    for wd, sub in d.groupby("nextwd"):
        s = sub.dropna(subset=["z20", "ex1"]); s = s.assign(x=s["z20"] * s["ex1"])
        m, t, D = daytt(s, "x"); r.append((wd, m, t))
    out["z20 x next excess by next weekday"] = pd.DataFrame(r, columns=["nextwd", "mean_prod", "t"])
    return out
