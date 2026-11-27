def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values; o = df["open"].values
            n = len(df)
            rng = h - l
            loc = np.where(rng > 0, (c - l) / np.where(rng > 0, rng, 1), np.nan)
            r1 = pd.Series(c).pct_change().values
            ret5 = pd.Series(c).pct_change(5).values
            ret20 = pd.Series(c).pct_change(20).values
            vol20 = pd.Series(r1).rolling(20).std().values
            ts = pd.to_datetime(df["timestamp"])
            for H in (2, 5):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, loc=loc[i], ret5=ret5[i], ret20=ret20[i], r1=r1[i],
                                     vol20=vol20[i], rngp=rng[i] / c[i], body=(c[i] - o[i]) / c[i],
                                     inprof=df["regime"].iloc[i] != "chop", wd=ts.iloc[i].dayofweek,
                                     fwd=c[i + H] / c[i] - 1))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby(["coin", "H"])["fwd"].transform("mean")
    g["un"] = g["fwd"] - g["drift"]
    g["volrel"] = g["vol20"] / g.groupby("coin")["vol20"].transform("median")
    def agg(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out = {}
    g["locb"] = pd.cut(g["loc"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["q1", "q2", "q3", "q4"])
    g["r5s"] = np.where(g["ret5"] < 0, "r5neg", "r5pos")
    g["r1b"] = pd.qcut(g["r1"], 5, labels=False)
    g["volb"] = pd.qcut(g["volrel"], 4, labels=False)
    g["r20b"] = pd.qcut(g["ret20"], 5, labels=False)
    for H in (2, 5):
        s = g[g.H == H]
        out[f"H{H} prof x loc x r5"] = s.groupby(["inprof", "locb", "r5s"])["un"].apply(agg).unstack()
        out[f"H{H} prof x r1 quintile"] = s.groupby(["inprof", "r1b"])["un"].apply(agg).unstack()
        out[f"H{H} out-prof vol x r1"] = s[~s.inprof].groupby(["volb", "r1b"])["un"].apply(agg).unstack()
        out[f"H{H} r20 quint x prof"] = s.groupby(["inprof", "r20b"])["un"].apply(agg).unstack()
        out[f"H{H} weekday"] = s.groupby("wd")["un"].apply(agg).unstack()
    s = g[(g.H == 5) & g.inprof]
    out["prof H5 spearman"] = pd.Series({k: stats.spearmanr(s[k], s["un"], nan_policy="omit")[0] for k in ["loc", "ret5", "ret20", "r1", "rngp", "body", "volrel"]})
    # book days
    dl = []
    for coin, ws in days.items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dl.append(d)
    D = pd.concat(dl)
    D = D.dropna(subset=["book_return"])
    act = D[D.book_return != 0]
    out["book active days"] = pd.Series(dict(n=len(act), mean=act.book_return.mean(), coinret_mean=act.coin_return.mean(),
                                            corr=act[["book_return", "coin_return"]].corr().iloc[0, 1]))
    out["book by window"] = act.groupby("w")["book_return"].agg(["count", "mean", "sum"])
    out["book by coin"] = act.groupby("coin")["book_return"].agg(["count", "mean", "sum"])
    q = act.book_return.quantile([0.05, 0.95])
    out["extreme days coin ret"] = pd.Series(dict(worst_mean_coin=act[act.book_return <= q.iloc[0]].coin_return.mean(),
                                                 best_mean_coin=act[act.book_return >= q.iloc[1]].coin_return.mean(),
                                                 share_sum_top5=act[act.book_return >= q.iloc[1]].book_return.sum() / act.book_return.sum()))
    return out
