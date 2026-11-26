def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def coin_mean(coin, h):
        rs = []
        for w, df in bars[coin].items():
            c = df["close"].values
            idx = np.arange(0, len(c) - h, h)
            rs += list(c[idx + h] / c[idx] - 1)
        return np.mean(rs) if rs else np.nan
    rows = []
    for coin in bars:
        means = {h: coin_mean(coin, h) for h in (7, 14, 28)}
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for i in range(0, n - 14, 14):
                if not (f[i] > 0):
                    continue
                r14p = c[i] / c[i - 14] - 1 if i >= 14 else np.nan
                vr = v[max(0, i - 13):i + 1].mean() / v[max(0, i - 29):i + 1].mean() - 1
                rec = dict(coin=coin, window=w, year=ts[i].year, day=ts[i].normalize(),
                           f=f[i], r14p=r14p, vr=vr)
                for h in (7, 14, 28):
                    rec[f"x{h}"] = (c[i + h] / c[i] - 1 - means[h]) if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def clt(x, w=None, days=None):
        x = np.asarray(x, float)
        w = np.ones_like(x) if w is None else np.asarray(w, float)
        m = np.sum(w * x) / np.sum(w)
        dev = pd.Series(w * (x - m)).groupby(np.asarray(days)).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / np.sum(w) if G > 1 else np.nan
        return m, m / se, len(x), G
    def summ(g, col="x14"):
        g = g.dropna(subset=[col])
        if len(g) < 3:
            return pd.Series(dict(mean=np.nan, t=np.nan, n=len(g), days=np.nan))
        m, t, n, G = clt(g[col], None, g["day"])
        return pd.Series(dict(mean=m, t=t, n=n, days=G))
    tot = {}
    for h in (7, 14, 28):
        g = d.dropna(subset=[f"x{h}"])
        m, t, n, G = clt(g[f"x{h}"], g["f"], g["day"])
        mu, tu, _, _ = clt(g[f"x{h}"], None, g["day"])
        tot[h] = dict(wmean=m, wt=t, mean=mu, t=tu, n=n, days=G)
    out["by horizon"] = pd.DataFrame(tot).T
    out["by year"] = d.groupby("year").apply(summ)
    out["by coin"] = d.groupby("coin").apply(summ)
    d["fq"] = pd.qcut(d["f"], 4, labels=False, duplicates="drop")
    out["by forecast quartile"] = d.groupby("fq").apply(summ)
    d["rq"] = pd.qcut(d["r14p"], 4, labels=False, duplicates="drop")
    out["by past 14d return quartile"] = d.groupby("rq").apply(summ)
    out["rq bounds"] = d.groupby("rq")["r14p"].agg(["min", "max"])
    d["vq"] = pd.qcut(d["vr"], 4, labels=False, duplicates="drop")
    out["by volume ratio quartile"] = d.groupby("vq").apply(summ)
    d["big"] = d["coin"].isin(["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD", "XRPUSD", "ZECUSD"])
    out["default vs other coins"] = d.groupby("big").apply(summ)
    out["spearman f vs x14"] = stats.spearmanr(d["f"], d["x14"], nan_policy="omit")[0]
    out["spearman r14p vs x14"] = stats.spearmanr(d["r14p"], d["x14"], nan_policy="omit")[0]
    return out
