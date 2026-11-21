def explore(data):
    import numpy as np, pandas as pd
    out = {}
    days = data["days"]; bars = data["bars"]; trades = data["trades"]
    coins = list(days.keys())
    wins = sorted({w for c in coins for w in days[c].keys()}, key=lambda s: int(s[1:]))
    # book daily returns: per window, per day, mean over coins
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c; frames.append(d)
        if not frames: continue
        f = pd.concat(frames)
        g = f.groupby("day").agg(book=("book_return", "mean"), hold=("coin_return", "mean")).sort_index()
        g["window"] = w
        rows.append(g.dropna())
    B = pd.concat(rows).reset_index()
    eq = (1 + B["book"]).cumprod()
    peak = eq.cummax(); dd = eq / peak - 1
    B["dd"] = dd.values
    heq = (1 + B["hold"]).cumprod(); B["hdd"] = (heq / heq.cummax() - 1).values
    yrs = len(B) / 365
    out["overall"] = pd.Series({"days": len(B), "yearly": eq.iloc[-1] ** (1 / yrs) - 1, "maxdd": dd.min(),
                                "hold_yearly": heq.iloc[-1] ** (1 / yrs) - 1, "hold_maxdd": B["hdd"].min()})
    # per window
    pw = B.groupby("window", sort=False).agg(book_sum=("book", "sum"), hold_sum=("hold", "sum"),
                                             min_dd=("dd", "min"), n=("book", "size"))
    pw["year"] = B.groupby("window", sort=False)["day"].first().astype(str).str[:4].values
    out["per_window"] = pw
    # deepest fall: from peak to trough
    ti = int(np.argmin(dd.values)); pi = int(np.argmax(eq.values[:ti + 1]))
    seg = B.iloc[pi + 1:ti + 1]
    out["deepest_fall"] = pd.Series({"len_days": len(seg), "windows": ",".join(seg["window"].unique()),
                                     "book_sum": seg["book"].sum(), "hold_sum": seg["hold"].sum(),
                                     "corr_book_hold": seg[["book", "hold"]].corr().iloc[0, 1]})
    # per-coin contribution in deepest fall
    seg_days = set(zip(seg["window"], seg["day"]))
    cc = {}
    for c in coins:
        s = 0; sh = 0
        for w in seg["window"].unique():
            if w in days[c]:
                d = days[c][w]
                m = d["day"].isin(seg.loc[seg["window"] == w, "day"])
                s += d.loc[m, "book_return"].sum(); sh += d.loc[m, "coin_return"].sum()
        cc[c] = (s / len(coins), sh / len(coins))
    out["deepest_fall_by_coin"] = pd.DataFrame(cc, index=["book_contrib", "hold_contrib"]).T
    # trades: features at entry
    recs = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            rng = (hi - lo).rolling(180, min_periods=45).mean()
            r42 = cl / cl.shift(42) - 1
            r180 = cl / cl.shift(180) - 1
            vol_ratio = (hi - lo).rolling(42).mean() / rng
            dist_hi180 = cl / hi.rolling(180).max() - 1
            brk = (cl - hi.shift(1).rolling(12).max()) / rng
            ret36 = cl.shift(-36) / cl - 1
            feat = pd.DataFrame({"ts": b["ts"], "r42": r42, "r180": r180, "vr": vol_ratio, "dh": dist_hi180,
                                 "brk": brk, "ret36": ret36, "alloc": b["postRebalance_current_allocation"]})
            t = trades[c].get(w) if isinstance(trades[c], dict) else None
            if t is None or len(t) == 0: continue
            t = t.copy(); t["et"] = pd.to_datetime(t["entry_time"])
            m = pd.merge_asof(t.sort_values("et"), feat.sort_values("ts"), left_on="et", right_on="ts", direction="backward")
            m["coin"] = c; m["window"] = w
            recs.append(m)
    T = pd.concat(recs)
    T["pl"] = T["net_profit_loss_percent"]
    out["trades_summary"] = pd.Series({"n": len(T), "mean_pl": T["pl"].mean(), "median_pl": T["pl"].median(),
                                       "win": (T["pl"] > 0).mean(), "mean_dur_h": T["duration_minutes"].mean() / 60,
                                       "worst5pct_mean": T["pl"].quantile(0.05)})
    res = {}
    for f in ["r42", "r180", "vr", "dh", "brk"]:
        q = pd.qcut(T[f], 5, labels=False, duplicates="drop")
        g = T.groupby(q)["pl"].agg(["mean", "count", lambda x: x.quantile(0.1)])
        g.columns = ["mean", "n", "p10"]
        g["fmid"] = T.groupby(q)[f].median()
        res[f] = g
    for k, v in res.items():
        out["q_" + k] = v
    out["pl_by_coin"] = T.groupby("coin")["pl"].agg(["mean", "count", "min"])
    return out
