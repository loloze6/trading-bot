def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]; trades = data["trades"]
    # book daily returns
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    book = D.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book_overall"] = pd.Series({"mean": book.mean(), "sd": book.std(), "sharpe": book.mean()/book.std()*np.sqrt(365), "n": len(book)})
    bw = D.groupby(["w", "day"]).agg(br=("book_return", "mean")).reset_index()
    out["book_by_window"] = bw.groupby("w")["br"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(365)])
    # contribution by coin: sum of coin's book_return / 6 share
    coin_sum = D.groupby("coin")["book_return"].sum()
    out["coin_share_of_sum"] = coin_sum / coin_sum.sum()
    # market rise part
    drift = D.groupby("coin")["coin_return"].mean()
    mr = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy(); b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last().fillna(0)
            mr.append(pd.DataFrame({"w": w, "day": pos.index, "c": c, "mr": pos.values * drift[c]}))
    MR = pd.concat(mr).groupby(["w", "day"])["mr"].mean()
    out["market_rise_part_vs_book_mean"] = pd.Series({"market_part": MR.mean(), "book_mean": book.mean()})
    # trades
    T = []
    for c in trades:
        for w, t in trades[c].items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["w"] = w; T.append(t)
    T = pd.concat(T)
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "mean": p.mean(), "median": p.median(), "win": (p > 0).mean(),
                               "top5_share_of_sum": p.head(5).sum()/p.sum(), "top10_share": p.head(10).sum()/p.sum(),
                               "sum_without_top5": p.iloc[5:].sum(), "mean_dur_days": T["duration_minutes"].mean()/1440})
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    # cases recomputed
    H = [3, 5, 10, 20]
    cases = []; normal = {h: [] for h in H}
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True); cl = b["close"].values; n = len(cl)
            for h in H:
                for i in range(0, n - h, h):
                    normal[h].append((c, cl[i+h]/cl[i]-1))
            f = b["forecast"].fillna(0).values
            rise = np.r_[f[0], np.diff(f)]
            prior_max = pd.Series(cl).shift(1).rolling(60, min_periods=20).max().values
            r1 = np.r_[np.nan, cl[1:]/cl[:-1]-1]
            r20 = pd.Series(cl).pct_change(20).values
            chg = np.abs(pd.Series(cl).diff(60)); vol = pd.Series(cl).diff().abs().rolling(60).sum()
            er = (chg/vol).values
            for g in range(0, n, 10):
                idx = [i for i in range(g, min(g+10, n)) if rise[i] >= 2]
                if not idx: continue
                i = idx[0]
                rec = {"coin": c, "w": w, "i": i, "r1": r1[i], "brk": cl[i]/prior_max[i]-1 if prior_max[i] == prior_max[i] else np.nan,
                       "r20past": r20[i], "er": er[i], "fc": f[i], "day": b["timestamp"].iloc[i]}
                for h in H:
                    rec[f"f{h}"] = cl[i+h]/cl[i]-1 if i+h < n else np.nan
                cases.append(rec)
    C = pd.DataFrame(cases)
    nd = {h: pd.DataFrame(normal[h], columns=["coin", "r"]).groupby("coin")["r"].mean() for h in H}
    for h in H:
        C[f"u{h}"] = C[f"f{h}"] - C["coin"].map(nd[h])
    def tday(col):
        x = C[["day", col]].dropna(); m = x[col].mean()
        s = (x[col]-m).groupby(x["day"]).sum(); G = len(s)
        se = np.sqrt((s**2).sum()*G/(G-1))/len(x)
        return m, m/se, len(x)
    out["unusual_by_horizon"] = pd.DataFrame({h: tday(f"u{h}") for h in H}, index=["mean", "t_day", "n"]).T
    out["u10_by_coin"] = C.groupby("coin")["u10"].agg(["count", "mean"])
    out["u10_by_window"] = C.groupby("w")["u10"].agg(["count", "mean"])
    for col in ["r1", "brk", "r20past", "er"]:
        q = pd.qcut(C[col], 3, labels=False, duplicates="drop")
        out[f"tercile_{col}"] = C.groupby(q).agg(lo=(col, "min"), hi=(col, "max"), n=("u10", "count"), u5=("u5", "mean"), u10=("u10", "mean"), u20=("u20", "mean"))
    out["spearman_u10"] = pd.Series({col: stats.spearmanr(C[col], C["u10"], nan_policy="omit")[0] for col in ["r1", "brk", "r20past", "er", "fc"]})
    return out
