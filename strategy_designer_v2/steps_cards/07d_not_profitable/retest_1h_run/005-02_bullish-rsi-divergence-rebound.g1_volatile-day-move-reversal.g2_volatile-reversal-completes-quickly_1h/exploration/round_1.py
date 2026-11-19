def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []; buck = []; hz = []; yr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            c = b["close"]
            r1 = c.shift(-1) / c - 1
            a = b["postRebalance_current_allocation"]
            gross = a * r1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            f = b["forecast"]
            af = f.abs()
            bk = pd.cut(af, [-0.01, 0.001, 2.5, 5, 10, 15, 20.01], labels=["0", "0-2.5", "2.5-5", "5-10", "10-15", "15-20"])
            year = pd.to_datetime(b["timestamp"]).dt.year
            d = pd.DataFrame({"coin": coin, "gross": gross, "fee": fee, "bk": bk, "side": np.sign(a), "absa": a.abs(), "year": year})
            buck.append(d)
            for h in [6, 24, 72, 168]:
                idx = np.arange(0, len(b) - h, h)
                fr = (c.shift(-h) / c - 1).iloc[idx]
                ff = f.iloc[idx]
                m = ff != 0
                hz.append(pd.DataFrame({"coin": coin, "h": h, "s": np.sign(ff[m]) * fr[m], "big": (ff[m].abs() >= 10), "fr": fr[m], "dir": np.sign(ff[m])}))
    B = pd.concat(buck)
    out["per_coin_gross_fee_mean_per_bar"] = B.groupby("coin")[["gross", "fee"]].mean() * 24
    g = B.groupby("bk", observed=True).agg(n=("gross", "size"), gross_sum=("gross", "sum"), fee_sum=("fee", "sum"), absa=("absa", "mean"))
    out["by_forecast_bucket"] = g
    out["by_side"] = B.groupby("side").agg(n=("gross", "size"), gross_sum=("gross", "sum"), fee_sum=("fee", "sum"))
    out["by_year"] = B.groupby("year").agg(gross_sum=("gross", "sum"), fee_sum=("fee", "sum"), n_active=("absa", lambda x: (x > 0).sum()))
    H = pd.concat(hz)
    def tt(x):
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 1 else np.nan})
    out["signed_fwd_by_h_big"] = H.groupby(["h", "big"])["s"].apply(tt).unstack()
    out["signed_fwd_by_h_dir"] = H.groupby(["h", "dir"])["s"].apply(tt).unstack()
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T)
    T["dur_h"] = T["duration_minutes"] / 60
    out["trades"] = T.groupby("side").agg(n=("side", "size"), pl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), dur_h=("dur_h", "median"))
    out["trades_by_dur"] = T.groupby(pd.cut(T["dur_h"], [0, 1, 3, 12, 48, 1e6])).agg(n=("side", "size"), pl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin))
    D = pd.concat(D)
    out["days"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std"])
    return out
