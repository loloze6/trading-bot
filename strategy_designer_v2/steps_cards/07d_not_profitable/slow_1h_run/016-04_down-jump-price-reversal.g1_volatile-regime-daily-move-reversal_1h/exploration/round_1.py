def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    gross_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            pos = b["postRebalance_current_allocation"].astype(float)
            r1 = b["close"].shift(-1) / b["close"] - 1
            gross = pos * r1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            turn = (pos - b["previous_allocation"].astype(float)).abs()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"day": ts.dt.floor("D"), "gross": gross, "fee": fee, "turn": turn,
                               "abspos": pos.abs(), "f": b["forecast"].astype(float)})
            d = df.groupby("day").agg(gross=("gross", "sum"), fee=("fee", "sum"), turn=("turn", "sum"),
                                      abspos=("abspos", "mean"))
            d["coin"] = coin; d["w"] = w
            rows.append(d)
            # hourly forecast changes
            gross_rows.append(pd.DataFrame({"coin": coin, "fchg": b["forecast"].diff().abs().mean(),
                                            "flip": (np.sign(b["forecast"]).diff().abs() > 0).mean(),
                                            "autocorr24": b["forecast"].autocorr(24),
                                            "autocorr1": b["forecast"].autocorr(1)}, index=[0]))
    D = pd.concat(rows)
    out["per_coin_daily"] = D.groupby("coin")[["gross", "fee", "turn", "abspos"]].mean()
    out["all_daily_mean"] = D[["gross", "fee", "turn", "abspos"]].mean()
    out["gross_t"] = float(D["gross"].mean() / (D["gross"].std() / np.sqrt(len(D))))
    out["fc_dynamics"] = pd.concat(gross_rows).groupby("coin").mean()
    # book daily returns from days table
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; dd.append(t)
    DD = pd.concat(dd)
    out["book_by_coin"] = DD.groupby("coin")[["book_return", "coin_return"]].mean()
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    out["trades_summary"] = T.groupby("side")[["profit_loss_percent", "net_profit_loss_percent", "total_commission", "duration_minutes"]].agg(["mean", "count"])
    return out
