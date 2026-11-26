def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "r1": r1, "r3": c / c.shift(3) - 1, "r7": c / c.shift(7) - 1,
                "r30": c / c.shift(30) - 1, "r60": c / c.shift(60) - 1,
                "vol30": r1.rolling(30).std(),
                "rng": (b["high"] - b["low"]) / c,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            for h in (1, 5, 10, 20):
                df["f%d" % h] = c.shift(-h) / c - 1
            df["regime"] = b["regime"]
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # coin drift per horizon (mean over all windows, non-overlapping)
    for h in (1, 5, 10, 20):
        g = D[D["pos"] % h == 0]
        drift = g.groupby("coin")["f%d" % h].mean()
        D["u%d" % h] = D["f%d" % h] - D["coin"].map(drift)
    D["z30"] = D["r30"] / (D["vol30"] * np.sqrt(30))
    D["trend"] = np.where(D["r60"] > 0.10, "rising", np.where(D["r60"] < -0.10, "falling", "choppy"))
    D.loc[D["r60"].isna(), "trend"] = np.nan

    def table(sub, key, h):
        g = sub[(sub["pos"] % h == 0)].dropna(subset=[key, "u%d" % h])
        res = []
        for name, gg in g.groupby("grp"):
            x = gg["u%d" % h]
            res.append({"grp": name, "n": len(x), "mean_u": x.mean(),
                        "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
        return pd.DataFrame(res)

    # 1. 30d move quintile -> next 5,10,20 days, by trend
    res = []
    for tr in ["choppy", "rising", "falling"]:
        for h in (5, 10, 20):
            g = D[(D["trend"] == tr) & (D["pos"] % h == 0)].dropna(subset=["z30", "u%d" % h])
            if len(g) < 30: continue
            rho, p = stats.spearmanr(g["z30"], g["u%d" % h])
            q = pd.qcut(g["z30"], 3, labels=False)
            m = g.groupby(q)["u%d" % h].mean()
            res.append({"trend": tr, "h": h, "n": len(g), "rho": rho, "p": p,
                        "low_tercile": m.iloc[0], "mid": m.iloc[1], "high_tercile": m.iloc[2]})
    out["z30_vs_future_by_trend"] = pd.DataFrame(res)

    # 2. daily return -> next day, by vol level and by size
    res = []
    g = D.dropna(subset=["r1", "u1", "vol30"]).copy()
    g["z1"] = g["r1"] / g["vol30"]
    g["volq"] = g.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    g["zb"] = pd.cut(g["z1"], [-99, -2, -1, 1, 2, 99])
    t = g.groupby(["volq", "zb"], observed=True)["u1"].agg(["count", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["next_day_after_zmove_by_volq"] = t.reset_index().astype(str)

    # 3. 7d and 3d moves -> next 5 days by trend
    res = []
    for tr in ["choppy", "rising", "falling"]:
        for k in ("r3", "r7"):
            gg = D[(D["trend"] == tr) & (D["pos"] % 5 == 0)].dropna(subset=[k, "u5", "vol30"])
            z = gg[k] / gg["vol30"]
            rho, p = stats.spearmanr(z, gg["u5"])
            res.append({"trend": tr, "past": k, "n": len(gg), "rho": rho, "p": p})
    out["short_moves_vs_next5"] = pd.DataFrame(res)

    # 4. close position in range -> next day/5 days
    gg = D.dropna(subset=["clpos", "u1"]).copy()
    gg["cb"] = pd.cut(gg["clpos"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    t = gg.groupby("cb", observed=True)["u1"].agg(["count", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["close_pos_next_day"] = t.reset_index().astype(str)

    # 5. weekday
    t = D.dropna(subset=["u1"]).groupby("wd")["u1"].agg(["count", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["weekday_next_day"] = t

    # 6. book daily returns, big days
    br = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; br.append(d)
    B = pd.concat(br)
    bk = B.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["count", "mean", "std"])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    out["trades"] = pd.DataFrame({"n": [len(T)], "mean_net": [T["net_profit_loss_percent"].mean()],
                                  "win_share": [(T["net_profit_loss_percent"] > 0).mean()],
                                  "mean_days": [T["duration_minutes"].mean() / 1440]})
    return out
