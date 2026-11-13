def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # trade table with entry context
    rows = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if t is None or len(t) == 0: continue
            b = data["bars"][coin][w].copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["sma100"] = b["close"].rolling(100).mean()
            b["ret"] = b["close"].pct_change()
            b["vol20"] = b["ret"].rolling(20).std()
            b["mom60"] = b["close"] / b["close"].shift(60) - 1
            tt = t.copy(); tt["coin"] = coin; tt["window"] = w
            tt["et"] = pd.to_datetime(tt["entry_time"])
            m = pd.merge_asof(tt.sort_values("et"), b[["ts", "close", "sma100", "vol20", "mom60"]].sort_values("ts"),
                              left_on="et", right_on="ts", direction="backward")
            rows.append(m)
    T = pd.concat(rows, ignore_index=True)
    s = T.sort_values("net_profit_loss_percent", ascending=False)
    out["top10_trades"] = s.head(10)[["coin", "window", "net_profit_loss_percent", "duration_minutes", "mom60"]].assign(
        dur_days=lambda x: x.duration_minutes / 1440).drop(columns="duration_minutes").reset_index(drop=True)
    T["above_sma100"] = np.where(T.sma100.isna(), "na", np.where(T.close > T.sma100, "above", "below"))
    out["trades_by_sma100"] = T.groupby("above_sma100")["net_profit_loss_percent"].agg(["count", "mean", "median", "sum", lambda x: (x > 0).mean()])
    T["mom_state"] = np.where(T.mom60.isna(), "na", np.where(T.mom60 > 0, "mom60_up", "mom60_down"))
    out["trades_by_mom60"] = T.groupby("mom_state")["net_profit_loss_percent"].agg(["count", "mean", "median", "sum"])
    T["volq"] = T.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=["calm", "mid", "wild"]))
    out["trades_by_vol"] = T.groupby("volq")["net_profit_loss_percent"].agg(["count", "mean", "median", "sum"])
    # log-return based net trade contribution (compounding-fair)
    T["lr"] = np.log1p(T.net_profit_loss_percent / 100)
    T["lr_gross"] = np.log1p(T.profit_loss_percent / 100)
    out["log_sums"] = pd.Series({"net_log_sum": T.lr.sum(), "gross_log_sum": T.lr_gross.sum(),
                                 "fee_share_log": 1 - T.lr.sum() / T.lr_gross.sum(),
                                 "net_log_ex_ZEC_w24": T[~((T.coin == "ZECUSD") & (T.window == "w24"))].lr.sum()})
    out["log_by_coin"] = T.groupby("coin")[["lr", "lr_gross"]].sum()
    # daily book Sharpe, overall and leaving out
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["book_return", "coin_return"]].copy(); dd["coin"] = coin; dd["window"] = w
            dd["year"] = pd.to_datetime(d["day"]).dt.year
            D.append(dd)
    D = pd.concat(D).dropna()
    sh = lambda x: x.mean() / x.std() * np.sqrt(365)
    out["book_sharpe_variants"] = pd.Series({
        "all": sh(D.book_return),
        "ex_ZEC_w24": sh(D[~((D.coin == "ZECUSD") & (D.window == "w24"))].book_return),
        "ex_ZEC": sh(D[D.coin != "ZECUSD"].book_return),
        "ex_2020": sh(D[D.year != 2020].book_return),
        "ex_2020_2024_2025": sh(D[~D.year.isin([2020, 2024, 2025])].book_return),
        "hold_all": sh(D.coin_return),
    })
    out["book_sharpe_by_year"] = D.groupby("year").apply(lambda x: pd.Series({"book": sh(x.book_return), "hold": sh(x.coin_return)}))
    # non-overlapping 10-bar forward coin return after new 20-day highs, by 60-bar momentum
    ev = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].reset_index(drop=True)
            hi = c.rolling(20).max()
            mom = c / c.shift(60) - 1
            fwd = c.shift(-10) / c - 1
            base = fwd.mean()
            last = -999
            for i in range(len(c)):
                if pd.notna(hi.iloc[i]) and c.iloc[i] >= hi.iloc[i] and i >= 20 and i - last >= 10 and pd.notna(fwd.iloc[i]) and pd.notna(mom.iloc[i]):
                    ev.append((coin, "up" if mom.iloc[i] > 0 else "down", fwd.iloc[i] - base)); last = i
    E = pd.DataFrame(ev, columns=["coin", "mom", "x"])
    out["events_by_mom60"] = E.groupby("mom")["x"].agg(["count", "mean", lambda x: stats.ttest_1samp(x, 0).statistic])
    out["events_by_coin"] = E.groupby("coin")["x"].agg(["count", "mean", lambda x: stats.ttest_1samp(x, 0).statistic])
    return out
