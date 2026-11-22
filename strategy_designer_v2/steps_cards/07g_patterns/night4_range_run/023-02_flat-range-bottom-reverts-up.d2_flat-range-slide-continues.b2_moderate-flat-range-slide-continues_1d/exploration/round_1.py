import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        grid_rets = []
        tmp = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, hi, lo = b["close"], b["high"], b["low"]
            rng = hi.rolling(30).max() - lo.rolling(30).min()
            mid = (hi.rolling(30).max() + lo.rolling(30).min()) / 2
            nmr = (c - c.shift(30)).abs() / rng
            pos = (c - mid) / (rng / 2)
            r10 = c / c.shift(10) - 1
            ext = r10 / r10.abs().rolling(60, min_periods=20).mean()
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            r3 = c / c.shift(3) - 1
            fwd = c.shift(-H) / c - 1
            d = pd.DataFrame({"nmr": nmr, "pos": pos, "r10": r10, "ext": ext, "vol20": vol20,
                              "r3": r3, "fwd": fwd, "fc": b["forecast"], "reg": b["regime"],
                              "alloc": b["postRebalance_current_allocation"]})
            d = d.iloc[::H]
            d["coin"] = coin; d["win"] = w
            grid_rets.append(d["fwd"].dropna())
            tmp.append(d)
        m = pd.concat(grid_rets).mean()
        for d in tmp:
            d["unus"] = d["fwd"] - m
            d["volq"] = np.nan
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["volq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    D = D.dropna(subset=["unus"])

    def summ(g):
        x = g["unus"].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    out = {}
    D["flat"] = np.where(D["nmr"] <= 0.3, "flat", "trend")
    D["posb"] = pd.cut(D["pos"], [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01])
    out["flat x pos bucket: unusual fwd5 (long side)"] = D.dropna(subset=["nmr", "pos"]).groupby(["flat", "posb"], observed=True).apply(summ)
    D["extb"] = pd.cut(D["ext"], [-10, -2, -1, 0, 1, 2, 10])
    out["flat x ext bucket"] = D.dropna(subset=["nmr", "ext"]).groupby(["flat", "extb"], observed=True).apply(summ)
    act = D[D["fc"] < 0].copy()
    act["fcq"] = pd.qcut(act["fc"], 4, labels=False, duplicates="drop")
    out["active: fc quartile (0=most negative) long-side unusual"] = act.groupby("fcq").apply(summ)
    out["active by coin"] = act.groupby("coin").apply(summ)
    out["active by window"] = act.groupby("win").apply(summ).sort_values("mean")
    D["r3q"] = D.groupby("coin")["r3"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["volq x r3 quintile"] = D.dropna(subset=["volq", "r3q"]).groupby(["volq", "r3q"]).apply(summ)
    out["regime"] = D.groupby("reg").apply(summ)
    # weekday daily returns
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; dd.append(x)
    DD = pd.concat(dd).dropna(subset=["coin_return"])
    DD["wd"] = pd.to_datetime(DD["day"]).dt.dayofweek
    out["weekday coin_return"] = DD.groupby("wd")["coin_return"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    bk = DD.dropna(subset=["book_return"])
    out["book: share of days nonzero, mean, sum top10 / sum all"] = pd.Series({
        "n": len(bk), "nonzero": (bk["book_return"] != 0).mean(), "mean": bk["book_return"].mean(),
        "top20sum": bk["book_return"].nlargest(20).sum(), "bot20sum": bk["book_return"].nsmallest(20).sum(),
        "total": bk["book_return"].sum()})
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    T["dur_d"] = T["duration_minutes"] / 1440
    T["durb"] = pd.cut(T["dur_d"], [0, 5.5, 10, 20, 1000])
    out["trades by duration"] = T.groupby("durb", observed=True)["net_profit_loss_percent"].agg(["count", "mean"])
    return out
