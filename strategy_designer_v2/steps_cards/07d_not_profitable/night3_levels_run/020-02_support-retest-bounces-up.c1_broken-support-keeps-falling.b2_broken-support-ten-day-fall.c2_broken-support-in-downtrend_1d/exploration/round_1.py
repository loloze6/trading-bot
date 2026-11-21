def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    case_rows = []
    trows = []
    for coin, wins in data["bars"].items():
        # coin drift: mean daily return across all windows
        dr = pd.concat([data["days"][coin][w]["coin_return"] for w in wins]).dropna()
        mu = dr.mean()
        # 10-bar grid returns for drift
        g = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - 10, 10):
                g.append(c[i + 10] / c[i] - 1)
        drift10 = np.mean(g); sd10 = np.std(g)
        for w, b in wins.items():
            d = data["days"][coin][w]
            b = b.copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day")
            dd["pos"] = pos.reindex(dd.index)
            dd = dd.dropna(subset=["book_return", "coin_return"])
            rows.append(pd.DataFrame({"coin": coin, "win": w, "book": dd["book_return"],
                                      "pos": dd["pos"], "cr": dd["coin_return"], "mu": mu}))
            c = b["close"].values; f = b["forecast"].fillna(0).values
            r60 = pd.Series(c).pct_change(60).values
            ma20 = pd.Series(c).rolling(20).mean().values
            r10p = pd.Series(c).pct_change(10).values
            for i in range(0, len(c) - 10, 10):
                if f[i] < 0:
                    tot = -(c[i + 10] / c[i] - 1)
                    case_rows.append({"coin": coin, "win": w, "absf": -f[i], "tot": tot,
                                      "exc": tot + drift10, "r60": r60[i],
                                      "r10": r10p[i], "dma": c[i] / ma20[i] - 1 if ma20[i] == ma20[i] else np.nan})
        for w, t in data["trades"][coin].items():
            if len(t):
                trows.append(t.assign(coin=coin))
    R = pd.concat(rows)
    R["mkt"] = R["pos"] * R["mu"]
    R["timing"] = R["pos"] * R["cr"] - R["mkt"]
    out["book_decomp_by_coin"] = R.groupby("coin")[["book", "mkt", "timing", "pos", "mu"]].mean()
    out["book_by_window"] = R.groupby("win")["book"].agg(["mean", "count"]).assign(
        sharpe=R.groupby("win")["book"].apply(lambda x: x.mean() / x.std() * np.sqrt(365) if x.std() > 0 else 0))
    out["share_days_short"] = float((R["pos"] < 0).mean())
    C = pd.DataFrame(case_rows)
    out["cases_n"] = len(C)
    C["r60q"] = pd.qcut(C["r60"], 4, labels=False)
    out["by_r60_quartile"] = C.groupby("r60q")[["r60", "tot", "exc"]].agg(["mean", "count"])
    C["r10q"] = pd.qcut(C["r10"], 4, labels=False)
    out["by_prior10_quartile"] = C.groupby("r10q")[["r10", "tot", "exc"]].mean()
    C["dmaq"] = pd.qcut(C["dma"], 4, labels=False)
    out["by_dist_ma20_quartile"] = C.groupby("dmaq")[["dma", "tot", "exc"]].mean()
    C["fq"] = pd.qcut(C["absf"].rank(method="first"), 4, labels=False)
    out["by_forecast_quartile"] = C.groupby("fq")[["absf", "tot", "exc"]].mean()
    out["by_coin_cases"] = C.groupby("coin")[["tot", "exc"]].agg(["mean", "count"])
    T = pd.concat(trows)
    out["trades"] = T.groupby("side")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["mean", "count"])
    out["trade_duration_days_mean"] = float(T["duration_minutes"].mean() / 1440)
    return out
