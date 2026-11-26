def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r3 = c / c.shift(3) - 1
            r60 = c / c.shift(60) - 1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": b["timestamp"].astype(str).str[:10],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "z1": r1 / sd30, "z3": r3 / (sd30 * np.sqrt(3)),
                "r60": r60, "fwd": fwd, "fwd1": fwd1,
                "fa": (b["regime"] == "unknown").astype(int),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "grid": (np.arange(len(b)) % H == 0)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d[d.grid].groupby("coin")["fwd"].mean().rename("drift")
    d = d.join(drift, on="coin")
    d["unus"] = d["fwd"] - d["drift"]
    g = d[d.grid].dropna(subset=["unus", "z1", "z3"])

    def tclust(x):
        if len(x) < 10: return pd.Series({"n": len(x), "mean": np.nan, "t": np.nan, "days": 0})
        dev = (x["unus"] - x["unus"].mean()).groupby(x["ts"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "mean": x["unus"].mean(), "t": x["unus"].mean() / se, "days": D})

    out = {}
    g["z1b"] = pd.cut(g["z1"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    g["z3b"] = pd.cut(g["z3"], [-99, -1.5, -0.7, -0.2, 0.2, 0.7, 1.5, 99])
    g["trend"] = pd.cut(g["r60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    out["fwd5 unusual by z1, FA"] = g[g.fa == 1].groupby("z1b").apply(tclust)
    out["fwd5 unusual by z1, not FA"] = g[g.fa == 0].groupby("z1b").apply(tclust)
    out["fwd5 unusual by z3, FA"] = g[g.fa == 1].groupby("z3b").apply(tclust)
    out["fwd5 unusual by z3, not FA"] = g[g.fa == 0].groupby("z3b").apply(tclust)
    out["fwd5 by trend x z3>0.7 (not FA)"] = g[(g.fa == 0) & (g.z3 > 0.7)].groupby("trend").apply(tclust)
    out["fwd5 by trend x z3<-0.7 (not FA)"] = g[(g.fa == 0) & (g.z3 < -0.7)].groupby("trend").apply(tclust)
    # weekday 1-day returns, all bars
    dd = d.dropna(subset=["fwd1"]).copy()
    dd["dm"] = dd["fwd1"] - dd.groupby("coin")["fwd1"].transform("mean")
    out["next-day return by weekday of signal bar, FA"] = dd[dd.fa == 1].groupby("wd")["dm"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["next-day return by weekday, not FA"] = dd[dd.fa == 0].groupby("wd")["dm"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # book: position share, gain when short
    out["share FA bars"] = float(d.fa.mean())
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    if len(tr):
        out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
