def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "ret5": c / c.shift(5) - 1,
                "vr": v.rolling(5).mean() / v.rolling(30).mean(),
                "lvr": np.log(v.rolling(5).mean() / v.rolling(30).mean()),
                "rng": (hi.rolling(5).max() - lo.rolling(5).min()) / (hi.rolling(30).max() - lo.rolling(30).min()),
                "vol20": r1.rolling(20).std(),
                "fwd3": c.shift(-3) / c - 1,
                "fwd7": c.shift(-7) / c - 1,
                "pos": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            df = df.iloc[::3]
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["fwd3", "lvr", "ret5", "vol20"])
    d["ex3"] = d["fwd3"] - d.groupby("coin")["fwd3"].transform("mean")
    d["nabs"] = d["fwd3"].abs() / (d["vol20"] * np.sqrt(3))
    out = {}
    def reg(x, col, y="ex3"):
        x = x.dropna(subset=[col, y])
        s = stats.linregress(x[col], x[y])
        return {"slope": s.slope, "t": s.slope / s.stderr, "n": len(x)}
    out["lvr slope by sign of ret5"] = pd.DataFrame({"all": reg(d, "lvr"), "up5": reg(d[d.ret5 > 0], "lvr"), "down5": reg(d[d.ret5 < 0], "lvr")}).T
    out["lvr slope per coin"] = pd.DataFrame({c: reg(x, "lvr") for c, x in d.groupby("coin")}).T
    out["lvr slope per year"] = pd.DataFrame({y: reg(x, "lvr") for y, x in d.groupby("yr")}).T
    # multivariate ret5 + lvr
    X = np.column_stack([np.ones(len(d)), d["ret5"], d["lvr"]])
    beta, *_ = np.linalg.lstsq(X, d["ex3"].values, rcond=None)
    res = d["ex3"].values - X @ beta
    s2 = res.var(ddof=3); cov = s2 * np.linalg.inv(X.T @ X)
    out["multi ret5+lvr"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["const", "ret5", "lvr"])
    # vol-normalised abs move by range compression and vr
    d["rq"] = pd.qcut(d["rng"].rank(method="first"), 5, labels=False)
    d["vq"] = pd.qcut(d["lvr"].rank(method="first"), 5, labels=False)
    out["normabs by rng quint"] = d.groupby("rq").agg(nabs=("nabs", "mean"), n=("nabs", "size"))
    out["normabs by vr quint"] = d.groupby("vq").agg(nabs=("nabs", "mean"), ex3=("ex3", "mean"))
    # 7-day horizon for lvr
    d7 = d.dropna(subset=["fwd7"]).copy()
    d7["ex7"] = d7["fwd7"] - d7.groupby("coin")["fwd7"].transform("mean")
    d7 = d7.iloc[::2]
    out["lvr slope 7d (sparser grid)"] = pd.Series(reg(d7, "lvr", "ex7"))
    # positions by vr quintile within down5
    dn = d[d.ret5 < 0]
    out["down5 position by vr quint"] = dn.groupby("vq").agg(pos=("pos", "mean"), fc=("fc", "mean"), ex3=("ex3", "mean"), fwd3=("fwd3", "mean"), n=("ex3", "size"))
    out["mean fwd3 down5 vs up5"] = pd.Series({"down5": dn["fwd3"].mean(), "up5": d[d.ret5 > 0]["fwd3"].mean(),
        "t_diff": stats.ttest_ind(dn["fwd3"], d[d.ret5 > 0]["fwd3"], equal_var=False).statistic})
    return out
