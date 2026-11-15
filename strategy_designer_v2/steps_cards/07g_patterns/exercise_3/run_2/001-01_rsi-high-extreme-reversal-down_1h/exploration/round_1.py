def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 12
    rows = []
    hr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            f = b["forecast"].values
            alloc = b["postRebalance_current_allocation"].values
            r1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            # hourly returns
            hr.append(pd.DataFrame({"coin": coin, "w": w, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                                    "r1": r1, "pos": alloc}))
            idx = np.arange(0, n - H, H)
            fwd = c[idx + H] / c[idx] - 1
            past = np.full(len(idx), np.nan)
            ok = idx >= H
            past[ok] = c[idx[ok]] / c[idx[ok] - H] - 1
            past72 = np.full(len(idx), np.nan)
            ok2 = idx >= 72
            past72[ok2] = c[idx[ok2]] / c[idx[ok2] - 72] - 1
            lr = np.log(c[1:] / c[:-1])
            vol = pd.Series(np.r_[np.nan, lr]).rolling(72).std().values[idx]
            rng = ((b["high"] - b["low"]) / b["close"]).rolling(24).mean().values[idx]
            rows.append(pd.DataFrame({"coin": coin, "w": w, "fwd": fwd, "past12": past, "past72": past72,
                                      "vol72": vol, "range24": rng, "f": f[idx], "pos": alloc[idx],
                                      "hour": ts.dt.hour.values[idx]}))
    g = pd.concat(rows, ignore_index=True)
    h = pd.concat(hr, ignore_index=True)
    drift = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - drift

    def tab(col, q=5):
        d = g.dropna(subset=[col, "ex"]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x, q, labels=False, duplicates="drop"))
        t = d.groupby(["q"])["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        pc = d.groupby(["coin", "q"])["ex"].mean().unstack()
        t = t.join(pc)
        return t.round(5)

    out["fwd12 excess by past12 quintile"] = tab("past12")
    out["fwd12 excess by past72 quintile"] = tab("past72")
    out["fwd12 excess by vol72 quintile"] = tab("vol72")
    nz = g[g["f"] != 0].copy()
    nz["q"] = pd.qcut(nz["f"].abs(), 5, labels=False, duplicates="drop")
    zz = g[g["f"] == 0]
    t = nz.groupby("q")["ex"].agg(["mean", "count", "std"])
    t.loc["zero"] = [zz["ex"].mean(), len(zz), zz["ex"].std()]
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["fwd12 excess by |forecast| quintile"] = t.round(5)
    # abs fwd return (vol) by vol quintile -> vol clustering, and by past12 sign
    # hour of day
    hh = h.dropna(subset=["r1"])
    ht = hh.groupby("hour")["r1"].agg(["mean", "std", "count"])
    ht["t"] = ht["mean"] / (ht["std"] / np.sqrt(ht["count"]))
    ht["mean_pos"] = hh.groupby("hour")["pos"].mean()
    out["1h return by hour (pooled)"] = ht.round(6)
    wt = hh.groupby("wd")["r1"].agg(["mean", "std", "count"])
    wt["t"] = wt["mean"] / (wt["std"] / np.sqrt(wt["count"]))
    out["1h return by weekday"] = wt.round(6)
    # book decomposition
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    D = pd.concat(dd, ignore_index=True)
    out["book per window"] = D.groupby(["w"])[["book_return", "coin_return"]].mean().round(5)
    # gross vs fee: position gain
    h["gain"] = h["pos"] * h["r1"]
    mr = h.groupby("coin")["r1"].transform("mean")
    out["hourly gain parts"] = pd.Series({
        "mean gain/h": h["gain"].mean(),
        "market part/h": (h["pos"] * mr).mean(),
        "mean pos": h["pos"].mean(),
        "share bars in position": (h["pos"] != 0).mean()}).round(7)
    T = []
    for coin, wins in data["trades"].items():
        for w, t2 in wins.items():
            t2 = t2.copy(); t2["coin"] = coin; T.append(t2)
    T = pd.concat(T, ignore_index=True)
    out["trades"] = pd.Series({"n": len(T), "mean pl%": T["profit_loss_percent"].mean(),
                               "mean net%": T["net_profit_loss_percent"].mean(),
                               "median dur min": T["duration_minutes"].median(),
                               "win share": (T["profit_loss_percent"] > 0).mean()}).round(4)
    return out
