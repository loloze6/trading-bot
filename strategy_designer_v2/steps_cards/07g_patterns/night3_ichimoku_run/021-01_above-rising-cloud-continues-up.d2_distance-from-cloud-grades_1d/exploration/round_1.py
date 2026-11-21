def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "fc": b["forecast"].astype(float),
                "ret1": r1, "ret7": c / c.shift(7) - 1, "ret26": c / c.shift(26) - 1,
                "vol14": r1.rolling(14).std(),
                "dhigh26": c / h.rolling(26).max() - 1,
                "dlow26": c / l.rolling(26).min() - 1,
                "rng1": (h - l) / c,
                "f7": c.shift(-7) / c - 1, "f26": c.shift(-26) / c - 1, "f3": c.shift(-3) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for H, col in [(3, "f3"), (7, "f7"), (26, "f26")]:
        g = A[A["pos"] % H == 0].copy()
        g = g.dropna(subset=[col])
        g["ex"] = g[col] - g.groupby("coin")[col].transform("mean")
        res = []
        for s in ["fc", "ret1", "ret7", "ret26", "vol14", "dhigh26", "dlow26", "rng1"]:
            gg = g.dropna(subset=[s]).copy()
            gg["z"] = gg.groupby("coin")[s].transform(lambda x: (x - x.mean()) / x.std())
            gg["ez"] = gg.groupby("coin")["ex"].transform(lambda x: x / x.std())
            sl = stats.linregress(gg["z"], gg["ez"])
            q = gg.groupby("coin")[s].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
            m = gg.groupby(q)["ex"].mean()
            res.append({"signal": s, "n": len(gg), "slope": sl.slope, "t": sl.slope / sl.stderr,
                        "q1": m.iloc[0], "q3": m.iloc[2], "q5": m.iloc[4]})
        out[f"h{H}_signals"] = pd.DataFrame(res).round(4)
    # 26-day forecast check by coin
    g = A[A["pos"] % 26 == 0].dropna(subset=["f26", "fc"]).copy()
    g["ex"] = g["f26"] - g.groupby("coin")["f26"].transform("mean")
    bc = []
    for coin, gg in g.groupby("coin"):
        sl = stats.linregress(gg["fc"], gg["ex"])
        bc.append({"coin": coin, "n": len(gg), "t": sl.slope / sl.stderr, "corr": sl.rvalue})
    out["fc_by_coin"] = pd.DataFrame(bc).round(3)
    # weekday daily returns
    wd = A.dropna(subset=["ret1"]).groupby("wd")["ret1"].agg(["mean", "std", "count"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday"] = wd.round(5)
    # vol regime: daily return next 7d by vol quintile and sign of ret26
    g = A[A["pos"] % 7 == 0].dropna(subset=["f7", "vol14", "ret26"]).copy()
    g["ex"] = g["f7"] - g.groupby("coin")["f7"].transform("mean")
    g["vq"] = g.groupby("coin")["vol14"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    g["up"] = g["ret26"] > 0
    out["vol_x_trend_f7"] = g.groupby(["vq", "up"])["ex"].agg(["mean", "count"]).round(4)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D, ignore_index=True).dropna(subset=["book_return"])
    D["year"] = pd.to_datetime(D["day"]).dt.year
    yb = D.groupby("year")[["book_return", "coin_return"]].mean()
    out["book_by_year"] = (yb * 1e4).round(2)
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean", "median", "count"]).round(3)
    return out
