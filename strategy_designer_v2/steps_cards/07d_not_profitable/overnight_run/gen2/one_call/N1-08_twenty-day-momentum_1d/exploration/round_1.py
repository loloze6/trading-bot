def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # trades summary
    rows = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t) == 0: continue
            d = t.copy(); d["coin"] = c; d["win"] = w
            rows.append(d)
    T = pd.concat(rows)
    T["dur_d"] = T["duration_minutes"] / 1440
    g = T.groupby("side").agg(n=("side", "size"), gross_mean=("profit_loss_percent", "mean"),
                              net_mean=("net_profit_loss_percent", "mean"), gross_sum=("profit_loss_percent", "sum"),
                              net_sum=("net_profit_loss_percent", "sum"), comm_sum=("total_commission", "sum"),
                              dur_med=("dur_d", "median"), dur_mean=("dur_d", "mean"), win=("profit_loss_percent", lambda x: (x > 0).mean()))
    out["trades_by_side"] = g
    out["trades_by_coin"] = T.groupby("coin").agg(n=("side", "size"), gross_sum=("profit_loss_percent", "sum"),
                                                  net_sum=("net_profit_loss_percent", "sum"), dur_med=("dur_d", "median"))
    T["absf"] = T["entry_forecast"].abs()
    T["fq"] = pd.qcut(T["absf"], 4, labels=False, duplicates="drop")
    out["trades_by_entry_absforecast_q"] = T.groupby("fq").agg(n=("side", "size"), absf=("absf", "mean"), gross_mean=("profit_loss_percent", "mean"), net_mean=("net_profit_loss_percent", "mean"), dur=("dur_d", "mean"))
    out["dur_bins"] = T.groupby(pd.cut(T["dur_d"], [0, 1.5, 3, 7, 20, 1000])).agg(n=("side", "size"), gross_mean=("profit_loss_percent", "mean"), net_mean=("net_profit_loss_percent", "mean"))

    # bars: non-overlapping forward 20 and book/hold per window
    nb = []
    wrows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            f = b["forecast"].values
            r1 = pd.Series(cl).pct_change()
            vol = r1.rolling(20).std()
            r20past = pd.Series(cl).pct_change(20)
            for i in range(0, len(b) - 20, 20):
                nb.append(dict(coin=c, win=w, f=f[i], fwd=cl[i + 20] / cl[i] - 1, fwd5=cl[min(i + 5, len(b)-1)] / cl[i] - 1,
                               vol=vol.iloc[i], past=r20past.iloc[i], year=b["timestamp"].iloc[i].year if hasattr(b["timestamp"].iloc[i], "year") else pd.Timestamp(b["timestamp"].iloc[i]).year))
            dd = data["days"][c][w]
            br = dd["book_return"].dropna(); cr = dd["coin_return"].dropna()
            alloc = b["postRebalance_current_allocation"]
            wrows.append(dict(coin=c, win=w, book=(1 + br).prod() - 1, hold=(1 + cr).prod() - 1,
                              absalloc=alloc.abs().mean(), long_share=(alloc > 0).mean(),
                              turnover=alloc.diff().abs().mean()))
    N = pd.DataFrame(nb).dropna(subset=["f"])
    N["fwd_ex"] = N["fwd"] - N.groupby("coin")["fwd"].transform("mean")
    N["fq"] = pd.qcut(N["f"], 5, labels=False, duplicates="drop")
    out["fwd20_by_forecast_quintile_nonoverlap"] = N.groupby("fq").agg(n=("f", "size"), f=("f", "mean"), fwd=("fwd", "mean"), fwd_ex=("fwd_ex", "mean"), signed=("fwd", lambda x: 0), fwd5=("fwd5", "mean"))
    N["sgnpnl"] = np.sign(N["f"]) * N["fwd"]
    N["volq"] = pd.qcut(N["vol"], 3, labels=["calm", "mid", "volatile"])
    out["signed_fwd20_by_vol"] = N.groupby("volq").agg(n=("f", "size"), signed=("sgnpnl", "mean"), t=("sgnpnl", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    out["signed_fwd20_by_side"] = N.groupby(np.sign(N["f"])).agg(n=("f", "size"), signed=("sgnpnl", "mean"), fwd=("fwd", "mean"), t=("sgnpnl", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    out["signed_fwd20_by_year"] = N.groupby("year").agg(n=("f", "size"), signed=("sgnpnl", "mean"), t=("sgnpnl", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    out["signed_fwd20_by_coin"] = N.groupby("coin").agg(n=("f", "size"), signed=("sgnpnl", "mean"), t=("sgnpnl", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    W = pd.DataFrame(wrows)
    W["mkt"] = np.where(W["hold"] > 0, "up", "down")
    out["windows_by_market"] = W.groupby("mkt").agg(n=("book", "size"), book=("book", "mean"), hold=("hold", "mean"), long_share=("long_share", "mean"))
    out["by_window"] = W.groupby("win").agg(book=("book", "mean"), hold=("hold", "mean"), absalloc=("absalloc", "mean"), turnover=("turnover", "mean"))
    return out
