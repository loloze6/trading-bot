def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    allret = {}
    for coin, ws in data["bars"].items():
        allret[coin] = pd.concat([b["close"].pct_change().dropna() for b in ws.values()]).mean()
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            sd = r.rolling(30).std()
            sd365med = sd.rolling(365, min_periods=60).median()
            tr60 = c / c.shift(60) - 1
            rng = (b["high"] - b["low"]) / c
            width = rng / sd
            low = (b["high"] - c) / (b["high"] - b["low"])
            for i in range(len(b) - 1):
                rows.append(dict(coin=coin, w=w, fc=b["forecast"].iloc[i], nxt=nxt.iloc[i],
                                 width=width.iloc[i], low=low.iloc[i], tr=tr60.iloc[i],
                                 calm=(sd.iloc[i] <= sd365med.iloc[i]) if pd.notna(sd365med.iloc[i]) else np.nan))
    d = pd.DataFrame(rows).dropna(subset=["nxt", "width", "low"])
    d["ex"] = d["nxt"] - d["coin"].map(allret)
    d["prod"] = d["width"] * d["low"]
    out = {}
    def summ(g):
        n = len(g)
        return pd.Series(dict(n=n, mean=g["ex"].mean(), t=g["ex"].mean() / (g["ex"].std() / np.sqrt(n)) if n > 1 else np.nan))
    def half(g, col):
        m = g[col].median()
        a = g.loc[g[col] > m, "ex"]; bb = g.loc[g[col] <= m, "ex"]
        return pd.Series(dict(n_hi=len(a), hi=a.mean(), n_lo=len(bb), lo=bb.mean(), diff=a.mean() - bb.mean(),
                              welch_t=stats.ttest_ind(a, bb, equal_var=False)[0]))
    act = d[d["fc"] > 0]
    out["active_halves"] = pd.DataFrame({k: half(act, k) for k in ["width", "low", "prod"]}).T
    # broader situation: rising (60d>10%), low close >=0.5, any width
    br = d[(d["tr"] > 0.10) & (d["low"] >= 0.5)]
    br["pq"] = pd.qcut(br["prod"], 5, labels=False)
    out["rising_lowclose_prod_quintiles"] = br.groupby("pq").apply(summ)
    out["rising_lowclose_spearman"] = pd.Series(dict(prod=stats.spearmanr(br["prod"], br["ex"])[0], n=len(br)))
    brc = br[br["calm"] == True]
    brc["pq"] = pd.qcut(brc["prod"], 5, labels=False)
    out["rising_calm_lowclose_prod_quintiles"] = brc.groupby("pq").apply(summ)
    out["rising_calm_lowclose_spearman"] = pd.Series(dict(prod=stats.spearmanr(brc["prod"], brc["ex"])[0], n=len(brc)))
    wide = d[(d["tr"] > 0.10) & (d["width"] >= 2)]
    wide["lq"] = pd.qcut(wide["low"], 4, labels=False, duplicates="drop")
    out["rising_wide_by_low_quartile"] = wide.groupby("lq").apply(summ)
    return out
