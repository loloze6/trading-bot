def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        # mean hourly return pooled over windows
        rets = []
        for w, b in wins.items():
            c = b["close"].values
            rets.append(c[1:] / c[:-1] - 1)
        mu = np.nanmean(np.concatenate(rets))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            day = ts.dt.floor("D")
            f = b["forecast"].values
            c = b["close"].values
            n = len(b)
            prev = np.r_[np.nan, f[:-1]]
            cross = (f <= -2) & (prev > -2)
            dser = pd.Series(day)
            last_idx = dser.groupby(dser).transform(lambda s: s.index[-1]).values
            seen = set()
            for i in np.where(cross)[0]:
                d = day.iloc[i]
                if d in seen:
                    continue
                seen.add(d)
                j = int(last_idx[i])
                hrs = j - i
                r = {}
                r["eod"] = -(c[j] / c[i] - 1) + mu * hrs
                for h in (1, 4, 24, 72, 168):
                    if i + h < n:
                        r["h%d" % h] = -(c[i + h] / c[i] - 1) + mu * h
                    else:
                        r["h%d" % h] = np.nan
                # 30 day trend of coin before signal
                r["tr30"] = c[i] / c[i - 720] - 1 if i >= 720 else np.nan
                r.update(coin=coin, win=w, f=f[i], hour=ts.iloc[i].hour, hrs=hrs,
                         year=ts.iloc[i].year)
                rows.append(r)
    df = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for k in ["eod", "h1", "h4", "h24", "h72", "h168"]:
            x = g[k].dropna()
            out[k + "_bp"] = x.mean() * 1e4
            out[k + "_t"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["n"] = len(g)
        return pd.Series(out)
    df["fb"] = pd.cut(df["f"], [-20.01, -19.99, -10, -5, -2])
    df["hb"] = pd.cut(df["hour"], [-1, 5, 11, 17, 23])
    df["trb"] = pd.qcut(df["tr30"], 3, labels=["down", "mid", "up"])
    return {
        "all": summ(df).to_frame().T,
        "by_f": df.groupby("fb", observed=True).apply(summ),
        "by_coin": df.groupby("coin").apply(summ),
        "by_year": df.groupby("year").apply(summ),
        "by_hour": df.groupby("hb", observed=True).apply(summ),
        "by_trend30": df.groupby("trb", observed=True).apply(summ),
    }
