def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            sd30 = r.rolling(30, min_periods=20).std()
            tr60 = (c / c.shift(60) - 1) * 100
            r5 = c / c.shift(5) - 1
            prev = r.shift(1)
            df = pd.DataFrame({"coin": coin, "win": w, "ts": b["timestamp"], "r": r, "prev": prev, "nxt": nxt,
                               "sd30": sd30, "tr60": tr60, "z": r / sd30, "r5z": r5 / (sd30 * np.sqrt(5)),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["ts"] = pd.to_datetime(d["ts"]); d["day"] = d["ts"].dt.floor("D"); d["year"] = d["ts"].dt.year
    d["adj"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    medsd = d.groupby("coin")["sd30"].transform("median")
    d["agit"] = np.where(d["sd30"] > medsd, "agit", "calm")
    d["trend"] = pd.cut(d["tr60"], [-1e9, -10, 10, 1e9], labels=["falling", "choppy", "rising"])
    d = d.dropna(subset=["adj", "trend", "sd30", "prev"])
    def summ(g):
        x = g["adj"]
        if len(x) < 5: return pd.Series({"n": len(x), "mean%": np.nan, "t": np.nan})
        m = x.mean(); dev = (x - m).groupby(g["day"]).sum()
        se = np.sqrt((dev**2).sum()) / len(x)
        return pd.Series({"n": len(x), "days": g["day"].nunique(), "mean%": 100*m, "t": m/se})
    def slope(g, col):
        g = g.dropna(subset=[col]); x = g[col] - g[col].mean(); y = g["adj"]
        b = (x*y).sum()/(x*x).sum(); e = y - y.mean() - b*x
        se = np.sqrt(((x*e).groupby(g["day"]).sum()**2).sum())/(x*x).sum()
        return pd.Series({"n": len(g), "slope%": 100*b, "t": b/se})
    out = {}
    up = d[d["r"] > 0].copy()
    up["after"] = np.where(up["prev"] < 0, "after_down", "after_up")
    out["up_by_trend_after"] = up.groupby(["trend", "after"]).apply(summ)
    out["slope_upz_by_trend_after"] = up.groupby(["trend", "after"]).apply(lambda g: slope(g, "z"))
    out["slope_r5z_upday_by_trend"] = up.groupby("trend").apply(lambda g: slope(g, "r5z"))
    out["slope_r5z_all_by_trend_agit"] = d.groupby(["trend", "agit"]).apply(lambda g: slope(g, "r5z"))
    dn = d[d["r"] < 0]
    out["slope_downz_by_trend_agit"] = dn.groupby(["trend", "agit"]).apply(lambda g: slope(g, "z"))
    f = d[d["trend"] == "falling"].copy(); f["upday"] = f["r"] > 0
    out["falling_up_by_year"] = f[f["upday"]].groupby("year").apply(summ)
    out["falling_up_by_coin"] = f[f["upday"]].groupby("coin").apply(summ)
    # book: largest gains/losses
    bk = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            bk.append(dy.assign(coin=coin, win=w))
    bk = pd.concat(bk).dropna(subset=["book_return"])
    br = bk.groupby(["win", "day"])["book_return"].mean()
    s = br.sort_values()
    tot = br.sum()
    out["book_share_top10_gain_days"] = float(s.tail(10).sum()/tot)
    out["book_share_worst10_loss_days"] = float(s.head(10).sum()/tot)
    out["book_mean_by_window_%"] = (br.groupby(level=0).mean()*100)
    return out
