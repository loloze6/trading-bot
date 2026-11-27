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
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            v = b["volume"].astype(float)
            rng = (h - l) / c
            r = c / c.shift(1) - 1
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret": r,
                "width": rng / rng.rolling(20, min_periods=20).mean(),
                "loc": ((c - l) / (h - l)).where(h > l),
                "n1": c.shift(-1) / c - 1,
                "r5p": c.shift(1) / c.shift(6) - 1,
                "vrel": v / v.rolling(20, min_periods=20).mean(),
                "vol30": r.rolling(30, min_periods=20).std(),
                "tr60": c / c.shift(60) - 1,
                "falling": b["regime"] != "chop",
                "case": b["forecast"] < 0,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            d["x1"] = d["n1"] - drift
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # agitation proxy: vol30 rank within coin over all its bars (descriptive)
    D["agit"] = D.groupby("coin")["vol30"].rank(pct=True) > 0.5

    def st(sub, col="x1", sign=1):
        s = sub.dropna(subset=[col])
        if len(s) < 5:
            return pd.Series({"n": len(s), "days": 0, "mean": np.nan, "t": np.nan})
        vv = sign * s[col]
        dev = (vv - vv.mean()).groupby(s["day"]).sum()
        nd = len(dev)
        se = np.sqrt((dev ** 2).sum() * nd / max(nd - 1, 1)) / len(vv)
        return pd.Series({"n": len(vv), "days": nd, "mean": vv.mean(), "t": vv.mean() / se if se > 0 else np.nan})

    out = {}
    up = D["ret"] > 0; dn = D["ret"] < 0; wide = D["width"] > 1
    fal = D["falling"]; choppy = (D["tr60"] >= -0.10) & (D["tr60"] <= 0.10); rising = D["tr60"] > 0.10
    ag = D["agit"]
    hc = D["loc"] >= .75; lc = D["loc"] <= .25
    g = {}
    g["upwide hc falling agit (short)"] = st(D[up & wide & hc & fal & ag], sign=-1)
    g["upwide hc falling calm (short)"] = st(D[up & wide & hc & fal & ~ag], sign=-1)
    g["upwide hc choppy agit (short)"] = st(D[up & wide & hc & choppy & ag], sign=-1)
    g["upwide hc choppy calm (short)"] = st(D[up & wide & hc & choppy & ~ag], sign=-1)
    g["upwide hc rising agit (short)"] = st(D[up & wide & hc & rising & ag], sign=-1)
    g["upwide hc rising calm (short)"] = st(D[up & wide & hc & rising & ~ag], sign=-1)
    g["dnwide lc choppy agit (long)"] = st(D[dn & wide & lc & choppy & ag])
    g["dnwide lc choppy calm (long)"] = st(D[dn & wide & lc & choppy & ~ag])
    g["dnwide lc rising agit (long)"] = st(D[dn & wide & lc & rising & ag])
    g["dnwide lc rising calm (long)"] = st(D[dn & wide & lc & rising & ~ag])
    out["groups by profile proxy"] = pd.DataFrame(g).T

    cs = D[D["case"]].copy()
    cs["r5q"] = pd.qcut(cs["r5p"], 3, labels=False, duplicates="drop")
    out["cases by prior 5d return tercile (short)"] = cs.groupby("r5q").apply(lambda s: st(s, sign=-1))
    cs["vq"] = pd.qcut(cs["vrel"], 3, labels=False, duplicates="drop")
    out["cases by rel volume tercile (short)"] = cs.groupby("vq").apply(lambda s: st(s, sign=-1))
    cs["rq"] = pd.qcut(cs["ret"], 3, labels=False, duplicates="drop")
    out["cases by day return tercile (short)"] = cs.groupby("rq").apply(lambda s: st(s, sign=-1))
    cs["fq"] = pd.qcut(-cs["fc"], 3, labels=False, duplicates="drop")
    out["cases by forecast strength tercile (short)"] = cs.groupby("fq").apply(lambda s: st(s, sign=-1))

    # choppy up wide high close: width and loc grading
    C = D[choppy & up & D["width"].notna()].copy()
    C["wq"] = pd.qcut(C["width"], 4, labels=False)
    out["choppy up days by width quartile (long sign)"] = C.groupby("wq").apply(lambda s: st(s))
    # rising down days width grading
    R = D[rising & dn & D["width"].notna()].copy()
    R["wq"] = pd.qcut(R["width"], 4, labels=False)
    out["rising down days by width quartile (long sign)"] = R.groupby("wq").apply(lambda s: st(s))

    # book: daily returns, largest days
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["day", "book_return", "coin_return"]].copy(); x["win"] = w; x["coin"] = coin
            dl.append(x)
    B = pd.concat(dl)
    Bd = B.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    nz = Bd[Bd["book_return"] != 0]
    out["book days nonzero"] = pd.Series({"n": len(nz), "mean": nz["book_return"].mean(),
        "top10 share of sum": nz["book_return"].nlargest(10).sum() / nz["book_return"].sum(),
        "worst10 sum": nz["book_return"].nsmallest(10).sum(), "corr with coin": nz["book_return"].corr(nz["coin_return"])})
    out["book by window"] = Bd.groupby(level=0)["book_return"].agg(["mean", "count", lambda s: (s != 0).sum()])
    return out
