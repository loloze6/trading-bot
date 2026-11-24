def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l)
            rr = rng / rng.rolling(20, min_periods=20).mean()
            body = (c - o).abs() / rng.replace(0, np.nan)
            sbody = (c - o) / rng.replace(0, np.nan)
            cloc = (c - l) / rng.replace(0, np.nan)
            r1 = c.pct_change()
            r5 = c / c.shift(5) - 1
            z5 = (r5 - r5.rolling(60, min_periods=20).mean()) / r5.rolling(60, min_periods=20).std()
            r20 = c / c.shift(20) - 1
            vol20 = r1.rolling(20).std()
            volq = vol20 / vol20.rolling(120, min_periods=40).mean()
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "rr": rr, "body": body, "sbody": sbody, "cloc": cloc, "r1": r1, "r5": r5, "z5": z5,
                               "r20": r20, "volq": volq, "f5": f5, "f1": f1, "f3": f3,
                               "regime": b["regime"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    # drift per coin on grid
    g5 = d[d.pos % 5 == 0]
    drift5 = g5.groupby("coin")["f5"].mean()
    drift1 = d.groupby("coin")["f1"].mean()
    d["x5"] = d["f5"] - d["coin"].map(drift5)
    d["x1"] = d["f1"] - d["coin"].map(drift1)
    usual5 = g5.groupby("coin")["f5"].std()
    d["s5"] = d["x5"] / d["coin"].map(usual5)

    def tday(s, days):
        x = pd.DataFrame({"v": s, "d": days}).dropna()
        if len(x) < 5: return (np.nan, len(x), np.nan, 0)
        m = x.v.mean()
        ds = (x.v - m).groupby(x.d).sum()
        se = np.sqrt((ds ** 2).sum()) / len(x)
        return (m, len(x), m / se if se > 0 else np.nan, x.d.nunique())

    def table(sub, col, val, q=5):
        sub = sub.dropna(subset=[col, val])
        sub = sub.assign(b=pd.qcut(sub[col], q, labels=False, duplicates="drop"))
        out = []
        for k, gg in sub.groupby("b"):
            m, n, t, nd = tday(gg[val], gg["day"])
            out.append({"bin": k, "lo": gg[col].min(), "hi": gg[col].max(), "mean": m, "n": n, "t": t, "days": nd})
        return pd.DataFrame(out)

    G = d[d.pos % 5 == 0]
    res = {}
    res["z5 -> x5 grid"] = table(G, "z5", "x5")
    res["rr -> x5 grid"] = table(G, "rr", "x5")
    res["cloc -> x5 grid"] = table(G, "cloc", "x5")
    res["sbody -> x5 grid"] = table(G, "sbody", "x5")
    res["r20 -> x5 grid"] = table(G, "r20", "x5")
    res["volq -> x5 grid"] = table(G, "volq", "x5")
    res["r1 -> x1 all"] = table(d, "r1", "x1", 10)
    # weekday
    wdo = []
    for k, gg in d.groupby("wd"):
        m, n, t, nd = tday(gg["x1"], gg["day"]); wdo.append({"wd": k, "mean": m, "n": n, "t": t})
    res["weekday next-day x1"] = pd.DataFrame(wdo)
    # wide flat days (all bars, not grid) by prior direction
    wf = d[(d.rr >= 1.5) & (d.body <= 0.1)].copy()
    wf["dir"] = np.sign(wf["r5"])
    o = []
    for k, gg in wf.groupby("dir"):
        for v in ["x1", "x5"]:
            m, n, t, nd = tday(gg[v], gg["day"]); o.append({"dir": k, "v": v, "mean": m, "n": n, "t": t, "days": nd})
    res["wide flat by prior dir"] = pd.DataFrame(o)
    # wide days (rr high) by signed body: continuation?
    wide = G[G.rr >= 1.5]
    res["wide days sbody -> x5"] = table(wide, "sbody", "x5", 4)
    res["wide days cloc -> x5"] = table(wide, "cloc", "x5", 4)
    res["counts"] = pd.Series({"bars": len(d), "grid": len(G), "wideflat": len(wf), "wide_grid": len(wide)})
    return res
