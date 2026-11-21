def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # trades: durations, gross vs net
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if t is None or len(t) == 0: continue
            d = t.copy(); d["coin"] = c; d["win"] = w; tr.append(d)
    tr = pd.concat(tr, ignore_index=True)
    out["trades_summary"] = pd.Series({
        "n_trades": len(tr),
        "share_long": (tr["side"] == "LONG").mean(),
        "median_duration_h": tr["duration_minutes"].median() / 60,
        "mean_duration_h": tr["duration_minutes"].mean() / 60,
        "share_duration_le_1h": (tr["duration_minutes"] <= 60).mean(),
        "mean_gross_pct": tr["profit_loss_percent"].mean(),
        "mean_net_pct": tr["net_profit_loss_percent"].mean(),
        "t_gross": tr["profit_loss_percent"].mean() / (tr["profit_loss_percent"].std() / np.sqrt(len(tr))),
        "share_net_positive": (tr["net_profit_loss_percent"] > 0).mean(),
    })
    # path of excess return after active 20:00 bars, by hour after
    rows = []
    for c in data["bars"]:
        # coin mean hourly return over all windows
        allr = []
        for w, b in data["bars"][c].items():
            allr.append(b["close"].pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            idx = np.where(b["forecast"].fillna(0).values > 0)[0]
            for i in idx:
                for h in [1, 2, 4, 8, 12, 24]:
                    if i + h < len(cl):
                        rows.append((c, h, cl[i + h] / cl[i] - 1 - mu * h, b["forecast"].iloc[i],
                                     b["postRebalance_current_allocation"].iloc[i],
                                     b["postRebalance_current_allocation"].iloc[i + 1] if i + 1 < len(b) else np.nan))
    df = pd.DataFrame(rows, columns=["coin", "h", "ex", "fc", "alloc", "alloc_next"])
    g = df.groupby("h")["ex"]
    out["excess_path_by_h"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
                                            "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    d1 = df[df.h == 1]
    out["alloc_at_signal"] = pd.Series({"mean_alloc": d1["alloc"].mean(),
                                        "mean_alloc_next_bar": d1["alloc_next"].mean(),
                                        "share_next_flat": (d1["alloc_next"].abs() < 1e-9).mean()})
    out["excess24_by_coin"] = df[df.h == 24].groupby("coin")["ex"].agg(["size", "mean"])
    # book: daily returns, held hours
    hb = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            a = b["postRebalance_current_allocation"].fillna(0)
            hb.append(pd.Series({"held_share": (a.abs() > 1e-9).mean(),
                                 "fee_drag": ((b["total_portfolio_value"].shift(-1) - b["postRebalance_total_value"]) * 0).sum()}))
    out["share_bars_held"] = float(pd.concat(hb, axis=1).T["held_share"].mean())
    return out
