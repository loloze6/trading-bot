import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]; lo = b["low"]
            r1 = c.pct_change()
            r24 = c / c.shift(6) - 1
            rng = (hi.rolling(6).max() - lo.rolling(6).min()) / c
            rm = rng / rng.rolling(180, min_periods=60).mean()
            vol = r1.rolling(180, min_periods=60).std()
            r7d = c / c.shift(42) - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "r24z": r24 / (vol * np.sqrt(6)), "rm": rm,
                               "r7dz": r7d / (vol * np.sqrt(42)),
                               "r4z": r1 / vol,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "yr": ts.dt.year})
            df["f1"] = c.shift(-1) / c - 1
            df["f6"] = c.shift(-6) / c - 1
            df["f6b"] = c.shift(-12) / c.shift(-6) - 1
            df["f42"] = c.shift(-42) / c - 1
            df["p6"] = r24
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for col, h in [("f1", 1), ("f6", 6), ("f6b", 6), ("f42", 42)]:
        d = A[A.pos % h == 0].groupby("coin")[col].mean()
        A["x" + col] = A[col] - A.coin.map(d)

    def summ(s, col, by):
        s = s.dropna(subset=[col])
        gg = s.groupby(by)[col]
        out = pd.DataFrame({"mean%": gg.mean() * 100, "n": gg.count()})
        out["t"] = gg.mean() / (gg.std() / np.sqrt(gg.count()))
        return out.round(3)

    res = {}
    g1 = A[A.pos % 1 == 0]
    A["h16"] = np.where(A.hour == 16, "h16", np.where(A.hour == 20, "h20", "other"))
    res["hour16/20 by year"] = summ(A[A.h16 != "other"], "xf1", ["h16", "yr"])
    res["hour16/20 by coin"] = summ(A[A.h16 != "other"], "xf1", ["h16", "coin"])
    # does the bar 16-20 return predict 20-24? (graded by size of the 16h bar move)
    s20 = A[A.hour == 20].copy()
    s20["q"] = pd.qcut(s20.r4z, 5, labels=False, duplicates="drop")
    res["hour20 bar: own 4h move quintile -> next 4h"] = summ(s20, "xf1", "q")
    res["friday by year"] = summ(A[A.wd == 4], "xf1", "yr")
    # panic: falls with top range quintile; second day split by first-day outcome
    g6 = A[A.pos % 6 == 0].copy()
    g6["rmq"] = pd.qcut(g6.rm, 5, labels=False, duplicates="drop")
    pan = g6[(g6.r24z < 0) & (g6.rmq == 4)].copy()
    pan["fallq"] = pd.qcut(pan.r24z, 4, labels=False, duplicates="drop")
    res["panic (fall, top range q): fall quartile -> 24h"] = summ(pan, "xf6", "fallq")
    res["panic: fall quartile -> 24h by year"] = summ(pan, "xf6", "yr")
    pan["day1"] = np.where(pan.f6 > 0, "day1 up", "day1 down")
    res["panic: next-day (24-48h) by day1 outcome"] = summ(pan, "xf6b", "day1")
    # non-panic: big rise with top range -> next 24h graded
    up = g6[(g6.r24z > 0) & (g6.rmq == 4)].copy()
    up["q"] = pd.qcut(up.r24z, 4, labels=False, duplicates="drop")
    res["wide rise: rise quartile -> 24h"] = summ(up, "xf6", "q")
    # 7d momentum robustness by year
    g42 = A[A.pos % 42 == 0].copy()
    g42["q"] = pd.qcut(g42.r7dz, 5, labels=False, duplicates="drop")
    g42["side"] = np.where(g42.q == 4, "top", np.where(g42.q == 0, "bottom", "mid"))
    res["7d mom top/bottom by year"] = summ(g42[g42.side != "mid"], "xf42", ["side", "yr"])
    g6["q7"] = pd.qcut(g6.r7dz, 5, labels=False, duplicates="drop")
    res["7d mom quintile -> 24h by coin top"] = summ(g6[g6.q7 == 4], "xf6", "coin")
    return res
