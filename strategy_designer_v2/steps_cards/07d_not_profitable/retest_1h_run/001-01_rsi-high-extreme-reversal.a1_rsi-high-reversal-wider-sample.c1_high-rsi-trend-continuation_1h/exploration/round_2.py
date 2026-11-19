def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            r = b["close"].shift(-1) / b["close"] - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            ts = pd.to_datetime(b["timestamp"])
            day = ts.dt.floor("D")
            # daily book from recorded values
            gross = pos * r
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            # slow positions: hold the position chosen at the first bar of each 24h / 168h block
            idx = np.arange(len(b))
            res = {"coin": coin, "w": w}
            for k, h in [("h1", 1), ("h24", 24), ("h72", 72), ("h168", 168)]:
                p = pos.values.copy()
                p = pd.Series(p).groupby(idx // h).transform("first").values
                turn = np.abs(np.diff(np.r_[0, p]))
                g = p * r.values
                res[k + "_gross"] = np.nansum(g)
                res[k + "_fee"] = np.nansum(turn) * 0.0011
            res["n"] = len(b)
            # forecast autocorr: share of bars where forecast changes sign of activity
            fc = b["forecast"]
            res["switch_on_off"] = ((fc > 0) != (fc.shift() > 0)).sum()
            res["dpos_from_fc"] = (b["sizing_signal_change"].abs().sum() if "sizing_signal_change" in b else np.nan)
            rows.append(res)
    R = pd.DataFrame(rows)
    tot = R.drop(columns=["coin", "w"]).sum()
    days = tot["n"] / 24
    summ = {}
    for k in ["h1", "h24", "h72", "h168"]:
        summ[k] = {"gross_per_day": tot[k + "_gross"] / days, "fee_per_day": tot[k + "_fee"] / days,
                   "net_per_day": (tot[k + "_gross"] - tot[k + "_fee"]) / days}
    out["slow_variants"] = pd.DataFrame(summ).T
    out["on_off_switches_per_day"] = float(tot["switch_on_off"] / days)
    # by window: slow h168 net vs h1 net
    R["h1_net"] = R.h1_gross - R.h1_fee; R["h168_net"] = R.h168_gross - R.h168_fee
    out["by_window"] = R.groupby("w")[["h1_gross", "h1_net", "h168_gross", "h168_net"]].sum()
    # daily book Sharpe recorded
    D = pd.concat([d.assign(coin=c, w=w) for c, ws in data["days"].items() for w, d in ws.items()])
    dm = D.groupby("day").book_return.mean()
    out["book_sharpe"] = float(dm.mean() / dm.std() * np.sqrt(365))
    out["book_mean_daily"] = float(dm.mean())
    # gross trade return by forecast level bucket at entry
    tr = pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    tr["fb"] = pd.cut(tr.entry_forecast, [-0.1, 2, 5, 10, 15, 20.1])
    out["trades_by_entry_fc"] = tr.groupby("fb").agg(n=("side", "size"), pl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60))
    return out
