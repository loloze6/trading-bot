def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vr = r1.rolling(24).std() / r1.rolling(720, min_periods=240).std()
            r24 = c / c.shift(24) - 1
            f = b["forecast"].astype(float)
            hr = pd.to_datetime(b["timestamp"]).dt.hour
            vol = b["volume"].astype(float)
            vrel = vol / vol.rolling(168, min_periods=48).mean()
            d = pd.DataFrame({"coin": coin, "w": w, "f": f, "r1": r1, "vr": vr, "r24": r24,
                              "hclose": (hr + 1) % 24, "vrel": vrel, "pos": np.arange(len(b)),
                              "alloc": b["postRebalance_current_allocation"].astype(float)})
            for h in [1, 4, 8, 12, 24]:
                d[f"fr{h}"] = c.shift(-h) / c - 1
            d["dalloc"] = d["alloc"].diff().abs()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = {}
    for h in [1, 4, 8, 12, 24]:
        drift[h] = D[D["pos"] % h == 0].groupby("coin")[f"fr{h}"].mean()
    D["absf"] = D["f"].abs()
    D["sgn"] = np.sign(D["f"])
    D["pr"] = D["absf"].rank(pct=True, method="first")
    D["bucket"] = pd.cut(D["pr"], [0, 0.5, 0.8, 0.9, 0.95, 0.99, 0.999, 1.0001],
                         labels=["0-50", "50-80", "80-90", "90-95", "95-99", "99-99.9", "top0.1"])
    try:
        out["absf at pct 50/80/95/99/99.9"] = D["absf"].quantile([0.5, 0.8, 0.95, 0.99, 0.999])
    except Exception as e:
        out["q err"] = str(e)
    try:
        tab = {}
        for h in [1, 4, 8, 12, 24]:
            g = D[D["pos"] % h == 0].copy()
            g["ex"] = g["sgn"] * (g[f"fr{h}"] - g["coin"].map(drift[h]))
            g["tot"] = g["sgn"] * g[f"fr{h}"]
            m = g.groupby("bucket", observed=True)["ex"].agg(["mean", "count", "std"])
            tab[f"h{h}_ex%"] = m["mean"] * 100
            tab[f"h{h}_t"] = m["mean"] / (m["std"] / np.sqrt(m["count"]))
            tab[f"h{h}_tot%"] = g.groupby("bucket", observed=True)["tot"].mean() * 100
            if h in (4, 24):
                tab[f"n{h}"] = m["count"]
        out["signed move by |forecast| pct bucket"] = pd.DataFrame(tab)
    except Exception as e:
        out["bucket err"] = str(e)
    try:
        g = D[(D["pos"] % 4 == 0) & (D["pr"] >= 0.95)].copy()
        g["ex4"] = g["sgn"] * (g["fr4"] - g["coin"].map(drift[4]))
        g["ex12"] = g["sgn"] * (g["fr12"] - g["coin"].map(drift[12]))
        g["side"] = np.where(g["sgn"] > 0, "long", "short")
        out["top5 by side ex4% ex12%"] = g.groupby("side")[["ex4", "ex12"]].mean() * 100
        g["settle"] = g["hclose"].isin([0, 8, 16])
        out["top5 by settle-hour close ex4% / n"] = g.groupby("settle")["ex4"].agg(["mean", "count"]).assign(mean=lambda x: x["mean"] * 100)
        g["withtrend"] = np.sign(g["r1"]) == np.sign(g["r24"] - g["r1"])
        out["top5 hour move with 24h trend? ex4% / ex12%"] = g.groupby("withtrend")[["ex4", "ex12"]].mean() * 100
        g["hivol"] = g["vrel"] > g["vrel"].median()
        out["top5 by volume high? ex4%/ex12%"] = g.groupby("hivol")[["ex4", "ex12"]].mean() * 100
        out["top5 by year ex4%"] = g.assign(y=0).groupby("w")["ex4"].mean().describe() * 100
    except Exception as e:
        out["top5 err"] = str(e)
    try:
        a = D[D["pos"] % 4 == 0].dropna(subset=["vr", "r1", "fr4"]).copy()
        a["ex"] = -np.sign(a["r1"]) * (a["fr4"] - a["coin"].map(drift[4]))
        a["vrq"] = pd.cut(a["vr"].rank(pct=True), [0, 1/3, 2/3, 1.0001], labels=["lowvr", "midvr", "highvr"])
        a["r1q"] = pd.cut(a.groupby("coin")["r1"].transform(lambda x: x.abs().rank(pct=True)),
                          [0, .5, .8, .95, .99, 1.0001], labels=["0-50", "50-80", "80-95", "95-99", "99+"])
        out["fade4 ex% by |r1| pct x vr tercile"] = a.pivot_table(index="r1q", columns="vrq", values="ex", aggfunc="mean", observed=True) * 100
        a["up"] = a["fr4"] - a["coin"].map(drift[4])
        out["raw excess 4h% by vr tercile (no sign)"] = a.groupby("vrq", observed=True)["up"].mean() * 100
    except Exception as e:
        out["vr err"] = str(e)
    try:
        out["mean |alloc change| per bar"] = float(D["dalloc"].mean())
        out["mean |alloc|"] = float(D["alloc"].abs().mean())
        out["share bars sign of alloc flips"] = float((np.sign(D["alloc"]) != np.sign(D.groupby(["coin", "w"])["alloc"].shift())).mean())
    except Exception as e:
        out["alloc err"] = str(e)
    try:
        T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
        out["trades gross/net %, dur h, n"] = pd.Series({"gross": T["profit_loss_percent"].mean(),
                                                         "net": T["net_profit_loss_percent"].mean(),
                                                         "dur_h": T["duration_minutes"].mean() / 60, "n": len(T)})
        T["absf"] = T["entry_forecast"].abs()
        T["fq"] = pd.cut(T["absf"].rank(pct=True), [0, .5, .8, .95, 1.0001], labels=["0-50", "50-80", "80-95", "95+"])
        out["trades by |entry forecast| pct"] = T.groupby("fq", observed=True)[["profit_loss_percent", "net_profit_loss_percent", "duration_minutes"]].mean()
    except Exception as e:
        out["trades err"] = str(e)
    try:
        Y = pd.concat([d.assign(coin=c) for c, ws in data["days"].items() for d in ws.values()], ignore_index=True)
        out["mean daily book vs coin %"] = Y[["book_return", "coin_return"]].mean() * 100
    except Exception as e:
        out["days err"] = str(e)
    return out
