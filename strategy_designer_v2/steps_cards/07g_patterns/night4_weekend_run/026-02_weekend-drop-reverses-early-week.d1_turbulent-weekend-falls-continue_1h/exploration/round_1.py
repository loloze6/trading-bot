def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    wk_rows = []; hr_rows = []; d_rows = []; mid_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp", "close"]].copy()
            b["timestamp"] = pd.to_datetime(b["timestamp"], utc=True)
            b = b.set_index("timestamp").sort_index()
            c = b["close"]
            r = c.pct_change()
            hr_rows.append(pd.DataFrame({"coin": coin, "wd": r.index.weekday, "hr": r.index.hour, "r": r.values}).dropna())
            # weekend: Mon 00:00 bars
            mons = c.index[(c.index.weekday == 0) & (c.index.hour == 0)]
            for t in mons:
                t0 = t - pd.Timedelta(hours=48); tp = t - pd.Timedelta(hours=216); t2 = t + pd.Timedelta(hours=48); t5 = t + pd.Timedelta(hours=120)
                if t0 in c.index and t2 in c.index:
                    rw = c[t] / c[t0] - 1
                    seg = r[(r.index > t0) & (r.index <= t)]
                    pre = r[(r.index > tp) & (r.index <= t0)]
                    vr = seg.std() / pre.std() if len(pre) > 100 else np.nan
                    fwd = c[t2] / c[t] - 1
                    fwd5 = c[t5] / c[t] - 1 if t5 in c.index else np.nan
                    # previous week (Mon->Sat) return
                    pw = c[t0] / c[tp + pd.Timedelta(hours=48)] - 1 if (tp + pd.Timedelta(hours=48)) in c.index else np.nan
                    wk_rows.append(dict(coin=coin, w=w, rw=rw, vr=vr, fwd=fwd, fwd5=fwd5, pw=pw))
            # midweek comparison: Wed 00:00 48h move -> next 48h
            weds = c.index[(c.index.weekday == 2) & (c.index.hour == 0)]
            for t in weds:
                t0 = t - pd.Timedelta(hours=48); t2 = t + pd.Timedelta(hours=48)
                if t0 in c.index and t2 in c.index:
                    mid_rows.append(dict(coin=coin, rw=c[t]/c[t0]-1, fwd=c[t2]/c[t]-1))
    wk = pd.DataFrame(wk_rows); mid = pd.DataFrame(mid_rows); H = pd.concat(hr_rows)
    # drift per coin 48h
    drift = wk.groupby("coin")["fwd"].mean()  # approximates; Mondays non-overlapping
    wk["ex"] = wk["fwd"] - wk["coin"].map(drift)
    wk["z"] = wk["rw"] / wk.groupby("coin")["rw"].transform("std")
    wk["q"] = pd.qcut(wk["z"], 5, labels=False)
    g = wk.groupby("q").agg(n=("ex", "size"), z=("z", "mean"), ex=("ex", "mean"), sd=("ex", "std"))
    g["t"] = g["ex"] / (g["sd"] / np.sqrt(g["n"]))
    out["weekend move quintile -> Mon-Tue excess"] = g
    wk["vq"] = pd.qcut(wk["vr"], 3, labels=False)
    g2 = wk.groupby(["vq", wk["rw"] < 0]).agg(n=("ex", "size"), ex=("ex", "mean"), sd=("ex", "std"))
    g2["t"] = g2["ex"] / (g2["sd"] / np.sqrt(g2["n"]))
    out["volratio tercile x weekend fell -> excess"] = g2
    out["corr rw,ex all; slope t"] = pd.Series({"corr": wk[["rw","ex"]].corr().iloc[0,1],
        "t_slope": stats.linregress(wk["z"], wk["ex"]).rvalue * np.sqrt(len(wk)-2) / np.sqrt(1-stats.linregress(wk["z"], wk["ex"]).rvalue**2), "n": len(wk)})
    wk["ex5"] = wk["fwd5"] - wk["coin"].map(wk.groupby("coin")["fwd5"].mean())
    out["weekend quintile -> Mon-Fri excess"] = wk.groupby("q")["ex5"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(x.count()))])
    wk["pz"] = wk["pw"] / wk.groupby("coin")["pw"].transform("std")
    wk["pq"] = pd.qcut(wk["pz"], 5, labels=False)
    out["prior week quintile -> weekend return"] = wk.groupby("pq")["rw"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(x.count()))])
    mid["ex"] = mid["fwd"] - mid.groupby("coin")["fwd"].transform("mean")
    mid["z"] = mid["rw"] / mid.groupby("coin")["rw"].transform("std")
    mid["q"] = pd.qcut(mid["z"], 5, labels=False)
    out["midweek Mon-Tue move quintile -> Wed-Thu excess"] = mid.groupby("q")["ex"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(x.count()))])
    # hour and weekday of hourly returns, excess vs coin mean
    H["ex"] = H["r"] - H.groupby("coin")["r"].transform("mean")
    f = lambda x: x.mean()/(x.std()/np.sqrt(x.count()))
    out["weekday excess hourly return (bp)"] = H.groupby("wd")["ex"].agg(n="count", bp=lambda x: x.mean()*1e4, t=f)
    out["hour excess hourly return (bp)"] = H.groupby("hr")["ex"].agg(n="count", bp=lambda x: x.mean()*1e4, t=f)
    out["per coin weekend fell: excess mean,t,n"] = wk[wk.rw < 0].groupby("coin")["ex"].agg(["count", "mean", f])
    return out
