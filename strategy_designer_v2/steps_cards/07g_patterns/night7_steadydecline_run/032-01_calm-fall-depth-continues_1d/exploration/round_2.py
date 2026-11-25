def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1) / c - 1).dropna())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            hl = (b["high"] - b["low"]).astype(float).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": c.shift(-1) / c - 1 - drift,
                "r2": c.shift(-2) / c - 1 - 2 * drift,
                "r3": c.shift(-3) / c - 1 - 3 * drift,
                "ret1": r, "ret30": c / c.shift(30) - 1,
                "vol20": r.rolling(20).std(),
                "clpos": (c - b["low"]) / hl,
                "rngv": hl / c / r.rolling(20).std(),
                "prof": (b["regime"] == "unknown").astype(int),
            })
            d["z1"] = d["ret1"] / d["vol20"]
            d["sclpos"] = 0.5 - d["clpos"]  # positive = close near low
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["wn"] = D["win"].str[1:].astype(int)

    def tday(s, col):
        s = s.dropna(subset=[col])
        ds = s.groupby("day")[col].sum()
        if len(ds) < 3: return (np.nan, np.nan, len(ds))
        return (s[col].mean(), ds.mean() / (ds.std(ddof=1) / np.sqrt(len(ds))), len(ds))

    def graded(S, feat, col, grid=1):
        if grid > 1: S = S[S["pos"] % grid == 0]
        S = S.dropna(subset=[feat, col]).copy()
        S["g"] = S[feat] * S[col]
        m, t, n = tday(S, "g")
        return m, t, n

    res = {}
    out = []
    for feat in ["sclpos", "z1"]:
        for col, g in [("r1", 1), ("r2", 2), ("r3", 3)]:
            S = D.copy()
            if feat == "z1": S["f"] = -S["z1"].clip(-3, 3)
            else: S["f"] = S["sclpos"]
            m, t, n = graded(S, "f", col, g)
            out.append({"feat": feat, "h": col, "graded mean": m, "t": t, "days": n})
    res["graded reversal, all"] = pd.DataFrame(out)

    # clpos -> r1 by coin, window half, profile, vol of range
    def qdiff(S):
        S = S.dropna(subset=["clpos", "r1"]).copy()
        lo = S[S.clpos < 0.25]; hi = S[S.clpos > 0.75]
        a = tday(lo, "r1"); b = tday(hi, "r1")
        return a[0], a[1], a[2], b[0], b[1], b[2]
    o = []
    for k, g in D.groupby("coin"):
        o.append((k,) + qdiff(g))
    for k, g in D.groupby(D.wn <= 12):
        o.append(("w7-12" if k else "w13-18",) + qdiff(g))
    for k, g in D.groupby("prof"):
        o.append(("in falling calm" if k else "out profile",) + qdiff(g))
    D["agit"] = D.groupby(["coin", "win"])["vol20"].transform(lambda x: x > x.median())
    for k, g in D.groupby("agit"):
        o.append(("vol20 above win median" if k else "vol20 below",) + qdiff(g))
    D["tr"] = np.sign(D["ret30"])
    for k, g in D.groupby("tr"):
        o.append((f"ret30 sign {k}",) + qdiff(g))
    res["close<0.25 vs >0.75 next day"] = pd.DataFrame(o, columns=["grp", "low m", "low t", "low days", "high m", "high t", "high days"])

    # wide day closing near low (range in vol units)
    S = D.dropna(subset=["clpos", "rngv", "r1"]).copy()
    S["rq"] = pd.qcut(S["rngv"], 3, labels=False)
    o = []
    for rq, g in S.groupby("rq"):
        lo = g[g.clpos < 0.25]; hi = g[g.clpos > 0.75]
        a = tday(lo, "r1"); b = tday(hi, "r1")
        o.append({"range tercile": rq, "lowclose m": a[0], "t": a[1], "days": a[2], "highclose m": b[0], "t2": b[1], "days2": b[2]})
    res["by range tercile"] = pd.DataFrame(o)

    # usual move & strength of low-close
    sd1 = D.groupby("coin")["r1"].std()
    L = D[D.clpos < 0.25].dropna(subset=["r1"]).copy()
    L["str"] = L["r1"] / L["coin"].map(sd1)
    res["low-close strength"] = L["str"].mean()
    res["low-close cases"] = len(L)
    return res
