def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            z = b.get("debug_info.components.rise.last_history_value")
            z = z.astype(float).values if z is not None else np.full(n, np.nan)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # recompute vol-scaled return from prices too
            s = pd.Series(r1)
            sd20 = s.rolling(20, min_periods=15).std().shift(1).values
            zr = r1 / sd20
            r30 = np.r_[np.full(30, np.nan), c[30:] / c[:-30] - 1] if n > 30 else np.full(n, np.nan)
            vol_rank = sd20
            ts = pd.to_datetime(b["timestamp"])
            for t in range(n):
                f5 = c[t + 5] / c[t] - 1 if t + 5 < n else np.nan
                f1 = c[t + 1] / c[t] - 1 if t + 1 < n else np.nan
                rows.append((coin, w, t, t % 5 == 0, b["regime"].iloc[t], z[t], zr[t], r1[t], r30[t],
                             sd20[t], f1, f5, ts.iloc[t].dayofweek, ts.iloc[t].year,
                             b["postRebalance_current_allocation"].iloc[t]))
    df = pd.DataFrame(rows, columns=["coin", "w", "t", "grid", "regime", "z", "zr", "r1", "r30", "sd20",
                                     "f1", "f5", "dow", "year", "alloc"])
    drift5 = df[df.grid].groupby("coin")["f5"].mean()
    drift1 = df.groupby("coin")["f1"].mean()
    df["x5"] = df["f5"] - df["coin"].map(drift5)
    df["x1"] = df["f1"] - df["coin"].map(drift1)
    g = df[df.grid].dropna(subset=["x5", "zr"])

    def summ(d, col):
        m = d[col].mean(); sd = d[col].std(); k = d[col].count()
        return pd.Series({"n": k, "mean": m, "t": m / (sd / np.sqrt(k)) if k > 1 else np.nan})

    g = g.copy()
    g["zb"] = pd.cut(g["zr"], [-np.inf, -3, -2, -1, 0, 1, 2, 3, np.inf])
    out["x5 by day z bucket and regime (grid)"] = g.groupby(["regime", "zb"]).apply(lambda d: summ(d, "x5")).round(4)
    a = df.dropna(subset=["x1", "zr"]).copy()
    a["zb"] = pd.cut(a["zr"], [-np.inf, -3, -2, -1, 0, 1, 2, 3, np.inf])
    out["next-day x1 by z bucket and regime"] = a.groupby(["regime", "zb"]).apply(lambda d: summ(d, "x1")).round(4)
    g2 = df[df.grid].dropna(subset=["x5", "r30"]).copy()
    g2["q30"] = g2.groupby("coin")["r30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["x5 by 30d return quintile (per coin)"] = g2.groupby("q30").apply(lambda d: summ(d, "x5")).round(4)
    g3 = df[df.grid].dropna(subset=["x5", "sd20"]).copy()
    g3["qv"] = g3.groupby("coin")["sd20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    g3["big"] = pd.cut(g3["zr"], [-np.inf, -2, 2, np.inf], labels=["bigdown", "mid", "bigup"])
    out["x5 by vol tercile and move"] = g3.groupby(["qv", "big"]).apply(lambda d: summ(d, "x5")).round(4)
    out["x5 by regime and coin"] = df[df.grid].dropna(subset=["x5"]).groupby(["coin", "regime"]).apply(lambda d: summ(d, "x5")).round(4)
    out["next-day x1 by weekday"] = df.dropna(subset=["x1"]).groupby("dow").apply(lambda d: summ(d, "x1")).round(4)
    # book days
    dl = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dl.append(d)
    D = pd.concat(dl)
    bk = D.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book daily by year"] = bk.groupby(pd.to_datetime(bk.index.get_level_values("day")).year).agg(["count", "mean", "std"]).round(5)
    out["book by window mean"] = bk.groupby(level="w").mean().describe().round(5)
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr)
    out["trades by side"] = T.groupby("side")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["count", "mean"]).round(3)
    return out
