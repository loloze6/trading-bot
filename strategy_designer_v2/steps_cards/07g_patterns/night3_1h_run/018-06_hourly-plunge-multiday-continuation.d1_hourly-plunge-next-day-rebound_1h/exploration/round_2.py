def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for coin in bars:
        wins = list(bars[coin].keys())
        for wi, w in enumerate(wins):
            df = bars[coin][w]
            c = df["close"].astype(float).reset_index(drop=True)
            n = len(c)
            r24 = c / c.shift(24) - 1
            z = r24 / r24.abs().rolling(720, min_periods=120).mean().shift(1)
            hi = c.rolling(720, min_periods=240).max(); lo = c.rolling(720, min_periods=240).min()
            pos = (c - lo) / (hi - lo)
            lr = np.log(c).diff()
            vr = lr.rolling(24).std() / lr.rolling(720, min_periods=240).std()
            for h in (24, 72, 168):
                idx = np.arange(0, n - h, h)
                f = c.values[idx + h] / c.values[idx] - 1
                rows.append(pd.DataFrame({"coin": coin, "w": w, "half": int(wi >= len(wins) / 2), "h": h,
                                          "z": z.values[idx], "pos": pos.values[idx], "vr": vr.values[idx],
                                          "r24": r24.values[idx], "f": f}))
    R = pd.concat(rows, ignore_index=True)
    g = R.groupby(["coin", "h"])["f"]
    R["drift"] = g.transform("mean"); R["sd"] = g.transform("std")
    R["s"] = (R["f"] - R["drift"]) / R["sd"]
    def summ(d):
        m = d.s.mean(); n = len(d)
        return pd.Series({"mean_s": m, "n": n, "t": m / (d.s.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "unusual_pct": (d.f - d.drift).mean() * 100, "total_pct": d.f.mean() * 100})
    d24 = R[(R.h == 24)].dropna(subset=["z"])
    deep = d24[d24.z <= -3]
    out["deep drop 24h by coin"] = deep.groupby("coin").apply(summ).round(3)
    out["deep drop 24h by half"] = deep.groupby("half").apply(summ).round(3)
    out["deep drop 24h by vr tercile"] = deep.groupby(pd.qcut(deep.vr, 3, labels=False)).apply(summ).round(3)
    dd = d24[d24.z < 0]
    out["drop z vs strength spearman (drops only)"] = pd.Series(
        {c: stats.spearmanr(-x.z, x.s)[0] for c, x in dd.groupby("coin")}).round(3)
    out["drop z finer"] = dd.groupby(pd.cut(dd.z, [-99, -5, -4, -3, -2.5, -2, -1.5, -1, 0])).apply(summ).round(3)
    d168 = R[(R.h == 168)].dropna(subset=["pos"])
    hi = d168[d168.pos > 0.9]
    out["near high 168h by coin"] = hi.groupby("coin").apply(summ).round(3)
    out["near high 168h by half"] = hi.groupby("half").apply(summ).round(3)
    out["pos spearman 168h by coin"] = pd.Series(
        {c: stats.spearmanr(x.pos, x.s)[0] for c, x in d168.groupby("coin")}).round(3)
    d72 = R[(R.h == 72)].dropna(subset=["vr", "r24"])
    d72 = d72.assign(sv=np.sign(d72.r24) * d72.vr)
    out["vr 72h by coin (vr>1.5)"] = d72[d72.vr > 1.5].groupby("coin").apply(summ).round(3)
    out["vr>1.5 72h by sign of r24"] = d72[d72.vr > 1.5].groupby(np.sign(d72.r24)).apply(summ).round(3)
    out["vr spearman 72h by coin"] = pd.Series(
        {c: stats.spearmanr(x.vr, x.s)[0] for c, x in d72.groupby("coin")}).round(3)
    return out
