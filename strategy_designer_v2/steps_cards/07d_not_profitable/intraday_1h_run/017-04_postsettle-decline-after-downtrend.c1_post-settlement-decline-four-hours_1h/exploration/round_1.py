def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []; trs = []; dys = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            b["hour"] = ts.dt.hour
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            b["gross"] = pos * b["ret1"]
            b["pos"] = pos
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["coin"] = c; b["w"] = w
            rows.append(b[["coin", "w", "hour", "ret1", "gross", "pos", "fee", "forecast", "regime"]])
            t = data["trades"][c].get(w)
            if t is not None and len(t):
                t = t.copy(); t["coin"] = c; trs.append(t)
            d = data["days"][c][w].copy(); d["coin"] = c; d["w"] = w; dys.append(d)
    B = pd.concat(rows); T = pd.concat(trs); D = pd.concat(dys)
    out["by_hour"] = B.groupby("hour").agg(share_held=("pos", lambda x: (x != 0).mean()), mean_pos=("pos", "mean"), gross=("gross", "mean"), fee=("fee", "mean"), ret=("ret1", "mean"))
    out["totals"] = pd.Series({"gross_per_bar_sum_mean_by_bar": B["gross"].mean(), "fee_per_bar": B["fee"].mean(), "gross_daily_approx": B["gross"].mean() * 24, "fee_daily_approx": B["fee"].mean() * 24, "book_daily": D["book_return"].mean()})
    T["dur_h"] = T["duration_minutes"] / 60
    out["trades"] = pd.Series({"n": len(T), "mean_pl_gross": T["profit_loss_percent"].mean(), "mean_pl_net": T["net_profit_loss_percent"].mean(), "mean_comm": T["total_commission"].mean(), "mean_dur_h": T["dur_h"].mean(), "share_short": (T["side"] == "SHORT").mean(), "t_gross": T["profit_loss_percent"].mean() / T["profit_loss_percent"].std() * np.sqrt(len(T))})
    out["dur_dist"] = T["dur_h"].round().value_counts().sort_index().head(15)
    out["by_coin"] = B.groupby("coin").agg(gross=("gross", "mean"), fee=("fee", "mean"), held=("pos", lambda x: (x != 0).mean()))
    act = B[B["pos"] != 0].copy()
    act["q"] = pd.qcut(act["forecast"].rank(method="first"), 3, labels=["strong", "mid", "weak"])
    out["by_fc_third"] = act.groupby("q").agg(n=("ret1", "size"), ret=("ret1", "mean"), gross=("gross", "mean"), abspos=("pos", lambda x: x.abs().mean()))
    out["T_by_year_dummy"] = T.assign(y=pd.to_datetime(T["entry_time"]).dt.year).groupby("y")[["profit_loss_percent", "net_profit_loss_percent"]].mean()
    return out
