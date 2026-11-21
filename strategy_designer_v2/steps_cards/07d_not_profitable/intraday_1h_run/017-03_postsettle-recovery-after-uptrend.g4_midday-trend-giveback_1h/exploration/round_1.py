def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t) == 0: continue
            d = t.copy(); d["coin"] = c; d["win"] = w
            tr.append(d)
    tr = pd.concat(tr)
    tr["gross"] = tr["profit_loss_percent"]; tr["net"] = tr["net_profit_loss_percent"]
    tr["fee_gap"] = tr["gross"] - tr["net"]
    out["trades_summary"] = pd.DataFrame({
        "n": [len(tr)], "mean_gross": [tr.gross.mean()], "mean_net": [tr.net.mean()],
        "mean_fee_gap": [tr.fee_gap.mean()], "median_dur_min": [tr.duration_minutes.median()],
        "t_gross": [stats.ttest_1samp(tr.gross.dropna(), 0).statistic],
        "share_gross_pos": [(tr.gross > 0).mean()]})
    tr["absf"] = tr["entry_forecast"].abs()
    tr["fq"] = pd.qcut(tr["absf"], 5, labels=False, duplicates="drop")
    out["by_entry_force_quintile"] = tr.groupby("fq").agg(n=("gross", "size"), absf=("absf", "mean"),
        gross=("gross", "mean"), net=("net", "mean"), fee=("fee_gap", "mean"))
    out["by_coin"] = tr.groupby("coin").agg(n=("gross", "size"), gross=("gross", "mean"), net=("net", "mean"), fee=("fee_gap", "mean"))
    out["by_side"] = tr.groupby("side").agg(n=("gross", "size"), gross=("gross", "mean"), net=("net", "mean"))
    # bar-level gross vs fee
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            r = b["close"].shift(-1) / b["close"] - 1
            pos = b["postRebalance_current_allocation"]
            g = pos * r
            fee = b["total_portfolio_value"] - b["postRebalance_total_value"]
            fee_frac = fee / b["total_portfolio_value"]
            hr = pd.to_datetime(b["timestamp"]).dt.hour
            rows.append(pd.DataFrame({"coin": c, "hr": hr, "g": g, "fee": fee_frac, "pos": pos.abs(),
                                      "chg": b["allocation_change"].abs() if "allocation_change" in b else np.nan}))
    B = pd.concat(rows)
    out["by_hour"] = B.groupby("hr").agg(gross=("g", "mean"), fee=("fee", "mean"), abspos=("pos", "mean"), chg=("chg", "mean")).loc[[9, 10, 11, 12, 13, 14]]
    out["daily_gross_vs_fee_per_coin_day"] = pd.Series({"gross_per_day": B.g.sum() / (len(B) / 24),
                                                        "fee_per_day": B.fee.sum() / (len(B) / 24)})
    # day book returns
    D = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            D.append(d.assign(win=w))
    D = pd.concat(D)
    out["book_by_year"] = D.assign(yr=pd.to_datetime(D["day"]).dt.year).groupby("yr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    return out
