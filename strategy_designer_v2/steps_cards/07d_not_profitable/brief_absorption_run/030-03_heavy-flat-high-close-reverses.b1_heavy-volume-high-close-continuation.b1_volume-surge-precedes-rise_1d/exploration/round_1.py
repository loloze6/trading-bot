def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted(set(w for c in coins for w in bars[c].keys()), key=lambda s: int(s[1:]))
    # book daily
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy(); d["coin"] = c; frames.append(d)
        df = pd.concat(frames)
        g = df.groupby("day")[["book_return", "coin_return"]].mean().reset_index(); g["win"] = w
        rows.append(g)
    book = pd.concat(rows).dropna().reset_index(drop=True)
    v = (1 + book.book_return).cumprod(); peak = v.cummax(); dd = v / peak - 1
    book["dd"] = dd.values
    hv = (1 + book.coin_return).cumprod(); book["hold_dd"] = (hv / hv.cummax() - 1).values
    out["book_maxdd"] = float(dd.min()); out["hold_maxdd"] = float(book.hold_dd.min())
    # episodes
    eps = []; i = 0; n = len(book)
    in_ep = False
    for j in range(n):
        if dd.iloc[j] < 0 and not in_ep: in_ep = True; s = j
        if in_ep and (dd.iloc[j] == 0 or j == n - 1):
            seg = book.iloc[s:j + 1]; k = seg.dd.idxmin()
            eps.append(dict(start_win=book.win.iloc[s], trough_win=book.win.loc[k], depth=seg.dd.min(),
                            days_to_trough=k - s + 1, coin_ret_to_trough=(1 + book.coin_return.iloc[s:k + 1]).prod() - 1,
                            book_ret_to_trough=(1 + book.book_return.iloc[s:k + 1]).prod() - 1))
            in_ep = False
    E = pd.DataFrame(eps).sort_values("depth").head(6)
    out["top_drawdowns"] = E
    # by year book vs hold
    book["year"] = pd.to_datetime(book.day).dt.year
    out["by_year"] = book.groupby("year").agg(book_mean=("book_return", "mean"), hold_mean=("coin_return", "mean"),
                                              book_sd=("book_return", "std"), n=("book_return", "size"))
    # grid analysis
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b.close.values; o = b.open.values; h = b.high.values; l = b.low.values; vol = b.volume.values
            f = b.forecast.values; al = b.postRebalance_current_allocation.values
            s = pd.Series(cl)
            r1 = s.pct_change().values
            r20 = (s / s.shift(20) - 1).values
            ma50 = s.rolling(50, min_periods=30).mean().values
            lv = np.log(pd.Series(vol) / pd.Series(vol).shift(1).rolling(20).mean()).values
            rng = h - l
            clv = np.where(rng > 0, (cl - l) / np.where(rng > 0, rng, 1), np.nan)
            for t in range(0, len(b) - 10, 10):
                recs.append(dict(coin=c, win=w, fwd=cl[t + 10] / cl[t] - 1, f=f[t], al=al[t], r1=r1[t], r20=r20[t],
                                 above50=cl[t] > ma50[t] if not np.isnan(ma50[t]) else np.nan, lv=lv[t], clv=clv[t]))
    G = pd.DataFrame(recs)
    G["ex"] = G.fwd - G.groupby("coin").fwd.transform("mean")
    G["sig"] = G.f > 0
    def tab(col, bins=None, labels=None):
        x = G.dropna(subset=[col]).copy()
        if bins is not None: x["grp"] = pd.cut(x[col], bins, labels=labels)
        else: x["grp"] = x[col]
        r = x.groupby(["grp", "sig"]).ex.agg(["mean", "count", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
        r.columns = ["mean_ex", "n", "t"]; return r
    out["ex_by_day_return_sign"] = tab("r1", [-9, 0, 9], ["down_day", "up_day"])
    out["ex_by_r20"] = tab("r20", [-9, -0.1, 0, 0.1, 9], ["<-10%", "-10..0", "0..10", ">10%"])
    out["ex_by_above_ma50"] = tab("above50")
    out["ex_by_clv"] = tab("clv", [-0.01, 0.33, 0.67, 1.01], ["low", "mid", "high"])
    out["mean_alloc_sig_vs_not"] = G.groupby("sig").al.agg(["mean", "count"])
    out["share_alloc_pos"] = float((G.al > 0).mean())
    return out
