def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days, bars, trades = data["days"], data["bars"], data["trades"]
    # book daily by window
    rows = []
    for c in days:
        for w, d in days[c].items():
            rows.append(dict(coin=c, w=w, book_mean=d.book_return.mean(), coin_mean=d.coin_return.mean(),
                             book_sum=d.book_return.sum(), coin_sum=d.coin_return.sum()))
    df = pd.DataFrame(rows)
    out["by_window"] = df.groupby("w")[["book_sum", "coin_sum"]].sum().round(3)
    # decomposition: market part vs timing
    seg = []
    for c in bars:
        allr = []
        for w, b in bars[c].items():
            r = b.close.shift(-1) / b.close - 1
            allr.append(r)
        mu = pd.concat(allr).mean()
        for w, b in bars[c].items():
            b = b.copy()
            b["r"] = b.close.shift(-1) / b.close - 1
            b["pos"] = b.postRebalance_current_allocation
            b["gain"] = b.pos * b.r
            b["mkt"] = b.pos * mu
            # context: 90-bar return and 200 MA distance
            b["ret90"] = b.close / b.close.shift(90) - 1
            b["ma100"] = b.close / b.close.rolling(100, min_periods=60).mean() - 1
            b["fall30"] = b["debug_info.components.fall30.last_history_value"]
            b["coin"] = c
            b["w"] = w
            b["mu"] = mu
            seg.append(b)
    B = pd.concat(seg)
    held = B[B.pos.abs() > 1e-9]
    out["held_share_bars"] = len(held) / len(B)
    out["gain_total_vs_mkt_part"] = pd.Series({"gain_sum": held.gain.sum(), "mkt_sum": held.mkt.sum(),
                                               "timing": held.gain.sum() - held.mkt.sum(),
                                               "mean_pos": held.pos.mean()})
    held = held.copy()
    held["ex"] = held.r - held.mu
    held["trend"] = np.where(held.ma100 > 0, "above_ma100", "below_ma100")
    out["by_ma100"] = held.groupby("trend").agg(n=("ex", "size"), ex_mean=("ex", "mean"), gain_sum=("gain", "sum"))
    held["q90"] = pd.qcut(held.ret90, 4, labels=False, duplicates="drop")
    out["by_ret90_q"] = held.groupby("q90").agg(n=("ex", "size"), ret90=("ret90", "mean"), ex_mean=("ex", "mean"), gain_sum=("gain", "sum"))
    # by days into holding (bars since regime start)
    held["bir"] = held["debug_info.bars_in_regime"]
    held["birb"] = pd.cut(held.bir, [-1, 0, 2, 5, 10, 1000])
    out["by_bars_in_regime"] = held.groupby("birb").agg(n=("ex", "size"), ex_mean=("ex", "mean"))
    # trades
    T = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c]])
    out["trades"] = pd.Series({"n": len(T), "mean_pl": T.profit_loss_percent.mean(), "mean_net": T.net_profit_loss_percent.mean(),
                               "win": (T.profit_loss_percent > 0).mean(), "med_dur_days": T.duration_minutes.median() / 1440})
    # forward 20 from event bars (fc>0 first) by ma100
    ev = []
    for (c, w), b in B.groupby(["coin", "w"]):
        b = b.reset_index(drop=True)
        f20 = b.close.shift(-20) / b.close - 1
        i = 0
        while i < len(b):
            if b.forecast.iloc[i] > 0 and not np.isnan(f20.iloc[i]):
                ev.append(dict(f20=f20.iloc[i], ma100=b.ma100.iloc[i], ret90=b.ret90.iloc[i], fall30=b.fall30.iloc[i]))
                i += 20
            else:
                i += 1
    E = pd.DataFrame(ev)
    E["trend"] = np.where(E.ma100 > 0, "above", "below")
    out["events_by_ma100"] = E.groupby("trend").f20.agg(["size", "mean", "median"])
    out["events_spearman_ret90_f20"] = stats.spearmanr(E.ret90, E.f20, nan_policy="omit").correlation
    out["events_spearman_fall30_f20"] = stats.spearmanr(E.fall30, E.f20, nan_policy="omit").correlation
    return out
