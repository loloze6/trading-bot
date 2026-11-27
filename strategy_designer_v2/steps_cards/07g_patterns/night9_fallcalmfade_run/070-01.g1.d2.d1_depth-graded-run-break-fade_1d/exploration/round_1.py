def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            r = np.full(len(c), np.nan); r[1:] = c[1:]/c[:-1]-1
            allr.append(r[~np.isnan(r)])
        mu = np.concatenate(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values; o = b["open"].astype(float).values
            h = b["high"].astype(float).values; l = b["low"].astype(float).values
            n = len(c)
            r = np.full(n, np.nan); r[1:] = c[1:]/c[:-1]-1
            nxt = np.full(n, np.nan); nxt[:-1] = r[1:]
            s = pd.Series(r)
            vol30 = s.rolling(30, min_periods=20).std().values
            tr60 = np.full(n, np.nan); tr60[60:] = c[60:]/c[:-60]-1
            ts = pd.to_datetime(b["timestamp"])
            for t in range(1, n-1):
                # prior down run before bar t
                k = 0; j = t-1
                while j >= 1 and r[j] < 0:
                    k += 1; j -= 1
                runloss = c[t-1]/c[t-1-k]-1 if k > 0 else 0.0
                rng = (h[t]-l[t])/c[t-1]
                clpos = (c[t]-l[t])/(h[t]-l[t]) if h[t] > l[t] else np.nan
                rows.append(dict(coin=coin, w=w, day=ts[t].normalize(), wd=ts[t].dayofweek,
                                 year=ts[t].year, r=r[t], nxt=nxt[t], mu=mu, k=k, runloss=runloss,
                                 vol=vol30[t], tr60=tr60[t], rng=rng, clpos=clpos,
                                 fc=b["forecast"].iloc[t]))
    d = pd.DataFrame(rows).dropna(subset=["r", "nxt"])
    d["ex"] = -(d["nxt"]-d["mu"])  # short-direction excess
    d["vrank"] = d.groupby("coin")["vol"].rank(pct=True)
    def summ(g):
        ds = g.groupby("day")["ex"].sum()
        t = ds.mean()/(ds.std()/np.sqrt(len(ds))) if len(ds) > 2 else np.nan
        return pd.Series(dict(n=len(g), days=len(ds), mean_ex=g["ex"].mean(), t_day=t))
    up = d[d.r > 0]; dn = d[d.r < 0]
    out = {}
    up2 = up.copy(); up2["kb"] = up2["k"].clip(upper=5)
    out["up days by prior down run length (short excess next day)"] = up2.groupby("kb").apply(summ)
    dn2 = dn.copy()
    # prior up run length for down days (mirror)
    out["all up vs down days short excess"] = pd.DataFrame({"up": summ(up), "down": summ(dn)}).T
    ev = d[(d.r > 0) & (d.k >= 2)].copy()
    ev["depthq"] = pd.qcut(ev["runloss"].rank(method="first"), 4, labels=["shallow", "q2", "q3", "deep"])
    out["events by run loss quartile"] = ev.groupby("depthq").apply(summ)
    ev["upq"] = pd.qcut(ev["r"].rank(method="first"), 4, labels=["small up", "q2", "q3", "big up"])
    out["events by up-day size quartile"] = ev.groupby("upq").apply(summ)
    upx = up.copy()
    upx["upq"] = upx.groupby("coin")["r"].transform(lambda x: pd.qcut(x.rank(method="first"), 4, labels=False))
    out["all up days by up size quartile (0 small)"] = upx.groupby("upq").apply(summ)
    for nm, g in [("events", ev), ("all up", up)]:
        g = g.copy()
        g["trend"] = pd.cut(g["tr60"], [-10, -0.1, 0.1, 10], labels=["falling", "choppy", "rising"])
        g["agit"] = np.where(g["vrank"] > 0.5, "agitated", "calm")
        out[nm+" by trend x agitation(proxy)"] = g.dropna(subset=["trend"]).groupby(["trend", "agit"]).apply(summ)
    out["events by weekday"] = ev.groupby("wd").apply(summ)
    out["events by year"] = ev.groupby("year").apply(summ)
    out["events by coin"] = ev.groupby("coin").apply(summ)
    ev["cq"] = pd.qcut(ev["clpos"].rank(method="first"), 3, labels=["close low", "mid", "close high"])
    out["events by close position in range"] = ev.groupby("cq").apply(summ)
    return out
