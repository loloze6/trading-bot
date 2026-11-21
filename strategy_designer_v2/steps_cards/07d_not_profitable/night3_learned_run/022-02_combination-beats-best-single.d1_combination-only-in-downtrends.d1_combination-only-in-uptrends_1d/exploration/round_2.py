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
            r5 = c / c.shift(5) - 1
            vol30 = lr.rolling(30).std()
            hi = c.rolling(min(90, len(c)), min_periods=20).max()
            near = c / hi
            n = len(c)
            r90 = b.get("debug_info.components.ret90.last_history_value", pd.Series([np.nan]*n))
            comb = b.get("debug_info.components.combined.post_pipeline_value", pd.Series([np.nan]*n))
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, reg=b["regime"].iloc[i], r28=r28.iloc[i], r1=r1.iloc[i],
                                 r5=r5.iloc[i], vol30=vol30.iloc[i], near=near.iloc[i], r90=r90.iloc[i],
                                 comb=comb.iloc[i], ex=c.iloc[i+H]/c.iloc[i]-1-mu, fwd=c.iloc[i+H]/c.iloc[i]-1,
                                 exz=(c.iloc[i+H]/c.iloc[i]-1-mu)/sd))
    d = pd.DataFrame(rows)
    t = d[d.reg == "trending"]
    out = {}
    sp = {}
    for s in ["r28", "r1", "r5", "vol30", "near", "r90", "comb"]:
        g = t.dropna(subset=[s, "ex"])
        rho, p = stats.spearmanr(g[s], g.ex)
        sp[s] = pd.Series({"n": len(g), "spearman": rho, "p": p})
    out["trend_signal_vs_ex"] = pd.DataFrame(sp).T
    sp2 = {}
    u = d[d.reg != "trending"]
    for s in ["r28", "r1", "r5", "vol30", "near"]:
        g = u.dropna(subset=[s, "ex"])
        rho, p = stats.spearmanr(g[s], g.ex)
        sp2[s] = pd.Series({"n": len(g), "spearman": rho, "p": p})
    out["unknown_signal_vs_ex"] = pd.DataFrame(sp2).T
    def summ(g):
        return pd.Series({"n": len(g), "fwd": g.fwd.mean(), "ex": g.ex.mean(),
                          "t_ex": g.ex.mean()/(g.ex.std()/np.sqrt(len(g))), "strength": g.exz.mean()})
    for s in ["r28", "r5", "vol30", "near"]:
        g = t.dropna(subset=[s]).copy()
        g["q"] = pd.qcut(g[s], 5, labels=False, duplicates="drop")
        out["trend_by_" + s] = g.groupby("q").apply(summ)
    g = t.dropna(subset=["vol30"]).copy()
    g["q"] = pd.qcut(g.vol30, 5, labels=False)
    out["vol30_q_mean"] = g.groupby("q").vol30.mean()
    return out
