def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    hourly = []
    daily = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            vr = v / v.rolling(720, min_periods=240).mean()
            z = r / sd
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "vr": vr, "r": r,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "fc": b["forecast"], "pos": b["postRebalance_current_allocation"],
                               "sd": sd})
            df["r30"] = c / c.shift(720) - 1
            for h in (1, 2, 6, 24):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["pos_idx"] = np.arange(len(df))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # usual move per coin per h from grid
    usual = {}
    for h in (1, 2, 6, 24):
        g = A[A["pos_idx"] % h == 0]
        usual[h] = g.groupby("coin")[f"f{h}"].agg(["mean", "std"])
    def strength(df, h):
        u = usual[h].loc[df["coin"]].reset_index(drop=True)
        return (df[f"f{h}"].reset_index(drop=True) - u["mean"]) / u["std"]
    zb = pd.cut(A["z"], [-np.inf, -4, -2.5, -1.5, 1.5, 2.5, 4, np.inf])
    vb = pd.cut(A["vr"], [0, 1.5, 3, np.inf])
    A["zb"] = zb.astype(str); A["vb"] = vb.astype(str)
    # grid-sampled continuation tables for h=2,6
    for h in (2, 6, 24):
        g = A[(A["pos_idx"] % h == (h - 1) if h > 1 else True)].copy() if False else A.copy()
        g["cell"] = g["pos_idx"] // h
        g = g.dropna(subset=["z", "vr", f"f{h}"])
        # first bar in each cell with |z|>1.5 as event, else cell's first bar
        ev = g[g["z"].abs() > 1.5].groupby(["coin", "w", "cell"]).head(1)
        ev = ev.reset_index(drop=True)
        ev["s"] = strength(ev, h).values
        t = ev.groupby(["zb", "vb"])["s"].agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        out[f"events strength h{h} by zbin x volbin"] = t.round(3)
    # hour of day (1h, each bar non-overlapping)
    g = A.dropna(subset=["f1"]).copy()
    g["s"] = strength(g, 1).values
    t = g.groupby("hour")["s"].agg(["count", "mean", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["hourly strength by UTC hour"] = t.round(4)
    # vol level and 30d trend on 24h grid
    g = A[A["pos_idx"] % 24 == 0].dropna(subset=["f24", "sd", "r30"]).copy()
    g["s"] = strength(g, 24).values
    g["sdq"] = g.groupby("coin")["sd"].transform(lambda x: pd.qcut(x, 5, labels=False))
    g["r30q"] = g.groupby("coin")["r30"].transform(lambda x: pd.qcut(x, 5, labels=False))
    for k in ("sdq", "r30q", "wd"):
        t = g.groupby(k)["s"].agg(["count", "mean", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
        out[f"24h strength by {k}"] = t.round(3)
    # forecast level vs next 24h
    g2 = g.copy(); g2["fcb"] = pd.cut(g2["fc"], [-0.1, 0.01, 2, 5, 10, 20.1])
    t = g2.groupby("fcb")["s"].agg(["count", "mean", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["24h strength by forecast bin (grid)"] = t.round(3)
    # book days
    D = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            d["prev_coin"] = d["coin_return"].shift(1)
            D.append(d)
    D = pd.concat(D).dropna(subset=["book_return", "coin_return"])
    D["bq"] = D.groupby("coin")["book_return"].transform(lambda x: pd.qcut(x, 10, labels=False, duplicates="drop"))
    out["days by book decile"] = D.groupby("bq")[["book_return", "coin_return", "prev_coin"]].mean().round(4)
    D["cq"] = D.groupby("coin")["coin_return"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["book by coin-day quintile"] = D.groupby("cq")[["book_return", "coin_return"]].mean().round(4)
    out["mean active allocation"] = float(A.loc[A["pos"].abs() > 0, "pos"].mean())
    out["share bars active"] = float((A["pos"].abs() > 0).mean())
    return out
