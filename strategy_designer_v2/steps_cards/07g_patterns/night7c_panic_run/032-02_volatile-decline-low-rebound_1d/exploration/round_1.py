def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            rng = (hi - lo) / c
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-H) / c - 1,
                "r1": c / c.shift(1) - 1,
                "r5": c / c.shift(5) - 1,
                "r30": c / c.shift(30) - 1,
                "rr": rng.rolling(10).mean() / rng.rolling(60).mean(),
                "brk": c / lo.shift(1).rolling(30).min() - 1,
                "bhi": c / hi.shift(1).rolling(30).max() - 1,
                "vol": c.pct_change().rolling(20).std(),
                "fc": b["forecast"].astype(float),
                "pos": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            df["clv"] = (c - lo) / (hi - lo).replace(0, np.nan)
            df = df.iloc[::H]
            rows.append(df)
    d = pd.concat(rows).dropna(subset=["fwd"])
    drift = d.groupby("coin")["fwd"].mean()
    d["ex"] = d["fwd"] - d["coin"].map(drift)
    def tab(col, q=5):
        x = d.dropna(subset=[col]).copy()
        x["b"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = x.groupby("b")["ex"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["lo"] = x.groupby("b")[col].mean()
        return g.round(4)
    out = {}
    for col in ["r1", "r5", "r30", "rr", "brk", "bhi", "vol", "clv"]:
        out["ex5 by quintile of " + col] = tab(col)
    g = d.groupby("wd")["ex"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["ex5 by weekday"] = g.round(4)
    g = d.groupby("yr")["ex"].agg(["mean", "count"]); out["ex5 by year"] = g.round(4)
    # interaction: falling + high vol
    x = d.dropna(subset=["r30", "vol", "brk"]).copy()
    x["hv"] = x.groupby("coin")["vol"].transform(lambda s: s > s.median())
    x["dn"] = x["r30"] < 0
    g = x.groupby(["dn", "hv"])["ex"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["ex5 by down30 x highvol"] = g.round(4)
    sub = x[x.dn & x.hv]
    sub = sub.assign(b=pd.qcut(sub["brk"].rank(method="first"), 4, labels=False))
    g = sub.groupby("b")["ex"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"])); g["brk"] = sub.groupby("b")["brk"].mean()
    out["in down+highvol, ex5 by brk quartile"] = g.round(4)
    # per-coin corr fwd vs r5, r30
    cc = d.dropna(subset=["r5", "r30"]).groupby("coin").apply(lambda z: pd.Series({"corr_r5": z["fwd"].corr(z["r5"]), "corr_r30": z["fwd"].corr(z["r30"]), "corr_bhi": z["fwd"].corr(z["bhi"]), "n": len(z)}))
    out["per coin correlations"] = cc.round(3)
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bd.append(dd.assign(coin=coin, win=w))
    bd = pd.concat(bd)
    br = bd.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book daily: mean, std, n, share nonzero"] = pd.Series({"mean": br.mean(), "std": br.std(), "n": len(br), "nz": (br.abs() > 1e-9).mean()})
    br_w = br.groupby(level=0).agg(["mean", "count"])
    out["book mean by window"] = (br_w * [1e4, 1]).round(3)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t.assign(coin=coin, win=w))
    tr = pd.concat(tr)
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
