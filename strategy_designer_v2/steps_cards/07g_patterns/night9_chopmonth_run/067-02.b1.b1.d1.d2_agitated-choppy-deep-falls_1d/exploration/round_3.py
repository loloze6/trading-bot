import pandas as pd, numpy as np

def tday(df, col):
    s = df.dropna(subset=[col])
    if len(s) < 3:
        return (len(s), s[col].mean() if len(s) else np.nan, np.nan, s["ts"].nunique() if len(s) else 0)
    m = s[col].mean()
    dv = (s[col] - m).groupby(s["ts"]).sum()
    K = len(dv)
    se = np.sqrt((dv**2).sum() * K / (K - 1)) / len(s) if K > 1 else np.nan
    return (len(s), m, m / se, K)

def explore(data):
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b))})
            d["ts"] = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            d["inprof"] = (b["regime"] == "unknown").values
            d["r1"] = c.pct_change().values
            d["r30"] = (c / c.shift(30) - 1).values
            d["r60"] = (c / c.shift(60) - 1).values
            d["sd30"] = c.pct_change().rolling(30).std().values
            d["alloc"] = b["postRebalance_current_allocation"].astype(float).values
            for h in [1, 3, 7, 21]:
                d[f"f{h}"] = (c.shift(-h) / c - 1).values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in [1, 3, 7, 21]:
        g = D[(D.pos % h == 0) & D[f"f{h}"].notna()]
        D[f"x{h}"] = D[f"f{h}"] - D.coin.map(g.groupby("coin")[f"f{h}"].mean())
    D["z30"] = D["r30"] / (D["sd30"] * np.sqrt(30))
    D["z1"] = D["r1"] / D["sd30"]
    out = {}
    # r30 scaled, terciles of z30, by r60 band, h 7 and 21
    res = []
    for h in [7, 21]:
        g = D[(D.pos % h == 0) & D.z30.notna() & D.r60.notna()].copy()
        g["band"] = pd.cut(g.r60, [-9, -0.10, 0.10, 99], labels=["fall", "chop", "rise"])
        g["q"] = pd.qcut(g.z30, 3, labels=False)
        for (bd, qq), s in g.groupby(["band", "q"], observed=True):
            n, m, t, K = tday(s, f"x{h}")
            res.append(dict(h=h, band=bd, q=qq, n=n, days=K, mean=m, t=t))
    out["z30 terciles by r60 band"] = pd.DataFrame(res)
    # top r30 tercile (scaled) reversal over 21 by window sign
    g = D[(D.pos % 21 == 0) & D.z30.notna()].copy()
    g["q"] = pd.qcut(g.z30, 5, labels=False)
    out["z30 quintile x21 all"] = pd.DataFrame([dict(q=qq, **dict(zip(["n", "mean", "t", "days"], tday(s, "x21")))) for qq, s in g.groupby("q")])
    # in-profile book: per-coin-day position return by r30 depth
    D["pg"] = D["alloc"] * D["f1"]
    act = D[D.alloc.abs() > 1e-6]
    out["position days, gain by r30 tercile"] = act.groupby(pd.qcut(act.r30, 3, labels=False))["pg"].agg(["count", "mean"])
    # down day z1 bottom quintile x1 by r60 band
    q1 = D.z1.quantile(0.2)
    g = D[(D.z1 <= q1) & D.r60.notna()].copy()
    g["band"] = pd.cut(g.r60, [-9, -0.10, 0.10, 99], labels=["fall", "chop", "rise"])
    res = []
    for bd, s in g.groupby("band", observed=True):
        for h in [1, 3]:
            n, m, t, K = tday(s[s.pos % h == 0], f"x{h}")
            res.append(dict(band=bd, h=h, n=n, days=K, mean=m, t=t))
    out["down day rebound by r60 band"] = pd.DataFrame(res)
    return out
