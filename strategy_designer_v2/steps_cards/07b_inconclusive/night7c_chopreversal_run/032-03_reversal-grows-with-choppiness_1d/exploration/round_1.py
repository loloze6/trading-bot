def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 7
    col = "debug_info.components.chop_rev.post_pipeline_value"
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            r1 = pd.Series(c).pct_change()
            sd30 = r1.rolling(30).std()
            ch = pd.Series(c).diff().abs().rolling(30).sum()
            net = (pd.Series(c) - pd.Series(c).shift(30)).abs()
            er = net / ch
            mv7 = pd.Series(c) / pd.Series(c).shift(7) - 1
            scaled = mv7 / (sd30 * np.sqrt(7))
            for p in range(0, n - H, H):
                fr = c[p + H] / c[p] - 1
                fr3 = c[min(p + 3, n - 1)] / c[p] - 1
                fr14 = c[p + 14] / c[p] - 1 if p + 14 < n else np.nan
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[p]).year,
                                 day=str(b["timestamp"].iloc[p])[:10], f=b[col].iloc[p] if col in b else np.nan,
                                 fr=fr, fr3=fr3, fr14=fr14, chop=1 - er.iloc[p], sc=scaled.iloc[p],
                                 sd=sd30.iloc[p]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby("coin")["fr"].transform("mean")
    d["ex"] = d["fr"] - d["drift"]
    d["ex14"] = d["fr14"] - d.groupby("coin")["fr14"].transform("mean")
    d["ex3"] = d["fr3"] - d.groupby("coin")["fr3"].transform("mean")
    d = d.dropna(subset=["f"])
    out = {}
    def slope(g, x="f", y="ex"):
        g = g.dropna(subset=[x, y])
        if len(g) < 15: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g[y])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))
    out["all"] = slope(d)
    out["by_coin"] = d.groupby("coin").apply(slope)
    out["by_window"] = d.groupby("w").apply(slope)
    out["by_year"] = d.groupby("year").apply(slope)
    d["fq"] = pd.qcut(d["f"], 5, labels=False)
    out["by_fq"] = d.groupby("fq").agg(n=("ex", "size"), fmean=("f", "mean"), ex=("ex", "mean"),
                                        dirmove=("ex", lambda s: (s * np.sign(d.loc[s.index, "f"])).mean()))
    d["side"] = np.sign(d["f"])
    out["by_side"] = d.groupby("side").apply(slope)
    dd = d.dropna(subset=["chop", "sc"])
    dd["cq"] = pd.qcut(dd["chop"], 4, labels=False)
    dd["msc"] = -dd["sc"]
    out["msc_by_chopq"] = dd.groupby("cq").apply(lambda g: slope(g, "msc", "ex"))
    out["msc_by_chopq_h14"] = dd.groupby("cq").apply(lambda g: slope(g, "msc", "ex14"))
    out["msc_by_chopq_h3"] = dd.groupby("cq").apply(lambda g: slope(g, "msc", "ex3"))
    out["f_h3"] = slope(d, "f", "ex3"); out["f_h14"] = slope(d, "f", "ex14")
    dd["vq"] = dd.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["msc_by_volq"] = dd.groupby("vq").apply(lambda g: slope(g, "msc", "ex"))
    return out
