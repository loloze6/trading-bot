def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            r = c.pct_change()
            lo20 = l.shift(1).rolling(20).min(); hi20 = h.shift(1).rolling(20).max()
            tr60 = (c / c.shift(60) - 1) * 100
            vol20 = r.rolling(20).std()
            volrank = vol20.rolling(60, min_periods=30).rank(pct=True)
            df = pd.DataFrame({
                "coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                "r": r, "z": r / vol20.shift(1),
                "dlo": (c / lo20 - 1) * 100, "dhi": (c / hi20 - 1) * 100,
                "tr60": tr60, "volrank": volrank,
                "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1, "f5": c.shift(-5) / c - 1,
                "mu": mu, "pos": np.arange(len(b)),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "regime": b["regime"],
            })
            df["clv"] = (c - l) / (h - l)
            df["rng"] = (h - l) / c / vol20.shift(1)
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["f1"] - D["mu"]; D["x3"] = D["f3"] - 3 * D["mu"]; D["x5"] = D["f5"] - 5 * D["mu"]
    D["day"] = D["ts"].dt.floor("D")
    D["trend"] = np.where(D["tr60"] > 10, "rising", np.where(D["tr60"] < -10, "falling", np.where(D["tr60"].notna(), "choppy", None)))

    def tday(sub, col, sign=1):
        s = sub.dropna(subset=[col])
        if len(s) == 0: return pd.Series({"n": 0, "days": 0, "mean": np.nan, "t": np.nan})
        g = (s[col] * sign).groupby(s["day"]).sum()
        n = len(s); m = (s[col] * sign).mean()
        t = g.mean() / (g.std(ddof=1) / np.sqrt(len(g))) if len(g) > 2 else np.nan
        return pd.Series({"n": n, "days": len(g), "mean": m, "t": t})

    out = {}
    # 1 downside breaks by trend, horizons
    dn = D[D["dlo"] < 0]
    up = D[D["dhi"] > 0]
    res = {}
    for tname, g in dn.groupby("trend"):
        for col in ["x1", "x3", "x5"]:
            res[("dn", tname, col)] = tday(g, col)
    for tname, g in up.groupby("trend"):
        for col in ["x1", "x3", "x5"]:
            res[("up", tname, col)] = tday(g, col)
    out["breaks by trend (raw sign, excess)"] = pd.DataFrame(res).T.round(4)
    # 2 depth terciles in choppy downside breaks
    ch = dn[dn["trend"] == "choppy"].copy()
    ch["dq"] = pd.qcut(ch["dlo"], 3, labels=["deep", "mid", "shallow"])
    out["choppy down break by depth"] = pd.DataFrame({k: tday(g, "x1") for k, g in ch.groupby("dq")}).T.round(4)
    chu = up[up["trend"] == "choppy"].copy()
    chu["dq"] = pd.qcut(chu["dhi"], 3, labels=["small", "mid", "large"])
    out["choppy up break by size x1"] = pd.DataFrame({k: tday(g, "x1") for k, g in chu.groupby("dq")}).T.round(4)
    # 3 large moves generally: next-day after z buckets, all bars
    A = D.dropna(subset=["z", "x1"]).copy()
    A["zb"] = pd.cut(A["z"], [-99, -3, -2, -1, 0, 1, 2, 3, 99])
    out["next day by today's z"] = pd.DataFrame({str(k): tday(g, "x1") for k, g in A.groupby("zb")}).T.round(4)
    # large down days by trend
    big = A[A["z"] < -2]
    out["after z<-2 by trend x1,x3"] = pd.DataFrame({(k, c): tday(g, c) for k, g in big.groupby("trend") for c in ["x1", "x3"]}).T.round(4)
    bigu = A[A["z"] > 2]
    out["after z>2 by trend x1,x3"] = pd.DataFrame({(k, c): tday(g, c) for k, g in bigu.groupby("trend") for c in ["x1", "x3"]}).T.round(4)
    # 4 weekday
    A["wd"] = A["ts"].dt.dayofweek
    out["weekday x1"] = pd.DataFrame({k: tday(g, "x1") for k, g in A.groupby("wd")}).T.round(4)
    # 5 close location
    A["cq"] = pd.cut(A["clv"], [-0.01, 0.1, 0.3, 0.7, 0.9, 1.01])
    out["next day by close location"] = pd.DataFrame({str(k): tday(g, "x1") for k, g in A.groupby("cq")}).T.round(4)
    # 6 volrank
    A["vq"] = pd.cut(A["volrank"], [0, 0.33, 0.66, 1.0])
    out["dn break x1 by volrank"] = pd.DataFrame({str(k): tday(g, "x1") for k, g in A[A["dlo"] < 0].groupby("vq")}).T.round(4)
    # 7 years
    A["yr"] = A["ts"].dt.year
    out["choppy dn break x1 by year"] = pd.DataFrame({k: tday(g, "x1") for k, g in A[(A["dlo"] < 0) & (A["trend"] == "choppy")].groupby("yr")}).T.round(4)
    return out
