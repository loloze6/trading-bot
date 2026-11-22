import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # coin mean daily return over all windows
    cmean = {}
    for c in coins:
        cr = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        cmean[c] = cr.mean()
    # pooled book daily returns per window, in window order
    wins = sorted(days[coins[0]].keys(), key=lambda s: int(s[1:]))
    recs = []
    for w in wins:
        parts = []
        for c in coins:
            d = days[c][w].copy()
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            alloc = b.groupby("day")["postRebalance_current_allocation"].mean()
            d["day"] = pd.to_datetime(d["day"])
            d = d.set_index("day")
            d["alloc"] = alloc.reindex(d.index)
            d["mkt"] = d["alloc"].shift(1) * cmean[c]
            # coin 30d prior return
            d["c30"] = d["close"] / d["close"].shift(30) - 1
            d["c7"] = d["close"] / d["close"].shift(7) - 1
            d["coin"] = c
            parts.append(d[["book_return", "coin_return", "alloc", "mkt", "c30", "c7", "coin"]])
        p = pd.concat(parts)
        g = p.groupby(level=0).agg({"book_return": "mean", "coin_return": "mean", "alloc": "mean", "mkt": "mean"})
        g["w"] = w
        recs.append(g)
        out_parts = p.assign(w=w)
        recs[-1] = (g, out_parts)
    book = pd.concat([r[0] for r in recs])
    allc = pd.concat([r[1] for r in recs])
    bd = book.dropna(subset=["book_return"])
    s = lambda x: x.mean() / x.std() * np.sqrt(365)
    out["sharpe"] = pd.Series({"book": s(bd.book_return), "hold": s(bd.coin_return),
                               "book_mean": bd.book_return.mean(), "hold_mean": bd.coin_return.mean(),
                               "mkt_part": bd.mkt.mean(), "mean_alloc": bd.alloc.mean(),
                               "corr_book_coin": bd.book_return.corr(bd.coin_return)})
    eq = (1 + bd.book_return).cumprod().values
    peak = np.maximum.accumulate(eq); dd = eq / peak - 1
    i = dd.argmin(); j = eq[:i + 1].argmax()
    seg = bd.iloc[j + 1:i + 1]
    out["deepest_fall"] = pd.Series({"depth": dd[i], "days": i - j, "coin_ret_in_fall": (1 + seg.coin_return).prod() - 1,
                                     "mean_alloc_in_fall": seg.alloc.mean(),
                                     "windows": ",".join(sorted(set(seg.w), key=lambda s: int(s[1:])))})
    pw = bd.groupby("w").agg(book=("book_return", lambda x: (1 + x).prod() - 1),
                             coin=("coin_return", lambda x: (1 + x).prod() - 1), alloc=("alloc", "mean"))
    out["per_window"] = pw.reindex(wins)
    # book return by coin's 30d return tercile (per coin)
    a = allc.dropna(subset=["book_return", "c30"]).copy()
    a["q30"] = pd.qcut(a["c30"], 3, labels=["down", "mid", "up"])
    out["book_by_coin30d"] = a.groupby("q30").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
                                                  alloc=("alloc", "mean"), n=("book_return", "size"))
    # case-level: 24-bar grid, forecast>=2
    rows = []
    for c in coins:
        drift = []
        for w in bars[c]:
            cl = bars[c][w]["close"].values
            idx = np.arange(0, len(cl) - 24, 24)
            drift.append(cl[idx + 24] / cl[idx] - 1)
        dr = np.concatenate(drift).mean()
        for w in bars[c]:
            b = bars[c][w]; cl = b["close"].values; f = b["forecast"].values
            r1 = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            for k in range(0, len(cl) - 24, 24):
                cell = np.where(f[k:k + 24] >= 2)[0]
                if len(cell) == 0: continue
                t = k + cell[0]
                if t + 24 >= len(cl): continue
                fwd = cl[t + 24] / cl[t] - 1
                p30 = cl[t] / cl[t - 720] - 1 if t >= 720 else np.nan
                p7 = cl[t] / cl[t - 168] - 1 if t >= 168 else np.nan
                vol7 = np.nanstd(r1[max(1, t - 168):t + 1])
                rows.append((c, w, f[t], fwd - dr, fwd, p30, p7, vol7, r1[t]))
    cs = pd.DataFrame(rows, columns=["coin", "w", "f", "unus", "tot", "p30", "p7", "vol7", "r1"])
    def summ(g):
        return pd.Series({"n": len(g), "unus": g.unus.mean(), "t": g.unus.mean() / g.unus.std() * np.sqrt(len(g))})
    cs["qf"] = pd.qcut(cs.f.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["cases_by_forecast"] = cs.groupby("qf").apply(summ)
    c2 = cs.dropna(subset=["p30"]).copy(); c2["q"] = pd.qcut(c2.p30, 3, labels=["down", "mid", "up"])
    out["cases_by_30d_ret"] = c2.groupby("q").apply(summ)
    c3 = cs.dropna(subset=["p7"]).copy(); c3["q"] = pd.qcut(c3.p7, 3, labels=["down", "mid", "up"])
    out["cases_by_7d_ret"] = c3.groupby("q").apply(summ)
    c4 = cs.dropna(subset=["vol7"]).copy(); c4["q"] = pd.qcut(c4.vol7, 3, labels=["low", "mid", "high"])
    out["cases_by_7d_vol"] = c4.groupby("q").apply(summ)
    out["cases_by_coin"] = cs.groupby("coin").apply(summ)
    # fees
    fees = []
    for c in coins:
        for w in data["trades"][c]:
            tr = data["trades"][c][w]
            fees.append(pd.Series({"gross": tr.profit_loss_percent.mean(), "net": tr.net_profit_loss_percent.mean(), "n": len(tr),
                                   "dur_h": tr.duration_minutes.mean() / 60}))
    ft = pd.DataFrame(fees)
    out["trades"] = pd.Series({"gross_mean": (ft.gross * ft.n).sum() / ft.n.sum(), "net_mean": (ft.net * ft.n).sum() / ft.n.sum(),
                               "n": ft.n.sum(), "dur_h": (ft.dur_h * ft.n).sum() / ft.n.sum()})
    # time in market
    tim = []
    for c in coins:
        for w in bars[c]:
            al = bars[c][w]["postRebalance_current_allocation"]
            tim.append(((al > 0.01).mean(), al[al > 0.01].mean()))
    tim = np.array(tim)
    out["time_long"] = pd.Series({"share_bars_long": tim[:, 0].mean(), "alloc_when_long": np.nanmean(tim[:, 1])})
    return out
