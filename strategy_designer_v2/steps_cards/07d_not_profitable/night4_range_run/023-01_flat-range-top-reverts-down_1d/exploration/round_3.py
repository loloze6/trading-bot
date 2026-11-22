import pandas as pd, numpy as np

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    H = 5
    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    # book in the drawdown windows w15-w19 vs others, by side and coin
    rows = []
    for c in days:
        for w, dd in days[c].items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b.timestamp).dt.floor("D")
            g = b.groupby("day").agg(alloc=("postRebalance_current_allocation", "last"), reg=("regime", "last"))
            t = dd.copy(); t["day"] = pd.to_datetime(t.day)
            t = t.merge(g, left_on="day", right_index=True, how="left")
            t["alloc_prev"] = t.alloc.shift(1)
            t["coin"] = c; t["wn"] = int(w[1:])
            rows.append(t)
    bk = pd.concat(rows)
    bk["dd_win"] = np.where(bk.wn.between(15, 19), "w15-19", "other")
    bk["side"] = np.select([bk.alloc_prev > 0.01, bk.alloc_prev < -0.01], ["long", "short"], "flat")
    bk["contrib"] = bk.book_return
    out["book_by_ddwin_side"] = bk.groupby(["dd_win", "side"]).agg(n=("book_return", "count"), book=("book_return", "mean"),
                                                                   coin=("coin_return", "mean"), sum_book=("book_return", "sum"))
    out["book_ddwin_by_coin"] = bk[bk.dd_win == "w15-19"].groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
                                                                             mean_alloc=("alloc_prev", "mean"))
    # flat regime: graded test within above-middle side; and r90 strength
    sr = []
    stats_c = {}
    for c in bars:
        rr = []
        for w, b in bars[c].items():
            b = b.reset_index(drop=True); cl = b.close.values; n = len(b)
            hi = b.high.rolling(30).max(); lo = b.low.rolling(30).min()
            ratio = (b.close - b.close.shift(29)).abs() / (hi - lo)
            mid = (b.close - (hi + lo) / 2) / b.close * 100
            pos = (b.close - lo) / (hi - lo)
            r90 = b.close / b.close.shift(89) - 1
            for i in range(0, n - H, H):
                r = cl[i + H] / cl[i] - 1; rr.append(r)
                sr.append(dict(coin=c, wn=int(w[1:]), r=r, ratio=ratio.iloc[i], mid=mid.iloc[i], pos=pos.iloc[i], r90=r90.iloc[i]))
        stats_c[c] = (np.mean(rr), np.std(rr))
    d = pd.DataFrame(sr).dropna(subset=["ratio", "mid"])
    d["ex"] = (d.r - d.coin.map(lambda c: stats_c[c][0])) / d.coin.map(lambda c: stats_c[c][1])
    f = d[d.ratio <= 0.33].copy()
    f["posq"] = pd.qcut(f.pos, 5, labels=False, duplicates="drop")
    out["flat_ex_by_range_position_q"] = f.groupby("posq").ex.apply(tt).unstack()
    out["flat_pos_mean_by_q"] = f.groupby("posq").pos.mean()
    a = f[f.mid > 0].copy()
    a["midq"] = pd.qcut(a.mid, 3, labels=False)
    out["flat_above_ex_by_midq"] = a.groupby("midq").ex.apply(tt).unstack()
    out["flat_above_corr_mid_ex"] = a[["mid", "ex"]].corr().iloc[0, 1]
    bl = f[f.mid < 0].copy()
    bl["midq"] = pd.qcut(bl.mid, 3, labels=False)
    out["flat_below_ex_by_midq"] = bl.groupby("midq").ex.apply(tt).unstack()
    out["flat_ex_by_ddwin"] = f.assign(g=np.where(f.wn.between(15, 19), "w15-19", "other"), rev=-np.sign(f.mid) * f.ex).groupby("g").rev.apply(tt).unstack()
    return out
