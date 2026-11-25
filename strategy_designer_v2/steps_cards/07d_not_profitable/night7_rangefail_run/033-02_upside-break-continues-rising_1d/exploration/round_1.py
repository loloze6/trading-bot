def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars, trades, days = data["bars"], data["trades"], data["days"]
    coins = list(days.keys())
    wins = sorted({w for c in coins for w in days[c].keys()}, key=lambda s: int(s[1:]))
    # book daily
    rows = []
    for w in wins:
        dfs = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                dfs.append(d)
        d = pd.concat(dfs)
        g = d.groupby("day").agg(book=("book_return", "mean"), hold=("coin_return", "mean")).dropna()
        g["win"] = w
        rows.append(g)
    B = pd.concat(rows)
    B["idx"] = np.arange(len(B))
    eq = (1 + B["book"]).cumprod()
    peak = eq.cummax()
    dd = eq / peak - 1
    B["dd"] = dd.values
    out["max_dd"] = float(dd.min())
    # episodes
    eps = []
    inn = False
    for i, v in enumerate(dd.values):
        if v < 0 and not inn:
            inn = True; s = i
        if v == 0 and inn:
            inn = False
            seg = dd.values[s:i]
            eps.append((s, i, seg.min(), s + seg.argmin()))
    if inn:
        seg = dd.values[s:]
        eps.append((s, len(dd), seg.min(), s + seg.argmin()))
    eps = sorted(eps, key=lambda e: e[2])[:6]
    er = []
    for s, e, m, t in eps:
        sub = B.iloc[s:t + 1]
        er.append({"depth": m, "days_to_trough": t - s + 1, "wins": ",".join(sorted(sub.win.unique(), key=lambda x: int(x[1:]))),
                   "hold_ret_in_fall": float((1 + sub.hold).prod() - 1), "book_ret_in_fall": float((1 + sub.book).prod() - 1)})
    out["deepest_falls"] = pd.DataFrame(er)
    # by window
    out["by_window"] = B.groupby("win").agg(book_mean=("book", "mean"), hold_mean=("hold", "mean"), n=("book", "size")).reindex(wins)
    # trades with features
    tr = []
    for c in coins:
        for w in trades[c]:
            T = trades[c][w]
            if T is None or len(T) == 0:
                continue
            b = bars[c][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values; hi = b["high"].values
            lr = np.log(cl[1:] / cl[:-1]); lr = np.r_[np.nan, lr]
            for _, r in T.iterrows():
                et = pd.to_datetime(r["entry_time"])
                pos = np.searchsorted(ts.values, np.datetime64(et))
                if pos >= len(b):
                    continue
                if ts.iloc[pos] != et and pos > 0:
                    pos = pos  # approx
                f = {"coin": c, "win": w, "net": r["net_profit_loss_percent"], "dur": r["duration_minutes"] / 1440, "side": r["side"]}
                f["brk"] = (cl[pos] / hi[max(0, pos - 20):pos].max() - 1) * 100 if pos >= 20 else np.nan
                f["r5"] = cl[pos] / cl[pos - 5] - 1 if pos >= 5 else np.nan
                f["r20"] = cl[pos] / cl[pos - 20] - 1 if pos >= 20 else np.nan
                f["r60"] = cl[pos] / cl[pos - 60] - 1 if pos >= 60 else np.nan
                f["v10"] = np.nanstd(lr[max(1, pos - 9):pos + 1]) if pos >= 10 else np.nan
                f["v60"] = np.nanstd(lr[max(1, pos - 59):pos + 1]) if pos >= 30 else np.nan
                f["vr"] = f["v10"] / f["v60"] if f["v60"] else np.nan
                f["r1"] = cl[pos] / cl[pos - 1] - 1 if pos >= 1 else np.nan
                # streak: number of breakouts in last 10 bars
                cnt = 0
                for k in range(max(20, pos - 10), pos):
                    if cl[k] > hi[k - 20:k].max():
                        cnt += 1
                f["prior_brk10"] = cnt
                tr.append(f)
    TR = pd.DataFrame(tr)
    out["trades_summary"] = pd.Series({"n": len(TR), "mean_net": TR.net.mean(), "win_share": (TR.net > 0).mean(),
                                       "mean_dur_days": TR.dur.mean(), "worst_decile_mean": TR.net.quantile(0.1)})
    out["dur_dist"] = TR.dur.describe()
    res = {}
    for col in ["brk", "r5", "r20", "r60", "vr", "v10", "r1", "prior_brk10"]:
        s = TR[[col, "net"]].dropna()
        if len(s) < 20 or s[col].nunique() < 4:
            continue
        q = pd.qcut(s[col].rank(method="first"), 4, labels=False)
        g = s.groupby(q).agg(lo=(col, "min"), hi=(col, "max"), mean_net=("net", "mean"), n=("net", "size"), loss_share=("net", lambda x: (x < 0).mean()))
        g.index = [f"{col}_q{i}" for i in g.index]
        res[col] = g
    out["by_feature_quartile"] = pd.concat(res.values())
    out["by_prior_brk10"] = TR.groupby(TR.prior_brk10.clip(upper=5)).net.agg(["mean", "size"])
    out["by_window_trades"] = TR.groupby("win").net.agg(["mean", "size", "sum"]).reindex(wins)
    return out
