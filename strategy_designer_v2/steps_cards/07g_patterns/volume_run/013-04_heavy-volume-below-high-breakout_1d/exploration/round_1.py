def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            n = len(b)
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(n),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "ret5p": c / c.shift(5) - 1,
                "ret20p": c / c.shift(20) - 1,
                "dist30": c / b["high"].astype(float).rolling(30, min_periods=30).max() - 1,
                "vol20": r1.rolling(20).std(),
                "vr": v.rolling(10).mean() / v.rolling(30).mean(),
                "f1": c.shift(-1) / c - 1,
                "f5": c.shift(-5) / c - 1,
                "f10": c.shift(-10) / c - 1,
                "trend": (b["regime"] == "trending").astype(int),
                "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # excess over coin mean (non-overlap grid)
    for h in [5, 10]:
        g = A[A.pos % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"] = A[f"f{h}"] - A.coin.map(m)
    m1 = A.groupby("coin")["f1"].mean(); A["x1"] = A.f1 - A.coin.map(m1)

    def bucket(var, h, q=5):
        g = A[(A.pos % h == 0)].dropna(subset=[var, f"x{h}"]).copy()
        g["q"] = g.groupby("coin")[var].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = g.groupby("q")[f"x{h}"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        sl = stats.linregress(g["q"], g[f"x{h}"])
        t.loc["slope_t"] = [sl.slope, len(g), np.nan, sl.slope / sl.stderr]
        return t.round(4)
    out["ret5p_vs_x5"] = bucket("ret5p", 5)
    out["ret20p_vs_x10"] = bucket("ret20p", 10)
    out["dist30_vs_x10"] = bucket("dist30", 10)
    out["vol20_vs_x10"] = bucket("vol20", 10)
    out["vr_vs_x10"] = bucket("vr", 10)
    out["vr_vs_x5"] = bucket("vr", 5)
    wd = A.dropna(subset=["x1"]).groupby("wd")["x1"].agg(["mean", "count", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday_x1"] = wd.round(5)
    tr = A[A.pos % 10 == 0].dropna(subset=["x10"]).groupby("trend")["x10"].agg(["mean", "count", "std"])
    out["trend_vs_x10"] = tr.round(4)
    # book daily stats by year
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    by = D.groupby("year")[["book_return", "coin_return"]].mean()
    out["book_by_year"] = (by * 1e4).round(2)
    # trades
    T = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["dq"] = pd.qcut(T["dur_d"].rank(method="first"), 4, labels=False)
    out["trades_by_duration"] = T.groupby("dq").agg(n=("net_profit_loss_percent", "size"),
        dur=("dur_d", "mean"), pnl=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean())).round(3)
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    return out
