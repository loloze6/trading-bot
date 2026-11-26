def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # 1) book daily returns, market drift part vs timing
    rows = []
    for c in days:
        mu = pd.concat([days[c][w]["coin_return"] for w in days[c]]).mean()
        for w in days[c]:
            d = days[c][w].copy()
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            alloc = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            d["dayk"] = pd.to_datetime(d["day"]).dt.floor("D")
            d["alloc"] = d["dayk"].map(alloc)
            d["drift"] = d["alloc"] * mu
            d["coin"] = c; d["win"] = w
            d["year"] = pd.to_datetime(d["day"]).dt.year
            rows.append(d)
    D = pd.concat(rows)
    bk = D.groupby(["win", "day"]).agg(br=("book_return", "mean"), dr=("drift", "mean"), cr=("coin_return", "mean")).dropna()
    out["book mean, drift part, timing"] = pd.Series({"book_mean": bk.br.mean(), "drift_part": bk.dr.mean(),
        "timing": bk.br.mean() - bk.dr.mean(), "sharpe": bk.br.mean() / bk.br.std() * np.sqrt(365), "ndays": len(bk)})
    out["book by window"] = bk.groupby(level=0).br.agg(["mean", "count", lambda s: s.sum()])
    out["book share by coin (sum of coin daily ret/6)"] = D.groupby("coin")["book_return"].sum() / 6
    out["book by year"] = D.groupby("year")["book_return"].agg(["mean", "sum"])
    # 2) trades concentration
    T = pd.concat([trades[c][w].assign(coin=c, win=w) for c in trades for w in trades[c] if len(trades[c][w])])
    r = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(r), "mean": r.mean(), "median": r.median(), "share_pos": (r > 0).mean(),
        "sum": r.sum(), "top5_sum": r.head(5).sum(), "top10_sum": r.head(10).sum(),
        "sum_without_top10": r.iloc[10:].sum()})
    # 3) break cases: forward returns by horizon and margin quintile
    cases = []
    allret = {h: [] for h in [1, 3, 5, 10, 20]}
    for c in bars:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            for h in allret:
                idx = np.arange(0, n - h, h)
                allret[h].append(pd.Series(cl[idx + h] / cl[idx] - 1).assign if False else pd.Series(cl[idx + h] / cl[idx] - 1, dtype=float))
            prox = b["debug_info.components.margin_prox.last_history_value"]
            brk = (b["regime"] == "trending").values
            last = -999
            ret20 = pd.Series(cl).pct_change(20).values
            for i in range(n):
                if brk[i] and i - last > 3:
                    last = i
                    p = prox.iloc[i]
                    rec = {"coin": c, "win": w, "margin": (1 / p - 1) if pd.notna(p) and p > 0 else np.nan,
                           "ret20": ret20[i], "consec": 0}
                    for h in allret:
                        rec[f"f{h}"] = cl[i + h] / cl[i] - 1 if i + h < n else np.nan
                    cases.append(rec)
    C = pd.DataFrame(cases)
    mu = {h: pd.concat(allret[h]).mean() for h in allret}
    for h in allret:
        C[f"x{h}"] = C[f"f{h}"] - mu[h]
    res = {}
    for h in allret:
        x = C[f"x{h}"].dropna()
        res[h] = {"n": len(x), "mean_excess": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)), "drift": mu[h]}
    out["break excess by horizon"] = pd.DataFrame(res).T
    C["mq"] = pd.qcut(C["margin"], 5, labels=False, duplicates="drop")
    out["excess by margin quintile"] = C.groupby("mq").agg(margin=("margin", "median"), n=("x3", "count"),
        x1=("x1", "mean"), x3=("x3", "mean"), x5=("x5", "mean"), x10=("x10", "mean"), x20=("x20", "mean"))
    C["r20q"] = pd.qcut(C["ret20"], 4, labels=False, duplicates="drop")
    out["excess by prior 20d return quartile"] = C.groupby("r20q").agg(r20=("ret20", "median"), n=("x3", "count"),
        x3=("x3", "mean"), x10=("x10", "mean"))
    out["excess by coin"] = C.groupby("coin").agg(n=("x3", "count"), x3=("x3", "mean"), x10=("x10", "mean"))
    return out
