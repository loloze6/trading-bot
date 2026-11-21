def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            c = df["close"].astype(float).reset_index(drop=True)
            n = len(c)
            r24 = c / c.shift(24) - 1
            scale = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            z = r24 / scale
            r72p = c / c.shift(72) - 1
            z72 = r72p / (r72p.abs().rolling(720, min_periods=120).mean().shift(1))
            hi = c.rolling(720, min_periods=240).max(); lo = c.rolling(720, min_periods=240).min()
            pos = (c - lo) / (hi - lo)
            lr = np.log(c).diff()
            volratio = lr.rolling(24).std() / lr.rolling(720, min_periods=240).std()
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            for h in (24, 72, 168):
                idx = np.arange(0, n - h, h)
                f = c.values[idx + h] / c.values[idx] - 1
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "z": z.values[idx], "z72": z72.values[idx],
                                          "pos": pos.values[idx], "vr": volratio.values[idx],
                                          "hour": ts.dt.hour.values[idx], "wd": ts.dt.weekday.values[idx], "f": f}))
    R = pd.concat(rows, ignore_index=True)
    g = R.groupby(["coin", "h"])["f"]
    R["drift"] = g.transform("mean"); R["sd"] = g.transform("std")
    R["s"] = (R["f"] - R["drift"]) / R["sd"]
    def tab(col, bins, h):
        d = R[(R.h == h)].dropna(subset=[col])
        d = d.assign(b=pd.cut(d[col], bins))
        a = d.groupby("b", observed=True)["s"].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["unusual_pct"] = d.groupby("b", observed=True).apply(lambda x: (x.f - x.drift).mean() * 100)
        return a.drop(columns="std").round(3)
    zb = [-99, -3, -2, -1, -0.5, 0, 0.5, 1, 2, 3, 99]
    for h in (24, 72, 168):
        out[f"z24 -> fwd {h}h strength"] = tab("z", zb, h)
    out["z72 -> fwd 168h"] = tab("z72", zb, 168)
    out["z72 -> fwd 72h"] = tab("z72", zb, 72)
    pb = [-0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.97, 1.01]
    out["range pos -> fwd 72h"] = tab("pos", pb, 72)
    out["range pos -> fwd 168h"] = tab("pos", pb, 168)
    out["volratio -> fwd 72h"] = tab("vr", [0, 0.5, 0.75, 1, 1.5, 2, 3, 99], 72)
    # per-coin spearman z vs s at 168h
    sp = {}
    for coin in R.coin.unique():
        for h in (24, 72, 168):
            d = R[(R.coin == coin) & (R.h == h)].dropna(subset=["z"])
            sp[(coin, h)] = stats.spearmanr(d.z, d.s)[0]
    out["spearman z24 vs strength"] = pd.Series(sp).unstack().round(3)
    # book: daily
    D = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D)
    D["day_ts"] = pd.to_datetime(D["day"])
    D["wd"] = D.day_ts.dt.weekday
    out["book by weekday"] = D.groupby("wd")[["book_return", "coin_return"]].mean().mul(1e4).round(1)
    D["yr"] = D.day_ts.dt.year
    out["book by year bps"] = D.groupby("yr")[["book_return", "coin_return"]].mean().mul(1e4).round(1)
    return out
