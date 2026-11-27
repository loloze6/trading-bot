def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            z = r / sd30
            hi = b["high"].astype(float); lo = b["low"].astype(float); op = b["open"].astype(float)
            clv = (c - lo) / (hi - lo)
            rng = (hi - lo) / c.shift(1) / sd30
            r3 = c / c.shift(3) - 1
            r5 = c / c.shift(5) - 1
            dd20 = c / c.rolling(20, min_periods=10).max() - 1
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            yr = pd.to_datetime(b["timestamp"]).dt.year
            n = len(b)
            for h in (1, 3, 5):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    rows.append(dict(coin=coin, w=w, h=h, inprof=b["regime"].iloc[i] == "unknown",
                                     z=z.iloc[i], clv=clv.iloc[i], rng=rng.iloc[i],
                                     z3=r3.iloc[i]/(sd30.iloc[i]*np.sqrt(3)) if sd30.iloc[i] else np.nan,
                                     z5=r5.iloc[i]/(sd30.iloc[i]*np.sqrt(5)) if sd30.iloc[i] else np.nan,
                                     dd20=dd20.iloc[i], wd=wd.iloc[i], yr=yr.iloc[i],
                                     ex=fwd.iloc[i] - ((1+mu)**h - 1), day=b["timestamp"].iloc[i]))
    df = pd.DataFrame(rows).dropna(subset=["ex"])
    out = {}
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g["ex"].mean(), t=g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))) if len(g) > 2 else np.nan))
    P = df[df.inprof]
    out["profile share by h"] = df.groupby("h")["inprof"].mean()
    for col in ["z", "z3", "z5", "clv", "rng", "dd20"]:
        for h in (1, 3, 5):
            s = P[P.h == h].dropna(subset=[col]).copy()
            if len(s) < 50: continue
            s["q"] = pd.qcut(s[col], 5, labels=False, duplicates="drop")
            out[f"{col} quintile h{h}"] = s.groupby("q").apply(summ)
    out["weekday h1"] = P[P.h == 1].groupby("wd").apply(summ)
    out["coin h1"] = P[P.h == 1].groupby("coin").apply(summ)
    out["coin h5"] = P[P.h == 5].groupby("coin").apply(summ)
    out["year h5"] = P[P.h == 5].groupby("yr").apply(summ)
    out["all profile h"] = P.groupby("h").apply(summ)
    out["outside profile h"] = df[~df.inprof].groupby("h").apply(summ)
    # book
    trs = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            trs.append(t.assign(coin=coin))
    if trs:
        T = pd.concat(trs)
        out["trades"] = T.groupby("side")[["net_profit_loss_percent", "profit_loss_percent"]].agg(["count", "mean"])
    return out
