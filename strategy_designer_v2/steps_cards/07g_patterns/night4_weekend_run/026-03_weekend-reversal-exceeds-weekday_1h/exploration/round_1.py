def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; out = {}
    rows = []; hrs = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]) + pd.Timedelta(hours=1)
            c = df["close"].values.astype(float); n = len(c)
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            hrs.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values, "r": r1}))
            idx = np.where(ts.dt.hour.values == 0)[0]
            idx = idx[(idx >= 48) & (idx + 48 < n)]
            wds = ts.dt.weekday.values
            for i in idx:
                rows.append((coin, w, wds[i], c[i]/c[i-48]-1, c[i]/c[i-24]-1,
                             c[i+48]/c[i]-1, c[i+24]/c[i]-1, np.std(np.diff(np.log(c[i-48:i+1])))))
    d = pd.DataFrame(rows, columns=["coin","w","wd","p48","p24","f48","f24","vol"])
    for col in ["p48","f48","p24","f24"]:
        d[col+"z"] = d.groupby("coin")[col].transform(lambda x: (x-x.mean())/x.std())
    res = []
    for wd, g in d.groupby("wd"):
        s = -g.p48z*g.f48z; s24 = -g.p24z*g.f24z
        res.append((wd, len(g), s.mean(), s.mean()/(s.std()/np.sqrt(len(s))),
                    s24.mean(), s24.mean()/(s24.std()/np.sqrt(len(s24))),
                    g.f24.mean()*100, g.f48.mean()*100))
    out["rev score by end weekday (close 00 UTC)"] = pd.DataFrame(res, columns=["wd","n","rev48","t48","rev24","t24","f24mean%","f48mean%"])
    res = []
    for coin, g in d.groupby("coin"):
        gg = g[g.wd == 0]; s = -gg.p48z*gg.f48z
        s2 = -g.p48z*g.f48z
        res.append((coin, len(gg), s.mean(), s.mean()/(s.std()/np.sqrt(len(s))), s2.mean()))
    out["weekend rev by coin"] = pd.DataFrame(res, columns=["coin","n","rev48","t","rev48_alldays"])
    d["volq"] = d.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    res = []
    for q, g in d.groupby("volq"):
        s = -g.p48z*g.f48z; s24 = -g.p24z*g.f24z
        res.append((q, len(g), s.mean(), s.mean()/(s.std()/np.sqrt(len(s))), s24.mean(), s24.mean()/(s24.std()/np.sqrt(len(s24)))))
    out["rev by vol tercile (all day starts, overlapping)"] = pd.DataFrame(res, columns=["volq","n","rev48","t48","rev24","t24"])
    h = pd.concat(hrs)
    g = h.groupby("hour")["r"]
    out["mean 1h return by close hour (bp)"] = pd.DataFrame({"mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.count())), "absmean_bp": g.apply(lambda x: x.abs().mean()*1e4)})
    g = h.groupby("wd")["r"]
    out["mean 1h return by weekday (bp)"] = pd.DataFrame({"mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.count())), "absmean_bp": g.apply(lambda x: x.abs().mean()*1e4)})
    dd = []
    for coin in data["days"]:
        for w, df in data["days"][coin].items():
            x = df.copy(); x["wd"] = pd.to_datetime(x["day"]).dt.weekday; dd.append(x)
    dd = pd.concat(dd)
    g = dd.groupby("wd")
    out["book & coin daily ret by weekday (bp)"] = pd.DataFrame({"book_bp": g.book_return.mean()*1e4, "book_t": g.book_return.mean()/(g.book_return.std()/np.sqrt(g.book_return.count())), "coin_bp": g.coin_return.mean()*1e4})
    t = []
    for coin in data["trades"]:
        for w, df in data["trades"][coin].items():
            t.append(df.assign(coin=coin))
    t = pd.concat(t)
    out["trades by side"] = t.groupby("side").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), dur_h=("duration_minutes", lambda x: x.mean()/60))
    return out
