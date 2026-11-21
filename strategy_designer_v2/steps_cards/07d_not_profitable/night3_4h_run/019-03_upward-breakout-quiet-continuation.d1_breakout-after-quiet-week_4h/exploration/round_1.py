def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    coins = list(days.keys())
    wins = sorted(set(w for c in coins for w in days[c].keys()), key=lambda s: int(s[1:]))
    # book daily, mean over coins per day, chained in window order
    chain = []; perwin = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c; frames.append(d)
        d = pd.concat(frames)
        g = d.groupby("day")[["book_return", "coin_return"]].mean().sort_index().dropna()
        g["w"] = w; g["pos"] = np.arange(len(g)); chain.append(g)
        eq = (1 + g.book_return).cumprod()
        perwin.append({"w": w, "book_ret": eq.iloc[-1] - 1, "hold_ret": (1 + g.coin_return).cumprod().iloc[-1] - 1,
                       "book_maxdd": (eq / eq.cummax() - 1).min(), "days": len(g)})
    ch = pd.concat(chain).reset_index(drop=True)
    eq = (1 + ch.book_return).cumprod(); dd = eq / eq.cummax() - 1
    yr = eq.iloc[-1] ** (365 / len(ch)) - 1
    out["calmar"] = pd.Series({"yearly": yr, "maxdd": dd.min(), "calmar": yr / -dd.min(), "days": len(ch)})
    # deepest fall location
    end = dd.idxmin(); start = eq[:end + 1].idxmax()
    out["deepest_fall_span"] = pd.Series({"start_w": ch.w[start], "start_pos": ch.pos[start], "end_w": ch.w[end],
                                          "end_pos": ch.pos[end], "n_days": end - start,
                                          "coin_avg_ret_during": (1 + ch.coin_return[start + 1:end + 1]).prod() - 1})
    pw = pd.DataFrame(perwin).set_index("w")
    out["per_window"] = pw.round(4)
    # bar-level features
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy()
            rng = (b.high - b.low) / b.close
            b["q"] = rng.rolling(42).mean() / rng.rolling(360).mean()
            b["r30"] = b.close / b.close.shift(180) - 1
            b["r7"] = b.close / b.close.shift(42) - 1
            b["vol7"] = np.log(b.close).diff().rolling(42).std()
            b["vol60"] = np.log(b.close).diff().rolling(360).std()
            b["vr"] = b.vol7 / b.vol60
            b["dd60"] = b.close / b.close.rolling(360).max() - 1
            b["gain"] = b.postRebalance_current_allocation * (b.close.shift(-1) / b.close - 1)
            b["alloc"] = b.postRebalance_current_allocation
            b["coin"] = c; b["w"] = w
            rows.append(b[["timestamp", "coin", "w", "q", "r30", "r7", "vr", "dd60", "gain", "alloc", "forecast"]])
    B = pd.concat(rows)
    inpos = B[B.alloc.abs() > 1e-6].dropna()
    for f in ["q", "r30", "r7", "vr", "dd60"]:
        inpos[f + "_qt"] = pd.qcut(inpos[f], 5, labels=False, duplicates="drop")
        g = inpos.groupby(f + "_qt").agg(mean_gain_bps=("gain", lambda x: x.mean() * 1e4), n=("gain", "size"),
                                         std=("gain", "std"), fmed=(f, "median"), alloc=("alloc", "mean"))
        g["t"] = g.mean_gain_bps / 1e4 / (g["std"] / np.sqrt(g.n))
        out["gain_by_" + f] = g.drop(columns="std").round(4)
    out["share_time_in_pos"] = float((B.alloc.abs() > 1e-6).mean())
    # trades with entry features
    T = []
    for c in coins:
        for w, t in trades[c].items():
            t = t.copy(); t["coin"] = c; t["w"] = w; T.append(t)
    T = pd.concat(T)
    T["entry_time"] = pd.to_datetime(T.entry_time); B["timestamp"] = pd.to_datetime(B.timestamp)
    # match on close time: entry at a bar's close = timestamp + 4h? try both
    m1 = T.merge(B, left_on=["coin", "w", "entry_time"], right_on=["coin", "w", "timestamp"], how="inner")
    out["trades_n_matched"] = pd.Series({"trades": len(T), "matched": len(m1),
                                         "mean_net": T.net_profit_loss_percent.mean(), "median_net": T.net_profit_loss_percent.median(),
                                         "share_win": (T.net_profit_loss_percent > 0).mean(),
                                         "mean_dur_h": T.duration_minutes.mean() / 60,
                                         "worst5pct_mean": T.net_profit_loss_percent.quantile(0.05)})
    m1 = m1.dropna(subset=["vr", "r30", "dd60"])
    for f in ["vr", "r30", "dd60", "r7"]:
        m1[f + "_qt"] = pd.qcut(m1[f], 5, labels=False, duplicates="drop")
        out["trade_net_by_" + f] = m1.groupby(f + "_qt").agg(net=("net_profit_loss_percent", "mean"),
                                                             n=("net_profit_loss_percent", "size"),
                                                             p05=("net_profit_loss_percent", lambda x: x.quantile(.05)),
                                                             fmed=(f, "median")).round(4)
    return out
