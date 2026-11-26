import numpy as np
import pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            allr.append((b["close"].shift(-1) / b["close"] - 1).dropna())
        mu1 = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, o, h, l = b["close"], b["open"], b["high"], b["low"]
            rng = (h - l)
            rr = rng / rng.rolling(20, min_periods=20).mean()
            cl = (c - l) / rng.replace(0, np.nan)
            body = (c - o) / rng.replace(0, np.nan)
            r1 = c.shift(-1) / c - 1
            r3 = c.shift(-3) / c - 1
            r5 = c.shift(-5) / c - 1
            past1 = c / c.shift(1) - 1
            past5 = c / c.shift(5) - 1
            vol = past1.rolling(20, min_periods=10).std()
            pos = np.arange(len(b))
            d = pd.DataFrame({
                "coin": coin, "win": w, "day": b["timestamp"].astype(str).str[:10],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "rr": rr, "cl": cl, "body": body, "r1x": r1 - mu1, "r1": r1,
                "r3": r3, "r5": r5, "g3": pos % 3 == 0, "g5": pos % 5 == 0,
                "past1z": past1 / vol, "past5": past5, "vol": vol,
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def ct(df, col):
        x = df[[col, "day"]].dropna()
        if len(x) < 5:
            return pd.Series({"mean": np.nan, "t": np.nan, "n": len(x), "days": 0})
        dev = x[col] - 0
        m = dev.mean()
        s = (dev - m).groupby(x["day"]).sum()
        D_ = len(s)
        se = np.sqrt((s ** 2).sum() * D_ / max(D_ - 1, 1)) / len(x)
        return pd.Series({"mean": m, "t": m / se if se > 0 else np.nan, "n": len(x), "days": D_})

    out = {}
    D["rrb"] = pd.cut(D["rr"], [0, 0.7, 1.0, 1.5, 2.0, 99], labels=["<0.7", "0.7-1", "1-1.5", "1.5-2", ">2"])
    D["clb"] = pd.cut(D["cl"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["q1low", "q2", "q3", "q4high"])
    g = D.groupby(["rrb", "clb"], observed=True).apply(lambda x: ct(x, "r1x"))
    out["r1x by range x closeloc"] = g
    # wide days, horizons
    wide = D[D["rr"] >= 1.5]
    res = []
    for lab, sub in wide.groupby("clb", observed=True):
        for hcol, gcol, hh in [("r3", "g3", 3), ("r5", "g5", 5)]:
            s = sub[sub[gcol]].copy()
            s["x"] = s[hcol]
            r = ct(s, "x"); r["clb"] = lab; r["h"] = hh
            res.append(r)
    out["wide days fwd 3/5 raw (grid)"] = pd.DataFrame(res)
    # prior run interaction for wide low close
    wl = D[(D["rr"] >= 1.5) & (D["cl"] <= 0.25)].copy()
    wl["p5b"] = pd.qcut(wl["past5"], 3, labels=["down", "mid", "up"])
    out["wide-low by past5"] = wl.groupby("p5b", observed=True).apply(lambda x: ct(x, "r1x"))
    wh = D[(D["rr"] >= 1.5) & (D["cl"] >= 0.75)].copy()
    wh["p5b"] = pd.qcut(wh["past5"], 3, labels=["down", "mid", "up"])
    out["wide-high by past5"] = wh.groupby("p5b", observed=True).apply(lambda x: ct(x, "r1x"))
    # large moves by z
    D["zb"] = pd.cut(D["past1z"], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])
    out["r1x by past1 z"] = D.groupby("zb", observed=True).apply(lambda x: ct(x, "r1x"))
    out["wide-low by weekday"] = wl.groupby("wd").apply(lambda x: ct(x, "r1x"))
    out["wide-low by year"] = wl.groupby("year").apply(lambda x: ct(x, "r1x"))
    out["wide-low by coin"] = wl.groupby("coin").apply(lambda x: ct(x, "r1x"))
    D["volb"] = D.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False, duplicates="drop"))
    wl2 = D[(D["rr"] >= 1.5) & (D["cl"] <= 0.25)]
    out["wide-low by vol tercile"] = wl2.groupby("volb").apply(lambda x: ct(x, "r1x"))
    return out
