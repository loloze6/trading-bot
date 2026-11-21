def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lo = b["low"].astype(float)
            f = b["forecast"].astype(float).fillna(0)
            fwd = c.shift(-5) / c - 1
            r5 = c / c.shift(5) - 1
            r90 = c / c.shift(90) - 1
            r30 = c / c.shift(30) - 1
            prevlo = lo.shift(1).rolling(60, min_periods=20).min()
            brk = c / prevlo - 1
            for i in range(0, len(b) - 5, 5):
                rows.append(dict(coin=coin, win=w, fwd=fwd[i], f=f[i], r5=r5[i], r90=r90[i], r30=r30[i],
                                 brk=brk[i], year=pd.Timestamp(b["timestamp"][i]).year))
    df = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = df.groupby("coin")["fwd"].mean()
    df["ex"] = df["fwd"] - df["coin"].map(drift)
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(),
                              t=stats.ttest_1samp(g["ex"], 0).statistic if len(g) > 2 else np.nan,
                              mean_fwd=g["fwd"].mean()))
    out = {}
    a = df[df.f > 0].dropna(subset=["r90"]).copy()
    a["q"] = pd.qcut(a["r90"], 4, labels=False, duplicates="drop")
    out["active_by_r90_q"] = a.groupby("q").apply(summ).join(a.groupby("q")["r90"].mean().rename("r90_mean"))
    a2 = df[df.f > 0].dropna(subset=["r30"]).copy()
    a2["q"] = pd.qcut(a2["r30"], 4, labels=False, duplicates="drop")
    out["active_by_r30_q"] = a2.groupby("q").apply(summ).join(a2.groupby("q")["r30"].mean().rename("r30_mean"))
    out["spearman_active_r90_ex"] = float(stats.spearmanr(a["r90"], a["ex"]).correlation)
    allb = df.dropna(subset=["r90"]).copy()
    allb["q"] = pd.qcut(allb["r90"], 4, labels=False, duplicates="drop")
    out["all_bars_by_r90_q"] = allb.groupby("q").apply(summ)
    # break below prior 60-day low: continuation?
    br = df.dropna(subset=["brk"]).copy()
    br["below"] = br["brk"] < 0
    out["close_below_prior60d_low"] = br.groupby("below").apply(summ)
    bb = br[br.below].copy()
    bb["q"] = pd.qcut(bb["brk"], 3, labels=False, duplicates="drop")
    out["below_low_by_depth_q"] = bb.groupby("q").apply(summ).join(bb.groupby("q")["brk"].mean().rename("depth"))
    bb2 = bb.dropna(subset=["r90"]).copy()
    bb2["down90"] = bb2["r90"] < 0
    out["below_low_by_r90_sign"] = bb2.groupby("down90").apply(summ)
    return out
