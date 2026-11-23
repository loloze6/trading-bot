def explore(data):
    import numpy as np, pandas as pd
    H = [4, 12, 24, 48]
    rows = []
    for coin, wins in data["bars"].items():
        acc = {h: [] for h in H}
        sd = {}
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                acc[h].extend(list(c[idx + h] / c[idx] - 1))
        drift = {h: np.mean(acc[h]) for h in H}
        sd = {h: np.std(acc[h], ddof=1) for h in H}
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            z = r / vol.shift(1)
            ret24 = c / c.shift(24) - 1
            ret72 = c / c.shift(72) - 1
            volreg = vol / vol.rolling(720, min_periods=200).median()
            ts = pd.to_datetime(d["timestamp"])
            n = len(d)
            cell = np.arange(n) // 24
            for thr in [-1.5, -2.5, -3.5]:
                mask = (z <= thr).values
                seen = set()
                for i in np.where(mask)[0]:
                    if cell[i] in seen:
                        continue
                    seen.add(cell[i])
                    if i + 24 >= n:
                        continue
                    rec = {"coin": coin, "thr": thr, "z": z[i], "year": ts.iloc[i].year,
                           "ret24": ret24[i], "ret72": ret72[i], "volreg": volreg[i]}
                    for h in H:
                        rec["u%d" % h] = (c[i + h] / c[i] - 1 - drift[h]) if i + h < n else np.nan
                    rec["s24"] = rec["u24"] / sd[24]
                    rows.append(rec)
    ev = pd.DataFrame(rows)
    def summ(g, col="u24"):
        x = g[col].dropna(); n = len(x); m = x.mean()
        return pd.Series({"n": n, "mean": m, "t": m / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    out["by_thr"] = pd.concat({h: ev.groupby("thr").apply(lambda g: summ(g, h)) for h in ["u4", "u12", "u24", "u48", "s24"]}, axis=1)
    e = ev[ev["thr"] == -2.5].copy()
    e["zb"] = pd.cut(e["z"], [-np.inf, -5, -4, -3, -2.5])
    out["t25_by_z"] = pd.concat({h: e.groupby("zb").apply(lambda g: summ(g, h)) for h in ["u4", "u24", "u48"]}, axis=1)
    e["vr"] = pd.qcut(e["volreg"], 4)
    out["t25_by_volreg"] = pd.concat({h: e.groupby("vr").apply(lambda g: summ(g, h)) for h in ["u4", "u24", "s24"]}, axis=1)
    e["tr"] = pd.cut(e["ret72"], [-np.inf, -0.08, -0.03, 0, 0.03, np.inf])
    out["t25_by_prior72"] = e.groupby("tr").apply(summ)
    out["t25_by_year"] = e.groupby("year").apply(summ)
    out["t25_by_coin"] = e.groupby("coin").apply(summ)
    hv = e[e["volreg"] > e["volreg"].median()]
    hv = hv.assign(zb=pd.cut(hv["z"], [-np.inf, -4, -3, -2.5]))
    out["t25_highvol_by_z"] = hv.groupby("zb").apply(summ)
    out["t25_highvol_by_year"] = hv.groupby("year").apply(summ)
    e2 = ev[ev["thr"] == -1.5].copy()
    e2["vr"] = pd.qcut(e2["volreg"], 4)
    out["t15_by_volreg"] = pd.concat({h: e2.groupby("vr").apply(lambda g: summ(g, h)) for h in ["u4", "u24", "s24"]}, axis=1)
    return out
