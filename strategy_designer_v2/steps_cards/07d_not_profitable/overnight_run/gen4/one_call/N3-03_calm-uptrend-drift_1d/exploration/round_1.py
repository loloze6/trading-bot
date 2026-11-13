def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if df is None or len(df) == 0: continue
            d = df.copy(); d["coin"] = c; d["win"] = w
            tr.append(d)
    tr = pd.concat(tr, ignore_index=True)
    tr["dur_d"] = tr["duration_minutes"] / 1440.0
    tr["fee"] = tr["profit_loss_percent"] - tr["net_profit_loss_percent"]
    out["trades_overall"] = pd.Series({
        "n": len(tr), "share_long": (tr["side"] == "LONG").mean(),
        "mean_dur_d": tr["dur_d"].mean(), "median_dur_d": tr["dur_d"].median(),
        "mean_gross": tr["profit_loss_percent"].mean(), "median_gross": tr["profit_loss_percent"].median(),
        "mean_net": tr["net_profit_loss_percent"].mean(), "mean_fee": tr["fee"].mean(),
        "win_rate_gross": (tr["profit_loss_percent"] > 0).mean(),
        "t_gross": tr["profit_loss_percent"].mean() / tr["profit_loss_percent"].std() * np.sqrt(len(tr)),
        "worst_gross": tr["profit_loss_percent"].min(), "best_gross": tr["profit_loss_percent"].max(),
        "p05_gross": tr["profit_loss_percent"].quantile(0.05), "p95_gross": tr["profit_loss_percent"].quantile(0.95)})
    tr["durb"] = pd.cut(tr["dur_d"], [0, 1.5, 3.5, 7.5, 15.5, 1000])
    out["trades_by_dur"] = tr.groupby("durb", observed=True).agg(n=("fee", "size"), gross=("profit_loss_percent", "mean"),
                                                          net=("net_profit_loss_percent", "mean"), fee=("fee", "mean"))
    out["trades_by_coin"] = tr.groupby("coin").agg(n=("fee", "size"), gross=("profit_loss_percent", "mean"),
                                                   net=("net_profit_loss_percent", "mean"), dur=("dur_d", "mean"))
    # bars: forecast buckets, non-overlapping 5-bar fwd
    rows = []
    dd = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            fwd5 = pd.Series(cl).shift(-5) / pd.Series(cl) - 1
            r1 = pd.Series(cl).pct_change()
            vol20 = r1.rolling(20).std()
            ret20 = pd.Series(cl) / pd.Series(cl).shift(20) - 1
            for i in range(0, n - 5, 5):
                rows.append(dict(coin=c, win=w, yr=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 f=b["forecast"].iloc[i], alloc=b["postRebalance_current_allocation"].iloc[i],
                                 regime=b["regime"].iloc[i], fwd5=fwd5.iloc[i], vol20=vol20.iloc[i], ret20=ret20.iloc[i]))
            v = b["postRebalance_total_value"].values
            pk = np.maximum.accumulate(v)
            dd.append(dict(coin=c, win=w, mdd=(v / pk - 1).min(), ret=v[-1] / v[0] - 1,
                           hold=cl[-1] / cl[0] - 1, active=(b["forecast"] > 0).mean()))
    s = pd.DataFrame(rows).dropna(subset=["fwd5"])
    s["fb"] = pd.cut(s["f"], [-1e-9, 1e-9, 0.5, 1, 1.5, 2.5, 100])
    out["fwd5_by_forecast_nonoverlap"] = s.groupby("fb", observed=True)["fwd5"].agg(["size", "mean", "std"]).assign(
        t=lambda x: x["mean"] / x["std"] * np.sqrt(x["size"]))
    s["regime_in"] = s["regime"]
    out["fwd5_by_regime"] = s.groupby("regime")["fwd5"].agg(["size", "mean", "std"])
    act = s[s["f"] > 0]
    out["active_by_year"] = act.groupby("yr")["fwd5"].agg(["size", "mean", "std"])
    out["flat_by_year"] = s[s["f"] <= 0].groupby("yr")["fwd5"].agg(["size", "mean"])
    act = act.copy()
    act["vq"] = pd.qcut(act["vol20"], 3, labels=["lowv", "midv", "highv"])
    out["active_by_vol_tercile"] = act.groupby("vq", observed=True)["fwd5"].agg(["size", "mean", "std"])
    act["rq"] = pd.qcut(act["ret20"], 3, labels=["lowr", "midr", "highr"])
    out["active_by_ret20_tercile"] = act.groupby("rq", observed=True)["fwd5"].agg(["size", "mean", "std"])
    D = pd.DataFrame(dd)
    out["dd_by_coin"] = D.groupby("coin")[["mdd", "ret", "hold", "active"]].mean()
    out["dd_by_window"] = D.groupby("win")[["mdd", "ret", "hold", "active"]].mean()
    # days pooled: book returns when long vs market up/down
    dl = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = c; dl.append(d)
    dl = pd.concat(dl).dropna(subset=["book_return", "coin_return"])
    inm = dl["book_return"].abs() > 1e-12
    out["days_invested"] = pd.Series({"share_invested": inm.mean(),
        "mean_book_inv": dl.loc[inm, "book_return"].mean(), "mean_coin_inv": dl.loc[inm, "coin_return"].mean(),
        "mean_coin_notinv": dl.loc[~inm, "coin_return"].mean(),
        "worst_book_day": dl["book_return"].min(), "p01_book": dl.loc[inm, "book_return"].quantile(0.01)})
    return out
