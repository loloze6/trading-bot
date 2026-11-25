def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l)
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "cl": np.where(rng > 0, (c - l) / rng, np.nan),
                "rangepct": rng / c,
                "body": (c - o) / c,
                "r0": c.pct_change(),
                "r5p": c / c.shift(5) - 1,
                "r1": c.shift(-1) / c - 1,
                "r2": c.shift(-2) / c - 1,
                "r3": c.shift(-3) / c - 1,
                "vol20": c.pct_change().rolling(20, min_periods=10).std(),
                "ret60": c / c.shift(60) - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos": np.arange(len(b)),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            df["rngrel"] = df["rangepct"] / df["rangepct"].rolling(20, min_periods=10).median()
            df["volrank"] = df["vol20"].rank(pct=True)
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["r1"].mean()
    d["x1"] = d["r1"] - d["coin"].map(mu)
    out = {}
    d["clb"] = pd.cut(d["cl"], [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0001], include_lowest=True)
    def summ(g, col="x1"):
        s = g[col].dropna()
        return pd.Series({"n": len(s), "mean%": s.mean()*100, "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out["x1 by close location"] = d.groupby("clb", observed=True).apply(summ)
    # 2- and 3-day, non-overlapping grids
    for hh in (2, 3):
        g = d[d["pos"] % hh == 0].copy()
        m = g.groupby("coin")[f"r{hh}"].mean()
        g["xh"] = g[f"r{hh}"] - g["coin"].map(m)
        out[f"x{hh} by cl (grid)"] = g.groupby("clb", observed=True).apply(lambda x: summ(x, "xh"))
    # interaction cl x relative range
    d["lowc"] = d["cl"] < 0.2; d["highc"] = d["cl"] > 0.8
    d["rq"] = pd.qcut(d["rngrel"], 3, labels=["narrow", "mid", "wide"])
    out["low close (<.2) by range tercile"] = d[d["lowc"]].groupby("rq", observed=True).apply(summ)
    out["high close (>.8) by range tercile"] = d[d["highc"]].groupby("rq", observed=True).apply(summ)
    d["vq"] = pd.qcut(d["volrank"], 3, labels=["calmv", "midv", "highv"])
    out["low close by vol tercile"] = d[d["lowc"]].groupby("vq", observed=True).apply(summ)
    out["high close by vol tercile"] = d[d["highc"]].groupby("vq", observed=True).apply(summ)
    d["tr"] = pd.cut(d["ret60"], [-10, -0.1, 0.1, 100], labels=["falling", "choppy", "rising"])
    out["low close by 60d trend"] = d[d["lowc"]].groupby("tr", observed=True).apply(summ)
    out["high close by 60d trend"] = d[d["highc"]].groupby("tr", observed=True).apply(summ)
    d["p5"] = pd.qcut(d["r5p"], 3, labels=["down5", "flat5", "up5"])
    out["low close by prior 5d"] = d[d["lowc"]].groupby("p5", observed=True).apply(summ)
    out["all bars by day return quintile"] = d.groupby(pd.qcut(d["r0"], 5), observed=True).apply(summ)
    out["by weekday"] = d.groupby("wd").apply(summ)
    out["low close by coin"] = d[d["lowc"]].groupby("coin").apply(summ)
    out["low close by window"] = d[d["lowc"]].groupby("win").apply(summ)
    # slope of x1 on cl in low half, per year
    d["yr"] = d["win"]
    return out
