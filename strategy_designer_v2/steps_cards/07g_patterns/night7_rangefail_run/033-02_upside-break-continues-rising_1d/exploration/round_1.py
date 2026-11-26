def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            hh = hi.shift(1).rolling(20, min_periods=20).max()
            ll = lo.shift(1).rolling(20, min_periods=20).min()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "pos": (c - ll) / (hh - ll),
                "above": (c / hh - 1) * 100,
                "below": (c / ll - 1) * 100,
                "r1": c.pct_change(),
                "r5p": c / c.shift(5) - 1,
                "r20p": c / c.shift(20) - 1,
                "tr60": c / c.shift(60) - 1,
                "fwd": c.shift(-H) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            f["vol20"] = f["r1"].rolling(20).std()
            f["volrel"] = f["vol20"] / f["r1"].rolling(60, min_periods=40).std()
            f["z1"] = f["r1"] / f["r1"].shift(1).rolling(20).std()
            f["grid"] = (np.arange(len(f)) % H == 0)
            f["wd"] = f["day"].dt.weekday
            f["year"] = f["day"].dt.year
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["grid"] & A["fwd"].notna()].copy()
    drift = G.groupby("coin")["fwd"].mean()
    sd = G.groupby("coin")["fwd"].std()
    G["unu"] = G["fwd"] - G["coin"].map(drift)
    A["unu1"] = A["fwd1"] - A["coin"].map(A.groupby("coin")["fwd1"].mean())

    def tday(df, col):
        df = df[df[col].notna()]
        n = len(df)
        if n < 5: return pd.Series({"n": n, "days": 0, "mean%": np.nan, "t": np.nan})
        m = df[col].mean()
        r = (df[col] - m).groupby(df["day"]).sum()
        D = len(r)
        var = D / (D - 1) * (r ** 2).sum() / n ** 2
        return pd.Series({"n": n, "days": D, "mean%": 100 * m, "t": m / np.sqrt(var)})

    out = {}
    out["drift5_sd5_by_coin"] = pd.DataFrame({"drift%": 100 * drift, "sd%": 100 * sd})
    G["posb"] = pd.cut(G["pos"], [-np.inf, 0, 0.2, 0.4, 0.6, 0.8, 1.0, np.inf])
    out["fwd5_by_rangepos"] = G.groupby("posb", observed=True).apply(lambda d: tday(d, "unu"))
    Gb = G[G["above"] > 0].copy()
    Gb["q"] = pd.qcut(Gb["above"], 3, labels=["small", "mid", "large"])
    out["fwd5_breakup_by_size"] = Gb.groupby("q", observed=True).apply(lambda d: tday(d, "unu"))
    Gd = G[G["below"] < 0].copy()
    Gd["q"] = pd.qcut(Gd["below"], 3, labels=["deep", "mid", "shallow"])
    out["fwd5_breakdown_by_size"] = Gd.groupby("q", observed=True).apply(lambda d: tday(d, "unu"))
    G["trend"] = pd.cut(G["tr60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    G["zone"] = np.where(G["above"] > 0, "breakup", np.where(G["below"] < 0, "breakdown", "inside"))
    out["fwd5_zone_x_trend"] = G.groupby(["zone", "trend"], observed=True).apply(lambda d: tday(d, "unu"))
    G["volq"] = pd.qcut(G["volrel"], 3, labels=["calmer", "mid", "wilder"])
    out["fwd5_zone_x_vol"] = G.groupby(["zone", "volq"], observed=True).apply(lambda d: tday(d, "unu"))
    G["z1b"] = pd.cut(G["z1"], [-np.inf, -2, -1, 1, 2, np.inf])
    out["fwd5_by_1day_shock_z"] = G.groupby("z1b", observed=True).apply(lambda d: tday(d, "unu"))
    G["r20b"] = pd.qcut(G["r20p"], 5)
    out["fwd5_by_20d_return_quint"] = G.groupby("r20b", observed=True).apply(lambda d: tday(d, "unu"))
    out["fwd5_zone_by_year"] = G.groupby(["year", "zone"]).apply(lambda d: tday(d, "unu")).unstack("zone")["mean%"]
    out["fwd1_by_weekday"] = A.groupby("wd").apply(lambda d: tday(d, "unu1"))
    out["fwd5_by_coin_zone"] = G.groupby(["coin", "zone"]).apply(lambda d: tday(d, "unu"))["mean%"].unstack()

    # book
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dl.append(d)
    Dd = pd.concat(dl, ignore_index=True)
    Dd["day"] = pd.to_datetime(Dd["day"])
    bk = Dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk["wd"] = bk.index.get_level_values("day").weekday
    out["book_by_window"] = bk.groupby("win").agg(book_mean=("book_return", "mean"), hold_mean=("coin_return", "mean"), n=("book_return", "size"))
    out["book_by_weekday"] = bk.groupby("wd")["book_return"].agg(["mean", "std", "size"])
    # trades
    tl = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; tl.append(t)
    T = pd.concat(tl, ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["fq"] = pd.qcut(T["entry_forecast"], 3, duplicates="drop")
    out["trades_by_entry_fc"] = T.groupby("fq", observed=True)["net_profit_loss_percent"].agg(["mean", "median", "count"])
    out["trades_by_dur"] = T.groupby(pd.cut(T["dur_d"], [0, 5.5, 10, 20, 1000]), observed=True)["net_profit_loss_percent"].agg(["mean", "count"])
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count", lambda s: (s > 0).mean()])
    return out
