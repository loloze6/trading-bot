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
            sc = r7 / (sd20 * np.sqrt(7))
            dist = c / c.rolling(30, min_periods=10).max() - 1
            r14p = c / c.shift(14) - 1
            inprof = b["regime"].astype(str).isin(["trending", "unknown"])
            for h in [3, 7, 14]:
                idx = np.arange(0, len(b) - h, h)
                fr = (c.shift(-h) / c - 1).values
                for i in idx:
                    rows.append(dict(coin=coin, w=w, h=h, ret=fr[i], sc=sc.iloc[i], r7=r7.iloc[i],
                                     dist=dist.iloc[i], r14p=r14p.iloc[i], inprof=bool(inprof.iloc[i]),
                                     sit=bool(b["regime"].iloc[i] == "trending"),
                                     fc=float(b["forecast"].iloc[i]), yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows).dropna(subset=["ret"])
    df["drift"] = df.groupby(["coin", "h"])["ret"].transform("mean")
    df["un"] = df["ret"] - df["drift"]
    def summ(g):
        n = len(g); m = g["un"].mean(); s = g["un"].std()
        return pd.Series(dict(n=n, unusual=m, total=g["ret"].mean(), t=m / (s / np.sqrt(n)) if n > 2 and s > 0 else np.nan))
    out = {}
    p = df[df.inprof]
    out["profile share of grid, by h"] = df.groupby("h")["inprof"].mean()
    out["in profile, by h and situation"] = p.groupby(["h", "sit"]).apply(summ)
    p7 = p[p.h == 7].dropna(subset=["sc"]).copy()
    p7["scbin"] = pd.qcut(p7["sc"], 5, labels=False, duplicates="drop")
    out["in profile h7, by scaled 7d move quintile"] = p7.groupby("scbin").apply(summ).join(p7.groupby("scbin")["sc"].mean().rename("sc_mean"))
    for h in [3, 14]:
        ph = p[p.h == h].dropna(subset=["sc"]).copy()
        ph["scbin"] = pd.qcut(ph["sc"], 5, labels=False, duplicates="drop")
        out[f"in profile h{h}, by scaled quintile"] = ph.groupby("scbin").apply(summ)
    p7d = p7.dropna(subset=["dist"]).copy()
    p7d["dbin"] = pd.qcut(p7d["dist"], 4, labels=False, duplicates="drop")
    out["in profile h7, by depth below 30d high quartile (0 deepest)"] = p7d.groupby("dbin").apply(summ).join(p7d.groupby("dbin")["dist"].mean().rename("dist_mean"))
    out["in profile h7, by coin and sign of 7d move"] = p7.assign(up=p7.r7 > 0).groupby(["coin", "up"]).apply(summ)
    out["in profile h7, by year and sign"] = p7.assign(up=p7.r7 > 0).groupby(["yr", "up"]).apply(summ)
    out["corr sc vs un, in profile, by h"] = p.dropna(subset=["sc"]).groupby("h").apply(lambda g: pd.Series(dict(rho=stats.spearmanr(g.sc, g.un)[0], n=len(g))))
    out["out of profile h7 by sign"] = df[(~df.inprof) & (df.h == 7)].assign(up=lambda x: x.r7 > 0).groupby("up").apply(summ)
    return out
