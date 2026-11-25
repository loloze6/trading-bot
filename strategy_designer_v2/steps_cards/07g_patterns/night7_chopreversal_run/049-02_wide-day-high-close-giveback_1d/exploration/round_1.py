def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            rng = (b["high"] - b["low"])
            clv = ((b["close"] - b["low"]) / rng.replace(0, np.nan))
            width = rng / rng.rolling(30, min_periods=20).mean()
            ret1 = b["close"].pct_change()
            vol30 = ret1.rolling(30, min_periods=20).std()
            tr60 = b["close"] / b["close"].shift(60) - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "clv": clv, "width": width, "r0": ret1,
                "z0": ret1 / vol30, "vol30": vol30, "tr60": tr60,
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
            })
            for h in (1, 2, 3, 5):
                df[f"f{h}"] = b["close"].shift(-h) / b["close"] - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # drift per coin, per horizon, on non-overlapping grid
    for h in (1, 2, 3, 5):
        g = D[D["pos"] % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(dr)
    # vol rank within coin
    D["volq"] = D.groupby("coin")["vol30"].rank(pct=True)

    def tday(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 10: return (np.nan, np.nan, len(s))
        m = s[col].mean()
        dev = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return (m * 100, m / se if se > 0 else np.nan, len(s))

    out = {}
    # 1. clv bucket x width tercile, next-day excess
    D["clvb"] = pd.cut(D["clv"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01], labels=["lo", "ml", "mid", "mh", "hi"])
    D["wq"] = D.groupby("coin")["width"].transform(lambda s: pd.qcut(s, 3, labels=["narrow", "normal", "wide"]))
    res = []
    for (c, wq), s in D.groupby(["clvb", "wq"], observed=True):
        m, t, n = tday(s, "x1")
        res.append({"clv": c, "width": wq, "mean_x1_%": m, "t": t, "n": n})
    out["clv_x_width_next_day"] = pd.DataFrame(res)
    # 2. same on 3-day horizon grid
    res = []
    g3 = D[D["pos"] % 3 == 0]
    for (c, wq), s in g3.groupby(["clvb", "wq"], observed=True):
        m, t, n = tday(s, "x3")
        res.append({"clv": c, "width": wq, "mean_x3_%": m, "t": t, "n": n})
    out["clv_x_width_3day"] = pd.DataFrame(res)
    # 3. after large standardized daily moves
    D["zb"] = pd.cut(D["z0"], [-99, -2, -1, 0, 1, 2, 99])
    res = []
    for zb, s in D.groupby("zb", observed=True):
        r = {"z0": str(zb)}
        for h in (1, 3, 5):
            gg = s[s["pos"] % h == 0]
            m, t, n = tday(gg, f"x{h}")
            r[f"x{h}_%"] = m; r[f"t{h}"] = t; r[f"n{h}"] = n
        res.append(r)
    out["after_move_size"] = pd.DataFrame(res)
    # 4. trend regime x clv (high vs low close on wide days)
    D["trend"] = pd.cut(D["tr60"], [-99, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    wide = D[D["wq"] == "wide"]
    res = []
    for (tr, c), s in wide.groupby(["trend", "clvb"], observed=True):
        m, t, n = tday(s, "x1")
        res.append({"trend": tr, "clv": c, "x1_%": m, "t": t, "n": n})
    out["wide_by_trend_clv"] = pd.DataFrame(res)
    # 5. vol quintile: next day by sign of today's return
    D["volb"] = pd.qcut(D["volq"], 3, labels=["calm", "mid", "agit"])
    res = []
    for (vb, sg), s in D.groupby(["volb", np.sign(D["r0"])], observed=True):
        m, t, n = tday(s, "x1")
        res.append({"vol": vb, "today_sign": sg, "x1_%": m, "t": t, "n": n})
    out["vol_x_sign"] = pd.DataFrame(res)
    # 6. weekday
    res = []
    for wd, s in D.groupby("wd"):
        m, t, n = tday(s, "x1")
        res.append({"wd": wd, "x1_%": m, "t": t, "n": n})
    out["weekday_next"] = pd.DataFrame(res)
    # 7. book: daily returns by window, and alloc sign gains
    days = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; dd["win"] = w; days.append(dd)
    DY = pd.concat(days)
    bk = DY.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["mean", "std", "count"]).assign(
        sharpe=lambda x: x["mean"] / x["std"] * np.sqrt(365))
    # position gain by side
    D["pg"] = D["alloc"] * D["f1"]
    out["gain_by_side"] = D.groupby(np.sign(D["alloc"]))["pg"].agg(["mean", "count", "sum"])
    return out
