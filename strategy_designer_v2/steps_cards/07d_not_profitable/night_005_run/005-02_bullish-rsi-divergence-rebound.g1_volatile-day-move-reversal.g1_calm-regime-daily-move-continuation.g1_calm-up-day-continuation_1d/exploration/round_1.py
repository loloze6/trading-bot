def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    hold_rows = []
    lag_rows = []
    fee_rows = []
    dd_rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = b["close"].shift(-1) / b["close"] - 1
            g = pos * r1
            fc = b["forecast"].fillna(0)
            ret = b["close"].pct_change()
            # bars since last positive forecast
            last = pd.Series(np.where(fc > 0, np.arange(len(b)), np.nan)).ffill()
            since = np.arange(len(b)) - last.values
            for k in range(0, 15):
                m = (since == k)
                if m.sum():
                    lag_rows.append(dict(coin=coin, k=k, n=int(m.sum()),
                                         pos=pos[m].mean(), r1=r1[m].mean(), g=g[m].mean()))
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]).clip(lower=0) / b["total_portfolio_value"]
            fee_rows.append(dict(coin=coin, fee_sum=fee.sum(), gross=g.sum(), active=(pos.abs() > 0.01).mean(),
                                 meanpos=pos.mean(), turnover=b["allocation_change"].abs().sum() if "allocation_change" in b else np.nan))
            d = data["days"][coin][w]
            rows.append(dict(coin=coin, w=w, book=d["book_return"].mean(), coin_r=d["coin_return"].mean(),
                             n=d["book_return"].notna().sum()))
    lag = pd.DataFrame(lag_rows)
    lagt = lag.assign(wg=lag.g * lag.n, wr=lag.r1 * lag.n, wp=lag.pos * lag.n).groupby("k")[["n", "wg", "wr", "wp"]].sum()
    lagt["g"] = lagt.wg / lagt.n; lagt["r1"] = lagt.wr / lagt.n; lagt["pos"] = lagt.wp / lagt.n
    out["by_days_since_signal"] = lagt[["n", "pos", "r1", "g"]]
    out["fees_by_coin"] = pd.DataFrame(fee_rows).groupby("coin").sum(numeric_only=True)
    wdf = pd.DataFrame(rows)
    out["by_window"] = wdf.pivot(index="w", columns="coin", values=["book", "coin_r"])
    # combined daily book: mean over coins per day
    allb = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            allb.append(d.assign(coin=coin, w=w))
    D = pd.concat(allb)
    out["daily_coin_overall"] = pd.Series(dict(book_mean=D.book_return.mean(), coin_mean=D.coin_return.mean(),
                                               book_sd=D.book_return.std(), coin_sd=D.coin_return.std()))
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    T["dur_d"] = T.duration_minutes / 1440
    out["trades"] = pd.Series(dict(n=len(T), mean_net=T.net_profit_loss_percent.mean(),
                                   mean_gross=T.profit_loss_percent.mean(), win=(T.net_profit_loss_percent > 0).mean(),
                                   med_dur=T.dur_d.median(), mean_dur=T.dur_d.mean(), mean_comm=T.total_commission.mean()))
    T["db"] = pd.cut(T.dur_d, [0, 1.5, 3.5, 6.5, 10.5, 1000])
    out["trades_by_dur"] = T.groupby("db")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    return out
