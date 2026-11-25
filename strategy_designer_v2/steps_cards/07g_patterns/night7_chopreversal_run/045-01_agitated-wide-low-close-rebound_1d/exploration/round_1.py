def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            h, l, c, o = b["high"], b["low"], b["close"], b["open"]
            rng = (h - l)
            base = rng.shift(1).rolling(30, min_periods=20).mean()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "clv": (c - l) / rng.replace(0, np.nan),
                "rw": rng / base,
                "ret0": c / c.shift(1) - 1,
                "body": (c - o) / rng.replace(0, np.nan),
                "nxt": c.shift(-1) / c - 1,
                "nxt2": c.shift(-2) / c - 1,
                "agit": (b["regime"] != "chop").astype(int),
                "alloc": b["postRebalance_current_allocation"],
                "tr60": c / c.shift(60) - 1,
                "vol20": (c / c.shift(1) - 1).rolling(20).std(),
            })
            d["gain"] = d["alloc"] * d["nxt"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["nxt"].transform("mean")
    D["dm"] = D["nxt"] - mu
    D["day"] = D["ts"].dt.floor("D")
    out = {}

    def tday(s, days):
        g = pd.DataFrame({"s": s, "d": days}).dropna().groupby("d")["s"].sum()
        n = len(s.dropna())
        m = s.mean()
        se = np.sqrt((g - g.mean() * 0).pow(2).sum()) / max(n, 1)
        return m, (s - m).groupby(days).sum().pow(2).sum() ** 0.5 / n

    def cell(x):
        x = x.dropna(subset=["dm"])
        m = x["dm"].mean()
        dev = (x["dm"] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(x) if len(x) else np.nan
        return pd.Series({"n": len(x), "mean%": 100 * m, "t": m / se if se else np.nan})

    D["clvq"] = pd.qcut(D["clv"], 5, labels=False, duplicates="drop")
    D["rwq"] = pd.qcut(D["rw"], 3, labels=["narrow", "mid", "wide"])
    out["agit x clv quintile"] = D.groupby(["agit", "clvq"]).apply(cell)
    out["agit x width x clv(low/high)"] = D[D["clvq"].isin([0, 4])].groupby(["agit", "rwq", "clvq"]).apply(cell)
    D["r0q"] = pd.qcut(D["ret0"], 5, labels=False)
    out["agit x ret0 quintile"] = D.groupby(["agit", "r0q"]).apply(cell)
    D["trend"] = np.where(D["tr60"] > 0.1, "rising", np.where(D["tr60"] < -0.1, "falling", np.where(D["tr60"].notna(), "choppy", None)))
    out["trend x agit x clv low/high"] = D[D["clvq"].isin([0, 4])].groupby(["trend", "agit", "clvq"]).apply(cell)
    D["wd"] = D["ts"].dt.weekday
    out["weekday all"] = D.groupby("wd").apply(cell)
    out["weekday held gain mean% (agit)"] = D[D["alloc"].abs() > 0].groupby("wd")["gain"].agg(["count", "mean"]).assign(mean=lambda x: 100 * x["mean"])
    # correlations by agit
    cr = {}
    for a in [0, 1]:
        x = D[D["agit"] == a].dropna(subset=["clv", "dm", "rw", "ret0"])
        cr[a] = {"corr clv": stats.spearmanr(x["clv"], x["dm"])[0],
                 "corr ret0": stats.spearmanr(x["ret0"], x["dm"])[0],
                 "corr clv*rw": stats.spearmanr(x["clv"] * x["rw"], x["dm"])[0],
                 "corr body": stats.spearmanr(x["body"], x["dm"])[0], "n": len(x)}
    out["spearman by agit"] = pd.DataFrame(cr)
    # book gains by window and coin
    days = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            days.append(d.assign(coin=coin, win=w))
    Dy = pd.concat(days)
    out["book by window"] = Dy.groupby("win")[["book_return", "coin_return"]].mean() * 100
    out["book by coin"] = Dy.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std"]) * 100
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades by duration"] = T.groupby(pd.cut(T["dur_d"], [0, 1.5, 3, 7, 1000]))["net_profit_loss_percent"].agg(["count", "mean"])
    return out
