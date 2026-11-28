def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [3, 5, 7]
    rows = []
    for coin, ws in bars.items():
        allr = {h: [] for h in H}
        for w, b in ws.items():
            c = b["close"].values
            for h in H:
                for i in range(0, len(c) - h, h):
                    allr[h].append(c[i + h] / c[i] - 1)
        drift = {h: np.mean(allr[h]) for h in H}
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            f = b["forecast"].fillna(0).values
            dr = c.pct_change()
            raw = (c / c.shift(7) - 1) / (dr.rolling(30).std() * np.sqrt(7))
            r60 = c / c.shift(60) - 1
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            low = 0.0
            for g in range(0, n, 3):
                for i in range(g, min(g + 3, n)):
                    if f[i] <= 0:
                        low = 0.0
                        continue
                    low = min(low, f[i]) if i > 0 and f[i - 1] > 0 else 0.0
                    if f[i] - low >= 2:
                        r = {"coin": coin, "window": w, "year": ts[i].year, "fc": f[i],
                             "raw": raw.iloc[i], "r60": r60.iloc[i],
                             "dayn": ts[i].normalize()}
                        for h in H:
                            r["u%d" % h] = (c.iloc[i + h] / c.iloc[i] - 1 - drift[h]) if i + h < n else np.nan
                        rows.append(r)
                        low = f[i]
                        break
    d = pd.DataFrame(rows)
    out = {}
    def summ(gr, col="u3"):
        x = gr[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["n_cases"] = len(d)
    out["by_horizon"] = pd.DataFrame({h: summ(d, "u%d" % h) for h in H}).T
    d["rq"] = pd.qcut(d["raw"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["raw_quartile_u3"] = d.groupby("rq").apply(lambda g: summ(g, "u3"))
    out["raw_quartile_u5"] = d.groupby("rq").apply(lambda g: summ(g, "u5"))
    out["raw_quartile_mean_raw"] = d.groupby("rq")["raw"].mean()
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 2, labels=["low", "high"])
    out["fc_half_u3"] = d.groupby("fq").apply(lambda g: summ(g, "u3"))
    out["spearman_raw_u3"] = float(stats.spearmanr(d["raw"], d["u3"], nan_policy="omit")[0])
    out["spearman_raw_u5"] = float(stats.spearmanr(d["raw"], d["u5"], nan_policy="omit")[0])
    d["deep"] = pd.qcut(d["r60"].rank(method="first"), 2, labels=["deeper_fall", "milder_fall"])
    out["by_60d_fall_u3"] = d.groupby("deep").apply(lambda g: summ(g, "u3"))
    return out
