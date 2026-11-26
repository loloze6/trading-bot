def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    # normal drift and usual move per coin per horizon
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs, ddof=1)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            pmax = cl.shift(1).rolling(60).max()
            pmin = cl.shift(1).rolling(60).min()
            mad = cl.pct_change().abs().shift(1).rolling(60).mean()
            W = (pmax - pmin) / pmin / mad
            brk = cl / pmax - 1
            fc = df["forecast"]
            n = len(df)
            seen = set()
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for i in range(n):
                if fc.iloc[i] > 0 and brk.iloc[i] > 0:
                    cell = i // 5
                    if cell in seen: continue
                    seen.add(cell)
                    r = {"coin": c, "win": w, "year": yr.iloc[i], "fc": fc.iloc[i], "W": W.iloc[i],
                         "brk": brk.iloc[i] / mad.iloc[i] if mad.iloc[i] > 0 else np.nan,
                         "fresh": int(not (cl.iloc[i-1] > pmax.iloc[i-1])) if i > 0 else np.nan}
                    for h in H:
                        r[f"u{h}"] = (cl.iloc[i+h] / cl.iloc[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                    rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g):
        out = {"n": len(g)}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"u{h}"] = x.mean()
            out[f"t{h}"] = x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    res = {}
    res["all"] = summ(d)
    res["by_coin"] = d.groupby("coin").apply(summ)
    res["by_year"] = d.groupby("year").apply(summ)
    d["Wq"] = pd.qcut(d["W"], 5, labels=False)
    res["by_W_quint"] = d.groupby("Wq").apply(summ)
    res["W_quint_means"] = d.groupby("Wq")["W"].mean()
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 5, labels=False)
    res["by_fc_quint"] = d.groupby("fq").apply(summ)
    d["bq"] = pd.qcut(d["brk"], 5, labels=False)
    res["by_brk_quint"] = d.groupby("bq").apply(summ)
    res["by_fresh"] = d.groupby("fresh").apply(summ)
    res["corr_spearman"] = pd.DataFrame({f"u{h}": [stats.spearmanr(d["W"], d[f"u{h}"], nan_policy="omit")[0],
                                                     stats.spearmanr(d["brk"], d[f"u{h}"], nan_policy="omit")[0],
                                                     stats.spearmanr(d["fc"], d[f"u{h}"], nan_policy="omit")[0]] for h in H},
                                        index=["W", "brk", "fc"])
    res["corr_W_fc"] = stats.spearmanr(d["W"], d["fc"], nan_policy="omit")[0]
    return res
