def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 10
    rows = []
    lens = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            n = len(b); lens.append(n)
            if n < 40: continue
            hi, lo, cl, vol = b["high"], b["low"], b["close"], b["volume"]
            ph20 = hi.shift(1).rolling(20).max()
            pl20 = lo.shift(1).rolling(20).min()
            r10 = hi.shift(1).rolling(10).max() - lo.shift(1).rolling(10).min()
            r30 = hi.shift(1).rolling(30).max() - lo.shift(1).rolling(30).min()
            ratio = r10 / r30
            ret1 = cl.pct_change()
            past10 = cl / cl.shift(10) - 1
            past20 = cl / cl.shift(20) - 1
            vol10 = ret1.rolling(10).std()
            vol30 = ret1.rolling(30).std()
            vr = vol / vol.shift(1).rolling(20).mean()
            pos20 = (cl - pl20) / (ph20 - pl20)
            fwd = cl.shift(-H) / cl - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=c, w=w, i=i, fwd=fwd[i], ratio=ratio[i], past10=past10[i],
                                 past20=past20[i], vratio=vol10[i] / vol30[i], vr=vr[i],
                                 ret1=ret1[i], pos20=pos20[i], vol30=vol30[i],
                                 brk=float(cl[i] > ph20[i]) if pd.notna(ph20[i]) else np.nan,
                                 wd=ts[i].dayofweek, year=ts[i].year))
    out = {"window lengths": pd.Series(lens).describe()}
    g = pd.DataFrame(rows)
    if len(g) == 0:
        return out
    g["mfwd"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["mfwd"]
    g["absfwd"] = g["fwd"].abs()
    def tert(col, y):
        d = g.dropna(subset=[col, y]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
        t = d.groupby("q")[y].agg(["mean", "count"])
        a, z = d[d.q == 2][y], d[d.q == 0][y]
        t.loc["top-bot_t", "mean"] = stats.ttest_ind(a, z, equal_var=False).statistic
        return t
    for col in ["ratio", "vratio", "vr", "vol30"]:
        out[col + "->absfwd"] = tert(col, "absfwd")
    for col in ["ratio", "past10", "past20", "vratio", "vr", "ret1", "pos20", "vol30"]:
        out[col + "->ex"] = tert(col, "ex")
    bk = g.dropna(subset=["brk", "ex"])
    out["breakout vs not ex"] = bk.groupby("brk")["ex"].agg(["mean", "count", "std"])
    out["year ex"] = g.groupby("year")["ex"].agg(["mean", "count"])
    cc = {}
    for c, d in g.groupby("coin"):
        d = d.dropna()
        cc[c] = {k: stats.spearmanr(d[k], d["ex"]).correlation for k in ["ratio", "past20", "vratio", "vr", "pos20"]}
        cc[c]["ratio_abs"] = stats.spearmanr(d["ratio"], d["absfwd"]).correlation
        cc[c]["n"] = len(d)
    out["spearman by coin"] = pd.DataFrame(cc).T
    dd = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin_"] = c; d["w_"] = w
            d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek
            d["prev_cr"] = d["coin_return"].shift(1)
            dd.append(d)
    D = pd.concat(dd, ignore_index=True).dropna(subset=["book_return", "coin_return"])
    out["by weekday"] = D.groupby("wd").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
        coin_t=("coin_return", lambda s: s.mean() / s.std() * np.sqrt(len(s))), n=("coin_return", "count"))
    E = D.dropna(subset=["prev_cr"]).copy()
    E["q"] = E.groupby("coin_")["prev_cr"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["next-day coin ret by prev-day quintile"] = E.groupby("q")["coin_return"].agg(["mean", "count",
        lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # book: largest days
    B = D.copy()
    thr_hi = B["book_return"].quantile(0.99); thr_lo = B["book_return"].quantile(0.01)
    out["book tails"] = pd.Series({"p99": thr_hi, "p01": thr_lo, "mean": B.book_return.mean(),
        "share_days_invested": (B.book_return != 0).mean(),
        "sum_top1pct": B.book_return[B.book_return >= thr_hi].sum(),
        "sum_bot1pct": B.book_return[B.book_return <= thr_lo].sum(), "sum_all": B.book_return.sum()})
    # trades
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            t = t.copy(); t["coin_"] = c; tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["dq"] = pd.cut(T["dur_d"], [0, 1.5, 3.5, 7.5, 1e9])
    out["trades by duration"] = T.groupby("dq")["profit_loss_percent"].agg(["mean", "count"])
    out["trades by coin"] = T.groupby("coin_")["profit_loss_percent"].agg(["mean", "count"])
    return out
