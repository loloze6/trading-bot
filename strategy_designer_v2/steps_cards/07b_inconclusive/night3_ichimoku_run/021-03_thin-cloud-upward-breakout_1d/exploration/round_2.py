def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 26
    rows = []
    drift = {}
    for coin, wins in bars.items():
        rets = {h: [] for h in (10, 26)}
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for h in rets:
                idx = np.arange(0, n - h, h)
                rets[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(v) for h, v in rets.items()}
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            reg = (df["regime"] == "trending").values
            seen = set()
            lr = np.log(c)
            dr = np.r_[np.nan, np.diff(lr)]
            for i in np.where(reg)[0]:
                if i + H >= n:
                    continue
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                r = {"coin": coin}
                r["u26"] = c[i + H] / c[i] - 1 - drift[coin][26]
                r["u10"] = c[i + 10] / c[i] - 1 - drift[coin][10]
                r["past26"] = c[i] / c[i - 26] - 1 if i >= 26 else np.nan
                r["past10"] = c[i] / c[i - 10] - 1 if i >= 10 else np.nan
                r["past100"] = c[i] / c[i - 100] - 1 if i >= 100 else np.nan
                r["ma100gap"] = c[i] / np.mean(c[i - 99:i + 1]) - 1 if i >= 99 else np.nan
                r["vol30"] = np.nanstd(dr[i - 29:i + 1]) if i >= 30 else np.nan
                r["bar_ret"] = dr[i]
                rows.append(r)
    d = pd.DataFrame(rows)
    out = {}
    sp = {}
    for v in ["past26", "past10", "past100", "ma100gap", "vol30", "bar_ret"]:
        for y in ["u26", "u10"]:
            m = d[[v, y]].dropna()
            sp[(v, y)] = {"n": len(m), "spearman": stats.spearmanr(m[v], m[y]).correlation, "pearson": stats.pearsonr(m[v], m[y])[0]}
    out["corr"] = pd.DataFrame(sp).T
    def summ(g):
        x = g["u26"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "median": x.median(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "share_pos": (x > 0).mean()})
    for v in ["past100", "ma100gap", "vol30", "past26"]:
        dd = d.dropna(subset=[v]).copy()
        dd["q"] = pd.qcut(dd[v], 3, labels=False, duplicates="drop")
        out["tercile_" + v] = dd.groupby("q").apply(summ)
    dd = d.dropna(subset=["past26"]).copy()
    dd["neg"] = dd["past26"] < 0
    out["past26_sign"] = dd.groupby("neg").apply(summ)
    x = d["u26"].sort_values(ascending=False)
    out["top_contrib"] = pd.Series({"sum_all": x.sum(), "sum_top5": x.iloc[:5].sum(), "sum_top10": x.iloc[:10].sum(), "max": x.iloc[0]})
    return out
