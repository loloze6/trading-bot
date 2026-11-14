def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if df is None or len(df) == 0: continue
            d = df.copy(); d["coin"] = c; d["win"] = w; tr.append(d)
    T = pd.concat(tr, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440.0
    T["fee"] = T["profit_loss_percent"] - T["net_profit_loss_percent"]
    out["trades_summary"] = pd.Series({
        "n": len(T), "share_long": (T.side == "LONG").mean(),
        "mean_days": T.days.mean(), "median_days": T.days.median(),
        "mean_gross": T.profit_loss_percent.mean(), "mean_net": T.net_profit_loss_percent.mean(),
        "mean_fee": T.fee.mean(), "win_rate_gross": (T.profit_loss_percent > 0).mean(),
        "sum_gross": T.profit_loss_percent.sum(), "sum_fee": T.fee.sum()})
    T["dur_b"] = pd.cut(T.days, [0, 1.5, 3.5, 7.5, 20.5, 60.5, 1e4])
    out["trades_by_duration"] = T.groupby("dur_b", observed=True).agg(
        n=("days", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), fee=("fee", "mean"), sumnet=("net_profit_loss_percent", "sum"))
    out["trades_by_coin"] = T.groupby("coin").agg(n=("days", "size"), days=("days", "mean"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), sumnet=("net_profit_loss_percent", "sum"))
    # days
    D = []
    for c, ws in data["days"].items():
        for w, df in ws.items():
            d = df.copy(); d["coin"] = c; d["win"] = w
            v = d["book_value"].values
            d["dd"] = v / np.maximum.accumulate(v) - 1
            d["cvol"] = d["coin_return"].rolling(20, min_periods=10).std().shift(1)
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    D["up"] = np.where(D.coin_return > 0, "coin_up", "coin_down")
    out["book_by_coin_dir"] = D.groupby("up").agg(n=("book_return", "size"),
        book=("book_return", "mean"), coin=("coin_return", "mean"), sumbook=("book_return", "sum"))
    D["volq"] = D.groupby("coin")["cvol"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["book_by_volq"] = D.groupby("volq").agg(n=("book_return", "size"),
        book=("book_return", "mean"), sd=("book_return", "std"), sumbook=("book_return", "sum"))
    out["book_by_year"] = D.groupby("year").agg(book=("book_return", "mean"),
        sumbook=("book_return", "sum"), coin=("coin_return", "mean"), mindd=("dd", "min"))
    out["maxdd_by_coin"] = D.groupby("coin").dd.min()
    out["worst_window_dd"] = D.groupby(["coin", "win"]).dd.min().sort_values().head(10).reset_index().assign(
        coin_ret=lambda x: x.apply(lambda r: (1 + D[(D.coin == r.coin) & (D.win == r.win)].coin_return.fillna(0)).prod() - 1, axis=1))
    # bars: forecast buckets non-overlapping 20-bar forward
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b.close.values; n = len(b)
            fwd20 = pd.Series(cl).shift(-20).values / cl - 1
            fwd5 = pd.Series(cl).shift(-5).values / cl - 1
            mom = pd.Series(cl).pct_change(20).values
            for i in range(0, n, 20):
                if not np.isnan(fwd20[i]):
                    rows.append((c, w, b.forecast.iloc[i], fwd20[i], mom[i]))
    R = pd.DataFrame(rows, columns=["coin", "win", "f", "fwd", "mom"])
    R["cm"] = R.groupby("coin").fwd.transform("mean")
    R["ex"] = R.fwd - R.cm
    R["fb"] = pd.cut(R.f, [-1e-9, 1e-9, 0.5, 1, 1.5, 2.5, 100], include_lowest=True)
    out["fwd20_by_forecast"] = R.groupby("fb", observed=True).agg(n=("ex", "size"),
        ex=("ex", "mean"), t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s)) if len(s) > 2 else np.nan),
        hit=("fwd", lambda s: (s > 0).mean()))
    R["momb"] = pd.cut(R.mom, [-10, 0, 0.1, 0.25, 0.5, 100])
    out["fwd20_by_mom_active"] = R[R.f > 0].groupby("momb", observed=True).agg(n=("ex", "size"), ex=("ex", "mean"),
        t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s)) if len(s) > 2 else np.nan))
    return out
