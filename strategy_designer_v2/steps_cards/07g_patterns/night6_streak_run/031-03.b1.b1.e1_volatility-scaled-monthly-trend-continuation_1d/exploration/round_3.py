def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = pd.Series(c).pct_change()
            vol60 = r1.rolling(60, min_periods=20).std().values
            r1 = r1.values
            ts = pd.to_datetime(b["timestamp"])
            raw = b.get("debug_info.components.vol_scaled_mom.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            for i in range(1, n):
                volp = vol60[i-1]
                rows.append(dict(coin=coin, w=w, i=i, day=ts[i].normalize(), yr=ts[i].year,
                                 z=r1[i]/volp if volp and volp > 0 else np.nan,
                                 f3=c[i+3]/c[i]-1 if i+3 < n else np.nan,
                                 f10=c[i+10]/c[i]-1 if i+10 < n else np.nan,
                                 vol=vol60[i], raw=raw[i]))
    d = pd.DataFrame(rows)
    d["vt"] = d.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))

    def slope(df, x, y):
        dd = df.dropna(subset=[x, y])
        if len(dd) < 30: return dict(n=len(dd), slope=np.nan, t=np.nan, days=0)
        X = dd[x] - dd[x].mean(); Y = dd[y]
        b = (X * Y).sum() / (X**2).sum()
        a = Y.mean() - b * dd[x].mean()
        e = Y - a - b * dd[x]
        s = (X * e).groupby(dd["day"]).sum()
        se = np.sqrt((s**2).sum()) / (X**2).sum()
        return dict(n=len(dd), slope=b, t=b/se, days=dd["day"].nunique())

    res = {}
    # 1: graded reversal after down days, 3-day horizon, on three grid offsets
    out = []
    for off in [0, 1, 2]:
        g = d[(d.i % 3) == off].copy()
        g["x3"] = g["f3"] - g.groupby("coin")["f3"].transform("mean")
        g["zdn"] = g["z"].clip(upper=0)
        g["zup"] = g["z"].clip(lower=0)
        r = slope(g, "zdn", "x3"); r["key"] = f"off{off}_zdn"; out.append(r)
        r = slope(g, "zup", "x3"); r["key"] = f"off{off}_zup"; out.append(r)
    res["3d excess on down-z / up-z, by grid offset"] = pd.DataFrame(out)
    # 2: 10d excess on raw ratio by vol tercile and sign, grid offsets 0 and 5
    out = []
    for off in [0, 5]:
        g = d[(d.i % 10) == off].copy()
        g["x10"] = g["f10"] - g.groupby("coin")["f10"].transform("mean")
        for vt in [0, 1, 2]:
            r = slope(g[g.vt == vt], "raw", "x10"); r["key"] = f"off{off}_vt{vt}"; out.append(r)
        r = slope(g[g.raw > 0], "raw", "x10"); r["key"] = f"off{off}_raw>0"; out.append(r)
        r = slope(g[g.raw <= 0], "raw", "x10"); r["key"] = f"off{off}_raw<=0"; out.append(r)
        r = slope(g, "raw", "x10"); r["key"] = f"off{off}_all"; out.append(r)
    res["10d excess on raw ratio, by vol tercile / sign"] = pd.DataFrame(out)
    # 3: book's extreme days: coin's own preceding move
    dr = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.reset_index(drop=True)
            t["prev"] = t["coin_return"].shift(1)
            t["prev5"] = (1 + t["coin_return"]).rolling(5).apply(np.prod, raw=True).shift(1) - 1
            dr.append(t.assign(coin=coin))
    D = pd.concat(dr).dropna(subset=["book_return"])
    D["bq"] = pd.qcut(D["book_return"].rank(method="first"), 20, labels=False)
    res["book day ventile -> coin same/prev/prev5"] = D[D.bq.isin([0, 1, 18, 19])].groupby("bq")[["book_return", "coin_return", "prev", "prev5"]].mean()
    return res
