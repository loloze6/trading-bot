def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=30).std().shift(0)
            z = r1 / sd30
            hi20 = c.rolling(20, min_periods=20).max()
            dist = (hi20 / c - 1) * 100
            ret60 = c / c.shift(60) - 1
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "z": z, "dist": dist, "r1": r1, "ret60": ret60,
                               "regime": b["regime"].values, "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            for h in (5, 10, 20):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["inprof"] = A["regime"] == "unknown"
    # coin drift per horizon on grid
    res = []
    for h in (5, 10, 20):
        g = A[(A["pos"] % h == 0)].dropna(subset=[f"f{h}"]).copy()
        drift = g.groupby("coin")[f"f{h}"].mean()
        usual = g.groupby("coin")[f"f{h}"].std()
        g["ex"] = g[f"f{h}"] - g["coin"].map(drift)
        g["str"] = g["ex"] / g["coin"].map(usual)
        def summ(m, name):
            s = g[m]
            if len(s) < 3:
                return
            t = s["ex"].mean() / (s["ex"].std() / np.sqrt(len(s)))
            res.append({"h": h, "group": name, "n": len(s), "tot%": 100*s[f"f{h}"].mean(),
                        "ex%": 100*s["ex"].mean(), "t": t, "strength": s["str"].mean()})
        up = g["z"] > 0
        ip = g["inprof"]
        summ(ip & up, "prof up day")
        summ(ip & (g["z"] > 1), "prof z>1")
        summ(ip & (g["z"] > 1.5), "prof z>1.5")
        summ(ip & (g["z"] > 1) & (g["dist"] < 1), "prof z>1 at high")
        summ(ip & (g["z"] > 0) & (g["dist"] < 1), "prof up at high")
        summ(ip & (g["dist"] < 1), "prof at high any day")
        summ(ip & (g["z"] <= 0), "prof down day")
        summ(ip, "prof all")
        summ(~ip & (g["z"] > 1), "outprof z>1")
        summ(~ip & (g["z"] > 1) & (g["dist"] < 1), "outprof z>1 at high")
        summ((g["z"] > 1) & (g["dist"] < 1) & (g["ret60"] > 0.1), "rising z>1 at high")
        summ((g["z"] > 1) & (g["ret60"].abs() <= 0.1), "choppy any-agit z>1")
        summ(ip & (g["fc"] > 0) & (g["fc"] >= g.loc[ip & (g["fc"] > 0), "fc"].median()), "prof fc top half")
        summ(ip & (g["fc"] > 0) & (g["fc"] < g.loc[ip & (g["fc"] > 0), "fc"].median()), "prof fc bottom half")
    out["groups"] = pd.DataFrame(res).round(4)
    # book: days
    d = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; d.append(x)
    D = pd.concat(d)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["mean", "std", "count"]).round(5)
    # trades
    t = []
    for coin, wins in data["trades"].items():
        for w, x in wins.items():
            if len(x):
                x = x.copy(); x["coin"] = coin; t.append(x)
    T = pd.concat(t)
    T["q"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades_by_fc_q"] = T.groupby("q").agg(n=("net_profit_loss_percent", "size"),
        fc=("entry_forecast", "mean"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), days=("duration_minutes", lambda s: s.mean()/1440)).round(3)
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean"]).round(3)
    return out
