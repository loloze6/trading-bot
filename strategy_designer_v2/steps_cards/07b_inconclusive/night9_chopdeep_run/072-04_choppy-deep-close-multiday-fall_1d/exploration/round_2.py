def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    drift = {}
    for coin, ws in bars.items():
        for h in (3, 5, 10):
            rets = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rets += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rets)
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]
            r = c.pct_change()
            sd = r.rolling(20).std()
            mh = hi.rolling(20).max()
            depth = (c - mh) / mh / sd
            chop = b["regime"].astype(str) == "unknown"
            n = len(b)
            for h in (3, 5, 10):
                idx = np.arange(0, n - h, h)
                fr = c.values[idx + h] / c.values[idx] - 1 - drift[(coin, h)]
                ts = pd.to_datetime(b["timestamp"].values[idx])
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "day": ts.floor("D"), "year": ts.year,
                                          "depth": depth.values[idx], "fc": b["forecast"].values[idx],
                                          "chop": chop.values[idx], "ex": fr}))
    D = pd.concat(rows).dropna(subset=["depth", "ex"])
    def slope(d, x):
        d = d.dropna(subset=[x])
        if len(d) < 30: return pd.Series({"n": len(d)})
        X = d[x].values; y = d["ex"].values
        Xc = X - X.mean(); b1 = (Xc * (y - y.mean())).sum() / (Xc ** 2).sum()
        e = y - y.mean() - b1 * Xc
        g = pd.DataFrame({"s": Xc * e, "d": d["day"].values}).groupby("d")["s"].sum()
        se = np.sqrt((g ** 2).sum()) / (Xc ** 2).sum()
        return pd.Series({"n": len(d), "slope": b1, "t": b1 / se})
    def dmean(d):
        g = d.groupby("day")["ex"].sum(); m = d["ex"].mean()
        dev = d.groupby("day")["ex"].apply(lambda x: (x - m).sum())
        se = np.sqrt((dev ** 2).sum()) / len(d)
        return pd.Series({"n": len(d), "days": d["day"].nunique(), "mean_ex": m, "t_day": m / se})
    out = {}
    ch = D[D.chop & (D.depth < 0)].copy()
    chf = ch[ch.fc < 0]
    out["slope_on_forecast_by_h"] = chf.groupby("h").apply(lambda d: slope(d, "fc"))
    out["slope_on_depth_fc_nonzero_by_h"] = chf.groupby("h").apply(lambda d: slope(d, "depth"))
    out["corr_fc_depth"] = float(chf[["fc", "depth"]].corr().iloc[0, 1])
    res = {}
    for h in (3, 5, 10):
        cc = ch[ch.h == h].copy(); cc["q"] = pd.qcut(cc.depth, 5, labels=False)
        out[f"h{h}_quintile_day_t"] = cc.groupby("q").apply(dmean)
        deep = cc[cc.q == 0]
        out[f"h{h}_deepest_by_year"] = deep.groupby("year").apply(lambda d: pd.Series({"n": len(d), "mean_ex": d.ex.mean()}))
        out[f"h{h}_deepest_by_coin"] = deep.groupby("coin").apply(lambda d: pd.Series({"n": len(d), "mean_ex": d.ex.mean()}))
    c10 = ch[ch.h == 10]
    out["h10_slope_by_year"] = c10.groupby("year").apply(lambda d: slope(d, "depth"))
    out["h10_slope_by_coin"] = c10.groupby("coin").apply(lambda d: slope(d, "depth"))
    return out
