def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        mu = np.nanmean(allr); sd = np.nanstd(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            lr = np.log(c).diff()
            r28 = c / c.shift(28) - 1
            r1 = c / c.shift(1) - 1
            vol30 = lr.rolling(30).std()
            near = c / c.rolling(90, min_periods=20).max()
            n = len(c)
            comb = b.get("debug_info.components.combined.post_pipeline_value", pd.Series([np.nan]*n))
            best = b.get("debug_info.components.best.post_pipeline_value", pd.Series([np.nan]*n))
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, reg=b["regime"].iloc[i],
                                 r28=r28.iloc[i], r1=r1.iloc[i], vol30=vol30.iloc[i], near=near.iloc[i],
                                 comb=comb.iloc[i], best=best.iloc[i],
                                 fwd=c.iloc[i+H]/c.iloc[i]-1, ex=c.iloc[i+H]/c.iloc[i]-1-mu,
                                 exz=(c.iloc[i+H]/c.iloc[i]-1-mu)/sd))
    d = pd.DataFrame(rows)
    t = d[d.reg == "trending"].dropna(subset=["r28", "comb"]).copy()
    out = {}
    cs = {}
    for s in ["r28", "r1", "vol30", "near"]:
        g = t.dropna(subset=[s])
        cs[s] = pd.Series({"comb": stats.spearmanr(g.comb, g[s])[0], "best": stats.spearmanr(g.best, g[s])[0],
                           "fwd_ex": stats.spearmanr(g[s], g.ex)[0]})
    out["comb_best_vs_signals_trend"] = pd.DataFrame(cs).T
    yy = {}
    for y, g in t.groupby("year"):
        if len(g) < 30: continue
        yy[y] = pd.Series({"n": len(g), "comb~r28": stats.spearmanr(g.comb, g.r28)[0],
                           "r28~ex": stats.spearmanr(g.r28, g.ex)[0], "comb~ex": stats.spearmanr(g.comb, g.ex)[0]})
    out["by_year_signs"] = pd.DataFrame(yy).T
    # r28 long side only in trend, graded size
    g = t[t.r28 > 0].copy()
    g["q"] = pd.qcut(g.r28, 4, labels=False)
    out["trend_r28pos_quartiles"] = g.groupby("q").apply(lambda x: pd.Series({
        "n": len(x), "r28_mean": x.r28.mean(), "total": x.fwd.mean(), "unusual": x.ex.mean(),
        "t": x.ex.mean()/(x.ex.std()/np.sqrt(len(x))), "strength": x.exz.mean()}))
    # comb sign vs r28 sign agreement
    t["agree"] = np.sign(t.comb) == np.sign(t.r28)
    out["comb_r28_agree"] = t.groupby("agree").apply(lambda x: pd.Series({
        "n": len(x), "share_comb_short": (x.comb < 0).mean(),
        "signed_ex_comb": (np.sign(x.comb)*x.ex).mean(), "signed_ex_r28": (np.sign(x.r28)*x.ex).mean()}))
    # book daily falls
    D = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            D.append(x.assign(coin=coin, w=w))
    D = pd.concat(D)
    out["book_by_window_mean"] = D.groupby("w").book_return.mean().describe()
    return out
