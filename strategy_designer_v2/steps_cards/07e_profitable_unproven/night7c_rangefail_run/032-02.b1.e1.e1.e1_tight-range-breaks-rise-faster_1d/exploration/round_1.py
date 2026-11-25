import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # coin mean daily return over all windows
    cmean = {}
    for c in coins:
        r = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        cmean[c] = r.mean()
    # book daily: mean over coins per (window, day)
    rows = []
    for c in coins:
        for w, d in days[c].items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            alloc = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day")
            dd["alloc_prev"] = alloc.reindex(dd.index)
            dd["coin"] = c; dd["window"] = w
            dd["year"] = dd.index.year
            dd["mkt"] = dd["alloc_prev"] * cmean[c]
            rows.append(dd.reset_index())
    D = pd.concat(rows)
    D = D.dropna(subset=["book_return"])
    out["per_coin"] = D.groupby("coin").agg(mean_book=("book_return", "mean"), mkt_part=("mkt", "mean"),
                                           share_in=("alloc_prev", lambda x: (x.abs() > 1e-6).mean()))
    out["per_window"] = D.groupby("window").agg(mean_book=("book_return", "mean"), mkt_part=("mkt", "mean"),
                                               coin_ret=("coin_return", "mean"))
    out["per_year"] = D.groupby("year").agg(mean_book=("book_return", "mean"), mkt_part=("mkt", "mean"),
                                           coin_ret=("coin_return", "mean"))
    out["total"] = pd.Series({"mean_book": D["book_return"].mean(), "mkt_part": D["mkt"].mean()})
    # trades concentration
    T = pd.concat([data["trades"][c][w].assign(coin=c, window=w) for c in coins for w in data["trades"][c]])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "mean_net": p.mean(), "median_net": p.median(),
                               "win_share": (p > 0).mean(), "sum": p.sum(), "sum_top5": p.head(5).sum(),
                               "sum_top10": p.head(10).sum()})
    # breakout cases recomputed, multiple horizons, features
    H = [1, 3, 5, 10, 20]
    cases = []
    for c in coins:
        # drift per horizon
        for w, b in bars[c].items():
            cl = b["close"].values; n = len(cl)
            lr = np.abs(np.diff(np.log(cl)))
            for t in range(60, n):
                pm = cl[t-60:t].max(); pmin = cl[t-60:t].min()
                if cl[t] > pm:
                    rec = {"coin": c, "window": w, "t": t, "dist": cl[t]/pm - 1,
                           "ret60": cl[t]/cl[t-60] - 1,
                           "W": (np.log(pm) - np.log(pmin)) / lr[t-60:t].mean(),
                           "prevbrk": int(cl[t-1] > cl[max(0, t-61):t-1].max()) if t > 60 else np.nan,
                           "ret1": cl[t]/cl[t-1]-1,
                           "volr": np.log(b["volume"].values[t]+1) - np.log(b["volume"].values[t-20:t].mean()+1)}
                    for h in H:
                        rec[f"f{h}"] = cl[t+h]/cl[t]-1 if t+h < n else np.nan
                    cases.append(rec)
    C = pd.DataFrame(cases)
    # drift per coin per horizon (non-overlapping)
    for h in H:
        dr = {}
        for c in coins:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl)-h, h)
                rs += list(cl[idx+h]/cl[idx]-1)
            dr[c] = np.mean(rs)
        C[f"u{h}"] = C[f"f{h}"] - C["coin"].map(dr)
    # per horizon all cases (overlapping, plus first-of-run)
    C["fresh"] = (C["prevbrk"] == 0)
    res = {}
    for h in H:
        for nm, sub in [("all", C), ("fresh", C[C.fresh]), ("repeat", C[~C.fresh])]:
            x = sub[f"u{h}"].dropna()
            res[(h, nm)] = {"n": len(x), "mean_u": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))}
    out["horizon_u"] = pd.DataFrame(res).T
    # graded by features, 5d and 10d unusual
    for f in ["dist", "ret60", "W", "volr", "ret1"]:
        C["q"] = C.groupby("coin")[f].transform(lambda x: pd.qcut(x.rank(method="first"), 4, labels=False))
        out[f"by_{f}"] = C.groupby("q").agg(n=("u5", "count"), fmean=(f, "mean"), u5=("u5", "mean"),
                                            u10=("u10", "mean"), u20=("u20", "mean"))
    out["cases_by_coin"] = C.groupby("coin").agg(n=("u5", "count"), u5=("u5", "mean"), u10=("u10", "mean"))
    out["cases_by_window"] = C.groupby("window").agg(n=("u5", "count"), u5=("u5", "mean"), u10=("u10", "mean"))
    return out
