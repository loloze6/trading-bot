def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            z = r1 / vol20
            tr = c / c.shift(60) - 1
            tr20 = c / c.shift(20) - 1
            vol30 = r1.rolling(30).std()
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            f3 = c.shift(-3) / c - 1
            f1 = c.shift(-1) / c - 1
            n = len(b)
            idx = np.arange(0, n, 3)
            d = pd.DataFrame({
                "coin": coin, "w": w, "z": z.values[idx], "r1": r1.values[idx],
                "tr60": tr.values[idx], "tr20": tr20.values[idx], "rng": rng.values[idx],
                "clpos": clpos.values[idx], "f3": f3.values[idx], "f1": f1.values[idx],
                "inprof": (b["regime"].values[idx] == "unknown"),
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek.values[idx],
                "pos": b["postRebalance_current_allocation"].values[idx],
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D").values[idx],
            })
            rows.append(d)
    df = pd.concat(rows)
    drift = df.groupby("coin")["f3"].transform("mean")
    df["u3"] = df["f3"] - drift
    df = df.dropna(subset=["u3"])
    def summ(g, col="u3"):
        x = g[col].dropna()
        if len(x) < 3: return pd.Series({"n": len(x), "mean%": np.nan, "t": np.nan})
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    df["zb"] = pd.cut(df["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    out = {}
    out["inprof_by_z"] = df.groupby(["inprof", "zb"]).apply(summ)
    df["trb"] = pd.cut(df["tr60"], [-9, -0.3, -0.1, 0.1, 0.3, 9])
    out["by_trend60"] = df.groupby("trb").apply(summ)
    df["tr20b"] = pd.qcut(df["tr20"], 5)
    out["by_tr20_quint"] = df.groupby("tr20b").apply(summ)
    df["clb"] = pd.cut(df["clpos"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    out["by_closepos"] = df.groupby("clb").apply(summ)
    df["rngb"] = pd.qcut(df["rng"], 5)
    out["by_range_quint"] = df.groupby("rngb").apply(summ)
    out["by_weekday_f1"] = df.assign(u1=df["f1"] - df.groupby("coin")["f1"].transform("mean")).groupby("wd").apply(lambda g: summ(g, "u1"))
    out["by_window"] = df[df.inprof].groupby("w").apply(summ)
    # correlations overall
    cc = df.dropna(subset=["z"])
    out["corr_z_u3_all"] = float(stats.pearsonr(cc["z"], cc["u3"])[0])
    out["n_all"] = int(len(cc))
    # book
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(d.assign(coin=coin, w=w))
    bd = pd.concat(bd)
    book = bd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = book.groupby("w").agg(["mean", "count"]) * 1
    return out
