def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lo = b["low"].astype(float).where(lambda s: s > 0)
            f = b["forecast"].astype(float).fillna(0)
            raw = b.get("debug_info.components.support_touches.last_history_value")
            raw = raw.astype(float) if raw is not None else pd.Series(np.nan, index=b.index)
            fwd = c.shift(-5) / c - 1
            r5 = c / c.shift(5) - 1
            lo90 = lo.rolling(90, min_periods=20).min()
            cl90 = c.rolling(90, min_periods=20).min()
            hi90 = c.rolling(90, min_periods=20).max()
            pos = (c - cl90) / (hi90 - cl90)
            for i in range(0, len(b) - 5, 5):
                rows.append(dict(coin=coin, win=w, fwd=fwd[i], f=f[i], raw=raw[i], r5=r5[i],
                                 dlo=c[i] / cl90[i] - 1, pos=pos[i]))
    df = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = df.groupby("coin")["fwd"].mean()
    df["ex"] = df["fwd"] - df["coin"].map(drift)
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(),
                              t=stats.ttest_1samp(g["ex"], 0).statistic if len(g) > 2 else np.nan,
                              wmean_ex=(g["ex"] * g["f"]).sum() / g["f"].sum() if g["f"].sum() > 0 else np.nan))
    out = {}
    a = df[df.f > 0].copy()
    a["pos_q"] = pd.qcut(a["pos"], 5, labels=False, duplicates="drop")
    out["active_by_pos_in_90d_range_q5"] = a.groupby("pos_q").apply(summ).join(a.groupby("pos_q")["pos"].mean().rename("pos_mean"))
    a["dlo_q"] = pd.qcut(a["dlo"], 6, labels=False, duplicates="drop")
    out["active_by_dist_90d_closelow_q6"] = a.groupby("dlo_q").apply(summ).join(a.groupby("dlo_q")["dlo"].median().rename("dlo_med"))
    nf = df[(df.f <= 0) & (df.r5 < 0)].copy()
    nf["pos_q"] = pd.qcut(nf["pos"], 5, labels=False, duplicates="drop")
    out["inactive_falls_by_pos_q5"] = nf.groupby("pos_q").apply(summ).join(nf.groupby("pos_q")["pos"].mean().rename("pos_mean"))
    out["spearman_active_pos_vs_ex"] = float(stats.spearmanr(a["pos"], a["ex"], nan_policy="omit").correlation)
    out["spearman_fallers_pos_vs_ex"] = float(stats.spearmanr(df.loc[df.r5 < 0, "pos"], df.loc[df.r5 < 0, "ex"], nan_policy="omit").correlation)
    # book chain falls
    ch = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            ch.append(pd.DataFrame(dict(win=w, i=np.arange(len(d)), br=d["book_return"].values)))
    bk = pd.concat(ch).dropna()
    bk["wn"] = bk["win"].str[1:].astype(int)
    daily = bk.groupby(["wn", "i"])["br"].mean().sort_index()
    v = (1 + daily).cumprod()
    dd = v / v.cummax() - 1
    out["book_deepest_fall"] = float(dd.min())
    out["book_yearly"] = float(v.iloc[-1] ** (365 / len(v)) - 1)
    return out
