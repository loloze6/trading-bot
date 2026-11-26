def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    # book daily returns
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        if not frames: continue
        f = pd.concat(frames)
        g = f.groupby("day").agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
        g["w"] = w
        rows.append(g)
    B = pd.concat(rows).dropna(subset=["br"]).reset_index(drop=True)
    v = (1 + B["br"]).cumprod()
    dd = v / v.cummax() - 1
    B["dd"] = dd
    out["book_dd_by_window"] = B.groupby("w").agg(minDD=("dd", "min"), sumret=("br", "sum"), n=("br", "size"))
    # per-window max drawdown inside window
    def wdd(s):
        vv = (1 + s).cumprod(); return (vv / vv.cummax() - 1).min()
    out["within_window_dd"] = B.groupby("w")["br"].apply(wdd)
    # trades with entry features
    T = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            n = len(b)
            al = b["postRebalance_current_allocation"].fillna(0).values
            # entries: allocation goes from 0 to >0
            prev = np.r_[0, al[:-1]]
            for i in np.where((al > 0) & (prev <= 0))[0]:
                j = i
                while j + 1 < n and al[j + 1] > 0: j += 1
                exit_i = min(j + 1, n - 1)
                ret = cl[exit_i] / cl[i] - 1
                path = cl[i:exit_i + 1] / cl[i] - 1
                ph = hi[max(0, i - 60):i]; pl = lo[max(0, i - 60):i]
                if len(ph) < 30: continue
                rng = ph.max() / pl.min() - 1
                over = cl[i] / ph.max() - 1
                r10 = cl[i] / cl[max(0, i - 10)] - 1
                r3 = cl[i] / cl[max(0, i - 3)] - 1
                lr = np.diff(np.log(cl[max(0, i - 30):i + 1]))
                vol = lr.std()
                fwd = [cl[min(i + k, n - 1)] / cl[i] - 1 for k in (1, 2, 3)]
                T.append(dict(coin=c, w=w, ret=ret, dur=exit_i - i, alloc=al[i], rng=rng, over=over, r10=r10, r3=r3, vol=vol,
                              mae=path.min(), d1=fwd[0], d2=fwd[1], d3=fwd[2], year=ts[i].year, contrib=ret * al[i]))
    T = pd.DataFrame(T)
    out["n_trades"] = len(T)
    out["trade_summary"] = T[["ret", "contrib", "mae", "dur", "alloc", "rng", "over", "r10", "vol"]].describe().T
    out["worst_trades"] = T.sort_values("contrib").head(12)[["coin", "w", "year", "ret", "contrib", "alloc", "rng", "over", "r10", "r3", "vol", "d1", "d3"]]
    out["by_coin"] = T.groupby("coin").agg(n=("ret", "size"), mret=("ret", "mean"), sumc=("contrib", "sum"), worst=("ret", "min"))
    out["by_year"] = T.groupby("year").agg(n=("ret", "size"), mret=("ret", "mean"), sumc=("contrib", "sum"))
    for col in ["rng", "over", "r10", "r3", "vol", "alloc"]:
        q = pd.qcut(T[col].rank(method="first"), 3, labels=["lo", "mid", "hi"])
        out["by_" + col] = T.groupby(q).agg(n=("ret", "size"), mret=("ret", "mean"), medret=("ret", "median"), mae=("mae", "mean"), sumc=("contrib", "sum"))
    # does early loss predict further loss (stop logic)
    T["rest"] = (1 + T["ret"]) / (1 + T["d2"]) - 1
    q = pd.cut(T["d2"], [-1, -0.05, -0.02, 0, 0.03, 1])
    out["after_day2"] = T.groupby(q).agg(n=("ret", "size"), rest=("rest", "mean"), total=("ret", "mean"))
    out["spearman"] = pd.Series({col: stats.spearmanr(T[col], T["ret"])[0] for col in ["rng", "over", "r10", "r3", "vol", "alloc"]})
    return out
