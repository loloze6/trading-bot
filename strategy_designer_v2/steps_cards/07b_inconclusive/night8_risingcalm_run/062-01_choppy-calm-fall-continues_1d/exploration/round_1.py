def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    # drift per coin over all windows, per horizon
    H = [1, 3, 5, 10, 20]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            f = df["forecast"].values
            reg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"])
            r = pd.Series(cl).pct_change()
            sd30 = r.rolling(30).std().values
            r5 = pd.Series(cl).pct_change(5).values
            for h in H:
                for i in range(0, len(cl) - h, h):
                    rows.append(dict(coin=c, win=w, year=ts.iloc[i].year, h=h,
                                     f=f[i], reg=reg[i], z=r5[i] / sd30[i] if sd30[i] > 0 else np.nan,
                                     ret=cl[i + h] / cl[i] - 1 - drift[(c, h)],
                                     day=ts.iloc[i].normalize()))
    d = pd.DataFrame(rows)
    def tclust(s):
        g = s.groupby(s["day"])["x"].sum()
        n = len(s); G = len(g)
        if G < 3: return np.nan
        m = s["x"].mean()
        se = np.sqrt((g - g.mean() * 0).pow(2).sum() * 0 + ((s.groupby("day")["x"].sum() - s.groupby("day")["x"].count() * m) ** 2).sum() * G / (G - 1)) / n
        return m / se
    def summ(sub):
        sub = sub.copy()
        return pd.Series(dict(n=len(sub), days=sub["day"].nunique(),
                              mean=sub["x"].mean(), t=tclust(sub)))
    out = {}
    # short side cases, all horizons
    cs = d[(d["f"] < 0)].copy(); cs["x"] = -cs["ret"]
    out["short cases by horizon"] = cs.groupby("h").apply(summ)
    c5 = cs[cs.h == 5]
    out["h5 short by coin"] = c5.groupby("coin").apply(summ)
    out["h5 short by year"] = c5.groupby("year").apply(summ)
    out["h5 short by window"] = c5.groupby("win").apply(summ)
    c5 = c5.copy(); c5["q"] = pd.qcut(c5["f"].abs(), 4, labels=False, duplicates="drop")
    out["h5 short by |f| quartile"] = c5.groupby("q").apply(summ)
    # in-profile rises (long side, mirror): regime unknown, f==0, z>0
    lp = d[(d.reg == "unknown") & (d.z > 0)].copy(); lp["x"] = lp["ret"]
    out["in-profile rises, long excess by horizon"] = lp.groupby("h").apply(summ)
    # all in-profile bars: z quartile vs 5d excess (raw)
    ip = d[(d.reg == "unknown") & (d.h == 5)].dropna(subset=["z"]).copy(); ip["x"] = ip["ret"]
    ip["zq"] = pd.qcut(ip["z"], 5, labels=False)
    out["in-profile h5 raw excess by z quintile"] = ip.groupby("zq").apply(summ)
    out["regime counts"] = d[d.h == 1]["reg"].value_counts()
    return out
