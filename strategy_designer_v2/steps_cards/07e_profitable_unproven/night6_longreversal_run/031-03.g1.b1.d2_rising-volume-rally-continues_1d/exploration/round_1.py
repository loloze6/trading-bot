def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # ---- book daily returns, market part vs timing
    rows = []
    coin_mean_daily = {}
    for c in bars:
        allr = []
        for w, d in days[c].items():
            allr.append(d["coin_return"].dropna())
        coin_mean_daily[c] = pd.concat(allr).mean()
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["held"] = b["postRebalance_current_allocation"].shift(1)
            d = days[c][w].copy()
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D")
            m = d.merge(b[["day", "held", "regime"]], on="day", how="left")
            m["coin"] = c; m["window"] = w
            m["year"] = m["day"].dt.year
            m["mkt"] = m["held"] * coin_mean_daily[c]
            rows.append(m)
    D = pd.concat(rows).dropna(subset=["book_return"])
    daily = D.groupby("day").agg(book=("book_return", "mean"), mkt=("mkt", "mean"),
                                 hold=("coin_return", "mean"))
    out["book mean/day, market part, timing"] = pd.Series({
        "book_mean": daily.book.mean(), "market_part": daily.mkt.mean(),
        "timing": daily.book.mean() - daily.mkt.mean(),
        "t_book": daily.book.mean() / daily.book.std() * np.sqrt(len(daily)),
        "n_days": len(daily), "hold_mean": daily.hold.mean(),
        "corr_book_hold": daily.book.corr(daily.hold)})
    # by year
    dy = daily.copy(); dy["year"] = dy.index.year
    out["by year"] = dy.groupby("year").agg(book=("book", "mean"), mkt=("mkt", "mean"),
                                            hold=("hold", "mean"), n=("book", "size"))
    # per coin: sum of book returns contribution (each day weighted 1/ncoins)
    nc = D.groupby("day")["coin"].transform("count")
    D["contrib"] = D["book_return"] / nc
    pc = D.groupby("coin").agg(contrib=("contrib", "sum"), mean_book=("book_return", "mean"),
                               mkt=("mkt", "mean"), hold=("coin_return", "mean"))
    pc["share"] = pc.contrib / pc.contrib.sum()
    out["by coin"] = pc.sort_values("share", ascending=False)
    # contribution by holding market state: coin's 30d return sign at day
    # ---- trades concentration
    T = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if len(t): T.append(t.assign(coin=c))
    T = pd.concat(T)
    r = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(r), "mean": r.mean(), "median": r.median(),
                               "win_share": (r > 0).mean(), "top10_sum_share": r.head(10).sum() / r.sum(),
                               "top5pct_sum_share": r.head(int(len(r)*0.05)).sum() / r.sum(),
                               "sum": r.sum()})
    # ---- signal decomposition on 14/7/28 grids
    res = []
    for H in [7, 14, 28]:
        cases = []
        for c in bars:
            allg = []
            for w, b in bars[c].items():
                cl = b["close"].values
                for i in range(0, len(cl) - H, H):
                    allg.append(cl[i + H] / cl[i] - 1)
            mu = np.mean(allg)
            for w, b in bars[c].items():
                cl = b["close"].values; f = b["forecast"].values
                v = b["volume"].values
                for i in range(0, len(cl) - H, H):
                    if i < 30: continue
                    r14 = cl[i] / cl[i - 14] - 1
                    r60 = cl[i] / cl[max(0, i - 60)] - 1 if i >= 60 else np.nan
                    vs = v[i-13:i+1].mean() / v[i-29:i+1].mean() - 1
                    cases.append((c, w, i, cl[i + H] / cl[i] - 1 - mu, r14, r60, vs, f[i]))
        C = pd.DataFrame(cases, columns=["coin", "w", "i", "ex", "r14", "r60", "vs", "f"])
        groups = {"f>0": C.f > 0, "r14>0&f==0": (C.r14 > 0) & (C.f <= 0),
                  "r14<=0": C.r14 <= 0, "r14>0 all": C.r14 > 0,
                  "r14>0&vs<=0": (C.r14 > 0) & (C.vs <= 0)}
        for k, g in groups.items():
            x = C.loc[g, "ex"]
            res.append({"H": H, "group": k, "n": len(x), "mean_ex": x.mean(),
                        "t": x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan})
        # graded: r14 quintiles
        C["q14"] = pd.qcut(C.r14, 5, labels=False)
        for q, x in C.groupby("q14")["ex"]:
            res.append({"H": H, "group": f"r14 q{q}", "n": len(x), "mean_ex": x.mean(),
                        "t": x.mean() / x.std() * np.sqrt(len(x))})
        Cs = C.dropna(subset=["r60"])
        Cs["q60"] = pd.qcut(Cs.r60, 5, labels=False)
        for q, x in Cs.groupby("q60")["ex"]:
            res.append({"H": H, "group": f"r60 q{q}", "n": len(x), "mean_ex": x.mean(),
                        "t": x.mean() / x.std() * np.sqrt(len(x))})
        sp = stats.spearmanr(C.r14, C.ex)
        res.append({"H": H, "group": "spearman r14", "n": len(C), "mean_ex": sp.correlation, "t": sp.pvalue})
        sub = C[C.r14 > 0]
        sp = stats.spearmanr(sub.vs, sub.ex)
        res.append({"H": H, "group": "spearman vs|r14>0", "n": len(sub), "mean_ex": sp.correlation, "t": sp.pvalue})
    out["grid decomposition"] = pd.DataFrame(res)
    return out
