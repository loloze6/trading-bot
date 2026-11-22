def explore(data):
    import pandas as pd, numpy as np
    bars, days, trades = data["bars"], data["days"], data["trades"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    out = {}
    # book daily series
    recs = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy(); d["coin"] = c; frames.append(d)
        df = pd.concat(frames)
        g = df.groupby("day")[["book_return", "coin_return"]].mean().dropna().reset_index()
        g["win"] = w; recs.append(g)
    book = pd.concat(recs, ignore_index=True)
    eq = (1 + book["book_return"]).cumprod()
    dd = eq / eq.cummax() - 1
    book["dd"] = dd.values
    yr = eq.iloc[-1] ** (365 / len(book)) - 1
    out["calmar"] = pd.Series({"yearly": yr, "maxdd": dd.min(), "calmar": yr / -dd.min(), "ndays": len(book)})
    # drawdown episodes
    peak_idx = eq.cummax()
    ep = []; in_dd = False
    for i in range(len(book)):
        if dd.iloc[i] < 0 and not in_dd:
            in_dd = True; start = i
        if in_dd and (dd.iloc[i] == 0 or i == len(book) - 1):
            seg = dd.iloc[start:i + 1]
            j = seg.idxmin()
            ep.append({"start": start, "trough": j, "end": i, "depth": seg.min(), "days_to_trough": j - start,
                       "win_start": book["win"].iloc[start], "win_trough": book["win"].iloc[j],
                       "coin_ret_during": (1 + book["coin_return"].iloc[start:j + 1]).prod() - 1})
            in_dd = False
    ep = pd.DataFrame(ep).sort_values("depth").head(8)
    out["deepest_falls"] = ep[["depth", "days_to_trough", "win_start", "win_trough", "coin_ret_during"]].reset_index(drop=True)
    # per window book stats
    pw = book.groupby("win").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"),
                                 worst_dd=("dd", "min"), n=("book_return", "size"))
    pw["book_total"] = book.groupby("win")["book_return"].apply(lambda x: (1 + x).prod() - 1)
    pw["coin_total"] = book.groupby("win")["coin_return"].apply(lambda x: (1 + x).prod() - 1)
    out["per_window"] = pw.reindex(wins)
    # trades with features at entry
    tr = []
    for c in coins:
        for w in trades[c]:
            t = trades[c][w]
            if t is None or len(t) == 0: continue
            b = bars[c][w].copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            cl = b["close"]; r = cl.pct_change()
            b["vol20"] = r.rolling(20).std()
            b["ret20"] = cl / cl.shift(20) - 1
            b["ret5"] = cl / cl.shift(5) - 1
            b["ret60"] = cl / cl.shift(60) - 1
            b["dd60"] = cl / cl.rolling(60).max() - 1
            b["volratio"] = b["vol20"] / r.rolling(60).std()
            b["dayz"] = r / b["vol20"].shift(1)
            b["alloc"] = b["postRebalance_current_allocation"]
            for _, x in t.iterrows():
                et = pd.to_datetime(x["entry_time"])
                k = b.index[b["ts"] <= et]
                if len(k) == 0: continue
                row = b.loc[k[-1]]
                tr.append({"coin": c, "win": w, "pnl": x["net_profit_loss_percent"], "alloc": row["alloc"],
                           "vol20": row["vol20"], "ret20": row["ret20"], "ret5": row["ret5"], "ret60": row["ret60"],
                           "dd60": row["dd60"], "volratio": row["volratio"], "dayz": row["dayz"],
                           "fc": x["entry_forecast"]})
    tr = pd.DataFrame(tr)
    tr["wpnl"] = tr["pnl"] * tr["alloc"].abs()
    out["trades_summary"] = pd.Series({"n": len(tr), "mean_pnl": tr["pnl"].mean(), "win_share": (tr["pnl"] > 0).mean(),
                                       "p05": tr["pnl"].quantile(.05), "p95": tr["pnl"].quantile(.95)})
    res = {}
    for f in ["vol20", "ret20", "ret5", "ret60", "dd60", "volratio", "dayz", "fc", "alloc"]:
        q = pd.qcut(tr[f], 4, labels=False, duplicates="drop")
        gg = tr.groupby(q)["pnl"]
        res[f] = pd.Series({f"q{int(i)}": v for i, v in gg.mean().items()})
        res[f]["worst5share_q"] = np.nan
    out["pnl_by_quartile"] = pd.DataFrame(res).T
    worst = tr.nsmallest(int(len(tr) * 0.1), "wpnl")
    out["worst10pct_vs_all_medians"] = pd.DataFrame({"worst": worst[["vol20", "ret20", "ret5", "ret60", "dd60", "volratio", "dayz", "fc", "alloc"]].median(),
                                                     "all": tr[["vol20", "ret20", "ret5", "ret60", "dd60", "volratio", "dayz", "fc", "alloc"]].median()})
    out["pnl_by_coin"] = tr.groupby("coin").agg(n=("pnl", "size"), mean=("pnl", "mean"), wsum=("wpnl", "sum"))
    return out
