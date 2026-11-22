def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []      # weekday-start 48h past vs 48h fwd
    hr_rows = []   # hourly returns
    d24 = []       # 24h grid past/fwd
    for coin, wins in bars.items():
        # coin usual 48h std from non-overlapping grid
        g48 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            g48 += list(c[idx + 48] / c[idx] - 1)
        s48 = np.std(g48); m48 = np.mean(g48)
        for w, b in wins.items():
            b = b.copy()
            ct = pd.to_datetime(b["timestamp"]) + pd.Timedelta(hours=1)
            c = pd.Series(b["close"].values, index=ct)
            c = c[~c.index.duplicated()]
            r1 = c.pct_change()
            vol = r1.rolling(720, min_periods=720).std()
            volr = vol / vol.expanding(min_periods=720).mean()
            reg = pd.Series(b["regime"].values, index=ct)
            reg = reg[~reg.index.duplicated()]
            hrdf = pd.DataFrame({"r": r1.shift(-1), "hour": c.index.hour, "wd": c.index.dayofweek})
            hrdf["coin"] = coin
            hr_rows.append(hrdf.dropna())
            mids = c.index[(c.index.hour == 0)]
            for T in mids:
                Tp = T - pd.Timedelta(hours=48); Tf = T + pd.Timedelta(hours=48)
                if Tp in c.index and Tf in c.index:
                    rows.append(dict(coin=coin, wd=T.dayofweek, past=(c[Tp]/c[T-pd.Timedelta(0)]) ,
                                     p=c[T]/c[Tp]-1, f=c[Tf]/c[T]-1, s=s48, m=m48,
                                     volr=volr.get(T, np.nan), reg=reg.get(T - pd.Timedelta(hours=1), None) if False else reg.get(T, None)))
            # 24h grid
            cv = c.values
            idx = np.arange(0, len(cv) - 48, 24)
            for i in idx:
                if i + 48 < len(cv):
                    d24.append(dict(coin=coin, p=cv[i+24]/cv[i]-1, f=cv[i+48]/cv[i+24]-1,
                                    vr=volr.iloc[i+24], wd=c.index[i+24].dayofweek))
    df = pd.DataFrame(rows)
    df["zp"] = df.p / df.s; df["zf"] = (df.f - df.m) / df.s
    def slope(d, x="zp", y="zf"):
        d = d.dropna(subset=[x, y])
        if len(d) < 20: return pd.Series(dict(n=len(d)))
        r = stats.linregress(d[x], d[y])
        sgn = np.mean(np.sign(d[x]) * d[y])
        tt = sgn / (np.std(np.sign(d[x]) * d[y], ddof=1) / np.sqrt(len(d)))
        return pd.Series(dict(n=len(d), slope=r.slope, t_slope=r.slope / r.stderr, signmove=sgn, t_sign=tt))
    out["48h past vs 48h fwd by weekday of T (0=Mon)"] = df.groupby("wd").apply(slope)
    df["calm"] = df.volr <= 1
    out["by weekday x calm(own volr proxy)"] = df.groupby(["wd", "calm"]).apply(slope)
    df["vq"] = pd.qcut(df.volr, 3, labels=["lowv", "midv", "highv"])
    out["Monday only by vol tercile"] = df[df.wd == 0].groupby("vq").apply(slope)
    out["Monday by coin"] = df[df.wd == 0].groupby("coin").apply(slope)
    out["Monday by abs zp tercile"] = df[df.wd == 0].assign(aq=lambda d: pd.qcut(d.zp.abs(), 3, labels=False)).groupby("aq").apply(slope)
    h = pd.concat(hr_rows)
    hs = h.groupby("hour").r.agg(["mean", "std", "count"])
    hs["t"] = hs["mean"] / (hs["std"] / np.sqrt(hs["count"]))
    out["next-hour return by hour of close"] = hs[["mean", "t", "count"]]
    ws = h.groupby("wd").r.agg(["mean", "std", "count"]); ws["t"] = ws["mean"] / (ws["std"] / np.sqrt(ws["count"]))
    out["next-hour return by weekday"] = ws[["mean", "t"]]
    d = pd.DataFrame(d24)
    d["s"] = d.groupby("coin").p.transform("std")
    d["zp"] = d.p / d.s; d["zf"] = d.f / d.s
    d["pq"] = d.groupby("coin").zp.transform(lambda x: pd.qcut(x, 5, labels=False))
    out["24h fwd by 24h past quintile"] = d.groupby("pq").zf.agg(["mean", "count", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    d["vq"] = pd.qcut(d.vr, 3, labels=["lowv", "midv", "highv"])
    out["24h past->fwd slope by vol tercile"] = d.groupby("vq").apply(slope)
    # book
    dd = []
    for coin, wins in days.items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    dd = pd.concat(dd).dropna(subset=["book_return"])
    dd["wd"] = pd.to_datetime(dd["day"]).dt.dayofweek
    bw = dd.groupby("wd")[["book_return", "coin_return"]].mean()
    out["book & coin daily mean by weekday"] = bw
    q = dd.book_return.quantile([0.01, 0.99])
    out["extreme book days weekday counts"] = pd.DataFrame({
        "worst1pct": dd[dd.book_return <= q.iloc[0]].wd.value_counts().sort_index(),
        "best1pct": dd[dd.book_return >= q.iloc[1]].wd.value_counts().sort_index()})
    return out
