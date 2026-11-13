def explore(data):
    import pandas as pd, numpy as np
    out = {}
    trows = []
    drows = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if t is None or len(t) == 0:
                continue
            tt = t.copy()
            tt["coin"] = coin; tt["window"] = w
            tt["year"] = pd.to_datetime(tt["entry_time"]).dt.year
            trows.append(tt)
    T = pd.concat(trows, ignore_index=True)
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; dd["window"] = w
            dd["year"] = pd.to_datetime(dd["day"]).dt.year
            # coin trailing 20d return known at close, and vol
            dd["trend20"] = dd["close"] / dd["close"].shift(20) - 1
            dd["vol20"] = dd["coin_return"].rolling(20).std()
            dd["nextbook"] = dd["book_return"].shift(-1)
            drows.append(dd)
    D = pd.concat(drows, ignore_index=True)

    out["trades_overall"] = pd.Series({
        "n": len(T), "gross_sum": T.profit_loss_percent.sum(), "net_sum": T.net_profit_loss_percent.sum(),
        "fee_share_of_gross": 1 - T.net_profit_loss_percent.sum() / T.profit_loss_percent.sum(),
        "win_rate_net": (T.net_profit_loss_percent > 0).mean(),
        "mean_dur_days": T.duration_minutes.mean() / 1440,
        "share_long": (T.side == "LONG").mean(),
    })
    s = T.net_profit_loss_percent.sort_values(ascending=False)
    tot = s.sum()
    out["top_trade_concentration"] = pd.Series({
        "top5_share": s.head(5).sum() / tot, "top10_share": s.head(10).sum() / tot,
        "top20_share": s.head(20).sum() / tot, "top1pct_share": s.head(max(1, len(s)//100)).sum() / tot,
        "net_sum_ex_top10": s.iloc[10:].sum(),
    })
    g = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "sum"),
                              net=("net_profit_loss_percent", "sum"), mean_net=("net_profit_loss_percent", "mean"),
                              win=("net_profit_loss_percent", lambda x: (x > 0).mean()))
    out["by_coin_trades"] = g
    out["by_year_trades"] = T.groupby("year").agg(n=("net_profit_loss_percent", "size"),
                                                   gross=("profit_loss_percent", "sum"),
                                                   net=("net_profit_loss_percent", "sum"))
    out["by_window_trades_net"] = T.pivot_table(index="window", columns="coin", values="net_profit_loss_percent", aggfunc="sum").round(1)
    out["by_regime_trades"] = T.groupby("entry_regime").agg(n=("net_profit_loss_percent", "size"),
                                                            net=("net_profit_loss_percent", "sum"),
                                                            mean=("net_profit_loss_percent", "mean"))
    # daily book returns by market state known at close (next day's book return)
    D2 = D.dropna(subset=["trend20", "vol20", "nextbook"])
    D2 = D2.assign(trend_state=np.where(D2.trend20 > 0, "up20", "down20"))
    D2["vol_q"] = D2.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=["calm", "mid", "wild"]))
    out["book_by_trend"] = D2.groupby("trend_state")["nextbook"].agg(["count", "mean", "sum"])
    out["book_by_vol"] = D2.groupby("vol_q")["nextbook"].agg(["count", "mean", "sum"])
    out["book_by_trend_vol"] = D2.groupby(["trend_state", "vol_q"])["nextbook"].agg(["count", "mean", "sum"])
    out["book_coin_year_sum"] = D.groupby(["coin", "year"])["book_return"].sum().unstack().round(2)
    return out
