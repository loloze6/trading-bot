import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars, days = data["bars"], data["days"]
    out = {}
    # --- book decomposition
    rows = []
    for c in days:
        mu = pd.concat([d["coin_return"] for d in days[c].values()]).mean()
        for w, d in days[c].items():
            b = bars[c][w]
            pos = b["postRebalance_current_allocation"].shift(1).values
            n = min(len(d), len(pos))
            dd = d.iloc[:n].copy()
            dd["pos"] = pos[:n]
            dd["mkt"] = dd["pos"] * mu
            dd["coin"] = c; dd["w"] = w
            dd["year"] = pd.to_datetime(dd["day"]).dt.year
            rows.append(dd)
    D = pd.concat(rows)
    D = D.dropna(subset=["book_return"])
    daily = D.groupby(["w", "day"]).agg(book=("book_return", "mean"), mkt=("mkt", "mean"), hold=("coin_return", "mean"))
    out["book_decomp"] = pd.Series({"book_mean": daily.book.mean(), "mkt_part": daily.mkt.mean(),
        "timing": daily.book.mean() - daily.mkt.mean(), "t_book": daily.book.mean() / daily.book.std() * np.sqrt(len(daily)),
        "sharpe": daily.book.mean() / daily.book.std() * np.sqrt(365), "hold_sharpe": daily.hold.mean() / daily.hold.std() * np.sqrt(365), "ndays": len(daily)})
    ncoin = D["coin"].nunique()
    out["by_coin_sum_contrib"] = D.groupby("coin")["book_return"].sum() / ncoin
    out["by_window"] = daily.groupby("w").agg(book_sum=("book", "sum"), hold_sum=("hold", "sum"))
    D2 = D.copy()
    out["by_year"] = D2.groupby("year")["book_return"].sum() / ncoin
    # top trades
    tr = pd.concat([t for c in data["trades"] for t in data["trades"][c].values()])
    p = tr["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "sum": p.sum(), "top5_sum": p.head(5).sum(), "top10_sum": p.head(10).sum(), "win_share": (p > 0).mean(), "median": p.median()})
    # --- breakout cases
    res = []
    for h in [5, 10, 20, 40]:
        cases = []
        for c in bars:
            allr = []
            for w, b in bars[c].items():
                cl = b["close"].values
                allr += list(cl[h::h] / cl[:-h:h][:len(cl[h::h])] - 1)
            mh = np.mean(allr)
            for w, b in bars[c].items():
                cl = b["close"].reset_index(drop=True)
                pm = cl.shift(1).rolling(60).max()
                R = cl.shift(1) / cl.shift(61) - 1
                absr = (cl / cl.shift(60) - 1).abs().rolling(120, min_periods=60).mean().shift(1)
                brk = cl > pm
                n = len(cl)
                for s in range(0, n, h):
                    idx = [i for i in range(s, min(s + h, n)) if brk.iloc[i]]
                    if not idx: continue
                    i = idx[0]
                    if i + h >= n: continue
                    cases.append(dict(h=h, coin=c, w=w, ts=str(b["timestamp"].iloc[i])[:10], R=R.iloc[i], Rm=R.iloc[i] / absr.iloc[i] if absr.iloc[i] > 0 else np.nan,
                                      dist=cl.iloc[i] / pm.iloc[i] - 1, ex=cl.iloc[i + h] / cl.iloc[i] - 1 - mh))
        res += cases
    C = pd.DataFrame(res)
    def summ(g):
        dd = g.groupby("ts")["ex"].sum()
        return pd.Series({"n": len(g), "mean_ex": g.ex.mean(), "t_day": dd.mean() / dd.std() * np.sqrt(len(dd)) if len(dd) > 2 else np.nan})
    out["all_by_h"] = C.groupby("h").apply(summ)
    C["Rq"] = C.groupby("h")["R"].transform(lambda x: pd.qcut(x, 3, labels=["low", "mid", "high"]))
    C["dq"] = C.groupby("h")["dist"].transform(lambda x: pd.qcut(x, 3, labels=["small", "mid", "big"]))
    out["by_runup_tercile"] = C.groupby(["h", "Rq"]).apply(summ)
    out["by_dist_tercile"] = C.groupby(["h", "dq"]).apply(summ)
    out["by_coin_h20"] = C[C.h == 20].groupby("coin").apply(summ)
    out["by_window_h20"] = C[C.h == 20].groupby("w").apply(summ)
    cor = []
    for h, g in C.dropna(subset=["Rm"]).groupby("h"):
        cor.append(dict(h=h, corr_Rm=stats.spearmanr(g.Rm, g.ex)[0], corr_dist=stats.spearmanr(g.dist, g.ex)[0]))
    out["spearman"] = pd.DataFrame(cor)
    return out
