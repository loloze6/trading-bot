import numpy as np, pandas as pd
from scipy import stats

def tstat(x):
    x = pd.Series(x).dropna()
    if len(x) < 3: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); vol = b["volume"].astype(float)
            r = c.pct_change()
            s = r.rolling(720, min_periods=120).std()
            v = vol / vol.rolling(720, min_periods=120).mean()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "z": r / s, "v": v, "s": s,
                               "r1": r, "r6p": c / c.shift(6) - 1, "r24p": c / c.shift(24) - 1,
                               "f6": c.shift(-6) / c - 1, "f24": c.shift(-24) / c - 1,
                               "f1": c.shift(-1) / c - 1,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "fc": b["forecast"], "pos": b["postRebalance_current_allocation"]})
            df["i"] = np.arange(len(df))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    res = {}
    for h, col in [(6, "f6"), (24, "f24"), (1, "f1")]:
        g = A[A["i"] % h == 0].copy()
        drift = g.groupby("coin")[col].transform("mean")
        g["u"] = g[col] - drift
        res[h] = g
    g6 = res[6].dropna(subset=["z", "v", "u"]).copy()
    g6["zb"] = pd.cut(g6["z"], [-np.inf, -4, -2.5, -1.5, 1.5, 2.5, 4, np.inf])
    g6["vb"] = pd.qcut(g6["v"], 3, labels=["thin", "mid", "heavy"])
    t = g6.groupby(["zb", "vb"], observed=True)["u"].agg(["mean", "count", tstat])
    out["6h unusual move by hour z x volume tercile"] = t
    # graded: momentum of past 6h / 24h, by volatility tercile
    g6["sb"] = g6.groupby("coin")["s"].transform(lambda x: pd.qcut(x, 3, labels=False))
    g6["sgn6"] = np.sign(g6["r6p"]); g6["us6"] = g6["u"] * g6["sgn6"]
    g6["r6z"] = g6["r6p"] / (g6["s"] * np.sqrt(6))
    g6["r6b"] = pd.cut(g6["r6z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["6h unusual after past-6h move (in usual 6h moves)"] = g6.groupby("r6b", observed=True)["u"].agg(["mean", "count", tstat])
    out["6h move signed by past 6h, by vol tercile"] = g6.groupby("sb")["us6"].agg(["mean", "count", tstat])
    g24 = res[24].dropna(subset=["r24p", "u", "s"]).copy()
    g24["r24z"] = g24["r24p"] / (g24["s"] * np.sqrt(24))
    g24["b"] = pd.cut(g24["r24z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["24h unusual after past-24h move"] = g24.groupby("b", observed=True)["u"].agg(["mean", "count", tstat])
    g1 = res[1].dropna(subset=["u"])
    out["1h unusual by hour UTC"] = g1.groupby("hour")["u"].agg(["mean", "count", tstat])
    out["1h unusual by weekday"] = g1.groupby("wd")["u"].agg(["mean", "count", tstat])
    # book days
    d = pd.concat([df.assign(coin=c, w=w) for c, ws in data["days"].items() for w, df in ws.items()])
    d["wd"] = pd.to_datetime(d["day"]).dt.weekday
    out["book daily return by weekday"] = d.groupby("wd")["book_return"].agg(["mean", "count", tstat])
    out["book daily return by year"] = d.assign(yr=pd.to_datetime(d["day"]).dt.year).groupby("yr")[["book_return", "coin_return"]].mean()
    # long vs flat bars gain
    A["gain"] = A["pos"] * A["f1"]
    out["book per-bar gain by forecast bin"] = A.assign(fb=pd.cut(A["fc"], [-21, -0.01, 0.01, 2, 5, 10, 21])).groupby("fb", observed=True)["gain"].agg(["mean", "count", tstat])
    return out
