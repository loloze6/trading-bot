def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; allrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            r24 = c / c.shift(24) - 1
            m = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            z = r24 / m
            vol_s = r1.rolling(72).std(); vol_l = r1.rolling(720).std()
            r6 = c / c.shift(6) - 1
            df = pd.DataFrame({"z": z, "vr": vol_s / vol_l, "r6z": r6 / m,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "g1": b["postRebalance_current_allocation"].astype(float) * (c.shift(-1) / c - 1)})
            df["coin"] = coin; df["win"] = w
            allrows.append(df[["z", "vr", "alloc", "g1", "coin", "win"]])
            for h in (24, 72):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df = df.iloc[::24].copy()
            rows.append(df)
    D = pd.concat(rows).dropna(subset=["z", "f24", "vr"])
    for h in (24, 72):
        g = D.groupby("coin")[f"f{h}"]
        D[f"x{h}"] = D[f"f{h}"] - g.transform("mean")
    dr = D[D["z"] < -1].copy()
    dr["zb"] = pd.cut(dr["z"], [-99, -3, -2, -1])
    dr["volr"] = pd.qcut(dr["vr"], 3, labels=["calm", "mid", "hot"])
    def agg(g):
        return pd.Series({"n": len(g), "x24": g["x24"].mean(), "t24": g["x24"].mean() / g["x24"].std() * np.sqrt(len(g)),
                          "x72": g["x72"].mean()})
    out["drop_x_vol"] = dr.groupby(["zb", "volr"], observed=True).apply(agg)
    # was the 24h drop recent (in last 6h) or slow
    dr["speed"] = pd.qcut(dr["r6z"] / dr["z"], 3, labels=["slow", "mid", "fast"])
    out["drop_by_speed"] = dr.groupby("speed", observed=True).apply(agg)
    # bar-level: gain by z bucket of position held
    A = pd.concat(allrows).dropna(subset=["z", "g1"])
    A["zb"] = pd.cut(A["z"], [-99, -3, -2, -1, -0.5, 0, 99])
    A["vq"] = pd.qcut(A["vr"], 3, labels=["calm", "mid", "hot"])
    out["held_gain_by_z_at_bar"] = A.groupby("zb", observed=True).agg(bars=("g1", "size"),
                                  mean_alloc=("alloc", "mean"), sum_gain=("g1", "sum"))
    out["held_gain_by_vol"] = A.groupby("vq", observed=True).agg(bars=("g1", "size"),
                                  mean_alloc=("alloc", "mean"), sum_gain=("g1", "sum"))
    out["share_bars_long"] = float((A["alloc"] > 0.01).mean())
    # falls: per window, book chain and share long, worst windows by book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    DD = pd.concat(dd)
    alloc_w = A.groupby("win")["alloc"].mean()
    pw = DD.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    wk = pw.groupby("win").agg(book=("book_return", "mean"), hold=("coin_return", "mean"))
    wk["alloc"] = alloc_w
    wk["wn"] = wk.index.str[1:].astype(int)
    out["alloc_vs_hold_by_window"] = wk.sort_values("wn")[["book", "hold", "alloc"]]
    out["corr_window_alloc_hold"] = float(wk["alloc"].corr(wk["hold"]))
    return out
