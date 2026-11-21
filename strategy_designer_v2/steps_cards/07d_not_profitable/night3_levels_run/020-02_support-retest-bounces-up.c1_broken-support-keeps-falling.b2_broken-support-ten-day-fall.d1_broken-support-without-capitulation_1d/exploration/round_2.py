def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 10
    cell_rows = []
    day_rows = []
    for coin, wins in data["bars"].items():
        g_all = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            g_all += list(c[idx + H] / c[idx] - 1)
        mu10 = np.mean(g_all); sd10 = np.std(g_all)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r10p = c / c.shift(10) - 1
            r5p = c / c.shift(5) - 1
            hi20 = c / c.rolling(20, min_periods=10).max() - 1
            cv = c.values
            idx = np.arange(0, len(cv) - H, H)
            for i in idx:
                f = b["forecast"].iloc[i]
                if f != 0 and not np.isnan(f):
                    r = cv[i + H] / cv[i] - 1
                    cell_rows.append({"coin": coin, "win": w, "f": f, "reg": b["regime"].iloc[i],
                                      "tot": np.sign(f) * r, "unus": np.sign(f) * (r - mu10),
                                      "str": np.sign(f) * (r - mu10) / sd10,
                                      "r10p": r10p.iloc[i], "r5p": r5p.iloc[i], "hi20": hi20.iloc[i],
                                      "wnum": int(w[1:])})
            d = data["days"][coin][w].copy()
            d["coin"] = coin; d["win"] = w
            day_rows.append(d[["coin", "win", "book_return", "coin_return"]])
    cells = pd.DataFrame(cell_rows)
    s = cells[cells.f < 0].dropna(subset=["r10p"]).copy()
    # graded: does unusual move of shorts fall with r10p? correlation and split
    out["short: corr(r10p, unus) and t"] = pd.Series({
        "n": len(s), "spearman": stats.spearmanr(s.r10p, s.unus).correlation,
        "pearson": stats.pearsonr(s.r10p, s.unus)[0]})
    dn = s[s.r10p < 0]; up = s[s.r10p >= 0]
    out["short split by r10p sign"] = pd.DataFrame({
        "n": [len(dn), len(up)], "tot": [dn.tot.mean(), up.tot.mean()], "unus": [dn.unus.mean(), up.unus.mean()],
        "strength": [dn["str"].mean(), up["str"].mean()],
        "t_tot": [stats.ttest_1samp(dn.tot, 0).statistic, stats.ttest_1samp(up.tot, 0).statistic]},
        index=["prior10d_down", "prior10d_up"])
    out["Welch down minus up (tot)"] = stats.ttest_ind(dn.tot, up.tot, equal_var=False).statistic
    s["qh"] = pd.qcut(s["hi20"], 4, labels=False, duplicates="drop")
    out["short by distance below 20d high quartile"] = s.groupby("qh").agg(n=("tot", "size"), hi20=("hi20", "mean"),
                                                                          tot=("tot", "mean"), unus=("unus", "mean"))
    # within prior-down shorts, graded by |f|
    dn = dn.copy(); dn["qf"] = pd.qcut(dn.f.abs().rank(method="first"), 3, labels=False)
    out["prior-down shorts by |f| tercile"] = dn.groupby("qf").agg(n=("tot", "size"), f=("f", "mean"), tot=("tot", "mean"), unus=("unus", "mean"))
    l = cells[cells.f > 0].dropna(subset=["r10p"]).copy()
    l["qr"] = pd.qcut(l["r10p"], 3, labels=False)
    out["long cells by prior 10d tercile"] = l.groupby("qr").agg(n=("tot", "size"), r10=("r10p", "mean"), tot=("tot", "mean"), unus=("unus", "mean"))
    # book daily
    days = pd.concat(day_rows, ignore_index=True).dropna()
    bd = days.groupby(["win"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    bd["wnum"] = bd.index.str[1:].astype(int)
    bd = bd.sort_values("wnum")
    out["book vs coins mean daily by window"] = bd[["book", "coin"]]
    out["corr book, coin daily"] = days.book_return.corr(days.coin_return)
    return out
