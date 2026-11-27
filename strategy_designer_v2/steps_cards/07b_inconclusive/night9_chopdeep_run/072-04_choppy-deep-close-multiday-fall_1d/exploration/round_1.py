def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for h in (1, 3, 5, 10):
            rets = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rets += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rets)
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]
            r = c.pct_change()
            sd = r.rolling(20).std()
            mh = hi.rolling(20).max()
            depth = (c - mh) / mh / sd
            ret60 = c / c.shift(60) - 1
            vol30 = r.rolling(30).std()
            ag = vol30.rolling(365, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            chop = b["regime"].astype(str) == "unknown"
            n = len(b)
            for h in (1, 3, 5, 10):
                idx = np.arange(0, n - h, h)
                fr = c.values[idx + h] / c.values[idx] - 1 - drift[(coin, h)]
                df = pd.DataFrame({"coin": coin, "w": w, "h": h, "pos": idx,
                                   "day": pd.to_datetime(b["timestamp"].values[idx]).floor("D"),
                                   "year": pd.to_datetime(b["timestamp"].values[idx]).year,
                                   "depth": depth.values[idx], "fc": b["forecast"].values[idx],
                                   "chop": chop.values[idx], "up": (r.values[idx] > 0),
                                   "ag": ag.values[idx], "ret60": ret60.values[idx], "ex": fr})
                rows.append(df)
    D = pd.concat(rows).dropna(subset=["depth", "ex"])
    def slope(d, x="depth"):
        d = d.dropna(subset=[x])
        if len(d) < 30: return pd.Series({"n": len(d)})
        X = d[x].values; y = d["ex"].values
        Xc = X - X.mean(); b1 = (Xc * (y - y.mean())).sum() / (Xc ** 2).sum()
        e = y - y.mean() - b1 * Xc
        g = pd.DataFrame({"s": Xc * e, "d": d["day"].values}).groupby("d")["s"].sum()
        se = np.sqrt((g ** 2).sum()) / (Xc ** 2).sum()
        return pd.Series({"n": len(d), "slope": b1, "t": b1 / se, "mean_ex": y.mean()})
    out = {}
    ch = D[D.chop & (D.depth < 0)]
    out["by_h_chop"] = ch.groupby("h").apply(slope)
    out["by_h_all"] = D[D.depth < 0].groupby("h").apply(slope)
    out["by_h_notchop"] = D[(~D.chop) & (D.depth < 0)].groupby("h").apply(slope)
    c3 = ch[ch.h == 3].copy(); c1 = ch[ch.h == 1].copy()
    out["h3_by_coin"] = c3.groupby("coin").apply(slope)
    out["h3_by_year"] = c3.groupby("year").apply(slope)
    out["h3_by_up"] = c3.groupby("up").apply(slope)
    out["h1_by_up"] = c1.groupby("up").apply(slope)
    c3["agit"] = c3.ag > 0.5
    out["h3_by_agit"] = c3.dropna(subset=["ag"]).groupby("agit").apply(slope)
    c1["agit"] = c1.ag > 0.5
    out["h1_by_agit"] = c1.dropna(subset=["ag"]).groupby("agit").apply(slope)
    for h, cc in ((1, c1), (3, c3)):
        cc = cc.copy(); cc["q"] = pd.qcut(cc.depth, 5, labels=False)
        out[f"h{h}_quintile"] = cc.groupby("q").agg(n=("ex", "size"), depth=("depth", "mean"),
                                                    ex=("ex", "mean"), t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    return out
