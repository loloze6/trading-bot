def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hi20 = c.rolling(20).max(); lo20 = c.rolling(20).min()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                "rng": (c - lo20) / (hi20 - lo20), "ret30": c / c.shift(30) - 1,
                "ret10": c / c.shift(10) - 1, "vol20": r1.rolling(20).std(),
                "fwd": c.shift(-H) / c - 1, "fwd1": c.shift(-1) / c - 1,
                "regime": b["regime"], "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "rng_post": b.get("debug_info.components.range20.post_pipeline_value"),
                "ext_post": b.get("debug_info.components.ext30.post_pipeline_value"),
                "year": ts.dt.year, "wd": ts.dt.weekday, "day": ts.dt.floor("D")})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    cm = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(cm)
    out = {}
    tr = G[G["regime"] == "trending"].dropna(subset=["ret30", "ex"]).copy()
    def ols(d, x):
        d = d.dropna(subset=[x, "ex"])
        r = stats.linregress(d[x], d["ex"])
        return pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(d)})
    # graded: ret30 clipped at 99th pct, and rank
    tr["r30c"] = tr["ret30"].clip(upper=tr["ret30"].quantile(0.99))
    tr["r30rank"] = tr.groupby("coin")["ret30"].rank(pct=True)
    tr["rngrank"] = tr["rng"]
    out["trend ols"] = pd.DataFrame({"ret30 clipped": ols(tr, "r30c"), "ret30 rank": ols(tr, "r30rank"),
        "rng": ols(tr, "rngrank"), "ret10": ols(tr, "ret10"), "ext_post": ols(tr, "ext_post"),
        "rng_post": ols(tr, "rng_post")}).T.round(4)
    # by year
    yy = []
    for y, d in tr.groupby("year"):
        s = ols(d, "r30rank"); s["year"] = y; yy.append(s)
    out["trend ret30rank slope by year"] = pd.DataFrame(yy).round(4)
    # by coin sign count
    cc = []
    for c_, d in tr.groupby("coin"):
        if len(d) > 15:
            s = ols(d, "r30rank"); s["coin"] = c_; cc.append(s)
    cc = pd.DataFrame(cc)
    out["trend ret30rank by coin"] = cc.round(3)
    # non-trend: ret30 rank slope
    un = G[G["regime"] != "trending"].copy()
    un["r30rank"] = un.groupby("coin")["ret30"].rank(pct=True)
    out["nontrend ols ret30rank"] = ols(un, "r30rank").round(4)
    # forecast composition in trending
    T = A[A["regime"] == "trending"]
    out["trend share fc<0, mean ext_post, mean rng_post"] = pd.Series({
        "share_fc_neg": (T["fc"] < 0).mean(), "mean_ext": T["ext_post"].mean(),
        "mean_rng": T["rng_post"].mean(), "share_ext_below_-1": (T["ext_post"] < -1).mean()}).round(4)
    # weekday effect on day-level cross-coin mean (clustered)
    dd = A.dropna(subset=["fwd1"]).groupby(["day", "wd"])["fwd1"].mean().reset_index()
    g = dd.groupby("wd")["fwd1"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["weekday day-clustered"] = g.round(4)
    # down-move next day, day-clustered: per-coin z<-1 indicator
    A["z"] = A["ret10"]
    return out
