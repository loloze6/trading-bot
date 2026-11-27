def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1) / c - 1).dropna())
        drift = pd.concat(allr).mean() if allr else 0.0
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l) / c
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret": c / c.shift(1) - 1,
                "width": rng / rng.rolling(20, min_periods=20).mean(),
                "loc": ((c - l) / (h - l)).where(h > l),
                "n1": c.shift(-1) / c - 1,
                "n3": c.shift(-3) / c - 1,
                "n1to3": c.shift(-3) / c.shift(-1) - 1,
                "tr60": c / c.shift(60) - 1,
                "vol10": (c / c.shift(1) - 1).rolling(10).std(),
                "falling": b["regime"] != "chop",
                "case": b["forecast"] < 0,
                "alloc": b["postRebalance_current_allocation"],
            })
            d["drift"] = drift
            d["x1"] = d["n1"] - drift
            d["x3"] = d["n3"] - 3 * drift
            d["x13"] = d["n1to3"] - 2 * drift
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["wd"] = D["day"].dt.dayofweek
    D["year"] = D["day"].dt.year

    def st(sub, col="x1", sign=1):
        s = sub.dropna(subset=[col])
        if len(s) < 5:
            return pd.Series({"n": len(s), "days": 0, "mean": np.nan, "t": np.nan})
        v = sign * s[col]
        dev = (v - v.mean()).groupby(s["day"]).sum()
        nd = len(dev)
        se = np.sqrt((dev ** 2).sum() * nd / max(nd - 1, 1)) / len(v)
        return pd.Series({"n": len(v), "days": nd, "mean": v.mean(), "t": v.mean() / se if se > 0 else np.nan})

    out = {}
    up = D["ret"] > 0; dn = D["ret"] < 0; wide = D["width"] > 1
    fal = D["falling"]
    notf = ~fal
    rising = D["tr60"] > 0.10
    choppy = (D["tr60"] >= -0.10) & (D["tr60"] <= 0.10)
    g = {}
    g["case falling (book)"] = st(D[D["case"]])
    g["upwide hiclose falling"] = st(D[up & wide & (D["loc"] >= .75) & fal])
    g["upwide hiclose rising"] = st(D[up & wide & (D["loc"] >= .75) & rising])
    g["upwide hiclose choppy"] = st(D[up & wide & (D["loc"] >= .75) & choppy])
    g["upwide loclow falling"] = st(D[up & wide & (D["loc"] < .5) & fal])
    g["upnarrow falling"] = st(D[up & ~wide & fal])
    g["dnwide loclose falling"] = st(D[dn & wide & (D["loc"] <= .25) & fal])
    g["dnwide loclose rising"] = st(D[dn & wide & (D["loc"] <= .25) & rising])
    g["dnwide loclose choppy"] = st(D[dn & wide & (D["loc"] <= .25) & choppy])
    g["dnwide hiclose falling"] = st(D[dn & wide & (D["loc"] >= .5) & fal])
    g["all falling"] = st(D[fal])
    g["all rising"] = st(D[rising])
    g["all choppy"] = st(D[choppy])
    out["next-day excess (long sign) by group"] = pd.DataFrame(g).T

    cs = D[D["case"]]
    h = {"x1 short": st(cs, "x1", -1), "x3 short": st(cs, "x3", -1), "day2-3 short": st(cs, "x13", -1)}
    out["cases horizons"] = pd.DataFrame(h).T

    F = D[fal & up & D["width"].notna()].copy()
    F["wq"] = pd.qcut(F["width"], 5, labels=False)
    out["falling up days by width quintile"] = F.groupby("wq").apply(lambda s: st(s))
    F["lq"] = pd.cut(F["loc"], [0, .25, .5, .75, 1.0001], labels=False, include_lowest=True)
    out["falling up days by loc bin"] = F.groupby("lq").apply(lambda s: st(s))
    Fd = D[fal & dn & D["width"].notna()].copy()
    Fd["wq"] = pd.qcut(Fd["width"], 5, labels=False)
    out["falling down days by width quintile"] = Fd.groupby("wq").apply(lambda s: st(s))
    # size of up move itself
    F["rq"] = pd.qcut(F["ret"] / F["vol10"], 5, labels=False, duplicates="drop")
    out["falling up days by ret/vol10 quintile"] = F.groupby("rq").apply(lambda s: st(s))
    out["cases by weekday (short)"] = cs.groupby("wd").apply(lambda s: st(s, "x1", -1))
    out["cases by year (short)"] = cs.groupby("year").apply(lambda s: st(s, "x1", -1))
    out["falling all days by weekday"] = D[fal].groupby("wd").apply(lambda s: st(s))
    return out
