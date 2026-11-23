def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float); v = b["volume"].astype(float)
            rng = (hi - lo).replace(0, np.nan)
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "cl": (2 * (c - lo) / rng - 1),
                "body": (c - o).abs() / rng,
                "vr": v / v.shift(1).rolling(20, min_periods=20).mean(),
                "r1": c / c.shift(1) - 1,
                "r5p": c / c.shift(5) - 1,
                "r20p": c / c.shift(20) - 1,
                "rngp": rng / c,
                "vol20": (c / c.shift(1) - 1).rolling(20, min_periods=15).std(),
                "fwd": c.shift(-H) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos": np.arange(len(b)),
            })
            df = df[df["pos"] % H == 0]
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d = d.dropna(subset=["fwd"])
    d["drift"] = d.groupby("coin")["fwd"].transform("mean")
    d["usd"] = d.groupby("coin")["fwd"].transform("std")
    d["un"] = (d["fwd"] - d["drift"]) / d["usd"]
    out = {}

    def slope(sub, x):
        s = sub.dropna(subset=[x, "un"])
        if len(s) < 30: return pd.Series({"n": len(s)})
        z = s.groupby("coin")[x].transform(lambda a: (a - a.mean()) / a.std())
        r = stats.linregress(z, s["un"])
        return pd.Series({"n": len(s), "slope": r.slope, "t": r.slope / r.stderr})

    res = {}
    for x in ["cl", "body", "vr", "r1", "r5p", "r20p", "rngp", "vol20"]:
        res[x + "_all"] = slope(d, x)
        res[x + "_vr2"] = slope(d[d["vr"] >= 2], x)
        res[x + "_vr1.5"] = slope(d[d["vr"] >= 1.5], x)
    out["slopes_std_unusual"] = pd.DataFrame(res).T

    # deciles of past moves
    for x in ["r1", "r5p", "r20p", "vol20", "vr", "rngp"]:
        q = d.groupby("coin")[x].transform(lambda a: pd.qcut(a.rank(method="first"), 5, labels=False) if a.notna().sum() > 10 else np.nan)
        g = d.assign(q=q).groupby("q")["un"].agg(["count", "mean", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        out["q5_" + x] = g
    g = d.groupby("wd")["un"].agg(["count", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["weekday"] = g
    # heavy volume flat days interaction: cl x direction of prior 5d
    hv = d[(d["vr"] >= 2)].copy()
    hv["sign_r1"] = np.sign(hv["r1"])
    g = hv.groupby("sign_r1")["un"].agg(["count", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["vr2_by_day_sign"] = g
    # book: largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, win=w))
    dd = pd.concat(dd)
    bk = dd.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = dd.groupby("win")["book_return"].agg(["count", "mean"]).T
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    tr = pd.concat(tr)
    out["trades_side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "std"])
    out["trades_coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
