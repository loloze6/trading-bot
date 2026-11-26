def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            hh = hi.shift(1).rolling(20, min_periods=20).max()
            ll = lo.shift(1).rolling(20, min_periods=20).min()
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w, "i": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "pos": (c - ll) / (hh - ll),
                "above": (c / hh - 1) * 100,
                "below": (c / ll - 1) * 100,
                "r1": r1,
                "r20p": c / c.shift(20) - 1,
                "tr60": c / c.shift(60) - 1,
                "z1": r1 / r1.shift(1).rolling(20).std(),
                "volrel": r1.rolling(20).std() / r1.rolling(60, min_periods=40).std(),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            for H in (3, 5, 10, 20):
                f[f"fwd{H}"] = c.shift(-H) / c - 1
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)

    def tday(df, col):
        df = df[df[col].notna()]
        n = len(df)
        if n < 5: return pd.Series({"n": n, "days": 0, "mean%": np.nan, "t": np.nan})
        m = df[col].mean()
        r = (df[col] - m).groupby(df["day"]).sum()
        D = len(r)
        var = D / (D - 1) * (r ** 2).sum() / n ** 2
        return pd.Series({"n": n, "days": D, "mean%": 100 * m, "t": m / np.sqrt(var)})

    def grid(H):
        G = A[(A["i"] % H == 0) & A[f"fwd{H}"].notna()].copy()
        G["unu"] = G[f"fwd{H}"] - G["coin"].map(G.groupby("coin")[f"fwd{H}"].mean())
        G["usual"] = G["coin"].map(G.groupby("coin")[f"fwd{H}"].std())
        G["str"] = G["unu"] / G["usual"]
        G["zone"] = np.where(G["above"] > 0, "breakup", np.where(G["below"] < 0, "breakdown", "inside"))
        return G

    out = {}
    res = {}
    for H in (3, 5, 10, 20):
        G = grid(H)
        G["posb"] = pd.cut(G["pos"], [-np.inf, 0.2, 0.4, 0.6, 0.8, 1.0, np.inf])
        res[H] = G.groupby("posb", observed=True).apply(lambda d: tday(d, "unu"))[["mean%", "t"]]
        # slope of unusual on clipped pos, day-pooled-ish simple corr
    out["unusual_by_rangepos_by_horizon"] = pd.concat(res, axis=1)

    G = grid(5)
    # shock continuation separated from breakouts
    G["shock"] = pd.cut(G["z1"], [-np.inf, -2, -1, 1, 2, np.inf])
    out["shock_x_breakup"] = G.groupby([G["above"] > 0, "shock"], observed=True).apply(lambda d: tday(d, "unu"))
    G["posq"] = pd.cut(G["pos"], [-np.inf, 0.5, 1.0, np.inf], labels=["lowhalf", "highhalf", "above"])
    out["shock_x_rangehalf"] = G.groupby(["posq", "shock"], observed=True).apply(lambda d: tday(d, "unu"))
    # graded within 20d return
    G["r20b"] = pd.qcut(G["r20p"], 10, labels=False)
    out["r20_decile"] = G.groupby("r20b").apply(lambda d: tday(d, "unu"))
    # range pos graded within agitation tercile, low half side
    G["volq"] = pd.qcut(G["volrel"], 2, labels=["calmer", "wilder"])
    G["posb"] = pd.cut(G["pos"], [-np.inf, 0, 0.3, 0.7, 1.0, np.inf])
    out["rangepos_x_vol"] = G.groupby(["volq", "posb"], observed=True).apply(lambda d: tday(d, "unu"))
    # correlation of pos (clipped) with unusual move, per coin
    G["posc"] = G["pos"].clip(-0.5, 1.5)
    out["corr_pos_unu_by_coin"] = G.groupby("coin").apply(lambda d: pd.Series({"corr": d["posc"].corr(d["unu"]), "n": d["unu"].notna().sum()}))
    out["corr_pos_unu_by_win"] = G.groupby("win").apply(lambda d: d["posc"].corr(d["unu"]))
    # breakup cases over longer horizons
    for H in (10, 20):
        g = grid(H)
        out[f"breakup_fwd{H}"] = g.groupby("zone").apply(lambda d: tday(d, "unu"))
    # book largest days
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dl.append(d)
    Dd = pd.concat(dl, ignore_index=True)
    bk = Dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk["book_return"].quantile([0.02, 0.98])
    top = bk[bk["book_return"] >= q.iloc[1]]; bot = bk[bk["book_return"] <= q.iloc[0]]
    out["book_extreme_days"] = pd.DataFrame({
        "n": [len(top), len(bot)],
        "book_mean%": [100 * top["book_return"].mean(), 100 * bot["book_return"].mean()],
        "coin_mean%": [100 * top["coin_return"].mean(), 100 * bot["coin_return"].mean()],
        "share_of_total_gain": [top["book_return"].sum() / bk["book_return"].sum(), bot["book_return"].sum() / bk["book_return"].sum()],
    }, index=["top2%", "bottom2%"])
    return out
