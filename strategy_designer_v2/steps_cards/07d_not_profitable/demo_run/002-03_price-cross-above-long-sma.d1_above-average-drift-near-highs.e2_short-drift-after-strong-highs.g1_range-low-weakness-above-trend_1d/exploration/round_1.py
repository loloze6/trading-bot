def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # pooled coin mean daily return over all windows
    rows = []
    daily = []
    for coin in data["days"]:
        dfs = [d.assign(window=w) for w, d in data["days"][coin].items()]
        dd = pd.concat(dfs)
        mu = dd["coin_return"].mean()
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["pos"] = b["postRebalance_current_allocation"]
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["gain"] = b["pos"] * b["ret1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            # distance above 200 SMA unknown in bars -> use 20d return and range pos
            c = b["close"]
            b["r20"] = c / c.shift(20) - 1
            b["r60"] = c / c.shift(60) - 1
            lo = c.rolling(20).min(); hi = c.rolling(20).max()
            b["rp"] = (c - lo) / (hi - lo)
            b["vol20"] = b["ret1"].shift(1).rolling(20).std()
            b["fwd5"] = c.shift(-5) / c - 1
            b["coin"] = coin; b["window"] = w; b["mu"] = mu
            b["grid"] = (np.arange(len(b)) % 5) == 0
            rows.append(b)
        dd["coin"] = coin
        daily.append(dd)
    B = pd.concat(rows, ignore_index=True)
    D = pd.concat(daily, ignore_index=True)
    out["coin_mean_daily"] = D.groupby("coin")["coin_return"].mean()
    out["book_mean_daily_by_coin"] = D.groupby("coin")["book_return"].mean()
    out["share_short_bars"] = float((B["pos"] < 0).mean())
    out["mean_pos_when_short"] = float(B.loc[B.pos < 0, "pos"].mean())
    # decomposition per bar
    s = B[B.pos < 0]
    out["gain_short_bars_mean"] = float(s["gain"].mean())
    out["fee_mean_all_bars"] = float(B["fee"].mean())
    out["drift_part"] = float((B["pos"] * B["mu"]).mean())
    out["total_gain_mean_per_bar"] = float(B["gain"].mean())
    # by window book
    out["book_by_window"] = D.groupby("window")["book_return"].agg(["mean", "count"]).sort_values("mean").head(24)
    # grid: fwd5 excess by range position bucket among trending
    g = B[B.grid & (B.regime == "trending")].copy()
    g["ex5"] = g["fwd5"] - g["mu"] * 5
    g["rpb"] = pd.cut(g["rp"], [-0.01, 0.1, 0.25, 0.5, 1.01])
    out["ex5_by_rp"] = g.groupby("rpb")["ex5"].agg(["mean", "count", "std"])
    g["short"] = g["forecast"] < 0
    g["r60b"] = pd.qcut(g["r60"], 3)
    out["ex5_short_by_r60"] = g[g.short].groupby("r60b")["ex5"].agg(["mean", "count"])
    g["volb"] = pd.qcut(g["vol20"], 3)
    out["ex5_short_by_vol"] = g[g.short].groupby("volb")["ex5"].agg(["mean", "count"])
    out["raw5_short_by_r60"] = g[g.short].groupby("r60b")["fwd5"].agg(["mean", "count"])
    # trades
    T = pd.concat([t for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"] = T.groupby("side")[["profit_loss_percent", "net_profit_loss_percent", "duration_minutes"]].agg(["mean", "count"])
    return out
