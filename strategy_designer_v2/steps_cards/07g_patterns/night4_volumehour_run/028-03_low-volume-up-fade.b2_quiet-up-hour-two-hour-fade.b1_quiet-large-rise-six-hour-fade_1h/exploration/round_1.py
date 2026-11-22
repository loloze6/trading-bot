import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    hr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            ma = r1.abs().rolling(720, min_periods=720).mean().shift(1)
            vm = v.rolling(720, min_periods=720).mean().shift(1)
            z = r1 / ma; vr = v / vm
            f6 = c.shift(-6) / c - 1
            f24 = c.shift(-24) / c - 1
            r24 = c / c.shift(24) - 1
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "z": z, "vr": vr, "f6": f6, "f24": f24,
                              "r24z": r24 / (ma * np.sqrt(24)), "ma": ma, "r1": r1,
                              "hour": ts.dt.hour, "wd": ts.dt.weekday, "pos": np.arange(len(b))})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    G = D[D.pos % 6 == 0].copy()
    G["drift"] = G.groupby("coin")["f6"].transform("mean")
    G["u6"] = G["f6"] - G["drift"]
    G = G.dropna(subset=["z", "vr", "u6"])
    G["zb"] = pd.cut(G.z, [-np.inf, -4, -2, -1, 1, 2, 4, np.inf])
    G["vb"] = pd.cut(G.vr, [0, 0.5, 1.5, 3, np.inf])
    def agg(x):
        return pd.Series({"n": len(x), "mean_u6_%": 100 * x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["u6 by z bin x vol bin"] = G.groupby(["zb", "vb"], observed=True)["u6"].apply(agg).unstack()
    # graded slope of u6 on z, by vol bin
    sl = []
    for vb, g in G.groupby("vb", observed=True):
        res = stats.linregress(g.z.clip(-10, 10), g.u6)
        sl.append({"vb": str(vb), "n": len(g), "slope_%perz": 100 * res.slope, "t": res.slope / res.stderr})
    out["slope u6 on z by vol"] = pd.DataFrame(sl)
    # signed in z direction, abs z>2, by coin and vol
    H = G[G.z.abs() > 2].copy(); H["s"] = np.sign(H.z) * H.u6
    out["continuation |z|>2 by coin x vol"] = H.groupby(["coin", "vb"], observed=True)["s"].apply(agg).unstack()
    # 24h return reversal/continuation graded
    G24 = D[D.pos % 24 == 0].dropna(subset=["r24z", "f24"]).copy()
    G24["u24"] = G24.f24 - G24.groupby("coin")["f24"].transform("mean")
    sl = []
    for coin, g in G24.groupby("coin"):
        res = stats.linregress(g.r24z.clip(-6, 6), g.u24)
        sl.append({"coin": coin, "n": len(g), "slope_%perz": 100 * res.slope, "t": res.slope / res.stderr})
    out["24h ret -> next 24h slope"] = pd.DataFrame(sl)
    # hour of day 1h returns
    D2 = D.dropna(subset=["r1"]).copy()
    D2["u1"] = D2.r1 - D2.groupby("coin")["r1"].transform("mean")
    out["hour of day u1"] = D2.groupby(["hour"])["u1"].apply(agg).unstack()
    out["weekday u1"] = D2.groupby(["wd"])["u1"].apply(agg).unstack()
    # vol level: abs move ratio after high vol
    G["mab"] = G.groupby("coin")["ma"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["u6 by vol quartile"] = G.groupby(["coin", "mab"])["u6"].apply(agg).unstack()
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, w=w))
    B = pd.concat(bk).dropna(subset=["book_return"])
    out["book mean daily by coin"] = B.groupby("coin")[["book_return", "coin_return"]].mean() * 100
    out["book corr with coin by coin"] = B.groupby("coin").apply(lambda x: x.book_return.corr(x.coin_return))
    return out
