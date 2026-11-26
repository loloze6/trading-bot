def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            r5p = c / c.shift(5) - 1
            vr = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            vr10 = np.log(v.rolling(10).mean() / v.shift(10).rolling(20).mean())
            vol20 = r1.rolling(20).std()
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            idx = np.arange(0, len(b), 5)
            d = pd.DataFrame({"coin": coin, "w": w, "r1": r1, "r5p": r5p, "r20": r20, "r60": r60, "vr": vr,
                              "vr10": vr10, "vol20": vol20, "fwd5": fwd5, "fwd1": fwd1, "rng": rng, "clpos": clpos,
                              "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                              "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                              "yr": pd.to_datetime(b["timestamp"]).dt.year}).iloc[idx]
            rows.append(d)
    g = pd.concat(rows).dropna(subset=["fwd5"])
    g["ex5"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")
    def summ(df, col):
        r = df.groupby(col, observed=True)["ex5"].agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.round(4)
    g["r20q"] = g.groupby("coin")["r20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["fwd5 by r20 quintile (per coin)"] = summ(g, "r20q")
    g["r5q"] = g.groupby("coin")["r5p"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["fwd5 by past5 quintile"] = summ(g, "r5q")
    g["vrq"] = g.groupby("coin")["vr"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["fwd5 by vr30 quintile all"] = summ(g, "vrq")
    g["vr10q"] = g.groupby("coin")["vr10"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["fwd5 by vr10 quintile all"] = summ(g, "vr10q")
    g["volq"] = g.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["fwd5 by vol20 quintile"] = summ(g, "volq")
    g["trend"] = np.where(g["r60"] > 0.1, "rising", np.where(g["r60"] < -0.1, "falling", np.where(g["r60"].notna(), "choppy", "na")))
    out["fwd5 by trend"] = summ(g, "trend")
    f = g[g["trend"] == "falling"].copy()
    f["vrq"] = pd.qcut(f["vr"], 4, labels=False, duplicates="drop")
    out["falling: fwd5 by vr30 quartile"] = summ(f, "vrq")
    f["r5q"] = pd.qcut(f["r5p"], 4, labels=False, duplicates="drop")
    out["falling: fwd5 by past5 quartile"] = summ(f, "r5q")
    ch = g[g["trend"] == "choppy"].copy()
    ch["r5q"] = pd.qcut(ch["r5p"], 4, labels=False, duplicates="drop")
    out["choppy: fwd5 by past5 quartile"] = summ(ch, "r5q")
    ch["vrq"] = pd.qcut(ch["vr"], 4, labels=False, duplicates="drop")
    out["choppy: fwd5 by vr30 quartile"] = summ(ch, "vrq")
    out["fwd5 by weekday"] = summ(g, "wd")
    out["fwd5 by year"] = summ(g, "yr")
    g["act"] = np.sign(g["alloc"].fillna(0))
    out["fwd5 by position sign"] = summ(g, "act")
    out["fwd5 by coin, active short"] = g[g["act"] < 0].groupby("coin")["ex5"].agg(["count", "mean"]).round(4)
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d[["book_return", "coin_return"]].copy(); x["coin"] = coin; x["w"] = w
            dd.append(x)
    dd = pd.concat(dd).dropna()
    out["book by window"] = dd.groupby("w")[["book_return", "coin_return"]].sum().round(4)
    out["book by coin"] = dd.groupby("coin")[["book_return", "coin_return"]].sum().round(4)
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    tr = pd.concat(tr)
    tr["dur_d"] = tr["duration_minutes"] / 1440
    out["trades summary"] = tr.groupby("side").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"),
                          med=("net_profit_loss_percent", "median"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()),
                          dur=("dur_d", "mean")).round(3)
    tr["fq"] = pd.qcut(tr["entry_forecast"], 4, labels=False, duplicates="drop")
    out["trades by entry forecast quartile"] = tr.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
    # daily: after large moves (1-day fwd), all bars
    al = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float)
            r1 = c.pct_change(); z = r1 / r1.rolling(20).std().shift(1)
            al.append(pd.DataFrame({"coin": coin, "z": z, "f3": c.shift(-3) / c - 1, "r60": c / c.shift(60) - 1}).iloc[::3])
    al = pd.concat(al).dropna()
    al["ex"] = al["f3"] - al.groupby("coin")["f3"].transform("mean")
    al["zb"] = pd.cut(al["z"], [-99, -2, -1, 0, 1, 2, 99])
    al["tr"] = np.where(al["r60"] > 0.1, "rising", np.where(al["r60"] < -0.1, "falling", "choppy"))
    r = al.groupby(["tr", "zb"], observed=True)["ex"].agg(["count", "mean", "std"])
    r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
    out["fwd3 by trend x day z"] = r.round(4)
    return out
