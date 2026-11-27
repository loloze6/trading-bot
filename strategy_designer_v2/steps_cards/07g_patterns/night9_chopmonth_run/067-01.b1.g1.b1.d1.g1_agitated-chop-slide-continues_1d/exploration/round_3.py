def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allret = []
        for w, df in wins.items():
            c = df["close"].reset_index(drop=True)
            allret += list((c.shift(-10) / c - 1).iloc[::10].dropna())
        drift = np.mean(allret); sd10 = np.std(allret, ddof=1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            r30 = c / c.shift(30) - 1
            r60 = c / c.shift(60) - 1
            f10 = c.shift(-10) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, len(df), 10):
                if pd.isna(f10.iloc[i]) or pd.isna(r60.iloc[i]) or pd.isna(r30.iloc[i]):
                    continue
                rows.append(dict(coin=coin, w=w, r30=r30.iloc[i], r60=r60.iloc[i],
                                 z30=r30.iloc[i] / (vol30.iloc[i] * np.sqrt(30)),
                                 ag=df["regime"].iloc[i] == "unknown",
                                 ex=f10.iloc[i] - drift, s=(f10.iloc[i] - drift) / sd10,
                                 day=ts.iloc[i].strftime("%Y-%m-%d"), yr=ts.iloc[i].year, wn=w))
    g = pd.DataFrame(rows)
    def ct(s, col="ex"):
        dev = s[col] - s[col].mean()
        gg = dev.groupby(s.day).sum()
        se = np.sqrt((gg ** 2).sum()) / len(s)
        return pd.Series(dict(n=len(s), days=s.day.nunique(), mean=s[col].mean(),
                              t=s[col].mean() / se if se > 0 else np.nan))
    out = {}
    ch = g[g.r60.abs() <= 0.10].copy()
    ch["sgn"] = np.sign(ch.r30)
    ch["dirx"] = ch.sgn * ch.ex
    out["choppy: direction-signed excess, all"] = ct(ch, "dirx")
    res = []
    for k, s in ch.groupby(ch.r30 < 0):
        r = ct(s, "dirx"); r["fall"] = k; res.append(r)
    for k, s in ch.groupby("ag"):
        r = ct(s, "dirx"); r["agit_regime"] = k; res.append(r)
    out["choppy dirx by side and by agit"] = pd.DataFrame(res)
    ch["zq"] = pd.qcut(ch.z30, 4, labels=False)
    res = []
    for q, s in ch.groupby("zq"):
        r = ct(s); r["zq"] = q; r["z"] = s.z30.mean(); res.append(r)
    out["choppy: excess by z30 quartile"] = pd.DataFrame(res)
    res = []
    for y, s in ch.groupby("yr"):
        r = ct(s, "dirx"); r["yr"] = y; res.append(r)
    out["choppy dirx by year"] = pd.DataFrame(res)
    out["choppy dirx by coin"] = ch.groupby("coin").dirx.agg(["size", "mean"])
    out["choppy corr z30 vs ex"] = pd.Series({"pearson": ch.z30.corr(ch.ex),
        "spearman": ch.z30.corr(ch.ex, method="spearman"), "n": len(ch)})
    nc = g[g.r60.abs() > 0.10].copy()
    nc["dirx"] = np.sign(nc.r30) * nc.ex
    out["not choppy dirx"] = ct(nc, "dirx")
    return out
