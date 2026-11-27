import pandas as pd, numpy as np

def tday(df, col):
    s = df.dropna(subset=[col])
    if len(s) < 3:
        return (len(s), s[col].mean() if len(s) else np.nan, np.nan, 0)
    m = s[col].mean()
    dv = (s[col] - m).groupby(s["ts"]).sum()
    K = len(dv)
    se = np.sqrt((dv**2).sum() * K / (K - 1)) / len(s)
    return (len(s), m, m / se, K)

def explore(data):
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b))})
            d["ts"] = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            d["yr"] = pd.to_datetime(b["timestamp"]).dt.year.values
            d["inprof"] = (b["regime"] == "unknown").values
            d["r1"] = c.pct_change().values
            d["r30"] = (c / c.shift(30) - 1).values
            d["r60"] = (c / c.shift(60) - 1).values
            d["rng"] = ((b["high"] - b["low"]) / c).values
            d["sd30"] = c.pct_change().rolling(30).std().values
            for h in [1, 2, 3, 5, 7, 21]:
                d[f"f{h}"] = (c.shift(-h) / c - 1).values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in [1, 2, 3, 5, 7, 21]:
        g = D[(D.pos % h == 0) & D[f"f{h}"].notna()]
        D[f"x{h}"] = D[f"f{h}"] - D.coin.map(g.groupby("coin")[f"f{h}"].mean())
    D["z1"] = D["r1"] / D["sd30"]
    D["zr"] = D["rng"] / D["sd30"]
    out = {}

    # A: big down day (bottom quintile of z1) -> excess over horizons, day-clustered t
    res = []
    q = D["z1"].quantile([0.2, 0.8])
    for h in [1, 2, 3, 5, 7]:
        g = D[(D.pos % h == 0)]
        for name, sub in [("down q1", g[g.z1 <= q.iloc[0]]),
                          ("up q5", g[g.z1 >= q.iloc[1]]),
                          ("mid", g[(g.z1 > q.iloc[0]) & (g.z1 < q.iloc[1])])]:
            n, m, t, K = tday(sub, f"x{h}")
            res.append(dict(set=name, h=h, n=n, days=K, mean=m, t=t))
    out["z1 groups day-t"] = pd.DataFrame(res)

    # B: 7-day after the big down day, starting next day (skip day1): x from t+1 to t+7
    # by window sign count for 1-day rebound of bottom quintile
    g = D[D.z1 <= q.iloc[0]]
    out["down q1 x1 by window"] = g.groupby("w")["x1"].agg(["count", "mean"])
    out["down q1 x1 by year"] = g.groupby("yr")["x1"].agg(["count", "mean"])

    # C: graded in choppy (|r60|<10%) : r30 quintiles -> x7 / x21 day t
    res = []
    for h in [7, 21]:
        g = D[(D.pos % h == 0) & D.r60.notna() & D.r30.notna()].copy()
        g["ch"] = g.r60.abs() < 0.10
        g["q"] = pd.qcut(g.r30, 5, labels=False)
        for ch in [True, False]:
            for qq, s in g[g.ch == ch].groupby("q"):
                n, m, t, K = tday(s, f"x{h}")
                res.append(dict(h=h, choppy=ch, q=qq, n=n, days=K, mean=m, t=t))
    out["r30 q by choppy60"] = pd.DataFrame(res)

    # D: r30 top quintile -> x21 by window (reversal)
    g = D[(D.pos % 21 == 0) & D.r30.notna()].copy()
    g["q"] = pd.qcut(g.r30, 5, labels=False)
    top = g[g.q == 4]
    out["r30 top x21 by window"] = top.groupby("w")["x21"].agg(["count", "mean"])
    n, m, t, K = tday(top, "x21")
    out["r30 top x21 day-t"] = f"n {n} days {K} mean {m:.4f} t {t:.2f}"
    # graded: corr of r30 with x21 overall
    s = g.dropna(subset=["x21"])
    out["corr r30 x21"] = s[["r30", "x21"]].corr().iloc[0, 1]

    # E: wide range quintile -> x1 and x7, day t
    res = []
    qr = D["zr"].quantile(0.8)
    for h in [1, 3, 7]:
        g = D[D.pos % h == 0]
        for name, sub in [("wide", g[g.zr >= qr]), ("rest", g[g.zr < qr])]:
            n, m, t, K = tday(sub, f"x{h}")
            res.append(dict(set=name, h=h, n=n, days=K, mean=m, t=t))
    out["wide range day-t"] = pd.DataFrame(res)
    return out
