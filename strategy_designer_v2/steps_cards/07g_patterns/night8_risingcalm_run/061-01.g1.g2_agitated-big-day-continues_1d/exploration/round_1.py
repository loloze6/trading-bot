def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.shift(1).rolling(30, min_periods=20).std()
            z = r / sd
            tr60 = c / c.shift(60) - 1
            rng = (b["high"] - b["low"]) / c
            clo = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            n = len(b)
            for h in (1, 5):
                pass
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            f2 = c.shift(-2) / c - 1
            df = pd.DataFrame({"coin": coin, "w": w, "ts": b["timestamp"], "z": z, "r": r, "f1": f1, "f2": f2, "f5": f5,
                               "agit": (b["regime"] != "chop").astype(int), "tr60": tr60, "clo": clo,
                               "pos": b["postRebalance_current_allocation"].astype(float), "grid5": (np.arange(n) % 5 == 0),
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday, "yr": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in ("f1", "f2", "f5"):
        d[h + "d"] = d[h] - d.groupby("coin")[h].transform("mean")
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    def ct(x, col):
        x = x.dropna(subset=[col])
        g = x.groupby("day")[col].agg(["sum", "count"])
        m = g["sum"].sum() / g["count"].sum()
        dev = x[col] - m
        s = dev.groupby(x["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / len(x)
        return pd.Series({"mean%": 100 * m, "t": m / se if se > 0 else np.nan, "n": len(x), "days": len(s)})
    out = {}
    g5 = d[d.grid5 & d.z.notna() & d.f5.notna()].copy()
    g5["sf5"] = np.sign(g5.z) * g5.f5d
    g5["zb"] = pd.cut(g5.z, [-99, -2, -1, 0, 1, 2, 99])
    out["f5 dem by z bucket x agit"] = g5.groupby(["agit", "zb"], observed=True).apply(lambda x: ct(x, "f5d")).round(3)
    g5["trend"] = np.where(g5.tr60 > 0.1, "rise", np.where(g5.tr60 < -0.1, "fall", np.where(g5.tr60.notna(), "chop", "na")))
    g5["big"] = (g5.z.abs() > 1.5)
    out["signed f5 big days by trend x agit"] = g5[g5.big].groupby(["trend", "agit"]).apply(lambda x: ct(x, "sf5")).round(3)
    # daily f1 (all bars, non-overlap trivially) by z bucket and side
    d1 = d[d.z.notna() & d.f1.notna()].copy()
    d1["zb"] = pd.cut(d1.z, [-99, -2, -1, 0, 1, 2, 99])
    out["f1 dem by z bucket x agit"] = d1.groupby(["agit", "zb"], observed=True).apply(lambda x: ct(x, "f1d")).round(3)
    out["f1 dem by weekday"] = d1.groupby("wd").apply(lambda x: ct(x, "f1d")).round(3)
    d1["cb"] = pd.cut(d1.clo, [-0.01, 0.2, 0.5, 0.8, 1.01])
    out["f1 dem by close loc x agit"] = d1.groupby(["agit", "cb"], observed=True).apply(lambda x: ct(x, "f1d")).round(3)
    # book: daily returns, largest gains/losses, by agit and year
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; dd.append(t)
    dd = pd.concat(dd)
    bk = dd.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    out["book by year"] = bk.groupby(pd.to_datetime(bk.index).year).agg(["mean", "count"]).round(5)
    q = bk.book_return.quantile([0.02, 0.98])
    out["coin ret on book extreme days"] = pd.DataFrame({
        "worst2%": bk[bk.book_return <= q.iloc[0]].mean(), "best2%": bk[bk.book_return >= q.iloc[1]].mean()}).round(4)
    out["pos side share"] = pd.Series({"long": (d.pos > 0).mean(), "short": (d.pos < 0).mean()}).round(3)
    return out
