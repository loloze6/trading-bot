def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # 1. book: daily returns, gross gain decomposition, fees
    drows = []
    for c in days:
        for w, d in days[c].items():
            drows.append(d.assign(coin=c, win=w))
    D = pd.concat(drows)
    # per bar position gain and fees
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            r1 = b["close"].shift(-1) / b["close"] - 1
            pos = b["postRebalance_current_allocation"]
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            rows.append(pd.DataFrame({"coin": c, "win": w, "pos": pos, "r1": r1, "gain": pos * r1, "fee": fee,
                                      "fc": b["forecast"], "reg": b["regime"],
                                      "hour": pd.to_datetime(b["timestamp"]).dt.hour,
                                      "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                                      "close": b["close"]}))
    B = pd.concat(rows, ignore_index=True)
    s = B.groupby("coin").agg(gross_gain_per_bar=("gain", "mean"), fee_per_bar=("fee", "mean"),
                              mean_pos=("pos", "mean"), share_long=("pos", lambda x: (x > 0).mean()),
                              mean_r1=("r1", "mean"))
    s["gross_per_day"] = s.gross_gain_per_bar * 24
    s["fee_per_day"] = s.fee_per_bar * 24
    s["market_part_per_day"] = s.mean_pos * s.mean_r1 * 24
    out["book_decomp_by_coin"] = s
    out["book_daily_by_coin"] = D.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    # 2. forward 240-bar returns by forecast bins, regime, non-overlapping grid
    g = []
    for c in bars:
        for w, b in bars[c].items():
            idx = np.arange(0, len(b), 240)
            cl = b["close"].values
            ok = idx + 240 < len(b)
            idx = idx[ok]
            fr = cl[idx + 240] / cl[idx] - 1
            past = np.full(len(idx), np.nan)
            m = idx >= 240
            past[m] = cl[idx[m]] / cl[idx[m] - 240] - 1
            past24 = np.full(len(idx), np.nan)
            m2 = idx >= 24
            past24[m2] = cl[idx[m2]] / cl[idx[m2] - 24] - 1
            lr = np.log(b["close"]).diff()
            vol = lr.rolling(240).std().values[idx]
            g.append(pd.DataFrame({"coin": c, "win": w, "fr": fr, "fc": b["forecast"].values[idx],
                                   "reg": b["regime"].values[idx], "past": past, "past24": past24, "vol": vol}))
    G = pd.concat(g, ignore_index=True)
    G["ex"] = G.fr - G.groupby("coin").fr.transform("mean")
    G["fcbin"] = pd.cut(G.fc, [-0.01, 0.001, 5, 10, 15, 20.1])
    out["fwd10d_by_forecast_bin"] = G.groupby("fcbin", observed=True).ex.agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["fwd10d_by_regime"] = G.groupby("reg").ex.agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # past 10d return quintile, per coin rank
    G["pq"] = G.groupby("coin").past.transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["fwd10d_by_past10d_q"] = G.groupby("pq").ex.agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    G["vq"] = G.groupby("coin").vol.transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["fwd10d_by_vol_q"] = G.groupby("vq").ex.agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # 3. 24h horizon: after large 24h moves, grid 24
    h = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(24, len(b) - 24, 24)
            h.append(pd.DataFrame({"coin": c, "f24": cl[idx + 24] / cl[idx] - 1, "p24": cl[idx] / cl[idx - 24] - 1,
                                   "p1": cl[idx] / cl[idx - 1] - 1}))
    H = pd.concat(h, ignore_index=True)
    H["ex"] = H.f24 - H.groupby("coin").f24.transform("mean")
    H["q"] = H.groupby("coin").p24.transform(lambda x: pd.qcut(x, 10, labels=False))
    out["fwd1d_by_past1d_decile"] = H.groupby("q").ex.agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # 4. hour/weekday of 1h returns
    out["r1_by_hour_t"] = B.groupby("hour").r1.agg(lambda x: x.mean() / x.std() * np.sqrt(len(x))).round(2)
    out["r1_by_wd"] = B.groupby("wd").r1.agg(["mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
                                          net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60))
    return out
