def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    drows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            vol90 = r1.rolling(90, min_periods=60).std()
            r60 = c / c.shift(60) - 1
            n1 = r1.shift(-1)
            n3 = c.shift(-3) / c - 1
            z1 = r1 / vol30.shift(1)
            clpos = (c - df["low"]) / (df["high"] - df["low"]).replace(0, np.nan)
            ts = pd.to_datetime(df["timestamp"])
            trend = np.where(r60 > 0.10, "rising", np.where(r60 < -0.10, "falling", "choppy"))
            trend = pd.Series(trend).where(r60.notna())
            agit = np.where(vol30 / vol90 > 1, "agit", "calm")
            agit = pd.Series(agit).where((vol30 / vol90).notna())
            drows.append(pd.DataFrame(dict(coin=coin, w=w, z1=z1, n1=n1, n3=n3, clpos=clpos,
                inprof=(df["regime"] == "unknown"), trend=trend, agit=agit,
                wd=ts.dt.weekday, day=ts.dt.strftime("%Y-%m-%d"), yr=ts.dt.year)))
    d = pd.concat(drows).dropna(subset=["n1", "z1"])
    # coin drift per day
    drift = d.groupby("coin").n1.transform("mean")
    d["ex1"] = d.n1 - drift
    def ct(s, col):
        s = s.dropna(subset=[col])
        dev = s[col] - s[col].mean()
        g = dev.groupby(s.day).sum()
        se = np.sqrt((g ** 2).sum()) / len(s)
        return pd.Series(dict(n=len(s), days=s.day.nunique(), mean=s[col].mean(), t_clust=s[col].mean() / se if se > 0 else np.nan))
    out = {}
    d["zq"] = pd.qcut(d.z1, 5, labels=False)
    res = []
    for (tr, ag, q), s in d.groupby(["trend", "agit", "zq"]):
        if q in (0, 4):
            r = ct(s, "ex1"); r["trend"] = tr; r["agit"] = ag; r["zq"] = q; res.append(r)
    out["next-day excess by z1 extreme quintile, by trend x agit proxy"] = pd.DataFrame(res)
    res = []
    for (tr, q), s in d.groupby(["trend", "zq"]):
        r = ct(s, "ex1"); r["trend"] = tr; r["zq"] = q; res.append(r)
    out["next-day excess by z1 quintile, by trend"] = pd.DataFrame(res)
    res = []
    for y, s in d[d.zq == 0].groupby("yr"):
        r = ct(s, "ex1"); r["yr"] = y; res.append(r)
    out["big down day next-day excess by year"] = pd.DataFrame(res)
    res = []
    for wd, s in d.groupby("wd"):
        r = ct(s, "ex1"); r["wd"] = wd; res.append(r)
    out["weekday next-day excess clustered"] = pd.DataFrame(res)
    res = []
    for (tr, wd), s in d.groupby(["trend", "wd"]):
        if wd in (3, 4):
            r = ct(s, "ex1"); r["trend"] = tr; r["wd"] = wd; res.append(r)
    out["thu/fri next-day by trend"] = pd.DataFrame(res)
    # up big day in choppy agitated -> short?
    s = d[(d.trend == "choppy") & (d.agit == "agit")]
    s = s.copy(); s["zq2"] = pd.qcut(s.z1, 5, labels=False)
    res = []
    for q, ss in s.groupby("zq2"):
        r = ct(ss, "ex1"); r["zq"] = q; r["z"] = ss.z1.mean(); res.append(r)
    out["choppy agitated proxy: next-day excess by z1 quintile"] = pd.DataFrame(res)
    return out
