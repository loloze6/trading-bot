def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    f = lambda x: x.mean()/(x.std()/np.sqrt(x.count())) if x.count() > 2 else np.nan
    ev = []; wk = []; base = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp", "close"]].copy()
            b["timestamp"] = pd.to_datetime(b["timestamp"], utc=True)
            c = b.set_index("timestamp")["close"].sort_index()
            c = c[~c.index.duplicated()]
            r = c.pct_change()
            idx = c.index
            # evening window: from close of 20:00 bar (time stamp 21:00 start) to close of 22:00 bar -> c[23:00]/c[21:00]
            t21 = idx[idx.hour == 21]
            for t in t21:
                te = t + pd.Timedelta(hours=2); tp = t - pd.Timedelta(hours=8); tv = t - pd.Timedelta(hours=168); t24 = t + pd.Timedelta(hours=24)
                if te in c.index and tp in c.index and tv in c.index:
                    seg = r[(r.index > tv) & (r.index <= t)]
                    ev.append(dict(coin=coin, w=w, yr=t.year, wd=t.weekday(), r2=c[te]/c[t]-1,
                                   p8=c[t]/c[tp]-1, vol=seg.std(),
                                   n24=(c[t24]/c[te]-1) if t24 in c.index else np.nan))
            # prior week Mon00->Sat00 vs weekend, plus same for any day: 5-day return -> next 48h
            for t in idx[idx.hour == 0]:
                t0 = t - pd.Timedelta(hours=120); t2 = t + pd.Timedelta(hours=48)
                if t0 in c.index and t2 in c.index:
                    base.append(dict(coin=coin, wd=t.weekday(), yr=t.year, p5=c[t]/c[t0]-1, f2=c[t2]/c[t]-1))
    E = pd.DataFrame(ev); B = pd.DataFrame(base)
    out["21-23h return by coin (bp, t)"] = E.groupby("coin")["r2"].agg(n="count", bp=lambda x: x.mean()*1e4, t=f)
    out["21-23h return by year"] = E.groupby("yr")["r2"].agg(n="count", bp=lambda x: x.mean()*1e4, t=f)
    out["21-23h return by weekday"] = E.groupby("wd")["r2"].agg(n="count", bp=lambda x: x.mean()*1e4, t=f)
    E["vq"] = E.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["21-23h by vol tercile (bp, and per unit vol)"] = E.assign(rv=E.r2/E.vol).groupby("vq").agg(n=("r2","count"), bp=("r2", lambda x: x.mean()*1e4), t=("r2", f), rv=("rv","mean"), tv=("rv", f))
    E["pz"] = E["p8"] / E["vol"]
    E["pq"] = E.groupby("coin")["pz"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["21-23h by prior 8h move quintile"] = E.groupby("pq").agg(n=("r2","count"), pz=("pz","mean"), bp=("r2", lambda x: x.mean()*1e4), t=("r2", f))
    out["after 23h: next 24h by 21-23 move quintile"] = E.assign(q=E.groupby("coin")["r2"].transform(lambda x: pd.qcut(x, 5, labels=False))).groupby("q")["n24"].agg(n="count", bp=lambda x: x.mean()*1e4, t=f)
    lr = stats.linregress(E.dropna(subset=["pz"])["pz"], E.dropna(subset=["pz"])["r2"])
    out["21-23 on prior8h/vol slope t"] = pd.Series({"slope": lr.slope, "t": lr.slope/lr.stderr, "n": len(E)})
    # 5-day move -> next 48h, by weekday of start (Sat = 5 is the weekend), non-overlap per weekday
    B["z"] = B["p5"] / B.groupby("coin")["p5"].transform("std")
    B["ex"] = B["f2"] - B.groupby("coin")["f2"].transform("mean")
    rows = {}
    for wd, g in B.groupby("wd"):
        l = stats.linregress(g["z"], g["ex"]); rows[wd] = dict(n=len(g), slope=l.slope, t=l.slope/l.stderr)
    out["5-day move z -> next 48h excess, slope by start weekday"] = pd.DataFrame(rows).T
    S = B[B.wd == 5]
    rows = {}
    for k, g in S.groupby("coin"):
        l = stats.linregress(g["z"], g["ex"]); rows[k] = dict(n=len(g), slope=l.slope, t=l.slope/l.stderr)
    for k, g in S.groupby("yr"):
        l = stats.linregress(g["z"], g["ex"]); rows["y"+str(k)] = dict(n=len(g), slope=l.slope, t=l.slope/l.stderr)
    out["Sat start: 5-day z -> weekend excess, by coin and year"] = pd.DataFrame(rows).T
    return out
