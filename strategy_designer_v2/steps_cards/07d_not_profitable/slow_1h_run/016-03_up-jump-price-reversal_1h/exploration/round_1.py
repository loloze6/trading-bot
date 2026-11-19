def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    bucket_rows = []
    for coin in data["bars"]:
        allb = []
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["gross"] = b["postRebalance_current_allocation"] * b["ret1"]
            b["fwd72"] = b["close"].shift(-72) / b["close"] - 1
            b["w"] = w
            allb.append(b)
        B = pd.concat(allb)
        mu = B["ret1"].mean()
        a = B["postRebalance_current_allocation"]
        d = pd.concat(data["days"][coin].values())
        rows.append({"coin": coin,
                     "book_daily_mean": d["book_return"].mean(),
                     "coin_daily_mean": d["coin_return"].mean(),
                     "gross_per_bar": B["gross"].mean(),
                     "fee_per_bar": B["fee"].mean(),
                     "drift_part_per_bar": (a * mu).mean(),
                     "share_short": (a < -1e-9).mean(),
                     "share_long": (a > 1e-9).mean(),
                     "mean_abs_alloc": a.abs().mean(),
                     "gross_when_short": B.loc[a < -1e-9, "gross"].sum() / len(B),
                     "gross_when_long": B.loc[a > 1e-9, "gross"].sum() / len(B),
                     "mean_abs_alloc_change": (a - B["previous_allocation"]).abs().mean()})
        # grid buckets of forecast
        g = []
        for w, b in data["bars"][coin].items():
            idx = np.arange(0, len(b), 72)
            s = b.iloc[idx].copy()
            s["fwd72"] = (b["close"].shift(-72) / b["close"] - 1).iloc[idx].values
            g.append(s)
        G = pd.concat(g)
        G = G[G["regime"] == "trending"].dropna(subset=["fwd72"])
        G["fb"] = pd.cut(G["forecast"], [-21, -10, -5, -1e-9, 1e-9, 5, 10, 21])
        G["coin"] = coin
        bucket_rows.append(G[["coin", "fb", "fwd72"]])
    out["per_coin"] = pd.DataFrame(rows).set_index("coin")
    Gall = pd.concat(bucket_rows)
    out["grid_fwd72_by_forecast"] = Gall.groupby("fb")["fwd72"].agg(["mean", "count", "std"])
    # forecast distribution on trending bars
    fc = pd.concat([pd.concat(data["bars"][c].values()) for c in data["bars"]])
    tr = fc[fc["regime"] == "trending"]["forecast"]
    out["trending_forecast_desc"] = tr.describe()
    out["share_bars_trending"] = float((fc["regime"] == "trending").mean())
    t = pd.concat([pd.concat(data["trades"][c].values()) for c in data["trades"]])
    out["trades_by_side"] = t.groupby("side").agg(n=("net_profit_loss_percent", "size"),
                                                gross=("profit_loss_percent", "mean"),
                                                net=("net_profit_loss_percent", "mean"),
                                                dur_h=("duration_minutes", lambda x: x.mean() / 60))
    return out
