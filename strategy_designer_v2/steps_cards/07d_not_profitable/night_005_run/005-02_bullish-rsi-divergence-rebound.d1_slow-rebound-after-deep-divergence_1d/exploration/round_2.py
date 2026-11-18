def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days, bars, trades = data["days"], data["bars"], data["trades"]
    rows = []
    for c in days:
        for w, d in days[c].items():
            rows.append(dict(coin=c, w=w, book_sum=d.book_return.sum(), coin_sum=d.coin_return.sum(),
                             book_n_active=(d.book_return.fillna(0).abs() > 1e-12).sum()))
    df = pd.DataFrame(rows)
    out["by_window"] = df.groupby("w")[["book_sum", "coin_sum", "book_n_active"]].sum().round(3)
    seg = []
    for c in bars:
        allr = pd.concat([(b.close.shift(-1) / b.close - 1) for b in bars[c].values()])
        mu = allr.mean()
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            b["r"] = b.close.shift(-1) / b.close - 1
            b["pos"] = b.postRebalance_current_allocation.fillna(0)
            b["gain"] = b.pos * b.r
            b["mkt"] = b.pos * mu
            b["ret90"] = b.close / b.close.shift(90) - 1
            b["ma100"] = b.close / b.close.rolling(100, min_periods=60).mean() - 1
            b["fall30"] = -(b.close / b.close.shift(30) - 1)
            b["ret5"] = b.close / b.close.shift(5) - 1
            b["f20"] = b.close.shift(-20) / b.close - 1
            b["f5"] = b.close.shift(-5) / b.close - 1
            b["coin"] = c; b["w"] = w; b["mu"] = mu
            seg.append(b)
    B = pd.concat(seg, ignore_index=True)
    held = B[B.pos.abs() > 1e-9].copy()
    out["held_share_bars"] = len(held) / len(B)
    out["gain_vs_mkt"] = pd.Series({"gain_sum": held.gain.sum(), "mkt_sum": held.mkt.sum(),
                                    "timing": held.gain.sum() - held.mkt.sum(), "mean_pos": held.pos.mean(),
                                    "n_held": len(held)})
    held["ex"] = held.r - held.mu
    held["trend"] = np.where(held.ma100 > 0, "above_ma100", "below_ma100")
    out["held_by_ma100"] = held.groupby("trend").agg(n=("ex", "size"), ex_mean=("ex", "mean"), gain_sum=("gain", "sum"))
    held["q90"] = pd.qcut(held.ret90, 4, labels=False, duplicates="drop")
    out["held_by_ret90_q"] = held.groupby("q90").agg(n=("ex", "size"), ret90=("ret90", "mean"), ex_mean=("ex", "mean"), gain_sum=("gain", "sum"))
    held["qf30"] = pd.qcut(held.fall30, 4, labels=False, duplicates="drop")
    out["held_by_fall30_q"] = held.groupby("qf30").agg(n=("ex", "size"), fall30=("fall30", "mean"), ex_mean=("ex", "mean"), gain_sum=("gain", "sum"))
    bir = held.get("debug_info.bars_in_regime")
    if bir is not None:
        held["birb"] = pd.cut(bir, [-1, 0, 2, 5, 10, 1000])
        out["held_by_bars_in_regime"] = held.groupby("birb").agg(n=("ex", "size"), ex_mean=("ex", "mean"), gain_sum=("gain", "sum"))
    T = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])])
    out["trades"] = pd.Series({"n": len(T), "mean_pl": T.profit_loss_percent.mean(), "mean_net": T.net_profit_loss_percent.mean(),
                               "win": (T.profit_loss_percent > 0).mean(), "med_dur_days": T.duration_minutes.median() / 1440,
                               "mean_dur_days": T.duration_minutes.mean() / 1440})
    ev = []
    for (c, w), b in B.groupby(["coin", "w"]):
        b = b.reset_index(drop=True); i = 0
        while i < len(b):
            if b.forecast.iloc[i] > 0 and not np.isnan(b.f20.iloc[i]):
                ev.append(b.iloc[i][["f20", "f5", "ma100", "ret90", "fall30", "ret5", "mu"]].to_dict()); i += 20
            else:
                i += 1
    E = pd.DataFrame(ev).astype(float)
    E["ex20"] = E.f20 - 20 * E.mu
    E["trend"] = np.where(E.ma100 > 0, "above", "below")
    out["events_by_ma100"] = E.groupby("trend").ex20.agg(["size", "mean", "median"])
    E["r90pos"] = np.where(E.ret90 > 0, "ret90_up", "ret90_down")
    out["events_by_ret90sign"] = E.groupby("r90pos").ex20.agg(["size", "mean", "median"])
    out["events_spearman"] = pd.Series({k: stats.spearmanr(E[k], E.ex20, nan_policy="omit").correlation for k in ["ret90", "ma100", "fall30", "ret5"]})
    out["events_f5_vs_f20"] = pd.Series({"f5_mean": E.f5.mean(), "f20_mean": E.f20.mean(), "ex20_mean": E.ex20.mean(), "n": len(E)})
    return out
