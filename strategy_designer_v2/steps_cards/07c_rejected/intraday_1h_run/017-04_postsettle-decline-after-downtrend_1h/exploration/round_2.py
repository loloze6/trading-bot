def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"]
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = c.shift(-1) / c - 1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            rows.append(pd.DataFrame({"coin": coin, "close_hour": (ts + pd.Timedelta(hours=1)).dt.hour,
                                      "year": ts.dt.year, "pos": pos, "gross": pos * r1, "fee": fee,
                                      "fc": b["forecast"], "regime": b["regime"]}))
    d = pd.concat(rows, ignore_index=True)
    act = d[d.pos.abs() > 0]
    out["active_by_close_hour"] = act.groupby("close_hour").agg(n=("pos", "size"), mean_pos=("pos", "mean"),
        gross_bp=("gross", lambda v: v.mean() * 1e4), t=("gross", lambda v: stats.ttest_1samp(v.dropna(), 0).statistic)).round(3)
    out["regime_by_close_hour"] = d[d.regime == "trending"].groupby("close_hour").size()
    out["fee_by_close_hour_bp"] = (d.groupby("close_hour")["fee"].sum() / d.groupby("coin").ngroups).round(5)
    out["total_gross_sum"] = float(d.gross.sum())
    out["total_fee_sum"] = float(d.fee.sum())
    out["gross_by_year"] = act.groupby("year").agg(n=("gross", "size"), gross_bp=("gross", lambda v: v.mean() * 1e4),
        t=("gross", lambda v: stats.ttest_1samp(v.dropna(), 0).statistic)).round(3)
    out["gross_by_coin"] = act.groupby("coin").agg(n=("gross", "size"), gross_bp=("gross", lambda v: v.mean() * 1e4),
        t=("gross", lambda v: stats.ttest_1samp(v.dropna(), 0).statistic)).round(3)
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin))
    dd = pd.concat(dd)
    out["daily_book_mean"] = float(dd.book_return.mean())
    return out
