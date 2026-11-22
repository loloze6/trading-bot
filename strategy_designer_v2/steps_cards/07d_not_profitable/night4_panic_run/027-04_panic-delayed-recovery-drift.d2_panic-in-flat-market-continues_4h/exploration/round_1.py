import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 78
    out = {}
    # normal drift per coin
    drift, usual = {}, {}
    for c, ws in data["bars"].items():
        rs = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - H, H)
            rs += list(cl[idx + H] / cl[idx] - 1)
        drift[c] = np.mean(rs); usual[c] = np.std(rs)
    out["drift_usual"] = pd.DataFrame({"drift": drift, "usual": usual})
    # cases
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; f = b["forecast"].values
            ts = pd.to_datetime(b["timestamp"])
            n = len(cl)
            # prior 30-day return (180 bars) for context
            for s in range(0, n - H, H):
                cell = np.where(f[s:s + H] <= -10)[0]
                if len(cell) == 0: continue
                i = s + cell[0]
                if i + H >= n: continue
                r = cl[i + H] / cl[i] - 1
                r1 = cl[min(i + 6, n - 1)] / cl[i] - 1
                r3 = cl[min(i + 18, n - 1)] / cl[i] - 1
                p30 = cl[i] / cl[i - 180] - 1 if i >= 180 else np.nan
                rows.append(dict(coin=c, w=w, year=ts.iloc[i].year, f=f[i],
                                 tot=-r, unus=-(r - drift[c]), short1d=-r1, short3d=-r3, p30=p30))
    d = pd.DataFrame(rows)
    def agg(g):
        return pd.Series(dict(n=len(g), tot=g.tot.mean(), unus=g.unus.mean(),
                              t_unus=stats.ttest_1samp(g.unus, 0).statistic if len(g) > 2 else np.nan,
                              s1d=g.short1d.mean(), s3d=g.short3d.mean()))
    out["cases_all"] = agg(d).to_frame().T
    out["cases_by_coin"] = d.groupby("coin").apply(agg)
    out["cases_by_year"] = d.groupby("year").apply(agg)
    d["fb"] = pd.cut(d.f, [-20.01, -19.9, -17, -15, -10])
    out["cases_by_f"] = d.groupby("fb").apply(agg)
    d["p30b"] = pd.qcut(d.p30, 4)
    out["cases_by_prior30"] = d.groupby("p30b").apply(agg)
    # book decomposition
    bk = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            a = b["postRebalance_current_allocation"].values
            r = b["close"].pct_change().shift(-1).values
            bk.append(dict(coin=c, w=w, mean_alloc=np.nanmean(a), share_active=np.mean(a != 0),
                           gross=np.nansum(a * r)))
    bk = pd.DataFrame(bk)
    out["book_by_coin"] = bk.groupby("coin")[["mean_alloc", "share_active", "gross"]].agg(["mean", "sum"])
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t) == 0: continue
            t = t.copy(); t["coin"] = c; tr.append(t)
    tr = pd.concat(tr)
    tr["dur_d"] = tr.duration_minutes / 1440
    out["trades"] = tr.groupby("coin").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
                                           net=("net_profit_loss_percent", "mean"),
                                           win=("net_profit_loss_percent", lambda x: (x > 0).mean()),
                                           dur=("dur_d", "mean"))
    # daily book
    dd = []
    for c, ws in data["days"].items():
        for w, x in ws.items():
            dd.append(x.assign(coin=c, w=w))
    dd = pd.concat(dd)
    dd["year"] = pd.to_datetime(dd.day).dt.year
    out["daily_by_year"] = dd.groupby("year")[["book_return", "coin_return"]].mean()
    return out
