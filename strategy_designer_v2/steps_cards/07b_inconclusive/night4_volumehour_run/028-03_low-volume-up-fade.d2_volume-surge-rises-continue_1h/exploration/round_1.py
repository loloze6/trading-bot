def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std().shift(1)
            vm = v.rolling(720, min_periods=240).mean().shift(1)
            z = r / sd; vr = v / vm
            df = pd.DataFrame({"z": z, "vr": vr, "fc": b["forecast"].astype(float),
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            for h in (1, 2, 3, 6, 12, 24):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["coin"] = coin; df["win"] = w; df["pos"] = np.arange(len(df))
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    # drift per horizon on grid
    drift = {}
    for h in (1, 2, 3, 6, 12, 24):
        g = d[d["pos"] % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
    for h in (1, 2, 3, 6, 12, 24):
        d[f"u{h}"] = d[f"f{h}"] - d["coin"].map(drift[h])
    # events: |z| big; one per 6-bar cell to keep independence
    d["cell"] = d["pos"] // 6
    def tab(mask, label_col):
        res = []
        e = d[mask].copy()
        for key, g in e.groupby(label_col, observed=True):
            g1 = g.groupby(["coin", "win", "cell"]).head(1)
            rec = {"grp": str(key), "n": len(g1)}
            for h in (1, 2, 3, 6, 12, 24):
                x = g1[f"u{h}"].dropna() * np.sign(g1.loc[x.index if False else g1.index, "z"]).loc[g1[f"u{h}"].dropna().index]
                rec[f"m{h}_bp"] = round(x.mean() * 1e4, 2)
                rec[f"t{h}"] = round(x.mean() / (x.std() / np.sqrt(len(x))), 2) if len(x) > 2 else np.nan
            res.append(rec)
        return pd.DataFrame(res)
    d["zb"] = pd.cut(d["z"].abs(), [3, 4, 6, 100])
    d["vb"] = pd.cut(d["vr"], [0, 1.5, 3, 5, 1000])
    d["side"] = np.where(d["z"] > 0, "up", "down")
    big = d["z"].abs() >= 3
    d["side_vb"] = d["side"] + "_" + d["vb"].astype(str)
    out["z>=3 by side x volume ratio (signed in move dir)"] = tab(big, "side_vb")
    d["side_zb"] = d["side"] + "_" + d["zb"].astype(str)
    surge = big & (d["vr"] >= 3)
    out["surge vr>=3, by side x z bucket"] = tab(surge, "side_zb")
    d["side_coin"] = d["side"] + "_" + d["coin"]
    out["surge by side x coin"] = tab(surge, "side_coin")
    d["side_year"] = d["side"] + "_" + d["year"].astype(str)
    out["surge by side x year"] = tab(surge, "side_year")
    # forecast bins on actual strategy
    d["fb"] = pd.cut(d["fc"], [0.001, 1, 5, 10, 20.1])
    out["by forecast bin (long, signed by z sign = up)"] = tab(d["fc"] > 0, "fb")
    return out
