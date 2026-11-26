def explore(data):
    import numpy as np, pandas as pd
    rows = []
    bars = data["bars"]
    for coin in bars:
        allg = {1: [], 3: [], 5: []}
        for w, b in bars[coin].items():
            c = b["close"].values
            for h in allg:
                idx = np.arange(0, len(c) - h, h)
                allg[h].append(c[idx + h] / c[idx] - 1)
        st = {h: (np.concatenate(v).mean(), np.concatenate(v).std()) for h, v in allg.items() if len(np.concatenate(v)) > 10}
        if len(st) < 3:
            continue
        d1 = np.concatenate([b["close"].pct_change().values[1:] for b in bars[coin].values()])
        sd1 = np.nanstd(d1)
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            o, h_, l, c = b["open"], b["high"], b["low"], b["close"]
            rng = h_ - l
            mult = rng / rng.rolling(20).mean()
            r1 = c / c.shift(1) - 1
            volr = rng.rolling(20).mean() / c
            volr_rel = volr / volr.rolling(60, min_periods=20).mean()
            past5 = c.shift(1) / c.shift(6) - 1
            loc = (c - l) / rng.replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for H in (1, 3, 5):
                fwd = c.shift(-H) / c - 1
                for i in range(0, n - H, H):
                    rows.append(dict(H=H, coin=coin, win=w, day=ts.iloc[i].floor("D"), yr=ts.iloc[i].year,
                                     r1z=r1.iloc[i] / sd1, volrel=volr_rel.iloc[i], mult=mult.iloc[i],
                                     past5=past5.iloc[i], loc=loc.iloc[i],
                                     str=(fwd.iloc[i] - st[H][0]) / st[H][1]))
    df = pd.DataFrame(rows).dropna(subset=["str", "r1z", "volrel"])

    def ct(g, col="str"):
        g = g.dropna(subset=[col])
        if len(g) < 5:
            return pd.Series(dict(n=len(g), days=0, mean=np.nan, t=np.nan))
        s = g.groupby("day")[col].agg(["sum", "count"])
        m = s["sum"].sum() / s["count"].sum()
        D = len(s)
        se = np.sqrt(((s["sum"] - s["count"] * m) ** 2).sum() * D / max(D - 1, 1)) / s["count"].sum()
        return pd.Series(dict(n=len(g), days=D, mean=m, t=m / se if se > 0 else np.nan))

    out = {}
    df["rev"] = -np.sign(df.r1z) * df["str"]  # move against the day's direction, in usual moves
    df["vq"] = pd.qcut(df.volrel, 5, labels=["v1", "v2", "v3", "v4", "v5"])
    out["reversal by H x volq"] = df.groupby(["H", "vq"]).apply(lambda g: ct(g, "rev"))
    d3 = df[df.H == 3].copy()
    d3["absr"] = pd.qcut(d3.r1z.abs(), 4, labels=["a1", "a2", "a3", "a4"])
    hv = d3[d3.volrel >= d3.volrel.quantile(0.8)]
    out["H3 high vol: reversal by |r1| quartile"] = hv.groupby("absr").apply(lambda g: ct(g, "rev"))
    out["H3 high vol: reversal by year"] = hv.groupby("yr").apply(lambda g: ct(g, "rev"))
    out["H3 high vol: reversal by sign of day"] = hv.groupby(np.sign(hv.r1z)).apply(lambda g: ct(g, "rev"))
    d3["volt"] = pd.qcut(d3.volrel, 3, labels=["low", "mid", "high"])
    d3["sig"] = d3.r1z.clip(-4, 4)
    res = {}
    for k, g in d3.groupby("volt"):
        x = g.sig.values; y = g["str"].values
        res[k] = np.polyfit(x, y, 1)[0]
    out["H3 slope of str on 1d z by vol tercile"] = pd.Series(res)
    hv2 = hv.copy(); hv2["coin_grp"] = np.where(hv2.coin.isin(["BTCUSD", "ETHUSD", "LTCUSD", "XRPUSD", "XMRUSD", "ZECUSD"]), "old", "other")
    out["H3 high vol: reversal by coin group"] = hv2.groupby("coin_grp").apply(lambda g: ct(g, "rev"))
    rw = d3[(d3.past5 > 0) & (d3.mult >= 2)]
    out["H3 rise5 & mult>=2: str by year"] = rw.groupby("yr").apply(ct)
    out["H3 rise5 & mult>=2: str by loc half"] = rw.groupby(rw["loc"] >= 0.5).apply(ct)
    return out
