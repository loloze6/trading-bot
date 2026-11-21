def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []      # 120-bar grid cases
    rows24 = []    # 24-bar grid cases
    hr = []
    for coin, ws in data["bars"].items():
        # coin drift/std over 120 and 24 bars, all windows
        f120all, f24all = [], []
        prep = {}
        for w, b in ws.items():
            c = b["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            ratio = r24 / r24.abs().rolling(720, min_periods=120).mean()
            r168 = c / c.shift(168) - 1
            vol = c.pct_change().rolling(168, min_periods=48).std()
            volrel = vol / c.pct_change().rolling(720, min_periods=240).std()
            f120 = c.shift(-120) / c - 1
            f24 = c.shift(-24) / c - 1
            g120 = np.arange(0, len(c), 120)
            g24 = np.arange(0, len(c), 24)
            f120all += list(f120.iloc[g120].dropna())
            f24all += list(f24.iloc[g24].dropna())
            prep[w] = (c, ts, ratio, r168, volrel, f120, f24, g120, g24)
            r1 = c.pct_change()
            hr.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday, "r1": r1}))
        d120, s120 = np.mean(f120all), np.std(f120all)
        d24, s24 = np.mean(f24all), np.std(f24all)
        for w, (c, ts, ratio, r168, volrel, f120, f24, g120, g24) in prep.items():
            rows.append(pd.DataFrame({"coin": coin, "ratio": ratio.iloc[g120].values,
                "wk": r168.iloc[g120].values, "volrel": volrel.iloc[g120].values,
                "ex": (f120.iloc[g120] - d120).values, "st": ((f120.iloc[g120] - d120) / s120).values}))
            rows24.append(pd.DataFrame({"coin": coin, "ratio": ratio.iloc[g24].values,
                "wk": r168.iloc[g24].values, "volrel": volrel.iloc[g24].values,
                "ex": (f24.iloc[g24] - d24).values, "st": ((f24.iloc[g24] - d24) / s24).values}))
    A = pd.concat(rows).dropna(); B = pd.concat(rows24).dropna()
    bins = [-np.inf, -2, -1.3, -0.7, 0, 0.7, 1.3, 2, np.inf]
    def summ(df, key):
        g = df.groupby(key, observed=True)
        r = g.agg(n=("ex", "size"), mean_ex=("ex", "mean"), strength=("st", "mean"))
        r["t"] = g["ex"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan)
        return r.round(4)
    A["rb"] = pd.cut(A["ratio"], bins); B["rb"] = pd.cut(B["ratio"], bins)
    out["120h by 24h ratio bin"] = summ(A, "rb")
    out["24h by 24h ratio bin"] = summ(B, "rb")
    A["wkpos"] = A["wk"] > 0; B["wkpos"] = B["wk"] > 0
    out["120h by ratio bin x week sign"] = summ(A, ["wkpos", "rb"])
    A["vq"] = A.groupby("coin")["volrel"].transform(lambda x: pd.qcut(x, 5, labels=False))
    B["vq"] = B.groupby("coin")["volrel"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["120h by vol quintile"] = summ(A, "vq")
    out["24h by vol quintile"] = summ(B, "vq")
    A["wq"] = A.groupby("coin")["wk"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["120h by 7d return quintile"] = summ(A, "wq")
    H = pd.concat(hr).dropna()
    g = H.groupby("hour")["r1"]
    hh = pd.DataFrame({"mean_bps": g.mean() * 1e4, "t": g.mean() / (g.std() / np.sqrt(g.size()))}).round(2)
    out["hourly ret by hour"] = hh
    # book days
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.reset_index(drop=True).copy()
            d["coin"] = coin
            d["prev_coin"] = d["coin_return"].shift(1)
            d["next_coin"] = d["coin_return"].shift(-1)
            d["next_book"] = d["book_return"].shift(-1)
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            D.append(d)
    D = pd.concat(D).dropna(subset=["book_return"])
    D["bq"] = pd.qcut(D["book_return"].rank(method="first"), 10, labels=False)
    out["around book days decile"] = D.groupby("bq")[["book_return", "prev_coin", "coin_return", "next_coin", "next_book"]].mean().round(5)
    gw = D.groupby("wd")["coin_return"]
    out["coin daily by weekday"] = pd.DataFrame({"mean": gw.mean(), "t": gw.mean() / (gw.std() / np.sqrt(gw.size())), "n": gw.size()}).round(4)
    return out
