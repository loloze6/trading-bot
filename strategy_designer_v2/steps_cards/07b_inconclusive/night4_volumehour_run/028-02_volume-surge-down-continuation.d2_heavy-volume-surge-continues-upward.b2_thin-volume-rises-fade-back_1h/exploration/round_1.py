def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    recs = []
    H = [1, 2, 4, 6, 12]
    drift = {}
    usual = {}
    for coin, wins in data["bars"].items():
        for h in H:
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr.append(c[idx + h] / c[idx] - 1)
            allr = np.concatenate(allr)
            drift[(coin, h)] = allr.mean(); usual[(coin, h)] = allr.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            r = c.pct_change()
            ma = r.abs().rolling(720, min_periods=720).mean()
            z = r / ma
            vr = v / v.rolling(720, min_periods=720).mean()
            yr = pd.to_datetime(b["timestamp"]).dt.year
            d = pd.DataFrame({"z": z, "vr": vr, "year": yr, "coin": coin, "win": w, "pos": np.arange(len(b))})
            for h in H:
                fr = c.shift(-h) / c - 1 - drift[(coin, h)]
                d["f%d" % h] = fr.where(d["pos"] % h == 0)
            recs.append(d)
    D = pd.concat(recs, ignore_index=True).dropna(subset=["z", "vr"])
    D["sgn"] = np.sign(D["z"])
    D["zb"] = pd.cut(D["z"].abs(), [0, 1, 2, 3, 4, 6, 100])
    D["vb"] = pd.cut(D["vr"], [0, 0.7, 1, 1.5, 2.5, 4, 1000])
    out = {}
    def summ(g, col):
        x = (g[col] * g["sgn"]).dropna()
        n = len(x)
        return pd.Series({"n": n, "mean_cont_%": 100 * x.mean() if n else np.nan,
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    out["4h cont by |z| x vol (rises)"] = D[D.sgn > 0].groupby(["vb", "zb"], observed=True).apply(lambda g: summ(g, "f4")).query("n>30")
    out["4h cont by |z| x vol (falls)"] = D[D.sgn < 0].groupby(["vb", "zb"], observed=True).apply(lambda g: summ(g, "f4")).query("n>30")
    big = D[(D.z > 2) & (D.vr <= 1)]
    rows = {}
    for h in H:
        rows[h] = summ(big, "f%d" % h)
    out["thin rise z>2, cont by horizon"] = pd.DataFrame(rows).T
    out["thin rise z>2, 4h by year"] = big.groupby("year").apply(lambda g: summ(g, "f4"))
    out["thin rise z>2, 4h by coin"] = big.groupby("coin").apply(lambda g: summ(g, "f4"))
    heavy = D[(D.z.abs() > 3) & (D.vr > 2.5)]
    rows = {}
    for h in H:
        rows[h] = summ(heavy, "f%d" % h)
    out["heavy |z|>3 vr>2.5 cont by horizon"] = pd.DataFrame(rows).T
    out["usual 4h"] = pd.Series({str(k): v for k, v in usual.items() if k[1] == 4})
    return out
