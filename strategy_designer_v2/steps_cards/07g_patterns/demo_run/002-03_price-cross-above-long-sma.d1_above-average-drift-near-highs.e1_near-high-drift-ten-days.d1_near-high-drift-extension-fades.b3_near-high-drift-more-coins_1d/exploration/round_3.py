def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                "ret30": c / c.shift(30) - 1, "ret10": c / c.shift(10) - 1,
                "fwd": c.shift(-H) / c - 1, "regime": b["regime"],
                "alloc": b["postRebalance_current_allocation"],
                "year": ts.dt.year})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    cm = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(cm)
    out = {}
    def ols(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 10:
            return pd.Series({"slope": np.nan, "t": np.nan, "n": len(d)})
        r = stats.linregress(d[x], d["ex"])
        return pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(d)})
    tr = G[G["regime"] == "trending"].dropna(subset=["ret10", "ex"]).copy()
    tr["r10rank"] = tr.groupby("coin")["ret10"].rank(pct=True)
    yy = []
    for y, d in tr.groupby("year"):
        s = ols(d, "r10rank"); s["year"] = y; yy.append(s)
    out["trend ret10rank slope by year"] = pd.DataFrame(yy).round(4)
    cc = []
    for c_, d in tr.groupby("coin"):
        s = ols(d, "r10rank"); s["coin"] = c_; cc.append(s)
    cc = pd.DataFrame(cc)
    out["trend ret10rank by coin"] = cc.round(3)
    out["coins positive slope share"] = float((cc["slope"] > 0).mean())
    # deciles of ret30 in trending: does the top decile fade?
    t3 = G[G["regime"] == "trending"].dropna(subset=["ret30", "ex"]).copy()
    t3["d"] = pd.qcut(t3["ret30"].rank(method="first"), 10, labels=False)
    g = t3.groupby("d").agg(mean=("ex", "mean"), std=("ex", "std"), n=("ex", "count"),
                            lo=("ret30", "min"), hi=("ret30", "max"))
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["n"]))
    out["trend ret30 decile"] = g.round(4)
    # nontrend ret10 slope
    un = G[G["regime"] != "trending"].copy()
    un["r10rank"] = un.groupby("coin")["ret10"].rank(pct=True)
    out["nontrend ret10rank"] = ols(un, "r10rank").round(4)
    # book short side in trending by year
    A["fwd1"] = A.groupby(["coin", "w"])["ret10"].transform(lambda s: np.nan)
    return out
