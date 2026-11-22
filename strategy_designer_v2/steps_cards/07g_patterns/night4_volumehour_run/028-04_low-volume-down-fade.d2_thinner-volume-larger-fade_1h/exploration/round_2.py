import numpy as np, pandas as pd
from scipy import stats

def tstat(x):
    x = pd.Series(x).dropna()
    if len(x) < 3: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def build(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            s = r.rolling(720, min_periods=120).std()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]), "s": s,
                               "r6p": c / c.shift(6) - 1, "r24p": c / c.shift(24) - 1,
                               "r72p": c / c.shift(72) - 1,
                               "f6": c.shift(-6) / c - 1, "f24": c.shift(-24) / c - 1,
                               "f1": c.shift(-1) / c - 1,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "yr": ts.dt.year})
            df["i"] = np.arange(len(df))
            rows.append(df)
    return pd.concat(rows, ignore_index=True)

def slope(x, y):
    m = pd.concat([x, y], axis=1).dropna()
    if len(m) < 30: return (np.nan, np.nan, len(m))
    lr = stats.linregress(m.iloc[:, 0], m.iloc[:, 1])
    return (lr.slope, lr.slope / lr.stderr, len(m))

def explore(data):
    A = build(data)
    out = {}
    # 6h momentum by vol tercile, graded slope, per coin and per window half
    g = A[A["i"] % 6 == 0].copy()
    g["u"] = g["f6"] - g.groupby("coin")["f6"].transform("mean")
    g["r6z"] = g["r6p"] / (g["s"] * np.sqrt(6))
    g["sb"] = g.groupby("coin")["s"].transform(lambda x: pd.qcut(x, 3, labels=False))
    g["half"] = np.where(g["wn"] <= 12, "early", "late")
    rr = []
    for (coin, half, sb), q in g.groupby(["coin", "half", "sb"]):
        sl, t, n = slope(q["r6z"], q["u"])
        rr.append({"coin": coin, "half": half, "volT": sb, "slope": sl, "t": t, "n": n})
    out["6h u on past-6h z: slope by coin/half/vol tercile"] = pd.DataFrame(rr)
    # 24h reversal graded, per coin and half, with 24h and 72h pasts
    h = A[A["i"] % 24 == 0].copy()
    h["u"] = h["f24"] - h.groupby("coin")["f24"].transform("mean")
    h["r24z"] = h["r24p"] / (h["s"] * np.sqrt(24))
    h["r72z"] = h["r72p"] / (h["s"] * np.sqrt(72))
    h["half"] = np.where(h["wn"] <= 12, "early", "late")
    rr = []
    for key, q in list(h.groupby(["coin", "half"])) + [(("all", "all"), h)]:
        for var in ["r24z", "r72z"]:
            sl, t, n = slope(q[var], q["u"])
            neg = q[q[var] < -2]["u"]
            rr.append({"coin": key[0], "half": key[1], "var": var, "slope": sl, "t": t, "n": n,
                       "u_after_z<-2": neg.mean(), "n_neg": len(neg), "t_neg": tstat(neg)})
    out["24h u on past 24h/72h z"] = pd.DataFrame(rr)
    # hour 20-21 UTC and Thursday effects: per coin, per year
    o = A.copy()
    o["u"] = o["f1"] - o.groupby("coin")["f1"].transform("mean")
    o["h2021"] = o["hour"].isin([20, 21])
    hh = o[o["h2021"]].groupby(["coin", "yr"])["u"].agg(["mean", "count", tstat])
    out["hours 20-21 UTC 1h u by coin/year"] = hh
    th = o[o["wd"] == 3].groupby(["coin", "yr"])["u"].agg(["mean", "count", tstat])
    out["Thursday 1h u by coin/year"] = th
    # Thursday by hour band pooled
    out["Thursday 1h u by 4h block"] = o[o["wd"] == 3].assign(blk=o["hour"] // 4).groupby("blk")["u"].agg(["mean", "count", tstat])
    return out
