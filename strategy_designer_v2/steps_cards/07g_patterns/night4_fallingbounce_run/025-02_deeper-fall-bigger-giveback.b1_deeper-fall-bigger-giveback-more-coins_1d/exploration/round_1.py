def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            z = r1 / vol20.shift(1)
            ret30 = c / c.shift(30) - 1
            ret10 = c / c.shift(10) - 1
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            df = pd.DataFrame({"coin": coin, "win": w, "z": z, "ret30": ret30, "ret10": ret10,
                               "vol20": vol20, "fwd5": fwd5, "fwd1": fwd1,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "yr": pd.to_datetime(b["timestamp"]).dt.year,
                               "rng": (b["high"] - b["low"]) / c,
                               "pos": np.arange(len(b))})
            daily.append(df)
            rows.append(df[df["pos"] % 5 == 0])
    g = pd.concat(rows); d = pd.concat(daily)
    g = g.dropna(subset=["fwd5"])
    st = g.groupby("coin")["fwd5"].agg(["mean", "std"])
    g = g.join(st, on="coin")
    g["ex"] = g["fwd5"] - g["mean"]; g["exs"] = g["ex"] / g["std"]
    out = {}
    gg = g.dropna(subset=["z", "ret30"])
    gg["zb"] = pd.cut(gg["z"], [-99, -2, -1, 1, 2, 99])
    gg["tr"] = np.where(gg["ret30"] < 0, "down30", "up30")
    out["fwd5 excess by z bucket x 30d sign"] = gg.groupby(["tr", "zb"])["exs"].agg(
        ["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))]).rename(columns={"<lambda_0>": "t"})
    def reg(x, y):
        m = ~(np.isnan(x) | np.isnan(y))
        r = stats.linregress(x[m], y[m]); return pd.Series({"n": m.sum(), "slope": r.slope, "t": r.slope / r.stderr})
    # ranks within coin
    for col in ["z", "ret30", "ret10", "vol20", "rng"]:
        gg[col + "_r"] = gg.groupby("coin")[col].rank(pct=True) - 0.5
    out["regressions of scaled excess fwd5"] = pd.DataFrame({c: reg(gg[c + "_r"].values, gg["exs"].values)
                                                for c in ["z", "ret30", "ret10", "vol20", "rng"]}).T
    out["ret30 slope by 30d sign"] = pd.DataFrame({k: reg(v["ret30_r"].values, v["exs"].values) for k, v in gg.groupby("tr")}).T
    gg["vq"] = gg.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["fwd5 raw by vol quartile"] = gg.groupby("vq")["fwd5"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    dd = d.dropna(subset=["fwd1"])
    out["next-day return by weekday"] = dd.groupby("wd")["fwd1"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    out["fwd5 excess by year"] = gg.groupby("yr")["exs"].agg(["count", "mean"])
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bk.append(x.assign(coin=coin))
    bk = pd.concat(bk).dropna(subset=["book_return"])
    act = bk[bk["book_return"].abs() > 1e-9]
    out["book active days"] = pd.Series({"n_active": len(act), "mean": act["book_return"].mean(),
                                         "corr_with_coin": act["book_return"].corr(act["coin_return"])})
    return out
