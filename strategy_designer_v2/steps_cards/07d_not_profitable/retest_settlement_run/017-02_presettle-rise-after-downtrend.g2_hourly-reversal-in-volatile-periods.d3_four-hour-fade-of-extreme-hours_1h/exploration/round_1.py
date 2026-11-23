def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vr = r1.rolling(24).std() / r1.rolling(720, min_periods=240).std()
            f = b["forecast"].astype(float)
            hr = pd.to_datetime(b["timestamp"]).dt.hour
            d = pd.DataFrame({"coin": coin, "w": w, "f": f, "r1": r1, "vr": vr, "hour": (hr + 1) % 24,
                              "pos": np.arange(len(b))})
            for h in [1, 2, 4, 8, 12, 24]:
                d[f"fr{h}"] = c.shift(-h) / c - 1
            d["turn"] = b["allocation_change"].astype(float).abs() if "allocation_change" in b else np.nan
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    # drift per coin per h on non-overlapping grid
    drift = {}
    for h in [1, 2, 4, 8, 12, 24]:
        g = D[D["pos"] % h == 0]
        drift[h] = g.groupby("coin")[f"fr{h}"].mean()
    D["absf"] = D["f"].abs()
    D["sgn"] = np.sign(D["f"])
    qs = D["absf"].quantile([0.5, 0.8, 0.9, 0.95, 0.99, 0.999]).values
    D["bucket"] = pd.cut(D["absf"], [-1e-9, qs[0], qs[1], qs[2], qs[3], qs[4], qs[5], 1e9],
                         labels=["0-50", "50-80", "80-90", "90-95", "95-99", "99-99.9", "top0.1"])
    tab = {}
    for h in [1, 4, 8, 12, 24]:
        g = D[(D["pos"] % h == 0)].copy()
        g["ex"] = g["sgn"] * (g[f"fr{h}"] - g["coin"].map(drift[h]))
        m = g.groupby("bucket", observed=True)["ex"].agg(["mean", "count", "std"])
        tab[f"h{h}_mean%"] = m["mean"] * 100
        tab[f"h{h}_t"] = m["mean"] / (m["std"] / np.sqrt(m["count"]))
        if h == 4:
            tab["n4"] = m["count"]
    out["signed excess move by |forecast| bucket"] = pd.DataFrame(tab)
    out["forecast quantiles"] = pd.Series(qs, index=["50", "80", "90", "95", "99", "99.9"])
    # top 5% : by side, by vol ratio tercile, by settlement hour
    g = D[(D["pos"] % 4 == 0) & (D["absf"] >= qs[3])].copy()
    g["ex"] = g["sgn"] * (g["fr4"] - g["coin"].map(drift[4]))
    g["ex24"] = g["sgn"] * (g["fr24"] - g["coin"].map(drift[24]))
    g["side"] = np.where(g["sgn"] > 0, "long", "short")
    out["top5 by side (4h,24h %)"] = g.groupby("side")[["ex", "ex24"]].agg(["mean", "count"]) * [100, 1, 100, 1]
    g["settle"] = g["hour"].isin([0, 8, 16])
    out["top5 by settle hour close"] = g.groupby("settle")[["ex"]].agg(["mean", "count"])
    # vol ratio alone vs with signal: fade of last hour among all bars, by vr tercile
    a = D[(D["pos"] % 4 == 0)].dropna(subset=["vr", "r1", "fr4"]).copy()
    a["ex"] = -np.sign(a["r1"]) * (a["fr4"] - a["coin"].map(drift[4]))
    a["vrq"] = pd.qcut(a["vr"], 3, labels=["lowvr", "midvr", "highvr"])
    a["r1q"] = a.groupby("coin")["r1"].transform(lambda x: pd.qcut(x.abs().rank(method="first"), 5, labels=False))
    out["fade 4h % by vr tercile x |r1| quintile"] = (a.pivot_table(index="r1q", columns="vrq", values="ex", aggfunc="mean", observed=True) * 100)
    a["up"] = (a["fr4"] - a["coin"].map(drift[4]))
    out["raw excess 4h % by vr tercile (no signal)"] = a.groupby("vrq", observed=True)["up"].mean() * 100
    # turnover
    out["mean |alloc change| per bar"] = float(D["turn"].mean())
    out["mean |alloc|"] = float(D["alloc"].abs().mean())
    out["share bars alloc sign flips"] = float((np.sign(D["alloc"]) != np.sign(D.groupby(["coin", "w"])["alloc"].shift())).mean())
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    out["trades: gross, net % mean, dur h"] = pd.Series({"gross": T["profit_loss_percent"].mean(),
                                                     "net": T["net_profit_loss_percent"].mean(),
                                                     "dur_h": T["duration_minutes"].mean() / 60, "n": len(T)})
    return out
