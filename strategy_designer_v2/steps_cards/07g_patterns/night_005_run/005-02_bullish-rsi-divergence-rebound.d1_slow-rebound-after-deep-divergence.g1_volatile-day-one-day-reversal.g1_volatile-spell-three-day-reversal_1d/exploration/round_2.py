def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.abs().shift(1).rolling(60, min_periods=20).mean()
            s20 = r1.rolling(20).std()
            vr = s20 / s20.rolling(60, min_periods=20).mean()
            r5 = c / c.shift(5) - 1
            f3 = c.shift(-3) / c - 1
            f5 = c.shift(-5) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "z": r1 / sd, "vr": vr, "r5z": r5 / (sd * np.sqrt(5)),
                               "f3": f3, "f5": f5})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["f3x"] = d["f3"] - d.groupby("coin")["f3"].transform("mean")
    d["f5x"] = d["f5"] - d.groupby("coin")["f5"].transform("mean")
    g3 = d[d["pos"] % 3 == 0].dropna(subset=["z", "f3x", "vr", "r5z"])
    g5 = d[d["pos"] % 5 == 0].dropna(subset=["z", "f5x", "vr", "r5z"])
    lo3 = g3[g3["vr"] < 1].copy(); hi3 = g3[g3["vr"] >= 1].copy()
    # signed product t for continuation in low vol
    def prod_t(s, x, y):
        p = np.clip(s[x], -3, 3) * s[y]
        return pd.Series({"mean": p.mean(), "t": p.mean() / (p.std() / np.sqrt(len(p))), "n": len(p)})
    res = {}
    res["lo z f3x"] = prod_t(lo3, "z", "f3x")
    res["hi z f3x"] = prod_t(hi3, "z", "f3x")
    res["lo r5z f3x"] = prod_t(lo3, "r5z", "f3x")
    res["hi r5z f3x"] = prod_t(hi3, "r5z", "f3x")
    lo5 = g5[g5["vr"] < 1]; hi5 = g5[g5["vr"] >= 1]
    res["lo r5z f5x"] = prod_t(lo5, "r5z", "f5x")
    res["hi r5z f5x"] = prod_t(hi5, "r5z", "f5x")
    res["lo z f5x"] = prod_t(lo5, "z", "f5x")
    out["product t"] = pd.DataFrame(res).T.round(4)
    # by coin, low vol, z f3x
    bc = {}
    for coin, s in lo3.groupby("coin"):
        bc[coin + " z"] = prod_t(s, "z", "f3x")
        bc[coin + " r5z"] = prod_t(s, "r5z", "f3x")
    for coin, s in hi3.groupby("coin"):
        bc[coin + " hi r5z"] = prod_t(s, "r5z", "f3x")
    out["low vol by coin"] = pd.DataFrame(bc).T.round(4)
    # low vol: graded within vr terciles
    lo3["vq"] = pd.qcut(lo3["vr"], 3, labels=False)
    vt = {}
    for q, s in lo3.groupby("vq"):
        vt[f"vr tercile {q} (mean {s['vr'].mean():.2f})"] = prod_t(s, "z", "f3x")
    out["low vol z by vr tercile"] = pd.DataFrame(vt).T.round(4)
    # low vol r5z quintiles
    lo3["q"] = pd.qcut(lo3["r5z"], 5, labels=False)
    a = lo3.groupby("q")["f3x"].agg(["mean", "count", "std"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["low vol r5z quint f3x"] = a.round(4)
    hi3["q"] = pd.qcut(hi3["r5z"], 5, labels=False)
    a = hi3.groupby("q")["f3x"].agg(["mean", "count", "std"]); a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["high vol r5z quint f3x"] = a.round(4)
    # window halves stability for low vol z
    lo3["wn"] = lo3["w"].str[1:].astype(int)
    hs = {}
    for h, s in lo3.groupby(lo3["wn"] <= 12):
        hs["w1-12" if h else "w13-24"] = prod_t(s, "z", "f3x")
    out["low vol z by window half"] = pd.DataFrame(hs).T.round(4)
    # book: days around largest gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.reset_index(drop=True).copy()
            x["nb"] = x["book_return"].shift(-1); x["nc"] = x["coin_return"].shift(-1)
            x["coin"] = coin; dd.append(x)
    D = pd.concat(dd, ignore_index=True).dropna(subset=["book_return", "nb"])
    D["bq"] = pd.qcut(D["book_return"], 10, labels=False, duplicates="drop")
    out["next day after book decile"] = D.groupby("bq")[["book_return", "nb", "nc"]].mean().round(5)
    return out
