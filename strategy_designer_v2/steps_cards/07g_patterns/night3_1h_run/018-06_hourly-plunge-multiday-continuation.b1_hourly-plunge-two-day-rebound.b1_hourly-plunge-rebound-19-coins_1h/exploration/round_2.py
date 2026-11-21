def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            mad = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            m = r24 / mad
            # vol level relative to coin's own past: 30d mad over the 180d mean of mad (known at close)
            relv = mad / mad.rolling(4320, min_periods=720).mean()
            ret1 = c.pct_change()
            n = len(c)
            for h in [48, 96]:
                idx = np.arange(0, n - h, h)
                fwd = (c.shift(-h) / c - 1).values[idx]
                rows.append(pd.DataFrame({"coin": coin, "win": w, "h": h, "m": m.values[idx],
                    "mad": mad.values[idx], "relv": relv.values[idx],
                    "year": ts.dt.year.values[idx], "fwd": fwd}))
    A = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    g = A.groupby(["coin", "h"])["fwd"]
    A["drift"] = g.transform("mean"); A["usual"] = g.transform("std")
    A["unus"] = A["fwd"] - A["drift"]; A["str"] = A["unus"] / A["usual"]
    A = A.dropna(subset=["m"])
    A["volq"] = A.groupby(["coin", "h"])["mad"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    def summ(x):
        v = x["unus"]; n = len(v)
        return pd.Series({"n": n, "mean_pct": 100 * v.mean(), "t": v.mean() / (v.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "strength": x["str"].mean(), "total_pct": 100 * x["fwd"].mean()})
    out = {}
    for h in [48, 96]:
        D = A[A.h == h]
        dr = D[D.m <= -2]; up = D[D.m >= 2]
        # high-vol drops: by coin positive share, by early/late half of years
        hv = dr[dr.volq == 2]
        if h == 48:
            pc = hv.groupby("coin")["unus"].mean()
            out["48h hi-vol drops: coins with positive mean / coins"] = f"{(pc>0).sum()} / {len(pc)}"
            out["48h hi-vol drops by year"] = hv.groupby("year").apply(summ)
            lv = up[up.volq == 0]
            pc2 = lv.groupby("coin")["unus"].mean()
            out["48h lo-vol rises: coins with positive mean / coins"] = f"{(pc2>0).sum()} / {len(pc2)}"
            out["48h lo-vol rises by year"] = lv.groupby("year").apply(summ)
        # graded: slope of strength on |m| within drops, by vol tercile; and on m within rises
        res = []
        for q in [0, 1, 2]:
            s = dr[dr.volq == q]; u = up[up.volq == q]
            sl = stats.linregress(-s.m.clip(-8), s.str) if len(s) > 10 else None
            su = stats.linregress(u.m.clip(upper=8), u.str) if len(u) > 10 else None
            res.append({"volq": q, "drop_slope": sl.slope, "drop_slope_t": sl.slope / sl.stderr,
                        "rise_slope": su.slope, "rise_slope_t": su.slope / su.stderr})
        out[f"{h}h slopes of strength on multiple, by vol tercile"] = pd.DataFrame(res)
        # interaction on all bars: strength on (-m * vol rank)
        D2 = D.dropna(subset=["relv"]).copy()
        D2["rq"] = pd.qcut(D2.relv.rank(method="first"), 3, labels=False)
        out[f"{h}h drops<=-2 by past-relative vol tercile"] = D2[D2.m <= -2].groupby("rq").apply(summ)
        out[f"{h}h rises>=2 by past-relative vol tercile"] = D2[D2.m >= 2].groupby("rq").apply(summ)
    # book: per-coin book Sharpe and gain
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    Dy = pd.concat(dd).dropna(subset=["book_return"])
    out["book daily by coin"] = Dy.groupby("coin")["book_return"].agg(lambda s: s.mean() / s.std() * np.sqrt(365)).rename("sharpe").to_frame()
    return out
