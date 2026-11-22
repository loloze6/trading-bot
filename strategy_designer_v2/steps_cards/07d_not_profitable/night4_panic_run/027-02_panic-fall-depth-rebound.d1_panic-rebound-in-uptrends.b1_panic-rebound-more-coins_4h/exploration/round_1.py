import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["wn"] = int(w[1:])
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"]).dropna()
    eq = (1 + B["book_return"]).cumprod().values
    ddv = eq / np.maximum.accumulate(eq) - 1
    B["dd"] = ddv
    out["book"] = pd.Series({"days": len(B), "mean": B.book_return.mean(), "std": B.book_return.std(),
                             "maxdd": ddv.min(), "yearly": eq[-1] ** (365 / len(B)) - 1,
                             "share_days_nonzero": (B.book_return.abs() > 1e-9).mean()})
    i = int(np.argmin(ddv)); p = int(np.argmax(eq[:i + 1]))
    out["deepest_fall"] = pd.Series({"peak_wn": B.wn.iloc[p], "trough_wn": B.wn.iloc[i], "days": i - p,
                                     "dd": ddv[i], "coin_mean": B.coin_return.iloc[p:i + 1].mean(),
                                     "book_mean": B.book_return.iloc[p:i + 1].mean()})
    g = B.groupby("wn")
    out["by_window"] = pd.DataFrame({"mean_book": g.book_return.mean(), "mean_coin": g.coin_return.mean(),
                                     "min_dd": g.dd.min()})
    tr = []; ex = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            a = b["postRebalance_current_allocation"].fillna(0).values
            ex.append(((a > 0).mean(), a[a > 0].mean() if (a > 0).any() else np.nan))
            t = data["trades"][c][w]
            if len(t) == 0:
                continue
            t = t.copy()
            ts = pd.to_datetime(b["timestamp"]).values
            cl = b["close"].values
            n = len(cl)
            r540 = pd.Series(cl).pct_change(540).values
            r6 = pd.Series(cl).pct_change(6).values
            r180 = pd.Series(cl).pct_change(180).values
            pos = np.clip(np.searchsorted(ts, pd.to_datetime(t["entry_time"]).values), 0, n - 1)
            t["r540"] = r540[pos]; t["r6"] = r6[pos]; t["r180"] = r180[pos]
            t["alloc"] = a[pos]
            # max adverse excursion within the trade
            mae = []
            for k, e in zip(pos, np.clip(np.searchsorted(ts, pd.to_datetime(t["exit_time"]).values), 0, n - 1)):
                seg = cl[k:e + 1]
                mae.append(seg.min() / cl[k] - 1 if len(seg) else np.nan)
            t["mae"] = mae
            t["wn"] = int(w[1:])
            tr.append(t)
    E = np.array(ex, dtype=float)
    out["exposure"] = pd.Series({"share_bars_long": np.nanmean(E[:, 0]), "mean_alloc_when_long": np.nanmean(E[:, 1])})
    T = pd.concat(tr)
    x = T.net_profit_loss_percent
    out["trades"] = pd.Series({"n": len(T), "mean_net": x.mean(), "median_net": x.median(), "win": (x > 0).mean(),
                               "t": stats.ttest_1samp(x, 0).statistic, "mean_days": (T.duration_minutes / 1440).mean(),
                               "mean_alloc": T.alloc.mean(), "mean_mae": T.mae.mean()})
    for col in ["r540", "r180", "r6", "alloc"]:
        b = pd.qcut(T[col], 4, duplicates="drop")
        out["by_" + col] = T.groupby(b, observed=True).agg(n=("net_profit_loss_percent", "size"),
                                                           mean=("net_profit_loss_percent", "mean"),
                                                           mae=("mae", "mean"))
    out["by_year"] = T.assign(y=pd.to_datetime(T.entry_time).dt.year).groupby("y").net_profit_loss_percent.agg(["count", "mean"])
    return out
