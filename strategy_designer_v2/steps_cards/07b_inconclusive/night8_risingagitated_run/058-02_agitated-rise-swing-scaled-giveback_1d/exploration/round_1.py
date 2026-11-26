def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    # drift and usual move per coin per horizon, on non-overlapping grids of all windows
    H = [1, 3, 5, 10]
    drift = {}
    rows = []
    for coin, wins in bars.items():
        for h in H:
            rets = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rets += list(c[idx + h] / c[idx] - 1)
            rets = np.array(rets)
            drift[(coin, h)] = (rets.mean(), rets.std(ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            dist = (c - sma) / (sd * c)
            fc = df["forecast"]
            ra = (df["regime"] == "unknown")
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                for i in idx:
                    fr = c.iloc[i + h] / c.iloc[i] - 1
                    m, s = drift[(coin, h)]
                    rows.append(dict(coin=coin, w=w, h=h, i=i, fc=fc.iloc[i], ra=ra.iloc[i],
                                     dist=dist.iloc[i], ex=fr - m, strength=(fr - m) / s,
                                     day=str(df["timestamp"].iloc[i])[:10],
                                     year=str(df["timestamp"].iloc[i])[:4]))
    R = pd.DataFrame(rows)
    out = {}
    def summ(g):
        n = len(g)
        mu = g["ex"].mean()
        t = mu / (g["ex"].std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series(dict(n=n, mean_ex_long=mu, t=t, strength_long=g["strength"].mean()))
    sig = R[(R.fc < 0)]
    out["signal cases by horizon (long-direction excess)"] = sig.groupby("h").apply(summ)
    s5 = sig[sig.h == 5].copy()
    out["h5 by coin"] = s5.groupby("coin").apply(summ)
    out["h5 by year"] = s5.groupby("year").apply(summ)
    out["h5 by window"] = s5.groupby("w").apply(summ)
    s5["q"] = pd.qcut(s5["fc"].rank(method="first"), 4, labels=["most_neg", "q2", "q3", "least_neg"])
    out["h5 by forecast quartile"] = s5.groupby("q").apply(summ)
    # positive distance in rising agitated vs other regimes (recomputed distance)
    R5 = R[(R.h == 5) & R.dist.notna()].copy()
    R5["above"] = R5.dist > 0
    out["h5 dist>0 by regime ra"] = R5[R5.above].groupby("ra").apply(summ)
    for ra in [True, False]:
        g = R5[R5.above & (R5.ra == ra)]
        if len(g) > 5:
            sl = stats.linregress(g["dist"], g["ex"])
            out[f"h5 slope ex on dist, above avg, ra={ra}"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(g)}"
    R5a = R5[R5.above & R5.ra].copy()
    R5a["dq"] = pd.qcut(R5a["dist"], 4, labels=["d1", "d2", "d3", "d4"])
    out["h5 ra above: by dist quartile"] = R5a.groupby("dq").apply(summ)
    for h in [10]:
        g = R[(R.h == h) & R.ra & (R.dist > 0)]
        sl = stats.linregress(g["dist"], g["ex"])
        out[f"h{h} ra above slope"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(g)} mean {g.ex.mean():.4f}"
    out["share bars ra by coin"] = pd.Series({c: np.mean([ (df.regime=='unknown').mean() for df in w.values()]) for c, w in bars.items()})
    return out
