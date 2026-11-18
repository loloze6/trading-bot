def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 10
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            n = len(b)
            if n < 130: continue
            hi, lo, cl, vol = b["high"], b["low"], b["close"], b["volume"]
            ph20 = hi.shift(1).rolling(20).max()
            r20 = hi.shift(1).rolling(20).max() - lo.shift(1).rolling(20).min()
            r100 = hi.shift(1).rolling(100).max() - lo.shift(1).rolling(100).min()
            ratio = r20 / r100
            ret1 = cl.pct_change()
            past10 = cl / cl.shift(10) - 1
            past20 = cl / cl.shift(20) - 1
            vol20 = ret1.rolling(20).std()
            vol100 = ret1.rolling(100).std()
            vr = vol / vol.shift(1).rolling(20).mean()
            brkstr = (cl - ph20) / ph20
            fwd = cl.shift(-H) / cl - 1
            for i in range(0, n - H, H):
                rows.append(dict(coin=c, w=w, i=i, fwd=fwd[i], ratio=ratio[i], past10=past10[i],
                                 past20=past20[i], vratio=vol20[i] / vol100[i], vr=vr[i],
                                 brk=brkstr[i], wd=pd.Timestamp(b["timestamp"][i]).dayofweek,
                                 year=pd.Timestamp(b["timestamp"][i]).year))
    g = pd.DataFrame(rows)
    g["mfwd"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["mfwd"]
    g["absfwd"] = g["fwd"].abs()
    out = {}
    def tert(col, y):
        d = g.dropna(subset=[col, y]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
        t = d.groupby("q")[y].agg(["mean", "count"])
        a, z = d[d.q == 2][y], d[d.q == 0][y]
        t.loc["top-bot_t", "mean"] = stats.ttest_ind(a, z, equal_var=False).statistic
        return t
    out["ratio->absfwd"] = tert("ratio", "absfwd")
    out["ratio->ex"] = tert("ratio", "ex")
    out["past20->ex"] = tert("past20", "ex")
    out["past10->ex"] = tert("past10", "ex")
    out["vratio->absfwd"] = tert("vratio", "absfwd")
    out["vratio->ex"] = tert("vratio", "ex")
    out["vr->ex"] = tert("vr", "ex")
    out["vr->absfwd"] = tert("vr", "absfwd")
    bk = g[g.brk > 0]
    out["breakout grid ex"] = pd.Series({"n": len(bk), "mean_ex": bk.ex.mean(),
                                         "t": stats.ttest_1samp(bk.ex.dropna(), 0).statistic,
                                         "nonbrk_mean_ex": g[g.brk <= 0].ex.mean()})
    out["year ex"] = g.groupby("year")["ex"].agg(["mean", "count"])
    # rank corrs per coin
    cc = {}
    for c, d in g.groupby("coin"):
        d = d.dropna()
        cc[c] = {k: stats.spearmanr(d[k], d["ex"]).correlation for k in ["ratio", "past20", "vratio", "vr"]}
        cc[c]["ratio_abs"] = stats.spearmanr(d["ratio"], d["absfwd"]).correlation
    out["spearman by coin"] = pd.DataFrame(cc).T
    # book
    dd = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"] = c; d["w"] = w
            d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek
            dd.append(d)
    D = pd.concat(dd).dropna(subset=["book_return", "coin_return"])
    out["book by weekday"] = D.groupby("wd")[["book_return", "coin_return"]].mean()
    t = D.groupby("wd")["coin_return"].apply(lambda s: s.mean() / s.std() * np.sqrt(len(s)))
    out["coin wd t"] = t
    return out
