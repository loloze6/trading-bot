def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    H = [1, 3, 5, 10]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            s20 = r.rolling(20).std()
            sma = c.rolling(20).mean()
            z = (c - sma) / sma / s20
            ret1z = r / s20
            r5 = c / c.shift(5) - 1
            r5z = r5 / (s20 * np.sqrt(5))
            rng = (b["high"] - b["low"]) / c / s20
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            vol30 = r.rolling(30).std()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": z, "r1z": ret1z,
                               "r5z": r5z, "rng": rng, "clpos": clpos, "vol30": vol30,
                               "chop": (b["regime"] != "chop").astype(int),
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            for h in H:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin per horizon from grid
    for h in H:
        g = A[A["pos"] % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"] = A[f"f{h}"] - A["coin"].map(dr)
    # vol level: within coin quantile of vol30 (median split)
    A["volhi"] = A.groupby("coin")["vol30"].transform(lambda s: (s > s.median()).astype(float).where(s.notna()))

    def tab(col, h, mask=None, q=5, name=None):
        g = A[(A["pos"] % h == 0)].copy()
        if mask is not None:
            g = g[mask(g)]
        g = g.dropna(subset=[col, f"x{h}"])
        g["b"] = pd.qcut(g[col], q, labels=False, duplicates="drop")
        t = g.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), mean_x=(f"x{h}", "mean"),
                               n=(f"x{h}", "size"), sd=(f"x{h}", "std"))
        t["t"] = t["mean_x"] / (t["sd"] / np.sqrt(t["n"]))
        return t.drop(columns="sd").round(4)

    out["z_chop_h10"] = tab("z", 10, lambda g: g["chop"] == 1)
    out["z_trend_h10"] = tab("z", 10, lambda g: g["chop"] == 0)
    out["z_chop_h3"] = tab("z", 3, lambda g: g["chop"] == 1)
    out["z_all_h5"] = tab("z", 5)
    out["r1z_all_h1"] = tab("r1z", 1, q=10)
    out["r1z_all_h3"] = tab("r1z", 3, q=5)
    out["r5z_all_h5"] = tab("r5z", 5, q=5)
    out["r1z_volhi_h3"] = tab("r1z", 3, lambda g: g["volhi"] == 1)
    out["r1z_vollo_h3"] = tab("r1z", 3, lambda g: g["volhi"] == 0)
    out["clpos_h1"] = tab("clpos", 1, q=5)
    out["rng_h3"] = tab("rng", 3, q=5)
    # weekday
    g = A.dropna(subset=["x1"])
    wd = g.groupby("wd")["x1"].agg(["mean", "std", "size"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    out["weekday_x1"] = wd.round(5)
    # book by window
    br = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            br.append(pd.DataFrame({"w": w, "coin": coin, "br": d["book_return"].values, "cr": d["coin_return"].values}))
    B = pd.concat(br)
    out["book_by_window"] = B.groupby("w").agg(book=("br", "mean"), coin=("cr", "mean"), n=("br", "size")).round(5)
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T = pd.concat(T)
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean", "median", "size"]).round(3)
    T["fq"] = pd.qcut(T["entry_forecast"].abs(), 4, labels=False, duplicates="drop")
    out["trades_by_absforecast"] = T.groupby(["side", "fq"])["net_profit_loss_percent"].agg(["mean", "size"]).round(3)
    return out
