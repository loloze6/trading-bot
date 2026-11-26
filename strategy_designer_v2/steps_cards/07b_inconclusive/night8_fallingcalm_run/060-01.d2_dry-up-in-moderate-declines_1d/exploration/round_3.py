def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    H = (5, 10, 20)
    drift = {}
    for coin, wins in bars.items():
        drift[coin] = {}
        for h in H:
            allr = []
            for w, b in wins.items():
                c = b["close"].values.astype(float)
                idx = np.arange(0, len(c) - h, h)
                allr += list(c[idx + h] / c[idx] - 1)
            drift[coin][h] = np.mean(allr)
    def summ(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 3:
            return pd.Series({"n": len(x), "days": np.nan, "mean": np.nan, "t": np.nan})
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "days": D, "mean": m, "t": m / se if se > 0 else np.nan})
    for h in H:
        rows = []
        for coin, wins in bars.items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].values.astype(float)
                v = b["volume"].values.astype(float)
                ts = pd.to_datetime(b["timestamp"])
                n = len(b)
                for t in range(0, n - h, h):
                    if t < 59:
                        continue
                    tr = c[t] / c[t - 60] - 1 if t >= 60 else c[t] / c[0] - 1
                    if tr >= -0.10:
                        continue
                    vr = v[t-29:t+1].mean() / max(v[t-59:t-29].mean(), 1e-12)
                    rows.append({"coin": coin, "win": w, "year": ts[t].year, "day": ts[t].normalize(),
                                 "vr": vr, "fall20": c[t] / c[t-20] - 1,
                                 "u": -(c[t+h] / c[t] - 1 - drift[coin][h])})
        df = pd.DataFrame(rows)
        res = {}
        res["shrunk_all"] = summ(df[df.vr < 1], "u")
        res["grown_all"] = summ(df[df.vr >= 1], "u")
        sh = df[df.vr < 1].copy()
        q = pd.qcut(sh["vr"].rank(method="first"), 3, labels=["most_shrunk", "mid", "least_shrunk"])
        for lab in ["most_shrunk", "mid", "least_shrunk"]:
            g = sh[q == lab]
            r = summ(g, "u"); r["vr_max"] = g.vr.max(); res[f"vr_{lab}"] = r
        q2 = pd.qcut(sh["fall20"].rank(method="first"), 3, labels=["deep", "mid", "mild"])
        for lab in ["deep", "mid", "mild"]:
            g = sh[q2 == lab]
            r = summ(g, "u"); r["vr_max"] = g.fall20.max(); res[f"fall20_{lab}"] = r
        out[f"h{h}_falling_grid"] = pd.DataFrame(res).T
        if h == 20:
            out["h20_shrunk_by_year"] = pd.DataFrame({k: summ(g, "u") for k, g in sh.groupby("year")}).T
            out["h20_shrunk_by_coin"] = pd.DataFrame({k: summ(g, "u") for k, g in sh.groupby("coin")}).T
            sh2 = sh.copy(); sh2["dry"] = -np.log(sh2.vr)
            out["h20_corr_dry_u"] = float(sh2[["dry", "u"]].corr().iloc[0, 1])
            out["h20_corr_fall20_u"] = float(sh2[["fall20", "u"]].corr().iloc[0, 1])
    return out
