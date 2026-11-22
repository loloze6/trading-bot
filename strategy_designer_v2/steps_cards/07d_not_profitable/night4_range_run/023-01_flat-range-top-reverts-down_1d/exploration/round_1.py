import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    H = 5
    rows = []
    allret = {}
    for c in bars:
        rr = []
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            hi = b["high"].rolling(30).max(); lo = b["low"].rolling(30).min()
            net = (b["close"] - b["close"].shift(29)).abs()
            ratio = net / (hi - lo)
            mid = (b["close"] - (hi + lo) / 2) / b["close"] * 100
            for i in range(0, n - H, H):
                r = cl[i + H] / cl[i] - 1
                rr.append(r)
                rows.append(dict(coin=c, w=w, f=b["forecast"].iloc[i], r=r,
                                 ratio=ratio.iloc[i], mid=mid.iloc[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
        allret[c] = (np.mean(rr), np.std(rr))
    d = pd.DataFrame(rows)
    d["drift"] = d.coin.map(lambda c: allret[c][0]); d["sd"] = d.coin.map(lambda c: allret[c][1])
    s = d[d.f != 0].copy()
    s["dir"] = np.sign(s.f)
    s["unusual"] = s.dir * (s.r - s.drift); s["total"] = s.dir * s.r
    s["strength"] = s.unusual / s.sd
    s["side"] = np.where(s.dir > 0, "long", "short")
    def agg(g):
        return pd.Series(dict(n=len(g), total=g.total.mean(), unusual=g.unusual.mean(),
                              strength=g.strength.mean(),
                              t=g.unusual.mean() / (g.unusual.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    out["size_all"] = agg(s).to_frame().T
    out["size_by_side"] = s.groupby("side").apply(agg)
    s["fq"] = pd.qcut(s.f.abs(), 4, labels=False, duplicates="drop")
    out["size_by_absforecast_q"] = s.groupby("fq").apply(agg)
    s["rq"] = pd.qcut(s.ratio, 4, labels=False, duplicates="drop")
    out["size_by_flatness_q"] = s.groupby("rq").apply(agg)
    out["size_by_coin"] = s.groupby("coin").apply(agg)
    out["drift_sd_5d"] = pd.DataFrame(allret, index=["drift", "sd"]).T
    # all bars reversion: mid distance vs forward return in flat vs non flat
    d2 = d.dropna(subset=["ratio", "mid"]).copy()
    d2["flat"] = d2.ratio <= 0.33
    d2["z"] = -np.sign(d2.mid) * (d2.r - d2.drift) / d2.sd
    out["reversion_flat_vs_not"] = d2.groupby("flat").z.agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    # book daily
    bk = []
    for c in days:
        for w, dd in days[c].items():
            b = bars[c][w]
            alloc = b.groupby(pd.to_datetime(b.timestamp).dt.floor("D"))["postRebalance_current_allocation"].last().values
            t = dd.copy(); t["coin"] = c; t["w"] = w
            t["alloc_prev"] = pd.Series(alloc[:len(t)]).shift(1).values
            bk.append(t)
    bk = pd.concat(bk)
    cm = bk.groupby("coin").coin_return.mean()
    bk["mkt"] = bk.alloc_prev * bk.coin.map(cm)
    daily = bk.groupby(["w", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean"), mkt=("mkt", "mean")).dropna()
    out["book_decomp"] = pd.Series(dict(book_mean=daily.book.mean(), hold_mean=daily.hold.mean(),
                                        market_part=daily.mkt.mean(), timing=daily.book.mean() - daily.mkt.mean(),
                                        book_sharpe=daily.book.mean() / daily.book.std() * np.sqrt(365),
                                        hold_sharpe=daily.hold.mean() / daily.hold.std() * np.sqrt(365),
                                        share_days_invested=(bk.alloc_prev.abs() > 0.01).mean(),
                                        mean_abs_alloc=bk.alloc_prev.abs().mean()))
    bk["side"] = np.select([bk.alloc_prev > 0.01, bk.alloc_prev < -0.01], ["long", "short"], "flat")
    out["book_by_side"] = bk.groupby("side").agg(n=("book_return", "count"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    out["book_by_window"] = daily.groupby("w").agg(book=("book", "mean"), hold=("hold", "mean"))
    # trades
    tr = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"] = tr.groupby("side").agg(n=("net_profit_loss_percent", "count"), gross=("profit_loss_percent", "mean"),
                                           net=("net_profit_loss_percent", "mean"), days=("duration_minutes", lambda x: x.mean() / 1440))
    return out
