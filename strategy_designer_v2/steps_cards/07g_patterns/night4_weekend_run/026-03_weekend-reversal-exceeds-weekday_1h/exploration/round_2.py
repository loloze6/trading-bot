def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; out = {}
    hrs = []; rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values.astype(float); n = len(c)
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            # bar's own return (open-to-close of bar starting at ts), label by start hour
            rb = np.r_[np.nan, c[1:]/c[:-1]-1]
            hrs.append(pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year.values, "h": ts.dt.hour.values,
                                     "wd": ts.dt.weekday.values, "rb": rb}))
            close_ts = ts + pd.Timedelta(hours=1)
            idx = np.where(close_ts.dt.hour.values == 0)[0]
            idx = idx[(idx >= 24) & (idx + 24 < n)]
            lr = np.diff(np.log(c))
            for i in idx:
                vol = np.std(lr[max(0, i-24*7):i]) if i > 48 else np.nan
                rows.append((coin, w, ts.dt.year.values[i], c[i]/c[i-24]-1, c[i+24]/c[i]-1, vol))
    h = pd.concat(hrs).dropna(subset=["rb"])
    h["b2122"] = h.h.isin([21, 22])
    # per coin: mean of bars starting 21,22 UTC (closing 22,23) vs others
    res = []
    for coin, g in h.groupby("coin"):
        a = g[g.b2122].rb; b = g[~g.b2122].rb
        from scipy import stats
        t = stats.ttest_ind(a, b, equal_var=False).statistic
        res.append((coin, len(a), a.mean()*1e4, b.mean()*1e4, t))
    out["bars 21-22h start: per coin (bp)"] = pd.DataFrame(res, columns=["coin","n","mean_2122","mean_other","welch_t"])
    # by year, pooled coins: daily sum of hours 21-22 per coin-day
    h["day"] = h.groupby(["coin","w"]).cumcount() // 24
    res = []
    for y, g in h[h.b2122].groupby("year"):
        res.append((y, len(g), g.rb.mean()*1e4, g.rb.mean()/(g.rb.std()/np.sqrt(len(g)))))
    out["bars 21-22h by year"] = pd.DataFrame(res, columns=["year","n","mean_bp","t"])
    res = []
    for wd, g in h[h.b2122].groupby("wd"):
        res.append((wd, len(g), g.rb.mean()*1e4, g.rb.mean()/(g.rb.std()/np.sqrt(len(g)))))
    out["bars 21-22h by weekday"] = pd.DataFrame(res, columns=["wd","n","mean_bp","t"])
    # one series per timestamp: average over coins to remove cross-coin dependence
    hh = pd.concat(hrs).dropna(subset=["rb"])
    hh["key"] = hh.w + "_" + hh.groupby(["coin","w"]).cumcount().astype(str)
    m = hh.groupby(["w","year","h","wd"]).rb  # not used
    # per-coin hour profile t for hour 21, 22, 14, 3 start
    res = []
    for coin, g in h.groupby("coin"):
        row = [coin]
        for hr in [2, 13, 20, 21]:
            x = g[g.h == hr].rb
            row.append(x.mean()/(x.std()/np.sqrt(len(x))))
        res.append(row)
    out["per coin t by bar start hour (2,13,20,21)"] = pd.DataFrame(res, columns=["coin","t_h2","t_h13","t_h20","t_h21"])
    # 24h reversal on non-overlapping daily grid
    d = pd.DataFrame(rows, columns=["coin","w","year","p24","f24","vol"]).dropna()
    d["volq"] = d.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    d["usual"] = d.groupby("coin")["f24"].transform("std")
    d["drift"] = d.groupby("coin")["f24"].transform("mean")
    d["un"] = -np.sign(d.p24)*(d.f24 - d.drift)
    d["str"] = d.un / d.usual
    res = []
    for (coin, q), g in d.groupby(["coin","volq"]):
        res.append((coin, q, len(g), g.un.mean()*100, g.str.mean(), g.str.mean()/(g.str.std()/np.sqrt(len(g)))))
    out["24h reversal per coin x vol tercile"] = pd.DataFrame(res, columns=["coin","volq","n","unusual%","strength","t"])
    d["pq"] = d.groupby("coin")["p24"].transform(lambda x: pd.qcut(x.abs()/x.std() if False else x/ (x.rolling(1).std() if False else 1), 5, labels=False))
    hv = d[d.volq == 2]
    res = []
    for q, g in hv.groupby("pq"):
        res.append((q, len(g), g.p24.mean()*100, (g.f24-g.drift).mean()*100, (g.f24-g.drift).mean()/((g.f24).std()/np.sqrt(len(g)))))
    out["high vol: next 24h by past-24h quintile"] = pd.DataFrame(res, columns=["pq","n","p24%","next_unusual%","t"])
    res = []
    for y, g in hv.groupby("year"):
        res.append((y, len(g), g.str.mean(), g.str.mean()/(g.str.std()/np.sqrt(len(g)))))
    out["high vol 24h reversal by year"] = pd.DataFrame(res, columns=["year","n","strength","t"])
    return out
