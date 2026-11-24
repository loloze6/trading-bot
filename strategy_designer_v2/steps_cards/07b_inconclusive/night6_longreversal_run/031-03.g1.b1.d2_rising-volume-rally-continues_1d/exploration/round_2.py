def explore(data):
    import numpy as np, pandas as pd
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
        m14 = coin_mean(coin, 14)
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].values
            hi = df["high"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for i in range(0, n - 14, 14):
                if not (f[i] > 0):
                    continue
                rec = dict(coin=coin, window=w, year=ts[i].year, day=ts[i].normalize(), f=f[i],
                           x14=c[i + 14] / c[i] - 1 - m14,
                           r30=c[i] / c[i - 30] - 1 if i >= 30 else np.nan,
                           r60=c[i] / c[i - 60] - 1 if i >= 60 else np.nan,
                           dd=c[i] / hi[max(0, i - 29):i + 1].max() - 1)
                rows.append(rec)
    d = pd.DataFrame(rows)
    def clt(x, w, days):
        x = np.asarray(x, float); w = np.asarray(w, float)
        m = np.sum(w * x) / np.sum(w)
        dev = pd.Series(w * (x - m)).groupby(np.asarray(days)).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / np.sum(w) if G > 1 else np.nan
        return m, m / se, len(x), G
    def summ(g):
        g = g.dropna(subset=["x14"])
        if len(g) < 3:
            return pd.Series(dict(wmean=np.nan, wt=np.nan, n=len(g), days=np.nan))
        m, t, n, G = clt(g["x14"], g["f"], g["day"])
        return pd.Series(dict(wmean=m, wt=t, n=n, days=G))
    out["all"] = summ(d)
    d["r30pos"] = np.where(d["r30"].isna(), "na", np.where(d["r30"] > 0, "up", "down"))
    out["by 30d return sign"] = d.groupby("r30pos").apply(summ)
    d["r60pos"] = np.where(d["r60"].isna(), "na", np.where(d["r60"] > 0, "up", "down"))
    out["by 60d return sign"] = d.groupby("r60pos").apply(summ)
    d["r30q"] = pd.qcut(d["r30"], 4, labels=False, duplicates="drop")
    out["by 30d return quartile"] = d.groupby("r30q").apply(summ)
    out["r30q bounds"] = d.groupby("r30q")["r30"].agg(["min", "max"])
    d["ddq"] = pd.qcut(d["dd"], 4, labels=False, duplicates="drop")
    out["by distance to 30d high quartile"] = d.groupby("ddq").apply(summ)
    out["ddq bounds"] = d.groupby("ddq")["dd"].agg(["min", "max"])
    # market breadth: share of coins on the same day with positive 14d forward? no - use same-day count of cases
    cnt = d.groupby("day")["coin"].transform("count")
    d["crowd"] = pd.cut(cnt, [0, 2, 5, 100], labels=["1-2", "3-5", "6+"])
    out["by cases same day"] = d.groupby("crowd").apply(summ)
    return out
