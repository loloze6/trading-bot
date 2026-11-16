def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # 1) forward 20-bar return on grid, by forecast bucket and regime
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            r1 = pd.Series(cl).pct_change().values
            for h in (5, 20):
                for i in range(0, n - h, h):
                    past20 = cl[i] / cl[i-20] - 1 if i >= 20 else np.nan
                    past5 = cl[i] / cl[i-5] - 1 if i >= 5 else np.nan
                    vol20 = np.nanstd(r1[max(1, i-19):i+1]) if i >= 10 else np.nan
                    rng = b["close"].iloc[max(0, i-19):i+1]
                    pos = (cl[i]-rng.min())/(rng.max()-rng.min()) if rng.max() > rng.min() else np.nan
                    rows.append(dict(coin=c, w=w, h=h, fwd=cl[i+h]/cl[i]-1, fc=b["forecast"].iloc[i],
                                     reg=b["regime"].iloc[i], past20=past20, past5=past5, vol20=vol20, pos=pos,
                                     wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday()))
    g = pd.DataFrame(rows)
    for h in (5, 20):
        d = g[g.h == h].copy()
        d["dm"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
        def summ(x):
            return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan))
        out[f"h{h} by regime"] = d.groupby("reg")["dm"].apply(summ).unstack()
        a = d[d.fc > 0].copy()
        a["fq"] = pd.qcut(a["fc"], 4, labels=False, duplicates="drop")
        out[f"h{h} active by fc quartile"] = a.groupby("fq")["dm"].apply(summ).unstack()
        for col in ("past20", "past5", "vol20", "pos"):
            e = d.dropna(subset=[col]).copy()
            e["q"] = e.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
            out[f"h{h} by {col} quintile"] = e.groupby("q")["dm"].apply(summ).unstack()
    # daily: weekday of next-day coin return and book return
    dd = []
    for c in days:
        for w, x in days[c].items():
            x = x.copy(); x["coin"] = c
            dd.append(x)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    out["coin daily ret by weekday"] = dd.groupby("wd")["coin_return"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["book daily ret by weekday"] = dd.groupby("wd")["book_return"].agg(["mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # trades
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            t = t.copy(); t["coin"] = c; tr.append(t)
    tr = pd.concat(tr)
    tr["dur_d"] = tr["duration_minutes"]/1440
    tr["dq"] = pd.qcut(tr["dur_d"].rank(method="first"), 4, labels=False)
    out["trades by duration quartile"] = tr.groupby("dq").agg(n=("dur_d", "size"), dur=("dur_d", "mean"), pl=("profit_loss_percent", "mean"), win=("profit_loss_percent", lambda s: (s > 0).mean()))
    out["trades by coin"] = tr.groupby("coin").agg(n=("dur_d", "size"), pl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    return out
