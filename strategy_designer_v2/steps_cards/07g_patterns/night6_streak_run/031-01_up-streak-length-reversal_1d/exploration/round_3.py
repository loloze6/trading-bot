def explore(data):
    import numpy as np, pandas as pd
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol60 = pd.Series(r1).rolling(60).std().values
            ts = pd.to_datetime(b["timestamp"])
            for H in (1, 2, 3):
                fwd = np.full(n, np.nan)
                if n > H:
                    fwd[:n-H] = c[H:] / c[:-H] - 1
                for i in range(0, n, H):
                    if np.isnan(fwd[i]) or not (vol60[i] > 0):
                        continue
                    recs.append(dict(H=H, coin=coin, win=w, r1z=r1[i] / vol60[i], fwd=fwd[i],
                                     year=ts.iloc[i].year, day=ts.iloc[i].normalize()))
    d = pd.DataFrame(recs)
    d["unus"] = d["fwd"] - d.groupby(["H", "coin"])["fwd"].transform("mean")
    d["q10"] = d.groupby(["H", "coin"])["r1z"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    def summ(g):
        x = g["unus"]
        dev = (g["unus"] - x.mean()).groupby(g["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev**2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "days": G, "mean_unus": x.mean(), "t_dayclust": x.mean() / se})
    out["decile_by_H"] = d.groupby(["H", "q10"]).apply(summ)
    neg = d[d.r1z < 0].copy()
    def graded(g):
        from scipy import stats
        r = stats.spearmanr(-g["r1z"], g["unus"])
        return pd.Series({"n": len(g), "spearman_size_vs_unus": r[0], "p": r[1]})
    out["down_days_graded_by_H"] = neg.groupby("H").apply(graded)
    out["down_days_graded_H1_by_coin"] = neg[neg.H == 1].groupby("coin").apply(graded)
    bq = d[(d.H == 1)]
    bq = bq[bq.groupby("coin")["r1z"].transform(lambda s: s <= s.quantile(0.2))]
    out["bottom_quintile_H1_by_coin"] = bq.groupby("coin").apply(summ)
    out["bottom_quintile_H1_by_year"] = bq.groupby("year").apply(summ)
    tq = d[(d.H == 1)]
    tq = tq[tq.groupby("coin")["r1z"].transform(lambda s: s >= s.quantile(0.8))]
    out["top_quintile_H1"] = summ(tq)
    return out
