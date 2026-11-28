def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            r7 = c / c.shift(7) - 1
            r3 = c / c.shift(3) - 1
            sc = r7 / (sd20 * np.sqrt(7))
            sc3 = r3 / (sd20 * np.sqrt(3))
            hi30 = c.rolling(30, min_periods=10).max()
            athigh = c >= hi30
            dist = c / hi30 - 1
            inprof = b["regime"].astype(str).isin(["trending", "unknown"])
            ts = pd.to_datetime(b["timestamp"])
            for h in [2, 3, 5, 7]:
                fr = (c.shift(-h) / c - 1).values
                for i in np.arange(0, len(b) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, ret=fr[i], sc=sc.iloc[i], sc3=sc3.iloc[i],
                                     athigh=bool(athigh.iloc[i]), dist=dist.iloc[i],
                                     inprof=bool(inprof.iloc[i]), day=ts.iloc[i].normalize(),
                                     yr=ts.iloc[i].year))
    df = pd.DataFrame(rows).dropna(subset=["ret"])
    df["drift"] = df.groupby(["coin", "h"])["ret"].transform("mean")
    df["un"] = df["ret"] - df["drift"]
    def tday(g):
        d = g.groupby("day")["un"].sum()
        nd = len(d); m = g["un"].mean()
        se = np.sqrt(((d - g.groupby("day")["un"].count() * m) ** 2).sum()) / len(g) * np.sqrt(nd / max(nd - 1, 1))
        return m / se if se > 0 else np.nan, nd
    def summ(g):
        t, nd = tday(g)
        return pd.Series(dict(n=len(g), days=nd, unusual=g["un"].mean(), total=g["ret"].mean(), t_day=t))
    out = {}
    p = df[df.inprof].dropna(subset=["sc"])
    pos = p[p.sc > 0].copy()
    out["in profile, rising 7d (sc>0), by h"] = pos.groupby("h").apply(summ)
    out["in profile, falling 7d (sc<=0), by h"] = p[p.sc <= 0].groupby("h").apply(summ)
    out["rising 7d, by h, at 30d high or below"] = pos.groupby(["h", "athigh"]).apply(summ)
    for h in [3, 5, 7]:
        ph = pos[pos.h == h].copy()
        ph["b"] = pd.qcut(ph["sc"], 3, labels=False, duplicates="drop")
        out[f"rising 7d h{h}, by sc tercile"] = ph.groupby("b").apply(summ).join(ph.groupby("b")["sc"].mean().rename("sc_mean"))
    out["rho sc vs un among rising, by h"] = pos.groupby("h").apply(lambda g: pd.Series(dict(rho=stats.spearmanr(g.sc, g.un)[0], n=len(g))))
    out["rho sc3 vs un in profile, by h"] = p.dropna(subset=["sc3"]).groupby("h").apply(lambda g: pd.Series(dict(rho=stats.spearmanr(g.sc3, g.un)[0], n=len(g))))
    p3 = pos[pos.h == 3]
    out["rising 7d h3, by coin"] = p3.groupby("coin").apply(summ)
    out["rising 7d h3, by year"] = p3.groupby("yr").apply(summ)
    out["rising 7d h3, by window"] = p3.groupby("w").apply(summ)
    return out
