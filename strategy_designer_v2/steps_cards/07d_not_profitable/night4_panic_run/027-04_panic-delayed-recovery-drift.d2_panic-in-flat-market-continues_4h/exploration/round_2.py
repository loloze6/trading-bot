import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 78
    out = {}
    drift = {}
    for c, ws in data["bars"].items():
        rs = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - H, H)
            rs += list(cl[idx + H] / cl[idx] - 1)
        drift[c] = np.mean(rs)
    # book: market part vs timing, per bar
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            a = b["postRebalance_current_allocation"].fillna(0).values
            f = b["forecast"].fillna(0).values
            cl = b["close"].values
            r = np.append(cl[1:] / cl[:-1] - 1, np.nan)
            p30 = pd.Series(cl).pct_change(180).values
            # bars since last forecast <= -10
            last = -10**9; since = np.full(len(f), np.nan)
            for i in range(len(f)):
                if f[i] <= -10: last = i
                if i - last < 10**8: since[i] = (i - last) / 6.0
            rows.append(pd.DataFrame(dict(coin=c, w=w, a=a, f=f, r=r, p30=p30, since=since)))
    d = pd.concat(rows)
    d = d.dropna(subset=["r"])
    d["g"] = d.a * d.r
    d["mkt_bar"] = d.coin.map({c: v / H for c, v in drift.items()})
    d["mkt"] = d.a * d.mkt_bar
    act = d[d.a != 0]
    out["bars_share"] = pd.Series(dict(share_f_nonzero=(d.f != 0).mean(), share_f_le10=(d.f <= -10).mean(),
                                      share_alloc_nonzero=(d.a != 0).mean(),
                                      mean_gain_bar=d.g.mean(), market_part=d.mkt.mean(),
                                      timing=d.g.mean() - d.mkt.mean()))
    act = act.copy()
    act["since_b"] = pd.cut(act.since, [-0.1, 1, 3, 7, 13, 30, 1000])
    out["held_by_days_since_signal"] = act.groupby("since_b").agg(
        n=("g", "size"), mean_a=("a", "mean"), gain_bar=("g", "mean"), mkt=("mkt", "mean"),
        t=("g", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    act["p30b"] = pd.qcut(act.p30, 4)
    out["held_by_prior30"] = act.groupby("p30b").agg(n=("g", "size"), gain_bar=("g", "mean"),
                                                    mkt=("mkt", "mean"))
    # case unusual move by prior-30 in finer bins, and short-direction move vs prior 30 correlation
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; f = b["forecast"].values; n = len(cl)
            for s in range(0, n - H, H):
                cell = np.where(f[s:s + H] <= -10)[0]
                if len(cell) == 0: continue
                i = s + cell[0]
                if i + H >= n or i < 180: continue
                r = cl[i + H] / cl[i] - 1
                cs.append(dict(coin=c, p30=cl[i] / cl[i - 180] - 1, p7=cl[i] / cl[i - 42] - 1,
                               unus=-(r - drift[c]), tot=-r))
    cs = pd.DataFrame(cs)
    cs["p30q"] = pd.qcut(cs.p30, 6)
    out["cases_prior30_sextiles"] = cs.groupby("p30q").agg(n=("unus", "size"), unus=("unus", "mean"),
                                                          tot=("tot", "mean"),
                                                          t=("unus", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    out["corr_unus_p30"] = pd.Series(dict(spearman=stats.spearmanr(cs.p30, cs.unus).correlation,
                                         spearman_p7=stats.spearmanr(cs.p7, cs.unus).correlation, n=len(cs)))
    # daily book: deepest falls
    dd = []
    for c, ws in data["days"].items():
        for w, x in ws.items():
            dd.append(x.assign(coin=c, w=w))
    dd = pd.concat(dd)
    m = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    byw = m.groupby(level=0).agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
                                 n=("book_return", "size"))
    out["daily_by_window"] = byw.sort_values("book").head(8)
    out["corr_book_coin_daily"] = float(m.book_return.corr(m.coin_return))
    return out
