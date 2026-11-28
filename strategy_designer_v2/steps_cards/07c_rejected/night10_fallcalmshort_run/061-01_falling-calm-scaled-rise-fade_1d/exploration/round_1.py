def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std(ddof=1).shift(1)
            z = r / sd
            df = pd.DataFrame({"coin": coin, "win": w, "z": z, "r": r,
                               "regime": b["regime"].astype(str),
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            for h in (1, 2, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["sd"] = sd
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["f1"].mean()
    d["fc"] = d["regime"].isin(["mean_reversion", "unknown"])
    for h in (1, 2, 3, 5):
        d[f"u{h}"] = d[f"f{h}"] - h * d["coin"].map(drift)
    d["zb"] = pd.cut(d["z"], [-np.inf, -2, -1, -0.5, 0.5, 1, 2, np.inf])
    def tab(x):
        g = x.groupby("zb", observed=True)
        out = g["u1"].agg(["count", "mean"])
        out["t1"] = g["u1"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan)
        for h in (2, 3, 5):
            out[f"u{h}"] = g[f"u{h}"].mean()
        out["u1_over_sd"] = g.apply(lambda s: (s["u1"] / s["sd"]).mean())
        return out
    fc = d[d["fc"]]
    res = {}
    res["regime share"] = d["regime"].value_counts(normalize=True)
    res["falling calm by z bucket (unusual, long dir)"] = tab(fc)
    res["outside profile by z bucket"] = tab(d[~d["fc"]])
    big = fc[fc["z"] >= 1.5]
    res["fc z>=1.5 by coin"] = big.groupby("coin")[["u1", "u2", "u3"]].agg(["count", "mean"])
    res["fc z>=1.5 by year"] = big.groupby("year")["u1"].agg(["count", "mean"])
    dn = fc[fc["z"] <= -1.5]
    res["fc z<=-1.5 by coin"] = dn.groupby("coin")[["u1", "u2", "u3"]].agg(["count", "mean"])
    res["fc corr z vs u1, spearman"] = float(fc[["z", "u1"]].dropna().corr("spearman").iloc[0, 1])
    res["fc corr z vs u3, spearman"] = float(fc[["z", "u3"]].dropna().corr("spearman").iloc[0, 1])
    res["fc overall unusual u1 mean, n"] = f"{fc['u1'].mean():.5f}, {fc['u1'].count()}"
    return res
