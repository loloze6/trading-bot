def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [24, 36, 48, 72]
    rows = []
    for coin, wins in data["bars"].items():
        drift = {}
        for h in H:
            vals = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals.append(c[idx + h] / c[idx] - 1)
            drift[h] = np.nanmean(np.concatenate(vals))
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = b["close"].pct_change()
            vol = r1.rolling(24).std()
            z = r1 / vol
            df = pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values,
                               "z": z.values, "r1": r1.values})
            for h in H:
                df["r%d" % h] = (b["close"].shift(-h) / b["close"] - 1).values - drift[h]
            rows.append(df[df["hour"] == 0])
    D = pd.concat(rows, ignore_index=True)
    D = D[np.isfinite(D["z"])].dropna(subset=["z", "r24"])
    D["sgn"] = -np.sign(D["z"]); D["az"] = D["z"].abs()
    out = {}
    def summ(g, h=24):
        x = (g["sgn"] * g["r%d" % h]).dropna()
        n = len(x)
        return pd.Series({"n": n, "mean_pct": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)),
                          "per_unit_pct": 100 * (g["sgn"] * g["r%d" % h]).sum() / g.loc[x.index, "az"].sum()})
    out["horizons"] = pd.DataFrame({h: summ(D.dropna(subset=["r%d" % h]), h) for h in H}).T
    bins = [0, 0.5, 1, 1.5, 2, 3, 4, 100]
    D["b"] = pd.cut(D["az"], bins)
    out["fine_bins_24"] = D.groupby("b", observed=True).apply(summ)
    out["by_weekday_24"] = D.groupby("wd").apply(summ)
    y = D["r24"].values
    fits = {}
    for name, x in {"z": D["z"], "sign": np.sign(D["z"]), "sqrt": np.sign(D["z"]) * np.sqrt(D["az"]),
                    "z|z|": D["z"] * D["az"], "raw_r1": D["r1"]}.items():
        s = stats.linregress(x.values, y)
        fits[name] = {"t": s.slope / s.stderr, "r2": s.rvalue ** 2}
    out["fits_24"] = pd.DataFrame(fits).T
    q = D["az"].quantile(2 / 3)
    out["top_third_vs_rest_per_unit"] = pd.DataFrame({"top": summ(D[D["az"] > q]), "rest": summ(D[D["az"] <= q])}).T
    return out
