def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in [1, 3, 5, 10]:
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(vals)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            ret = c.pct_change()
            sd30 = ret.rolling(30).std()
            r60 = c / c.shift(60) - 1
            r7 = c / c.shift(7) - 1
            r1 = ret
            r3 = c / c.shift(3) - 1
            hi20 = df["high"].rolling(20).max()
            lo20 = df["low"].rolling(20).min()
            pos20 = (c - lo20) / (hi20 - lo20)
            clv = (c - df["low"]) / (df["high"] - df["low"])
            reg = df["regime"]
            n = len(df)
            for h in [1, 3, 5, 10]:
                for i in range(0, n - h, h):
                    if reg.iloc[i] != "unknown":
                        continue
                    fwd = c.iloc[i + h] / c.iloc[i] - 1
                    rows.append(dict(coin=coin, w=w, h=h, fwd=fwd, unus=fwd - drift[(coin, h)],
                                     r60=r60.iloc[i], sc7=r7.iloc[i] / sd30.iloc[i] / np.sqrt(7),
                                     sc1=r1.iloc[i] / sd30.iloc[i], sc3=r3.iloc[i] / sd30.iloc[i] / np.sqrt(3),
                                     pos20=pos20.iloc[i], clv=clv.iloc[i],
                                     day=str(df["timestamp"].iloc[i])[:10]))
    R = pd.DataFrame(rows)

    def summ(g):
        s = -g["unus"]
        d = g.assign(s=s).groupby("day")["s"].sum()
        t = d.mean() / (d.std(ddof=1) / np.sqrt(len(d))) if len(d) > 2 else np.nan
        return pd.Series(dict(n=len(g), days=len(d), short_unus=s.mean(), t_day=t, short_total=(-g["fwd"]).mean()))

    out["profile all cases, short side, by horizon"] = pd.DataFrame({h: summ(R[R.h == h]) for h in [1, 3, 5, 10]}).T.round(4)
    out["profile all cases by coin h3"] = R[R.h == 3].groupby("coin").apply(summ).round(4)
    sp = []
    for feat in ["r60", "sc7", "sc1", "sc3", "pos20", "clv"]:
        for h in [1, 3, 5, 10]:
            G = R[(R.h == h)].dropna(subset=[feat])
            r, p = stats.spearmanr(G[feat], G["unus"])
            sp.append(dict(feat=feat, h=h, n=len(G), rho=r, p=p))
    out["spearman feature vs unusual fwd (neg rho = short gains as feature rises)"] = pd.DataFrame(sp).round(4)
    res = []
    for feat in ["r60", "sc1", "sc3", "pos20"]:
        G = R[R.h == 3].dropna(subset=[feat]).copy()
        G["q"] = pd.qcut(G[feat], 3, labels=False)
        for q, g in G.groupby("q"):
            s = summ(g); s["feat"] = feat; s["q"] = q; s["fmean"] = g[feat].mean()
            res.append(s)
    out["h3 terciles by feature"] = pd.DataFrame(res).round(4)
    return out
