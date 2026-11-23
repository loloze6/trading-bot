def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]; v = b["volume"]
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "r0": r, "loc": (h - c) / (h - l).replace(0, np.nan),
                "vol20": r.rolling(20, min_periods=10).std(),
                "vrel": v / v.rolling(20, min_periods=10).mean(),
                "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1,
                "pos": np.arange(len(b)),
                "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")
    g3 = D[D["pos"] % 3 == 0].copy()
    g3["x3"] = g3["f3"] - g3.groupby("coin")["f3"].transform("mean")
    D["r0z"] = D["r0"] / D["vol20"]
    D["lvr"] = np.log(D["vrel"])
    D["yr"] = D["ts"].dt.year
    out = {}
    E = D.dropna(subset=["x1", "r0", "vol20", "loc", "lvr"]).copy()
    E["r0vol"] = E["r0"] * E["vol20"] / E.groupby("coin")["vol20"].transform("median")
    E["locvol"] = E["loc"] * E["vol20"]
    def ols(df, y, cols):
        X = np.column_stack([np.ones(len(df))] + [df[c].values for c in cols])
        yy = df[y].values
        bta = np.linalg.lstsq(X, yy, rcond=None)[0]
        res = yy - X @ bta
        s2 = res @ res / (len(yy) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        return pd.DataFrame({"b": bta, "t": bta / se}, index=["c"] + cols).round(5)
    out["x1 ~ r0 + r0*volnorm + lvr + locvol"] = ols(E, "x1", ["r0", "r0vol", "lvr", "locvol"])
    out["x1 ~ lvr + r0 + lvr*r0"] = ols(E.assign(lr=E.lvr * E.r0), "x1", ["lvr", "r0", "lr"])
    # per coin & per year: slope t of x1 on r0, and on lvr
    def slope_t(df, col):
        df = df.dropna(subset=[col, "x1"])
        s = stats.linregress(df[col], df["x1"]); return round(s.slope / s.stderr, 2)
    out["by coin: t(r0), t(lvr), n"] = E.groupby("coin").apply(lambda g: pd.Series({"t_r0": slope_t(g, "r0"), "t_lvr": slope_t(g, "lvr"), "n": len(g)}))
    out["by year: t(r0), t(lvr)"] = E.groupby("yr").apply(lambda g: pd.Series({"t_r0": slope_t(g, "r0"), "t_lvr": slope_t(g, "lvr")}))
    # graded: down-day size quintile by per-coin rank of r0, high-vol half only
    E["vh"] = E.groupby("coin")["vol20"].rank(pct=True) > 0.5
    E["rq"] = pd.qcut(E.groupby("coin")["r0"].rank(pct=True), 10, labels=[f"r{i}" for i in range(1, 11)])
    out["x1% by r0 decile x high vol"] = E.groupby(["rq", "vh"], observed=True)["x1"].agg(lambda s: f"{100*s.mean():.3f} n={len(s)} t={s.mean()/(s.std()/np.sqrt(len(s))):.2f}").unstack()
    E["vq"] = pd.qcut(E.groupby("coin")["vrel"].rank(pct=True), 5, labels=[f"v{i}" for i in range(1, 6)])
    out["x1% by relvol quintile x down/up day"] = E.groupby(["vq", E.r0 < 0], observed=True)["x1"].agg(lambda s: f"{100*s.mean():.3f} n={len(s)} t={s.mean()/(s.std()/np.sqrt(len(s))):.2f}").unstack()
    # 3-day non-overlapping
    G = g3.dropna(subset=["x3", "r0", "vrel", "vol20"]).copy()
    G["lvr"] = np.log(G["vrel"])
    out["3d nonoverlap: x3 ~ r0 + lvr"] = ols(G, "x3", ["r0", "lvr"]).assign(n=len(G))
    # share of windows where relvol top quintile beats rest
    E["top"] = E["vq"] == "v5"
    ww = E.groupby("win").apply(lambda g: g.loc[g.top, "x1"].mean() - g.loc[~g.top, "x1"].mean())
    out["relvol top minus rest, windows positive share"] = f"{(ww>0).mean():.2f} of {len(ww)}; mean {100*ww.mean():.3f}%"
    # book days: largest gains/losses vs coin
    B = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            B.append(d.assign(coin=coin, win=w))
    B = pd.concat(B).dropna(subset=["book_return", "coin_return"])
    B["bq"] = pd.qcut(B["book_return"], 10, labels=False)
    out["book return decile: mean coin ret, mean book ret"] = B.groupby("bq")[["book_return", "coin_return"]].mean().mul(100).round(3)
    return out
