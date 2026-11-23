def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allg = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            allg.append(c[idx + 24] / c[idx] - 1)
        drift = np.concatenate(allg).mean()
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            ch = (ts.dt.hour + 1) % 24
            r1 = c.pct_change()
            r2 = c / c.shift(2) - 1
            z2 = r2 / r2.abs().rolling(720, min_periods=200).mean()
            r24 = c / c.shift(24) - 1
            z24 = r24 / r24.abs().rolling(720, min_periods=200).mean()
            f24 = c.shift(-24) / c - 1 - drift
            nxt1 = c.shift(-1) / c - 1
            vrel = r1.rolling(168).std() / r1.rolling(720).std()
            volrel = d["volume"] / d["volume"].rolling(168, min_periods=48).median()
            rows.append(pd.DataFrame({"coin": coin, "w": w, "ch": ch.values, "wd": ts.dt.weekday.values,
                                      "z2": z2, "z24": z24, "f24": f24, "nxt1": nxt1, "vrel": vrel,
                                      "volrel": volrel, "pos": np.arange(len(d))}))
    A = pd.concat(rows, ignore_index=True)
    out = {}

    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean_bp": x.mean() * 1e4,
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    h = A.groupby("ch")["nxt1"].apply(tt).unstack()
    h["volrel_med"] = A.groupby("ch")["volrel"].median()
    out["next 1h return by close hour (bp)"] = h.round(3)

    def hourrow(g):
        g = g.dropna(subset=["z2", "f24"])
        fall = g[g.z2 <= -1.5]["f24"]
        rise = g[g.z2 >= 1.5]["f24"]
        rho = stats.spearmanr(g.z2, g.f24).correlation
        return pd.Series({"n_fall": len(fall), "fall_f24_bp": fall.mean() * 1e4,
                          "fall_t": fall.mean() / (fall.std() / np.sqrt(len(fall))),
                          "rise_f24_bp": rise.mean() * 1e4,
                          "rise_t": rise.mean() / (rise.std() / np.sqrt(len(rise))),
                          "spearman_z2_f24": rho})
    out["24h excess after 2h move, by close hour"] = A.groupby("ch").apply(hourrow).round(3)

    G = A[A.pos % 24 == 0].dropna(subset=["f24"])
    g = G.dropna(subset=["z24"])
    q = pd.qcut(g.z24, 5, labels=False)
    out["grid: f24 by 24h-move quintile"] = g.groupby(q)["f24"].apply(tt).unstack().round(3)
    g = G.dropna(subset=["vrel"])
    q = pd.qcut(g.vrel, 5, labels=False)
    out["grid: f24 by vol-ratio quintile"] = g.groupby(q)["f24"].apply(tt).unstack().round(3)
    g = G.dropna(subset=["volrel"])
    q = pd.qcut(g.volrel, 5, labels=False)
    out["grid: f24 by volume-ratio quintile"] = g.groupby(q)["f24"].apply(tt).unstack().round(3)
    out["grid: f24 by weekday"] = G.groupby("wd")["f24"].apply(tt).unstack().round(3)

    D = pd.concat([df.assign(coin=c, w=w) for c, ws in data["days"].items() for w, df in ws.items()])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book daily by weekday"] = D.groupby("wd")["book_return"].apply(tt).unstack().round(3)
    out["book daily by year"] = D.groupby("year").agg(book_bp=("book_return", lambda x: x.mean() * 1e4),
                                                     coin_bp=("coin_return", lambda x: x.mean() * 1e4)).round(2)
    return out
