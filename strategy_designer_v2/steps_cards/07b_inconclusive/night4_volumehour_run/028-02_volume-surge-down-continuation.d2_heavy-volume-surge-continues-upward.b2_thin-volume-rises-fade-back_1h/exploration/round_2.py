def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = [2, 4, 6]
    drift = {}
    for coin, wins in data["bars"].items():
        for h in H:
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr.append(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.concatenate(allr).mean()
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            r = c.pct_change()
            ma = r.abs().rolling(720, min_periods=720).mean()
            z = r / ma
            vr = v / v.rolling(720, min_periods=720).mean()
            r7 = c / c.shift(168) - 1
            vol30 = r.rolling(720).std()
            volrel = vol30 / vol30.rolling(2160, min_periods=720).mean()
            d = pd.DataFrame({"z": z, "vr": vr, "r7": r7, "volrel": volrel,
                              "fc": b["forecast"], "year": pd.to_datetime(b["timestamp"]).dt.year,
                              "hour": pd.to_datetime(b["timestamp"]).dt.hour,
                              "coin": coin, "pos": np.arange(len(b))})
            for h in H:
                d["f%d" % h] = (c.shift(-h) / c - 1 - drift[(coin, h)]).where(d["pos"] % h == 0)
            recs.append(d)
    D = pd.concat(recs, ignore_index=True)
    def summ(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean_%": 100 * x.mean() if n else np.nan,
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    # short-side of test's forecast cases (approx: forecast <= -2 on grid)
    S = D[(D.fc <= -2)].copy()
    S["short4"] = -S["f4"]
    S["fb"] = pd.cut(-S["fc"], [2, 5, 10, 15, 20.01])
    out["forecast<=-2 grid, short 4h by |fc|"] = S.groupby("fb", observed=True)["short4"].apply(summ).unstack()
    out["by year"] = S.groupby("year")["short4"].apply(summ).unstack()
    S["trend7"] = np.where(S.r7 > 0, "up7d", "down7d")
    out["by 7d trend"] = S.groupby("trend7")["short4"].apply(summ).unstack()
    S["vq"] = pd.cut(S.volrel, [0, 0.8, 1.2, 100])
    out["by vol regime"] = S.groupby("vq", observed=True)["short4"].apply(summ).unstack()
    S["hb"] = pd.cut(S.hour, [-1, 7, 15, 23])
    out["by hour block"] = S.groupby("hb", observed=True)["short4"].apply(summ).unstack()
    # heavy-volume continuation at 6h, brief's own idea
    Hv = D[(D.z.abs() > 3) & (D.vr > 2.5)].copy()
    Hv["c6"] = Hv["f6"] * np.sign(Hv["z"])
    Hv["side"] = np.where(Hv.z > 0, "up", "down")
    out["heavy cont 6h by side"] = Hv.groupby("side")["c6"].apply(summ).unstack()
    out["heavy cont 6h by year"] = Hv.groupby("year")["c6"].apply(summ).unstack()
    return out
