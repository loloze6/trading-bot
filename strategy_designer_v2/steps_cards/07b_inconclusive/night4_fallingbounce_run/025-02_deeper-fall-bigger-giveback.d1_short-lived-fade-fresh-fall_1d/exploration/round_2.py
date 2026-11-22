def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=20).std().shift(1)
            z = r1 / vol
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "z": z, "r90": c / c.shift(90) - 1, "r30": c / c.shift(30) - 1})
            for h in [1, 2, 3]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = {h: A[A["pos"] % h == 0].groupby("coin")[f"f{h}"].mean() for h in [1, 2, 3]}
    usual = {h: A[A["pos"] % h == 0].groupby("coin")[f"f{h}"].std() for h in [1, 2, 3]}
    def stat(sub, h):
        v = (-(sub[f"f{h}"] - sub["coin"].map(drift[h]))).dropna()
        n = len(v)
        s = (v / sub.loc[v.index, "coin"].map(usual[h])).mean()
        return pd.Series({"n": n, "mean": v.mean(), "t": v.mean() / (v.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "total": (-sub[f"f{h}"]).mean(), "strength": s})
    out = {}
    res = []
    for h in [1, 2, 3]:
        g = A[A["pos"] % h == 0]
        for name, m in [("r90neg", g["r90"] < 0), ("r90neg_r30neg", (g["r90"] < 0) & (g["r30"] < 0)),
                        ("r90pos", g["r90"] > 0)]:
            for zl in [1.0, 1.5, 2.0]:
                s = g[m & (g["z"] > zl)]
                r = stat(s, h); r["h"] = h; r["set"] = name; r["zmin"] = zl; res.append(r)
    out["pooled"] = pd.DataFrame(res)[["set", "h", "zmin", "n", "mean", "t", "total", "strength"]]
    # graded slope among rises, 1-day
    slopes = []
    for h in [1, 2, 3]:
        g = A[A["pos"] % h == 0]
        for name, m in [("r90neg", g["r90"] < 0), ("r90pos", g["r90"] > 0)]:
            s = g[m & (g["z"] > 0)].dropna(subset=["z", f"f{h}"])
            y = -(s[f"f{h}"] - s["coin"].map(drift[h]))
            lr = stats.linregress(s["z"].clip(upper=5), y)
            slopes.append(pd.Series({"set": name, "h": h, "n": len(s), "slope": lr.slope, "t": lr.slope / lr.stderr}))
    out["slope_short_on_z"] = pd.DataFrame(slopes)
    g = A[(A["r90"] < 0) & (A["z"] > 1.5)]
    out["h1_r90neg_z>1.5_by_coin"] = g.groupby("coin").apply(lambda s: stat(s, 1))
    out["h1_r90neg_z>1.5_by_year"] = g.groupby("year").apply(lambda s: stat(s, 1))
    return out
