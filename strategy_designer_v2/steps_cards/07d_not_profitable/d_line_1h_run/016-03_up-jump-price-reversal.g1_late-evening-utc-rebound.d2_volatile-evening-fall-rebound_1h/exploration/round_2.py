def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book daily returns
    br = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["coin"] = c; x["win"] = w; br.append(x)
    br = pd.concat(br)
    daily = br.groupby(["win", "day"])[["book_return", "coin_return"]].mean()
    out["book_daily"] = pd.Series({
        "mean_book": daily["book_return"].mean(),
        "sharpe_book": daily["book_return"].mean() / daily["book_return"].std() * np.sqrt(365),
        "mean_hold": daily["coin_return"].mean(),
        "n_days": len(daily)})
    # fee per trade, gross per trade vs first-hour bar return
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if t is None or len(t) == 0: continue
            tr.append(t)
    tr = pd.concat(tr)
    out["fee_per_trade_pct"] = float((tr["profit_loss_percent"] - tr["net_profit_loss_percent"]).mean())
    # per-case: excess over first hour, hours 1->24, by year and by forecast thirds, raw 24h return
    rows = []
    for c in data["bars"]:
        allr = []
        for w, b in data["bars"][c].items():
            cl = b["close"].values
            g = np.arange(0, len(cl) - 24, 24)
            allr.append(cl[g + 24] / cl[g] - 1)
        mu24 = np.concatenate(allr).mean()
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            fc = b["forecast"].fillna(0).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for i in np.where(fc > 0)[0]:
                if i + 24 < len(cl):
                    rows.append((c, w, yr[i], fc[i], cl[i + 1] / cl[i] - 1, cl[i + 24] / cl[i + 1] - 1,
                                 cl[i + 24] / cl[i] - 1, cl[i + 24] / cl[i] - 1 - mu24))
    df = pd.DataFrame(rows, columns=["coin", "win", "yr", "fc", "r1", "r1_24", "r24", "ex24"])
    def tt(s): return s.mean() / (s.std() / np.sqrt(len(s)))
    out["split_first_hour_vs_rest"] = pd.Series({
        "n": len(df), "mean_r1": df.r1.mean(), "t_r1": tt(df.r1),
        "mean_r1_24": df.r1_24.mean(), "t_r1_24": tt(df.r1_24),
        "mean_raw24": df.r24.mean(), "t_raw24": tt(df.r24),
        "raw24_minus_fee_0.001": df.r24.mean() - 0.001,
        "share_raw24_pos": (df.r24 > 0).mean()})
    g = df.groupby("yr")
    out["by_year"] = pd.DataFrame({"n": g.size(), "mean_r1": g.r1.mean(), "mean_raw24": g.r24.mean(),
                                   "mean_ex24": g.ex24.mean(), "t_ex24": g.ex24.apply(tt)})
    df["third"] = pd.qcut(df.fc.rank(method="first"), 3, labels=["low", "mid", "high"])
    g = df.groupby("third")
    out["by_forecast_third"] = pd.DataFrame({"n": g.size(), "mean_fc": g.fc.mean(), "mean_r1": g.r1.mean(),
                                             "mean_raw24": g.r24.mean(), "t_raw24": g.r24.apply(tt)})
    # loo by window of 24h-hold mean
    wins = df.win.unique()
    out["min_mean_raw24_loo_window"] = float(min(df[df.win != w].r24.mean() for w in wins))
    out["share_windows_raw24_pos"] = float((df.groupby("win").r24.mean() > 0).mean())
    return out
